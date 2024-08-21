# Sales - Forecast

The task is to forecast the demands of next 9 months

*** For model service, you have to run "python src/main.py" on terminal

However,  I highly recommend to use dockerize flask service version with help of below shell scripts

1) docker build --tag sales-forecast-app:1.0 .
2) docker run -p 1100:1100 --name sales-forecast-app sales-forecast-app:1.0

## Service

After training and forecasting process, you can use Postman to test. You can find postman file under "collection" file. You have to import that json file to the Postman. 

Services return dataframe as a json message.
