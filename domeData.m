% Inputs to function:
% -Choice: Must be a string, one of "ts","hs","ph","pt","pv" or uppercase version. 
% This controls which themodynamic state properties are put into the output arrays. 
% If you want "st" instead of "ts" for example, just generate with ts and switch 
% the order when you plot. 
% 
% -Resolution: this must be an integer, and it controls the number of points to generate
% along the saturation line. Higher number here will introduce slightly more computation time, 
% but smoother data.
% 
% -threshold - this is a float which exists to truncate the data in the PV plot because Vg
% exhibits asymptotic behavior at low values of pressure. This will cut off both P and V data
% if there is a jump from consecutive data points larger than it. It should be controlled with
% an inverse relation to resolution. If resolution increases, the threshold needs to be lowered.
% User can explore different values as needed. For all other plots, the value has no effect, and
% I recommend a placeholder of 1.
% 
% Outputs to function: (Units are T, K, kj/kg, kj/kg*k)
% Output 1 - will be an array with length 2*var2 with entries of the thermodynamic state property
% that corresponds to the second letter in the choice string
% 
% Output 2 - will be an array with length 2*var2 with entries of the thermodynamic state property
% that corresponds to the first letter in the var1 string.
% 
% Output 3 - will be the critical point's x-coordinate for whichever thermodynamic state property 
% corresponds to x
% 
% Output 4 - will be the critical point's y-coordinate for whichever thermodynamic state property
% corresponds to y
% 
% In order to make use of the arrays, plot(output 1,output 2) and plot(output 3,output 4) on an 
% existing thermodynamic plot (or new one). Reminder, if you wanted "ST" instead of "TS" you can
% just plot(output2,output1)

function [output_x,output_y,x_crit,y_crit]=domeData(choice,resolution,threshold)
%Change input to lowercase
choice=lower(choice);

%Define water local to the function
w=Water();

%Initialize Steam Table
T=linspace(273.16,647.096,resolution);
soln=zeros(resolution,8);
soln(:,1)=T;

%Calculate Steam Table
%Columns (in order) T,P,Vf,Vg,Hf,Hg,Sf,Sg
for i=1:resolution
    setState_Tsat(w,[T(i),0]);
    soln(i,2)=pressure(w);
    soln(i,3)=1/density(w);
    soln(i,5)=enthalpy_mass(w)/1000;
    soln(i,7)=entropy_mass(w)/1000;
    setState_Tsat(w,[T(i),1]);
    soln(i,4)=1/density(w);
    soln(i,6)=enthalpy_mass(w)/1000;
    soln(i,8)=entropy_mass(w)/1000;
end

%Stitch data together based off user determined plot

if choice=="pv"
    output_x=[soln(:,3);flipud(soln(:,4))];
    output_y=[soln(:,2);flipud(soln(:,2))];
    %PV diagram has additional step to prevent plotting asymptotic behavior
    delta=abs(diff(output_x))
    last_stable=find(delta>threshold,1,'first')+1;
    output_x = output_x(1:last_stable);
    output_y = output_y(1:last_stable);
    x_crit=soln(end,3);
    y_crit=soln(end,2);
end

if choice=="pt"
    output_x=soln(:,1);
    output_y=soln(:,2);
    x_crit=soln(end,1);
    y_crit=soln(end,2);
end

if choice=="ph"
    output_x=[soln(:,5);flipud(soln(:,6))];
    output_y=[soln(:,2);flipud(soln(:,2))];
    x_crit=soln(end,5);
    y_crit=soln(end,2);
end

if choice=="hs"
    output_x=[soln(:,7);flipud(soln(:,8))];
    output_y=[soln(:,5);flipud(soln(:,6))];
    x_crit=soln(end,7);
    y_crit=soln(end,5);
end

if choice=="ts"
    output_x=[soln(:,7);flipud(soln(:,8))];
    output_y=[soln(:,1);flipud(soln(:,1))];
    x_crit=soln(end,7);
    y_crit=soln(end,1);
end
end

