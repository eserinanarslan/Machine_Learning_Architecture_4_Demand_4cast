"""
File: util.py
Author: Eser Inan Arslan
Email: eserinanarslan@gmail.com
Description: Description: This file contains the code for running and forecasting with the model developed for Bestseller.
"""

import pandas as pd
import numpy as np
import configparser
from math import sqrt
from sklearn.metrics import mean_squared_error, mean_absolute_error, mean_squared_log_error

# Read dataset
def read_data(file_path):
    try:
        df = pd.read_csv(file_path)
    except pd.errors.ParserError as e:
        print(f'Error while parsing CSV file: {e}')
    return df

# Error measurement metrics
def mean_absolute_percentage_error(y_true, y_pred):
    return np.mean(np.abs((np.array(y_true) - np.array(y_pred)) / y_true)) * 100

def accuracy_control(test_dataset, predictions_list, threshold):
    lstm_rmse = []
    lstm_mape = []
    lstm_rmse.append(sqrt(mean_squared_error([test_dataset['Sales']], [predictions_list])))
    lstm_mape.append(mean_absolute_percentage_error([test_dataset['Sales']], [predictions_list]))
    print('lstm_rmse = ', lstm_rmse)
    print('lstm_mape = ', lstm_mape)

    if (lstm_mape[0] <= threshold) :
        return lstm_mape[0], True
    else :
        return lstm_mape[0], False

    return

# Read config file
def read_config(config_path):
    config = configparser.ConfigParser()
    config.read(config_path)
    return config



