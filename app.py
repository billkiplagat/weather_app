from flask import Flask, request, render_template, jsonify
import requests

# Initialize Flask application
app = Flask(__name__)

# Read the OpenWeatherMap API key from a file
API_KEY = open('api_key', 'r').read()


def fetch_weather_data(query):
    """
    Fetch current weather and forecast data from OpenWeatherMap API.

    Args:
    query (str): The query string to be appended to the API URL (e.g., "q=London" or "lat=35&lon=139").

    Returns:
    tuple: A dictionary containing weather data if successful, otherwise None and an error message.
    """
    # Make API request to OpenWeatherMap for current weather
    current_url = f"http://api.openweathermap.org/data/2.5/weather?{query}&appid={API_KEY}"
    current_response = requests.get(current_url)
    current_data = current_response.json()
    print(current_data)

    # Check if city not found
    if current_data.get('cod') == '404':
        return None, "City not found"

    # Make API request to OpenWeatherMap for forecast
    forecast_url = f"http://api.openweathermap.org/data/2.5/forecast?{query}&appid={API_KEY}"
    forecast_response = requests.get(forecast_url)
    forecast_data = forecast_response.json()

    # Extract relevant current weather data
    current_temperature = round(current_data['main']['temp'] - 273.15, 1)  # Convert from Kelvin to Celsius
    current_humidity = current_data['main']['humidity']
    current_wind_speed = current_data['wind']['speed'] * 3.6  # Convert from m/s to km/h
    current_conditions = current_data['weather'][0]['description']

    # Extract relevant forecast data
    forecast_list = forecast_data['list']
    forecast_days = []
    for forecast in forecast_list:
        forecast_date = forecast['dt_txt'][:10]  # Extract date from datetime string
        forecast_temperature = round(forecast['main']['temp'] - 273.15, 1)  # Convert from Kelvin to Celsius
        forecast_conditions = forecast['weather'][0]['description']
        forecast_days.append(
            {'date': forecast_date, 'temperature': forecast_temperature, 'conditions': forecast_conditions})

    # Prepare weather data dictionary
    weather_data = {
        'city': current_data['name'],
        'current_temperature': current_temperature,
        'current_humidity': current_humidity,
        'current_wind_speed': current_wind_speed,
        'current_conditions': current_conditions,
        'forecast_days': forecast_days
    }

    return weather_data, None


@app.route('/', methods=['GET', 'POST'])
def get_weather():
    """
    Handle requests to the root URL.

    For GET requests, render the index.html form.
    For POST requests, fetch and return weather data for the specified city.

    Returns:
    str: Rendered HTML template for GET requests or JSON data for POST requests.
    """
    if request.method == 'POST':
        city = request.json.get('city')
        if not city:
            return jsonify(error="Please provide a valid city name."), 400

        query = f"q={city}"
        weather_data, error = fetch_weather_data(query)
        if error:
            return jsonify(error=error), 404

        return jsonify(weather_data)

    # For GET requests, render the form
    return render_template('index.html')


@app.route('/weather', methods=['GET'])
def get_weather_by_coords():
    """
    Handle requests to fetch weather data by geographic coordinates.

    Args:
    None

    Returns:
    JSON: Weather data for the specified coordinates or an error message.
    """
    lat = request.args.get('lat')
    lon = request.args.get('lon')
    if not lat or not lon:
        return jsonify(error="Coordinates not provided"), 400

    query = f"lat={lat}&lon={lon}"
    weather_data, error = fetch_weather_data(query)
    if error:
        return jsonify(error=error), 404

    return jsonify(weather_data)


# Run the Flask app
if __name__ == '__main__':
    app.run()
