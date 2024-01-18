## FORECAST HUNTER TEST PROGRAM ##

import pytest
import pandas as pd
from project import find_closest_point, search_file, process_ensemble_data, calculate_eto

def test_find_closest_point():
    station_location = (40, 5)
    grid_points = pd.DataFrame({
        "I": [1, 2, 3],
        "J": [1, 2, 3],
        "Latitude": [60, 50, 40],
        "Longitude": [7, 6, 5],
    })
    closest_point = find_closest_point(station_location, grid_points)
    assert closest_point == (3, 3, 40, 5, 0)

def test_search_file():
    tests_directory_path = r"C:\Users\Utilizador\Desktop\ForecastHunter\tests_directory"
    point = (1, 3)
    assert search_file(tests_directory_path, point) == "swf_001_003.csv"
    with pytest.raises(FileNotFoundError):
        search_file(tests_directory_path, (2, 1))

def test_process_ensemble_data():
    file_path = r"C:\Users\Utilizador\Desktop\ForecastHunter\tests_directory\swf_001_003.csv"
    expected_medians_df = pd.DataFrame({
        "Date": ["01/01/2024", "02/01/2024", "03/01/2024"],
        "TMPmax_M": [25.5, 26.5, 27.5],
        "TMPmin_M": [15.5, 16.5, 17.5],
        "SWDsum_M": [20.5, 21.5, 22.5]
    })
    pd.testing.assert_frame_equal(process_ensemble_data(file_path), expected_medians_df)

def test_calculate_eto():
    observations_file_path = r"C:\Users\Utilizador\Desktop\ForecastHunter\tests_directory\observations.csv"
    medians_df = pd.DataFrame({
        "Date": ["01/01/2024", "02/01/2024", "03/01/2024"],
        "TMPmax_M": [25.5, 26.5, 27.5],
        "TMPmin_M": [15.5, 16.5, 17.5],
        "SWDsum_M": [20.5, 21.5, 22.5]
    })
    expected_eto_df = pd.DataFrame({
        "Date": ["01/01/2024", "02/01/2024", "03/01/2024"],
        "ETo_For": [2.33, 2.51, 2.69],
        "ETo_Obs": [1.92, 2.11, 2.30]
    }) 
    pd.testing.assert_frame_equal(calculate_eto(medians_df, observations_file_path), expected_eto_df, atol=0.01)