import curses
import time
from enum import Enum
import sympy
from VSMAT_engine import VSMATEngine

MICRONS_TO_INCH = 3.93701e-5
FEET_TO_INCH = 12
NMILES_TO_INCH = 72913.398659
METER_TO_INCH = 39.3701
KILOMETER_TO_INCH = METER_TO_INCH * 1000
NANOMETER_TO_INCH = METER_TO_INCH * 1e-9
MRAD_TO_RAD = 1.0e-3
URAD_TO_RAD = 1.0e-3 * MRAD_TO_RAD
DEG_TO_RAD = 0.0174533
AS_TO_RAD = 4.84814e-6
MAS_TO_RAD = AS_TO_RAD * 1.0e-3

class ParamBox(object):
    class ParamBoxStatus(Enum):
        EMPTY = 1
        MANUAL = 2
        COMPUTED = 3
        OVERCONSTRAINED = 4

    def __init__(self, y, x, name, symbol, width=30, dimension=None):
        self.name = name
        self.symbol = symbol
        self.width = width
        self.win = curses.newwin(6, self.width, y, x)
        self.namePadWidth = int((self.width - len(self.name)) / 2)

        self.dimension = dimension
        if self.dimension is None:
            self.availableUnits = ['  ']
        elif self.dimension == 'length':
            self.availableUnits = ['in', 'ft', 'kft', 'nmi', 'm', 'km', 'nm']
        elif self.dimension == 'angle':
            self.availableUnits = ['r', 'mr', 'ur', 'deg', 'as', 'mas']

        self.displayUnitIndex = 0
        self.displayUnit = self.availableUnits[self.displayUnitIndex]

        self._internalVal = None
        self._displayVal = None

        self.status = self.ParamBoxStatus.EMPTY
        self.isActive = False

    def clearValue(self):
        self._internalVal = None
        self.status = self.ParamBoxStatus.EMPTY

    def computedSetValue(self, val):
        self._internalVal = val
        self.status = self.ParamBoxStatus.COMPUTED
        
    def manualSetValue(self, val):
        if val is None:
            #Clear
            self.clearValue()
        else:
            entryUnits = self.displayUnit

            if entryUnits == '  ':
                self._internalVal = val
            elif entryUnits == 'in':
                self._internalVal = val
            elif entryUnits == 'ft':
                self._internalVal = val * FEET_TO_INCH
            elif entryUnits == 'kft':
                self._internalVal = val * FEET_TO_INCH * 1000.
            elif entryUnits == 'nmi':
                self._internalVal = val * NMILES_TO_INCH
            elif entryUnits == 'm':
                self._internalVal = val * METER_TO_INCH
            elif entryUnits == 'nm':
                self._internalVal = val * NANOMETER_TO_INCH
            elif entryUnits == 'km':
                self._internalVal = val * KILOMETER_TO_INCH

            elif entryUnits == 'r':
                self._internalVal = val
            elif entryUnits == 'mr':
                self._internalVal = val * MRAD_TO_RAD
            elif entryUnits == 'ur':
                self._internalVal = val * URAD_TO_RAD
            elif entryUnits == 'deg':
                self._internalVal = val * DEG_TO_RAD
            elif entryUnits == 'as':
                self._internalVal = val * AS_TO_RAD
            elif entryUnits == 'mas':
                self._internalVal = val * MAS_TO_RAD
            
            self.status = self.ParamBoxStatus.MANUAL

    def update(self):
        self.win.erase()
        self.displayUnit = self.availableUnits[self.displayUnitIndex]
        if self.isActive:
            self.win.border()
        self.win.addstr(1, self.namePadWidth, self.name)

        if self._internalVal is not None:
            if self.displayUnit == '  ':
                self._displayVal = self._internalVal
            elif self.displayUnit == 'in':
                self._displayVal = self._internalVal
            elif self.displayUnit == 'ft':
                self._displayVal = self._internalVal / FEET_TO_INCH
            elif self.displayUnit == 'kft':
                self._displayVal = self._internalVal / (FEET_TO_INCH * 1000.)
            elif self.displayUnit == 'nmi':
                self._displayVal = self._internalVal / NMILES_TO_INCH
            elif self.displayUnit == 'm':
                self._displayVal = self._internalVal / METER_TO_INCH
            elif self.displayUnit == 'nm':
                self._displayVal = self._internalVal / NANOMETER_TO_INCH
            elif self.displayUnit == 'km':
                self._displayVal = self._internalVal / KILOMETER_TO_INCH

            elif self.displayUnit == 'r':
                self._displayVal = self._internalVal
            elif self.displayUnit == 'mr':
                self._displayVal = self._internalVal / MRAD_TO_RAD
            elif self.displayUnit == 'ur':
                self._displayVal = self._internalVal / URAD_TO_RAD
            elif self.displayUnit == 'deg':
                self._displayVal = self._internalVal / DEG_TO_RAD
            elif self.displayUnit == 'as':
                self._displayVal = self._internalVal / AS_TO_RAD
            elif self.displayUnit == 'mas':
                self._displayVal = self._internalVal / MAS_TO_RAD

            self.win.addstr(3, 1, "%.3f"%self._displayVal)

        self.win.addstr(3, self.width-4, self.displayUnit.ljust(3))
        self.updateColor()
        self.win.refresh()

    def updateColor(self):
        if self.status == self.ParamBoxStatus.EMPTY:
            self.win.bkgd(' ', curses.color_pair(1) | curses.A_BOLD)
        elif self.status == self.ParamBoxStatus.MANUAL:
            self.win.bkgd(' ', curses.color_pair(4) | curses.A_BOLD)
        elif self.status == self.ParamBoxStatus.COMPUTED:
            self.win.bkgd(' ', curses.color_pair(3) | curses.A_BOLD)
        elif self.status == self.ParamBoxStatus.OVERCONSTRAINED:
            self.win.bkgd(' ', curses.color_pair(5) | curses.A_BOLD)



def afunc(stdscr):
    if not curses.has_colors():
        print("No color support.")
        quit()
    curses.start_color()
    curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_BLACK, curses.COLOR_WHITE)
    curses.init_pair(3, curses.COLOR_WHITE, curses.COLOR_BLUE)
    curses.init_pair(4, curses.COLOR_WHITE, curses.COLOR_GREEN)
    curses.init_pair(5, curses.COLOR_WHITE, curses.COLOR_RED)
    curses.noecho()
    stdscr.nodelay(True)

    paramBoxes = [
            [None, None, None],
            [None, None, None],
            [None, None, None],
            [None, None, None],
            [None, None, None],
            [None, None, None],
            ]

    eng = VSMATEngine()

    paramBoxes[0][0] = ParamBox(0, 0, "Focal Ratio", eng.f, dimension=None)
    paramBoxes[0][1] = ParamBox(0, 31, "Focal Length", eng.F, dimension='length')
    paramBoxes[0][2] = ParamBox(0, 62, "Primary Diameter", eng.D, dimension='length')

    paramBoxes[1][0] = ParamBox(7, 0, "Wavelength", eng.wl, dimension='length')
    paramBoxes[1][1] = ParamBox(7, 31, "Diff. Lim. Angle", eng.theta_d, dimension='angle')
    paramBoxes[1][2] = ParamBox(7, 62, "Diff. Lim. GSD", eng.d, dimension='length')

    paramBoxes[2][0] = ParamBox(14, 0, "Altitude", eng.A, dimension='length')
    paramBoxes[2][1] = ParamBox(14, 31, "GSD", eng.g, dimension='length')
    paramBoxes[2][2] = ParamBox(14, 62, "Q", eng.Q, dimension=None)

    paramBoxes[3][0] = ParamBox(21, 0, "Pixel Pitch", eng.p, dimension='length')
    paramBoxes[3][1] = ParamBox(21, 31, "X Pixels", eng.Px, dimension=None)
    paramBoxes[3][2] = ParamBox(21, 62, "Y Pixels", eng.Py, dimension=None)

    paramBoxes[4][0] = ParamBox(28, 0, "Sens. Size X", eng.Sx, dimension='length')
    paramBoxes[4][1] = ParamBox(28, 31, "Ang. FoV X", eng.alpha_x, dimension='angle')
    paramBoxes[4][2] = ParamBox(28, 62, "Swath Width X", eng.Wx, dimension='length')

    paramBoxes[5][0] = ParamBox(35, 0, "Sens. Size Y", eng.Sy, dimension='length')
    paramBoxes[5][1] = ParamBox(35, 31, "Ang. FoV Y", eng.alpha_y, dimension='angle')
    paramBoxes[5][2] = ParamBox(35, 62, "Swath Width Y", eng.Wy, dimension='length')

    #paramBoxesFlat =  [x for xs in paramBoxes for x in xs if x is not None]

    activeParamBox = [0, 0]
    paramBoxes[0][0].isActive = True

    keyBuffer = ""

    while True:

        oldActiveParamBox = list(activeParamBox)


        for row in paramBoxes:
            for cell in row:
                if cell is not None:
                    cell.update()

        activeCell = paramBoxes[activeParamBox[0]][activeParamBox[1]]

        try:
            ch = stdscr.getkey()
            if ch == 'KEY_RIGHT':
                if activeParamBox[1] < 2:
                    activeParamBox[1] += 1
            elif ch == 'KEY_LEFT':
                if activeParamBox[1] > 0:
                    activeParamBox[1] -= 1
            elif ch == 'KEY_UP':
                if activeParamBox[0] > 0:
                    activeParamBox[0] -= 1
            elif ch == 'KEY_DOWN':
                if activeParamBox[0] < 5:
                    activeParamBox[0] += 1
            elif ord(ch[0]) == 21:
                if activeCell.displayUnitIndex == (len(activeCell.availableUnits) - 1):
                    activeCell.displayUnitIndex = 0
                else:
                    activeCell.displayUnitIndex += 1
                keyBuffer = ''
            elif ch in '1234567890.e':
                keyBuffer += ch

            elif ord(ch[0]) == 10:
                #Enter
                if keyBuffer == '':
                    activeCell.clearValue()
                else:
                    try:
                        val = float(keyBuffer)
                        activeCell.manualSetValue(val)
                    except ValueError:
                        pass
                    finally:
                        keyBuffer = ''

                #solve
                eng.initEqns()
                for row in paramBoxes:
                    for cell in row:
                        if cell is not None:
                            if cell.status == cell.ParamBoxStatus.MANUAL:
                                eng.eqns.append( sympy.Eq(cell.symbol, cell._internalVal) )
                soln = eng.solve()
                if soln is None:
                    #No solution, must be overconstrained
                    stdscr.bkgd(' ', curses.color_pair(5) | curses.A_BOLD)
                else:
                    stdscr.bkgd(' ', curses.color_pair(1) | curses.A_BOLD)
                    for row in paramBoxes:
                        for cell in row:
                            if cell is not None:
                                if cell.status != cell.ParamBoxStatus.MANUAL:
                                    #See if there's a number to put in here
                                    val = soln.get(cell.symbol)
                                    try:
                                        numVal = float(val)
                                        cell.computedSetValue(numVal)
                                    except TypeError:
                                        cell.clearValue()

            else:
                pass

        except curses.error:
            pass


        if activeParamBox != oldActiveParamBox:
            paramBoxes[oldActiveParamBox[0]][oldActiveParamBox[1]].isActive = False
            paramBoxes[activeParamBox[0]][activeParamBox[1]].isActive = True
            keyBuffer = ""


        time.sleep(0.1)


curses.wrapper(afunc)
