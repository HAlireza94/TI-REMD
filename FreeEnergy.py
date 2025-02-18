import numpy as np
from lmfit import Model
import sys 
import math


if len(sys.argv) != 3:
    print("This program aims to fit the free energy as a function of temperature")
    print("The equation that is to be fitted is A + B * (T - T0) + C * T * np.log(T / T0)")
    print("A, B, and C are fitting parameters, while T0 is the reference temperature that should be provided.")
    print("Note, you should choose which Free Energy Technique you want to use.")
    print("usage: Free-Energy.py T0 BAR/MBAR < Free Energy output")
    sys.exit()

dg_bar, er_bar = [], []
dg_mbar, er_mbar = [], []
T = []

T0 = float(sys.argv[1])
for line in sys.stdin:
    while line.startswith("Temperature"):
        line = sys.stdin.readline()
    p = line.split()
    T.append(float(p[0]))
    dg_bar.append(float(p[1]))
    er_bar.append(float(p[2]))
    dg_mbar.append(float(p[3]))
    er_mbar.append(float(p[4]))


def delG(A, B, C, t, T0):
    return A + B * (t - T0) + C * t * np.log(t / T0)

if sys.argv[2] == 'MBAR':
    model = Model(delG, independent_vars=['t', 'T0'])
    params1 = model.make_params(A=1, B=0.2, C=0.002)
    result1 = model.fit(dg_mbar, params1, t=T, T0=T0)

    a1 = result1.params['A'].value
    b1 = result1.params['B'].value
    c1 = result1.params['C'].value



    T = np.array(T)
    DELTAG_fit1 = delG(a1,b1,c1,T,T0)


    print(result1.fit_report())
    print("")
    print("")
    print("")
    print("================================== Fitting Vs Sim Data from MBAR Calculations =================================")
    print("")
    print(f"{'Temperature (K)':<20}{'delta-G (kj/mol)':<20}{'Fitted sim data':<20}")

    for i in range(len(T)):
        print(f"{T[i]:<20}{dg_mbar[i]:<20}{DELTAG_fit1[i]:<20.3f}")

else:
    model = Model(delG, independent_vars=['t', 'T0'])
    params1 = model.make_params(A=1, B=0.2, C=0.002)
    result1 = model.fit(dg_bar, params1, t=T, T0=T0)

    a1 = result1.params['A'].value
    b1 = result1.params['B'].value
    c1 = result1.params['C'].value



    T = np.array(T)
    DELTAG_fit1 = delG(a1,b1,c1,T,T0)


    print(result1.fit_report())
    print("")
    print("")
    print("")
    print("================================== Fitting Vs Sim Data from BAR Calculations =================================")
    print("")
    print(f"{'Temperature (K)':<20}{'delta-G (kj/mol)':<20}{'Fitted sim data':<20}")

    for i in range(len(T)):
        print(f"{T[i]:<20}{dg_mbar[i]:<20}{DELTAG_fit1[i]:<20.3f}")

    

    
