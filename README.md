# Traffic Trend Prediction System

## Setup Instructions

### Backend (Flask API)
1. Install the required packages:
    ```sh
    pip install flask
    ```

2. Run the Flask API:
    ```sh
    python backend/app.py
    ```

### Frontend (Web Dashboard)
1. Open `frontend/index.html` in a web browser.

### API Testing
1. Install `requests` if not already installed:
    ```sh
    pip install requests
    ```

2. Run the API testing script:
    ```sh
    python backend/test_api.py
    ```

### Rule-Based Prediction Logic
- **Vehicle Count** > 70 → "Very High"
- **Vehicle Count** > 50 → "High" (unless "Rainy" weather or "Weekend Rush")
- **Vehicle Count** > 30 → "Medium"
- **Rainy Weather + High Traffic** → "Very High"
- **Weekend Rush (Friday/Saturday) + High Traffic** → "High"