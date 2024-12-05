# Water-Saturation-Dome
Summary: Function in python and Matlab to plot water saturation line and critical point in 2d thermodynamic state variable plots.

Motivation:
-While examples exist, such as https://cantera.org/examples/python/thermo/vapordome.py.html, they are typically exclusively for python. 
-Existing open source code does not generate saturation line and critical point data within a user function
-Existing open source code focuses on generating standalone plots for the vapor dome. This function seeks to output arrays of data for the desired two thermodynamic state variables (as well as the critical point, in a format that can easily be incorporated into a pre-existing plot.  

Function
Inputs: 
-choice - this must be a string, and it controls the type of plot generated. Supported plots are listed below, with the correct input listed in quotes:
  Pressure-Volume "PV" or "pv"
  Pressure-Temperature "PT" or "pt" 
  
  Pressure-Enthalpy "PH" or "ph"
  
  Enthalpy-Entropy "HS" or "hs" 
  Temperature-Entropy "TS" or "ts"
This controls which themodynamic state properties are put into the output arrays. The order cannot be currently reversed, but if the user needs that capability, they can simply plot the arrays in "reverse" order. 
-resolution - this must be an integer, and it controls the number of points to generate along the saturation line. Higher number here will introduce slightly more computation time, but smoother data. 
-threshold - this is a float, 


Future Work:
-switching from Water.yaml to liquidvapor.yaml will provide better performance on the saturated vapor side of the dome, as well as potentially allow for species other than water to be used. It has been avoided thus far because Cantera does not support directly setting thermodynamic state via temperature and quality for Solution.liquidvapor.yaml. 
-eliminating hard coded choices for user plots by interpreting input strings 

