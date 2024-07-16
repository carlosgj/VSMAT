import logging
import numpy as np
import sympy

class VSMATEngine(object):
    def __init__(self):
        self.initParams()
        self.initEqns()

    def initParams(self):
        self.params = []

        self.f = sympy.Symbol('f') #Focal ratio
        self.params.append(self.f)

        self.F = sympy.Symbol('F') #Focal length (in)
        self.params.append(self.F)

        self.D = sympy.Symbol('D') #Primary diameter (in)
        self.params.append(self.D)

        self.A = sympy.Symbol('A') #Altitude (in)
        self.params.append(self.A)

        self.g = sympy.Symbol('g') #GSD (in)
        self.params.append(self.g)

        self.p = sympy.Symbol('p') #Pixel pitch (in)
        self.params.append(self.p)

        self.Px = sympy.Symbol('Px') #X pixel count
        self.params.append(self.Px)

        self.Py = sympy.Symbol('Py') #Y pixel count
        self.params.append(self.Py)

        self.Sx = sympy.Symbol('Sx') #X sensor size (in)
        self.params.append(self.Sx)

        self.Sy = sympy.Symbol('Sy') #Y sensor size (in)
        self.params.append(self.Sy)

        self.theta_d = sympy.Symbol('theta_d') #Diffraction limited angle
        self.params.append(self.theta_d)

        self.d = sympy.Symbol('d') #Diffraction limited spot size
        self.params.append(self.d)

        self.Q = sympy.Symbol('Q') #Sampling ratio
        self.params.append(self.Q)

        self.Wx = sympy.Symbol('Wx') #X swath width (in)
        self.params.append(self.Wx)

        self.Wy = sympy.Symbol('Wy') #Y swath width (in)
        self.params.append(self.Wy)

        self.wl = sympy.Symbol('wl') #Wavelength (in)
        self.params.append(self.wl)

        self.alpha_x = sympy.Symbol('alpha_x') #Angular X FoV (rad)
        self.params.append(self.alpha_x)

        self.alpha_y = sympy.Symbol('alpha_y') #Angular Y FoV (rad) 
        self.params.append(self.alpha_y)


    def initEqns(self):
        self.eqns = []
        #Optics
        self.eqns.append( sympy.Eq(self.f, self.F/self.D) )
        self.eqns.append( sympy.Eq(self.alpha_x, self.Sx/self.F) )
        self.eqns.append( sympy.Eq(self.alpha_y, self.Sy/self.F) )
        self.eqns.append( sympy.Eq(self.Wx, self.A/(self.F/self.Sx)) )
        self.eqns.append( sympy.Eq(self.Wy, self.A/(self.F/self.Sy)) )
        self.eqns.append( sympy.Eq(self.g, self.A/(self.F/self.p)) )
        self.eqns.append( sympy.Eq(self.theta_d, 1.22 * self.wl / self.D) )
        self.eqns.append( sympy.Eq(self.d, self.theta_d * self.A) )

        #Sensor
        self.eqns.append( sympy.Eq(self.Sx, self.p*self.Px) )
        self.eqns.append( sympy.Eq(self.Sy, self.p*self.Py) )
        self.eqns.append( sympy.Eq(self.Q, self.d/self.g) )

    def solve(self):
        soln = sympy.solve(self.eqns, self.params, dict=True, manual=True)
        if len(soln) < 1:
            return None
        else:
            return soln[0]

if __name__ == "__main__":
    this = VSMATEngine()

    #Knowns
    this.eqns.append( sympy.Eq(this.D, 100) )
    this.eqns.append( sympy.Eq(this.F, 200) )
    this.eqns.append( sympy.Eq(this.p, 3.75) )
    #this.eqns.append( sympy.Eq(this.wl, 2e-5) )
    #this.eqns.append( sympy.Eq(this.Px, 10000) )
    #this.eqns.append( sympy.Eq(this.A, 600 * 1000 * 40.) )

    this.solve()

