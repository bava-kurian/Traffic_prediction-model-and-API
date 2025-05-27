import pandas as pd
import matplotlib.pyplot as plt
import joblib
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error
from datetime import datetime

# Step 1: Load the dataset
file_path = "ml_model/Metro_Interstate_Traffic_Volume.csv"
df = pd.read_csv(file_path)

# Step 2: Data Preprocessing
# Convert 'date_time' to datetime format
df['date_time'] = pd.to_datetime(df['date_time'])

# Extract useful time features
df['hour'] = df['date_time'].dt.hour
df['day_of_week'] = df['date_time'].dt.dayofweek  # Monday=0, Sunday=6
df['month'] = df['date_time'].dt.month

# Convert 'holiday' column to binary (1 = Holiday, 0 = Not a Holiday)
df['holiday'] = df['holiday'].apply(lambda x: 0 if x == 'None' else 1)

# Encode 'weather_main' as categorical labels
df['weather_main'] = df['weather_main'].astype('category').cat.codes

# Drop unnecessary columns
df.drop(columns=['date_time', 'weather_description'], inplace=True)

# Step 3: Define Features and Target Variable
X = df.drop(columns=['traffic_volume'])
y = df['traffic_volume']

# Split dataset (80% train, 20% test)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Step 4: Train the Model
model = RandomForestRegressor(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Step 5: Save the Model
joblib.dump(model, "ml_model/traffic_prediction_model.pkl")
print("Model saved successfully!")

# Step 6: Make Predictions
y_pred = model.predict(X_test)

# Step 7: Evaluate Model Performance
mae = mean_absolute_error(y_test, y_pred)
mse = mean_squared_error(y_test, y_pred)
rmse = mse ** 0.5
print(f"Mean Absolute Error (MAE): {mae:.2f}")
print(f"Root Mean Squared Error (RMSE): {rmse:.2f}")

# Step 8: Visualize Predictions
plt.figure(figsize=(10, 5))
plt.plot(y_test.values[:100], label='Actual Traffic Volume', color='blue')
plt.plot(y_pred[:100], label='Predicted Traffic Volume', color='red', linestyle='dashed')
plt.xlabel('Sample Index')
plt.ylabel('Traffic Volume')
plt.title('Actual vs Predicted Traffic Volume')
plt.legend()

# Save the plot instead of showing it interactively
plt.savefig("traffic_predictions.png")
print("Plot saved as traffic_predictions.png")