from flask import Flask, request, jsonify, render_template
import mysql.connector
import numpy as np
import joblib
import os

app = Flask(__name__)

# Load trained ML model and scaler
model = joblib.load("cibil_score_model.pkl")  # ✅ Using joblib
scaler = joblib.load("scaler.pkl")  # ✅ Load the scaler

# Database connection details
db_config = {
    "host": "localhost",
    "user": "root",
    "password": "root1@3$",
    "database": "cibidb"
}

def get_user_data(user_id):
    """Fetch user data from MySQL"""
    connection = mysql.connector.connect(**db_config)
    cursor = connection.cursor(dictionary=True)
    
    query = "SELECT upi_transactions, income, expenditure, bill_payments_time FROM Dataset WHERE user_id = %s"
    cursor.execute(query, (user_id,))
    
    user_data = cursor.fetchone()
    cursor.close()
    connection.close()
    return user_data

@app.route("/")
def home():
    return render_template("index.html")  # Frontend

@app.route("/predict", methods=["POST"])
def predict():
    user_id = request.form["user_id"]
    user_data = get_user_data(user_id)

    if user_data:
        # Convert user data to NumPy array
        input_features = np.array([[user_data["upi_transactions"], user_data["income"], user_data["expenditure"], user_data["bill_payments_time"]]])
        
        # Scale the input features using the saved MinMaxScaler
        input_features_scaled = scaler.transform(input_features)
        
        # Get prediction
        prediction = int(model.predict(input_features_scaled)[0])  # Ensure integer output

        return jsonify({"prediction": prediction})
    else:
        return jsonify({"error": "User not found"}), 404

if __name__ == "__main__":
    app.run(debug=False)
