## FORECAST HUNTER ##

import pandas as pd
import numpy as np
from haversine import haversine, Unit
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score
import os
import re

def main():
    # Base data (coordinates, files and directory paths) -> users should adapt this code for their study case
    le_crau_station = (43.643, 4.994)
    grid_points_file = r"C:\Users\Utilizador\Desktop\ForecastHunter\wrf_ens_HUB_grid_points.csv"
    observations_file = r"C:\Users\Utilizador\Desktop\ForecastHunter\Observations.csv"
    directory_ensembles_path = r"C:\Users\Utilizador\Desktop\ForecastHunter\SWF_Ensembles"

    # Find the grid point that is the closest to the meteorological station
    grid_points = pd.read_csv(grid_points_file)
    closest_point = find_closest_point(le_crau_station, grid_points)
    print(f"Closest Point: I = {closest_point[0]}, J = {closest_point[1]} | lat: {closest_point[2]:.3f} N, lon: {closest_point[3]:.3f} E | distance = {closest_point[4]:.3f} km")

    # Find the right forecast ensemble file
    ensemble_data_file = search_file(directory_ensembles_path, closest_point)

    # Process forecast ensemble data (build the path to the selected ensemble file and get medians for meteorological variables)
    ensemble_data_file_path = os.path.join(directory_ensembles_path, ensemble_data_file)
    ensemble_medians = process_ensemble_data(ensemble_data_file_path)

    # Calculate ETo
    ETo = calculate_eto(ensemble_medians, observations_file)

    # Plot the results
    EToPlotter(ETo)


# Input: (tuple, DataFrame)
def find_closest_point(station_location, grid_points):
    # Initialize the variables
    min_distance = float("inf")
    closest_point = None
    # Iterate through all the rows of the dataframe and calculate distances in km
    for index, row in grid_points.iterrows():
        I = int(row["I"])
        J = int(row["J"])
        lat = float(row["Latitude"])
        lon = float(row["Longitude"])
        distance = haversine(station_location, (lat, lon), unit=Unit.KILOMETERS)
        # Update the variables when a smaller distance is calculated
        if distance < min_distance:
            min_distance = distance
            closest_point = (I, J, lat, lon, distance)
    # Output: (tupple)
    return closest_point


# Input: (string, tuple)
def search_file(directory_path, point):
    # Define the wanted base pattern with a regular expression
    pattern = re.compile(r".+(\d{3})_(\d{3})\.csv$")
    # Iterate through the files in the directory
    for filename in os.listdir(directory_path):
        # Check if the filename matches the base pattern and the reference of the point
        match = pattern.search(filename)
        if match and str(point[0]) in match.group(1) and str(point[1]) in match.group(2):
            # Output: (string)
            return filename
    # If no matching file is found, raise an error and stop the program
    raise FileNotFoundError(f"No file found for point (I:{point[0]}, J:{point[1]}) in directory {directory_path}")


# Input: (string)
def process_ensemble_data(file_path):
    forecast_ensemble = pd.read_csv(file_path, sep=";")
    # Select columns for Tmax, Tmin and Solar Radiation, from the 12 forecast ensemble members
    Tmax_M = forecast_ensemble[["TMPmax_1", "TMPmax_2", "TMPmax_3", "TMPmax_4", "TMPmax_5", "TMPmax_6", "TMPmax_7", "TMPmax_8", "TMPmax_9", "TMPmax_10", "TMPmax_11", "TMPmax_12"]]
    Tmin_M = forecast_ensemble[["TMPmin_1", "TMPmin_2", "TMPmin_3", "TMPmin_4", "TMPmin_5", "TMPmin_6", "TMPmin_7", "TMPmin_8", "TMPmin_9", "TMPmin_10", "TMPmin_11", "TMPmin_12"]]
    Swd_M = forecast_ensemble[["SWDsum_1", "SWDsum_2", "SWDsum_3", "SWDsum_4", "SWDsum_5", "SWDsum_6", "SWDsum_7", "SWDsum_8", "SWDsum_9", "SWDsum_10", "SWDsum_11", "SWDsum_12"]]
    # Calculate medians along rows for the three variables and add the medians as new columns
    forecast_ensemble["TMPmax_M"] = np.median(Tmax_M, axis=1)
    forecast_ensemble["TMPmin_M"] = np.median(Tmin_M, axis=1)
    forecast_ensemble["SWDsum_M"] = np.median(Swd_M, axis=1)
    # Create a new DataFrame with only the date column and the new median columns
    ensemble_medians = forecast_ensemble[["Date", "TMPmax_M", "TMPmin_M", "SWDsum_M"]]
    # Output: (DataFrame)
    return ensemble_medians


# Input: (Dataframe, string)
def calculate_eto(ensemble_medians_df, observations_file):
    # Read the observations csv file
    observations = pd.read_csv(observations_file, sep=";")
    # Calculate forecasted and observed ETo using the Hargreaves equation
    ensemble_medians_df["ETo_For"] = 0.0023 * ((0.5 * ensemble_medians_df["TMPmax_M"] + 0.5 * ensemble_medians_df["TMPmin_M"]) + 17.8) * np.sqrt(ensemble_medians_df["TMPmax_M"] - ensemble_medians_df["TMPmin_M"]) * (ensemble_medians_df["SWDsum_M"] * 0.408)
    observations["ETo_Obs"] = 0.0023 * ((0.5 * observations["TMPmax_Obs"] + 0.5 * observations["TMPmin_Obs"]) + 17.8) * np.sqrt(observations["TMPmax_Obs"] - observations["TMPmin_Obs"]) * (observations["RS_Obs"] * 0.408)
    # Create a new DataFrame with Date, ETo_For and ETo_Obs
    ETo = pd.DataFrame({
        "Date": ensemble_medians_df["Date"],
        "ETo_For": ensemble_medians_df["ETo_For"],
        "ETo_Obs": observations["ETo_Obs"]
        })
    # Output: (DataFrame)
    return ETo


class EToPlotter:
    def __init__(self, eto_df):
        self.eto_df = eto_df
        self.plot()

    def plot(self):
        # Create a scatter plot
        self.eto_df.plot.scatter(x="ETo_Obs", y="ETo_For", alpha=0.5, color="lightgreen")

        # Perform linear regression
        X = self.eto_df[["ETo_Obs"]]
        y = self.eto_df["ETo_For"]
        regression_model = LinearRegression().fit(X, y)
        y_pred = regression_model.predict(X)  # Get predicted values
        plt.plot(X, y_pred, color="darkgreen", linewidth=2)  # Add regression line to the plot
        r_squared = r2_score(y, y_pred)  # Calculate R²

        # Add the regression equation to the plot
        equation = f"y = {regression_model.coef_[0]:.3f}x + {regression_model.intercept_:.2f}"
        plt.annotate(equation, xy=(0.05, 0.85), xycoords="axes fraction", fontsize=12)
        # Add R² to the plot
        r_squared_text = f"R² = {r_squared:.3f}"
        plt.annotate(r_squared_text, xy=(0.05, 0.79), xycoords="axes fraction", fontsize=12)

        # Edit plot presentation features
        # Set the scale and proportions between axes
        plt.gca().set_aspect("equal", adjustable="box")
        # Find the maximum value of both axes and set the maximum value for both axes
        max_value = max(self.eto_df["ETo_Obs"].max() + 1, self.eto_df["ETo_For"].max() + 1)
        plt.xlim(0, max_value)
        plt.ylim(0, max_value)
        # Increase the size of the axis labels
        plt.xlabel("ETo_Obs", fontsize=12)
        plt.ylabel("ETo_For", fontsize=12)
        
        # Show the plot
        plt.show()


if __name__ == "__main__":
    main()
