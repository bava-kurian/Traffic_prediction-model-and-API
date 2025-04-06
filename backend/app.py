from flask import Flask, request, jsonify
from flask_cors import CORS
import joblib
import pandas as pd
from datetime import datetime

app = Flask(__name__)
CORS(app)

# Load model
model = joblib.load("ml_model/traffic_prediction_model.pkl")

# Define traffic level based on predicted volume
def get_traffic_level(volume):
    if volume > 5000:
        return "Very High"
    elif volume > 3000:
        return "High"
    elif volume > 1500:
        return "Medium"
    else:
        return "Low"

# Define signal timing based on traffic level
def get_signal_timing(level):
    timings = {
        "Low": {"green": 30, "red": 60},
        "Medium": {"green": 45, "red": 75},
        "High": {"green": 60, "red": 90},
        "Very High": {"green": 90, "red": 120},
    }
    return timings[level]

@app.route('/predict', methods=['POST'])
def predict():
    try:
        data = request.get_json()

        print("\n--- Incoming Request ---")
        print("Raw JSON Data:", data)

        # Simulate environmental data for now
        weather_map = {"Clear": 0, "Clouds": 1, "Rain": 2, "Snow": 3}
        day_map = {"Monday": 0, "Tuesday": 1, "Wednesday": 2, "Thursday": 3, "Friday": 4, "Saturday": 5, "Sunday": 6}

        hour = int(data['hour'])
        day_of_week = day_map.get(data['day'], 0)
        weather_main = weather_map.get(data['weather'], 0)
        holiday = int(data.get('holiday', 0))
        month = int(data.get('month', datetime.now().month))
        clouds_all = int(data.get('clouds_all', 50))
        rain_1h = float(data.get('rain_1h', 0))
        snow_1h = float(data.get('snow_1h', 0))
        temp = float(data.get('temp', 285))

        # Form feature array
        features = pd.DataFrame([[holiday, temp, rain_1h, snow_1h, clouds_all,
                                  weather_main, hour, day_of_week, month]],
                                columns=[
                                    'holiday', 'temp', 'rain_1h', 'snow_1h', 'clouds_all',
                                    'weather_main', 'hour', 'day_of_week', 'month'
                                ])

        print("\nFeature Vector Sent to Model:")
        print(features)

        predicted_volume = model.predict(features)[0]
        traffic_level = get_traffic_level(predicted_volume)
        signal_timing = get_signal_timing(traffic_level)

        print("\nPrediction Output:")
        print(f"Predicted Volume: {predicted_volume}")
        print(f"Traffic Level: {traffic_level}")
        print(f"Signal Timing: {signal_timing}")
        print("----------------------------\n")

        return jsonify({
            "predicted_volume": round(predicted_volume, 2),
            "traffic_level": traffic_level,
            "signal_timing": signal_timing
        })

    except Exception as e:
        print("Error:", str(e))
        return jsonify({"error": str(e)}), 500

@app.route('/intersections', methods=['GET'])
def intersections():
    try:
        # Dummy intersection coordinates
        dummy_intersections = [
            {"name": "Intersection A", "latitude": 9.9312, "longitude": 76.2673},
            {"name": "Intersection B", "latitude": 9.9380, "longitude": 76.2665},
            {"name": "Intersection C", "latitude": 9.9256, "longitude": 76.2708},
            {"name": "Intersection D", "latitude": 9.9401, "longitude": 76.2764}
        ]

        # Sample environmental input (can later make dynamic per intersection)
        common_input = {
            'holiday': 0,
            'temp': 285,
            'rain_1h': 0,
            'snow_1h': 0,
            'clouds_all': 40,
            'weather_main': 0,  # Clear
            'hour': 10,
            'day_of_week': 1,  # Tuesday
            'month': 4
        }

        features = pd.DataFrame([[
            common_input['holiday'], common_input['temp'], common_input['rain_1h'],
            common_input['snow_1h'], common_input['clouds_all'], common_input['weather_main'],
            common_input['hour'], common_input['day_of_week'], common_input['month']
        ]] * len(dummy_intersections), columns=[
            'holiday', 'temp', 'rain_1h', 'snow_1h', 'clouds_all',
            'weather_main', 'hour', 'day_of_week', 'month'
        ])

        predictions = model.predict(features)

        enriched_data = []
        for i, intersection in enumerate(dummy_intersections):
            volume = predictions[i]
            level = get_traffic_level(volume)
            timing = get_signal_timing(level)

            enriched_data.append({
                "name": intersection["name"],
                "latitude": intersection["latitude"],
                "longitude": intersection["longitude"],
                "predicted_volume": round(volume, 2),
                "traffic_level": level,
                "signal_timing": timing
            })

        return jsonify(enriched_data)

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
