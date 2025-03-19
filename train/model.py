import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error
import joblib
import warnings

# Suppress warnings
warnings.filterwarnings("ignore")

# Load dataset
data = pd.read_csv(r'C:\Users\sanjay\Desktop\Project\nonbank_users_dataset_v2.csv')

# Define Features & Target
features = ["upi_transactions", "income", "expenditure", "bill_payments_time"]
target = "generated_credit_score"

X = data[features]
y = data[target]

# Normalize the target (Credit Score should be between 300-900)
y = 300 + ((y - y.min()) * (600 / (y.max() - y.min())))

# Train-Test Split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Scaling Features (MinMaxScaler ensures values remain in a meaningful range)
scaler = MinMaxScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# Train Model (RandomForestRegressor for better interpretability)
model = RandomForestRegressor(n_estimators=200, random_state=42)
model.fit(X_train_scaled, y_train)

# Evaluate Model
y_pred = model.predict(X_test_scaled)
mae = mean_absolute_error(y_test, y_pred)
print(f"Mean Absolute Error: {mae:.2f}")

# Save Model and Scaler
joblib.dump(model, "cibil_score_model.pkl")
joblib.dump(scaler, "scaler.pkl")