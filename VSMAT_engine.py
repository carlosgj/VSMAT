import logging
import numpy as np
import sympy

MICRONS_TO_INCH = 3.93701e-5
FEET_TO_INCH = 12
MILES_TO_INCH = 5280 * FEET_TO_INCH
METER_TO_INCH = 39.3701
KILOMETER_TO_INCH = METER_TO_INCH * 1000
NANOMETER_TO_INCH = METER_TO_INCH * 1e-9

params = []

f = sympy.Symbol('f') #Focal ratio
params.append(f)

F = sympy.Symbol('F') #Focal length (in)
params.append(F)

D = sympy.Symbol('D') #Primary diameter (in)
params.append(D)

A = sympy.Symbol('A') #Altitude (in)
params.append(A)

g = sympy.Symbol('g') #GSD (in)
params.append(g)

p = sympy.Symbol('p') #Pixel pitch (in)
params.append(p)

Px = sympy.Symbol('Px') #X pixel count
params.append(Px)

Py = sympy.Symbol('Py') #Y pixel count
params.append(Py)

Sx = sympy.Symbol('Sx') #X sensor size (in)
params.append(Sx)

Sy = sympy.Symbol('Sy') #Y sensor size (in)
params.append(Sy)

theta_d = sympy.Symbol('theta_d') #Diffraction limited angle
params.append(theta_d)

d = sympy.Symbol('d') #Diffraction limited spot
params.append(d)

Q = sympy.Symbol('Q') #Sampling ratio
params.append(Q)

Wx = sympy.Symbol('Wx') #X swath width (in)
params.append(Wx)

Wy = sympy.Symbol('Wy') #Y swath width (in)
params.append(Wy)

wl = sympy.Symbol('wl') #Wavelength (in)
params.append(wl)

alpha_x = sympy.Symbol('alpha_x') #Angular X FoV (rad)
params.append(alpha_x)

alpha_y = sympy.Symbol('alpha_y') #Angular Y FoV (rad) 
params.append(alpha_y)

eqns = []

#Optics
eqns.append( sympy.Eq(f, F/D) )
eqns.append( sympy.Eq(alpha_x, Sx/F) )
eqns.append( sympy.Eq(alpha_y, Sy/F) )
eqns.append( sympy.Eq(Wx, A/(F/Sx)) )
eqns.append( sympy.Eq(Wy, A/(F/Sy)) )
eqns.append( sympy.Eq(g, A/(F/p)) )
eqns.append( sympy.Eq(theta_d, 1.22 * wl / D) )
eqns.append( sympy.Eq(d, theta_d * A) )

#Sensor
eqns.append( sympy.Eq(Sx, p*Px) )
eqns.append( sympy.Eq(Sy, p*Py) )

#Knowns
eqns.append( sympy.Eq(D, 10 * FEET_TO_INCH) )
eqns.append( sympy.Eq(F, 10 * METER_TO_INCH) )
eqns.append( sympy.Eq(p, 3.75*MICRONS_TO_INCH) )
eqns.append( sympy.Eq(Px, 10000) )
eqns.append( sympy.Eq(A, 600 * KILOMETER_TO_INCH) )
eqns.append( sympy.Eq(wl, 500 * NANOMETER_TO_INCH) )

foo = sympy.solve(eqns, params, dict=True)

print(foo)