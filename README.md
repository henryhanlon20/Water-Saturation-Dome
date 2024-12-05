# Water-Saturation-Dome
**Summary:** Function in python and Matlab to plot water saturation line and critical point in 2d thermodynamic state variable plots.

Contents of Repo:

-domeData_example.m: Example code for implementation in Matlab

-domeData.m: Matlab file with just the function

-domeData_example.py: Example code for implementation in Python

-domeData.py: Python file with just the function

**Motivation:**

-While examples exist, such as https://cantera.org/examples/python/thermo/vapordome.py.html, they are typically exclusively for python. 

-Existing open source code does not generate saturation line and critical point data within a user function

-Existing open source code focuses on generating standalone plots for the vapor dome. This function seeks to output arrays of data for the desired two thermodynamic state variables (as well as the critical point, in a format that can easily be incorporated into a pre-existing plot.  

-This function also splices together gas/fluid arrays of h,v and s for simplicity of plotting, rather than plotting multiple arrays, as is common with existing open source code. 


**Function**

**Inputs:**

-choice - this must be a string, and it controls the type of plot generated. Supported plots are listed below, with the correct input listed in quotes:

  Pressure-Volume "PV" or "pv"
  
  Pressure-Temperature "PT" or "pt" 
  
  Pressure-Enthalpy "PH" or "ph"
  
  Enthalpy-Entropy "HS" or "hs" 
  
  Temperature-Entropy "TS" or "ts"
  
This controls which themodynamic state properties are put into the output arrays. The order cannot be currently reversed, but if the user needs that capability, they can simply plot the arrays in "reverse" order. 

-resolution - this must be an integer, and it controls the number of points to generate along the saturation line. Higher number here will introduce slightly more computation time, but smoother data. 

-threshold - this is a float which exists to truncate the data in the PV plot because Vg exhibits asymptotic behavior at low values of pressure. This will cut off both P and V data if there is a jump from consecutive data points larger than it. It should be controlled with an inverse relation to resolution. If resolution increases, the threshold needs to be lowered. User can explore different values as needed. For all other plots, the value has no effect, and I recommend a placeholder of 1.

**Outputs:**

Suppose you call the function as such x,y,a,b=domeData("var1",var2,var3)

x- will be an array with length 2*var2 with entries of the thermodynamic state property that corresponds to the second letter in the var1 string. 

y- will be an array with length 2*var2 with entries of the thermodynamic state property that corresponds to the first letter in the var1 string. 

a - will be the critical point's x-coordinate for whichever thermodynamic state property corresponds to x

b - will be the critical point's y-coordinate for whichever thermodynamic state property corresponds to y

In order to make use of the arrays, plot(x,y) and plot(a,b) on an existing thermodynamic plot (or new one). 

**Future Work:**

-switching from Water.yaml to liquidvapor.yaml will provide better performance on the saturated vapor side of the dome, as well as potentially allow for species other than water to be used. It has been avoided thus far because Cantera does not support directly setting thermodynamic state via temperature and quality for Solution.liquidvapor.yaml. 

-eliminating hard coded choices for user plots by interpreting input strings 

