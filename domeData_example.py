import cantera as ct
import pandas as pd
import numpy as np
from matplotlib import pyplot as plt

"""
Inputs to function:
-Choice: Must be a string, one of "ts","hs","ph","pt","pv" or uppercase version. 
This controls which themodynamic state properties are put into the output arrays. 
If you want "st" instead of "ts" for example, just generate with ts and switch 
the order when you plot. 

-Resolution: this must be an integer, and it controls the number of points to generate
along the saturation line. Higher number here will introduce slightly more computation time, 
but smoother data.

-threshold - this is a float which exists to truncate the data in the PV plot because Vg
exhibits asymptotic behavior at low values of pressure. This will cut off both P and V data
if there is a jump from consecutive data points larger than it. It should be controlled with
an inverse relation to resolution. If resolution increases, the threshold needs to be lowered.
User can explore different values as needed. For all other plots, the value has no effect, and
I recommend a placeholder of 1.

Outputs to function: (Units are T, K, kj/kg, kj/kg*k)
Output 1 - will be an array with length 2*var2 with entries of the thermodynamic state property
that corresponds to the second letter in the choice string

Output 2 - will be an array with length 2*var2 with entries of the thermodynamic state property
that corresponds to the first letter in the var1 string.

Output 3 - will be the critical point's x-coordinate for whichever thermodynamic state property 
corresponds to x

Output 4 - will be the critical point's y-coordinate for whichever thermodynamic state property
corresponds to y

In order to make use of the arrays, plot(output 1,output 2) and plot(output 3,output 4) on an 
existing thermodynamic plot (or new one). Reminder, if you wanted "ST" instead of "TS" you can
just plot(output2,output1)
"""

def domeData(choice,resolution,threshold):
    w = ct.Water()
    t_crit=647.096
    columns = ['t_', 'p_',
           't', 'p',
           'v', 'h',
           's']

    temp=np.linspace(273.16,t_crit,resolution)
    df = pd.DataFrame(0, index=np.arange(2*len(temp)), columns=columns)
    nan_array=np.full(len(temp),np.nan)
    df.t_ = np.append(temp,nan_array)

    arr = ct.SolutionArray(w, len(temp))

    # saturated vapor data
    arr.TQ = temp, 1
    P = arr.P_sat
    vg = arr.v
    hg = arr.enthalpy_mass / 1.e3
    sg = arr.entropy_mass / 1.e3

    # saturated liquid data
    arr.TQ = temp, 0
    vf = arr.v
    hf = arr.enthalpy_mass / 1.e3
    sf = arr.entropy_mass / 1.e3

    #Create data for table
    df.p_=np.append(P,nan_array)
    df.p=np.append(P,np.flip(P))
    df.t=np.append(temp,np.flip(temp))
    df.s=np.append(sf,np.flip(sg))
    df.h=np.append(hf,np.flip(hg))
    df.v=np.append(vf,np.flip(vg))
    
    choice=choice.lower()
    choices={"ts","hs","ph","pt","pv"}
    if choice not in choices:
        raise ValueError("invalid plot choice. try a different pair of state variables, or switch the order")
    if choice=="ts":
        output_x=df.s
        output_y=df.t
        x_crit=sf[-1]
        y_crit=t_crit
    if choice=="hs":
        output_x=df.s
        output_y=df.h
        x_crit=sf[-1]
        y_crit=hf[-1]
    if choice=="ph":
        output_x=df.h
        output_y=df.p
        x_crit=hf[-1]
        y_crit=P[-1]
    if choice=="pt":
        output_x=df.t_
        output_y=df.p_
        x_crit=t_crit
        y_crit=P[-1]
    if choice=="pv":
        output_x=df.v
        output_y=df.p
        delta=np.abs(np.diff(output_x))
        last_stable=np.argmax(delta>threshold)+1
        output_x=output_x[:last_stable]
        output_y=output_y[:last_stable]
        x_crit=vf[-1]
        y_crit=P[-1]
#Optional Step: output to CSV (uncomment)
#df.to_csv('saturated_steam_T.csv', index=False)
    return output_x,output_y,x_crit,y_crit

#Suppose we know that the answer to our problem is 2 thermodynamic states, and we want to plot them on a TS-plot
plt.figure(1)
t_data=np.array([500,400])
s_data=np.array([12,8])
plt.scatter(s_data,t_data)
plt.text(s_data[0], t_data[0], "State 1", fontsize=12, ha='right')
plt.text(s_data[1], t_data[1], "State 2", fontsize=12, ha='right')
plt.xlabel('Entropy [kJ/kg*k]') 
plt.ylabel('Temperature [k]')

#Now we want to add our vapor dome to the plot:
ans1,ans2,ans3,ans4=domeData("ts",50,1)
plt.plot(ans1,ans2)
plt.scatter(ans3,ans4,marker='o', label='Critical point')
plt.show()