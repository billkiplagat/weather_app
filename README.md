# WeatherWise
WeatherWise is a user-friendly web application that provides real-time weather information and a 5-day forecast for any city worldwide. The application fetches data from the OpenWeatherMap API and displays current temperature, humidity, wind speed, and weather conditions, along with a forecast. The app also supports geolocation-based weather information, allowing users to get weather updates based on their current location.

# Technologies Used
* Backend: Flask (Python)
* Frontend: HTML, CSS, JavaScript
* API: OpenWeatherMap API
* Version Control: Git and GitHub
* Project Management: Trello or similar Kanban board

# Third-Party Services
* OpenWeatherMap API: To fetch real-time weather data and forecasts.
* Geolocation API: To determine the user's current location for location-based weather updates.

# Installation
1. Clone the repository
`git clone https://github.com/yourusername/weatherwise.git
cd weatherwise
`
2. Create a virtual environment and activate it
`python3 -m venv venv
source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
`
3. Set up the OpenWeatherMap API key:
* Sign up at OpenWeatherMap to get an API key.
* Create a file named `api_key` in the project root and paste your API key into it.

4. Run the application
`python app.py
`
5. Open your browser and navigate to
`http://127.0.0.1:5000/
`
# Usage
1. Search for a city's weather:
* Enter the city name in the input field and click the "Get Weather" button to fetch and display the current weather and 5-day forecast.

2. Get weather for your current location:
* Click the "Get Weather for My Location" button to fetch weather data based on your current geolocation.
