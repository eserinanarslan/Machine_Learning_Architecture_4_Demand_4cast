"""
File: main.py
Author: Eser Inan Arslan
Email: eserinanarslan@gmail.com
Description: Description: This file contains the code for running and forecasting with the model developed for Bestseller.
"""

import os
import logging
from logging.handlers import RotatingFileHandler
from flask import Flask, request
import configparser
import util

# Create a 'logs' directory if it doesn't exist
if not os.path.exists('logs'):
    os.makedirs('logs')

# Configure logging
logging.basicConfig(level=logging.DEBUG)  # Set the logging level to DEBUG
logger = logging.getLogger(__name__)  # Create a logger instance for this module

# Add a file handler to save logs to a file
file_handler = RotatingFileHandler('logs/app.log', maxBytes=10240, backupCount=10)
file_handler.setFormatter(logging.Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'))
file_handler.setLevel(logging.DEBUG)
logger.addHandler(file_handler)

# Parse config.ini file
config = configparser.ConfigParser()
config.read("config.ini")

# Read configuration from the config file
config_path = "config.ini"
config = util.read_config(config_path)
# Get values from the config file
dataset_path = config.get("Settings", "dataset_path")
test_dataset = util.read_data(dataset_path)

predictions_string = config.get("Settings", "predictions_values")
predictions_list = [int(value.strip()) for value in predictions_string.split(',')]
threshold = int(config.get("Settings", "threshold"))
logger.debug('threshold = %d', threshold)  # Log the threshold value

jj_accuracy_result, jj = util.accuracy_control(test_dataset.iloc[:5], predictions_list[:5], threshold)
vm_accuracy_result, vm = util.accuracy_control(test_dataset.iloc[4:], predictions_list[4:], threshold)

logger.debug('accuracy_result %s', jj_accuracy_result)  # Log the accuracy result
app = Flask(__name__)

class PostService:
    def __init__(self, config):
        self.users = {config["User1"]["username"]: config["User1"]["password"],
                      config["User2"]["username"]: config["User2"]["password"]}

    def authenticate(self, username, password):
        return username in self.users and self.users[username] == password

    def get_post_response(self, username):
        if ((username == "JackAndJones") and
                (jj is True)):
            return ('This is ' + username + ' and model accuracy is % ' +
                    str(100 - round(jj_accuracy_result, 1)) + ' !!!')

        elif ((username == "VeroModa") and
              (jj is False)):
            return 'This is ' + username + (' and forecast results are lower than expectations !!!'
                                            ' Model is retraining.')

        elif ((username == "VeroModa") and
              (vm is True)):
            return ('This is ' + username + ' and model accuracy is ' +
                    str(100 - round(vm_accuracy_result, 1)) + ' !!!')

        elif ((username == "VeroModa") and
              (vm is False)):
            return 'This is ' + username + (' and forecast results are lower than expectations !!!'
                                            ' Model is retraining.')

        else:
            return "User can not be found !.."

# Initialize PostService with config
post_service = PostService(config)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        if post_service.authenticate(username, password):
            return post_service.get_post_response(username)
        else:
            logger.warning("Authentication failed for username: %s", username)  # Log authentication failure
            return "Username or Password are not correct or matched each other. Please try again !!"
    return "Please Log in ."

# Run the Flask app
try:
    app.run(host=config["Service"]["Host"], port=int(config["Service"]["Port"]), debug=True)
except Exception as e:
    logger.error("Error running Flask app: %s", e)  # Log the error
    # Handle the error as needed, e.g., exit the program or set default values
