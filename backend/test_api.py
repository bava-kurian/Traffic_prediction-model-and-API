import requests

def test_prediction():
    url = 'http://127.0.0.1:5000/predict'
    data = {
        'Time': 8,  # Hour of the day (0-23)
        'Day': 'Monday',  # Day of the week
        'Weather': 'Clear'  # Weather condition
    }

    response = requests.post(url, json=data)

    print(f"Status Code: {response.status_code}")
    print(f"Raw Response: {response.text}")

    try:
        print("JSON Response:", response.json())
    except requests.exceptions.JSONDecodeError:
        print("Error: Response is not in JSON format.")

if __name__ == '__main__':
    test_prediction()
