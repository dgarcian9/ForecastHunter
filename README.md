# <div align="center"> Forecast Hunter</div>
___<div align="center"> A toolbox for assessing seasonal weather forecast data usability on ETo estimation </div>___

<div align="center">Project developed by Daniel Garcia, student number 23790, within the scope of the course "Introduction to Python 2023/2024", integrated into the Master's program in Green Data Science at the Higher Institute of Agronomy.</div><br><br>


## Background and objective:

Decision-making processes always involve a component of risk/uncertainty, especially in activities strongly influenced by climate, such as agriculture. The ability to anticipate medium to long-term weather conditions allows for a preventive approach and decision-making in line with that knowledge. Seasonal forecasts produced by numerical models aim to address this need.

This project arises from an interest in evaluating the performance of seasonal forecasts as a tool to support irrigation management. The Python program developed aims to compare Reference Evapotranspiration (ET<sub>0</sub>) values, a variable used to model soil water balance and estimate irrigation needs, obtained using observed data and seasonal forecast data. The program provides the user with a graphical element for visualizing this comparison.<br><br>


## Project composition:

- Information ("README.md")
- Base data ("Observations.csv," "wrf_ens_HUB_grid_points.csv," "SWF_Ensembles," "tests_directory")
- Programs ("project.py" and "test_project.py")
- Pip-installable libraries ("requirements.txt")<br><br>


## Project base data:

Data produced within the scope of HubIS project.

1. "Observations.csv": Decimal coordinates and daily data of maximum temperature (°C), minimum temperature (°C), and solar radiation at the top of the atmosphere (MJ m<sup>-2</sup>) for the period between 01/10/2013 and 30/09/2023 (csv format), referring to the INRAE station in Salon-de-Provence, France.

2. "wrf_ens_HUB_grid_points.csv": Grid of points with 18x18 km resolution (8181 points), containing the point identifiers (I, J) and its decimal coordinates (latitude, longitude) (csv format).

3. "SWF_Ensembles": Daily data of maximum temperature (°C), minimum temperature (°C), and solar radiation at the top of the atmosphere (MJ m<sup>-2</sup>) for the period between 01/10/2013 and 30/09/2023, produced by a seasonal forecast model (hindcasts). Each grid point has a dedicated csv file, with the file name including the point identifiers (I, J). The used seasonal forecast data consist of an ensemble of 12 members for each considered meteorological variable. The different ensemble members correspond to model forecast runs with distinct initial conditions. The forecasts have a temporal horizon of 6 months and are produced twice a year (March, for the April-September period, and September, for the October-March period).

4. "tests_directory": Folder containing manually created and filled files. This is a requirement for testing the main program. It should accompany the program test function, and its content must not be edited.<br><br>


## Program structure:

The developed program ("project.py") consists of a main function, four additional functions (find_closest_point, search_file, process_ensemble_data, calculate_eto), and a class (EToPlotter) with a userdefined method (plot). In summary, based on the provided base data, this program identifies the closest grid point to the considered meteorological station (find_closest_point), identifies the file with corresponding seasonal forecast data (search_file), processes and treats forecast data by calculating daily ensemble medians for each variable (process_ensemble_data), calculates daily ET<sub>0</sub> values based on observed data and ensemble medians of seasonal forecasts, according to the Hargreaves equation (calculate_eto), and constructs a scatter plot between observed ET<sub>0</sub> and predicted ETo, adjusting a linear regression model and calculating the coefficient of determination (R<sup>2</sup>) (EtoPlotter). A more detailed description of the program can be found in the code itself, through accompanying notes.

Associated to the main program is also a test code to execute with pytest ("test_project.py"). It tests the main program and its additional functions with some test and corner cases, ensuring that the obtained output is as intended and guaranteeing the program's reliability.<br><br>


### Some considerations:
>The correct functioning of this version of the program depends on the structure of the base data files. It requires those to be organized in the format described throughout the code (csv filling, variable names, etc.). For simplification reasons, out of the 8181 files with seasonal forecast data, only the file used in the case study ("wrf_ens_HUB_ALL_070_070.csv") has been adapted to this format.

>For the GitHub repository, the decision was made not to import the entire contents of the "SWF_Ensembles" folder due to the excessive and unnecessary volume of data that it would represent.
