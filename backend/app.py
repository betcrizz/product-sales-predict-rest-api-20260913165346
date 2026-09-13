# Import necessary libraries
import numpy as np
import joblib  # For loading the serialized model
import pandas as pd  # For data manipulation
from flask import Flask, request, jsonify  # For creating the Flask API

# Initialize the Flask application
sales_predictor_api = Flask("SuperKart Product Store Sales Predictor")

# Load the trained machine learning model
model = joblib.load("product_store_sales_prediction_model_v1_0.joblib")

# Define a route for the home page (GET request)
@sales_predictor_api.get('/')
def home():
    """
    This function handles GET requests to the root URL ('/') of the API.
    It returns a simple welcome message.
    """
    return "Welcome to SuperKart Product Store Sales API!"

# Define an endpoint for single store sales prediction (POST request)
@sales_predictor_api.post('/v1/sales')
def predict_sales():
    """
    This function handles POST requests to the '/v1/sales' endpoint.
    It expects a JSON payload containing sales details and returns
    the predicted sales price as a JSON response.
    """
    # Get the JSON data from the request body
    prod_store_data = request.get_json()

    # Extract relevant features from the JSON data
    sample = {
        'Product_Weight': prod_store_data['Product_Weight'],
        'Product_Sugar_Content': prod_store_data['Product_Sugar_Content'],
        'Product_Allocated_Area': prod_store_data['Product_Allocated_Area'],
        'Product_MRP': prod_store_data['Product_MRP'],
        'Store_Size': prod_store_data['Store_Size'],
        'Store_Location_City_Type': prod_store_data['Store_Location_City_Type'],
        'Store_Type': prod_store_data['Store_Type'],
        'Product_Id_char': prod_store_data['Product_Id_char'],
        'Store_Age_Years': prod_store_data['Store_Age_Years'],
        'Product_Type_Category': prod_store_data['Product_Type_Category'],
    }

    # Convert the extracted data into a Pandas DataFrame
    input_data = pd.DataFrame([sample])

    # Make prediction (get Product_Store_Sales_Total)
    predicted_sales = model.predict(input_data)[0]

    # Return the actual price
    return jsonify({'Predicted Sales ': predicted_sales})


# Define an endpoint for batch prediction (POST request)
@sales_predictor_api.post('/v1/salesbatch')
def predict_sales_batch():
    """
    This function handles POST requests to the '/v1/salesbatch' endpoint.
    It expects a CSV file containing sales details for multiple records
    and returns the predicted sales as a dictionary in the JSON response.
    """
    # Get the uploaded CSV file from the request
    file = request.files['Batch_Data_SuperKart.csv']

    # Read the CSV file into a Pandas DataFrame
    input_data = pd.read_csv(file)

    # Make predictions for all properties in the DataFrame
    predicted_sales = model.predict(input_data).tolist()

    # Create a dictionary of predictions with  as key
    output_dict = dict(zip(input_data, predicted_sales))  # Use actual prices

    # Return the predictions dictionary as a JSON response
    return output_dict

# Run the Flask application in debug mode if this script is executed directly
if __name__ == '__main__':
    sales_predictor_api.run(debug=True)
