from flask import Flask, request, render_template, jsonify
import requests

app = Flask(__name__)
API_KEY = open('api_key', 'r').read()


def fetch_weather_data(query):
    current_url = f"http://api.openweathermap.org/data/2.5/weather?{query}&appid={API_KEY}"
    current_response = requests.get(current_url)
    current_data = current_response.json()

    if current_data.get('cod') == '404':
        return None, "City not found"

    forecast_url = f"http://api.openweathermap.org/data/2.5/forecast?{query}&appid={API_KEY}"
    forecast_response = requests.get(forecast_url)
    forecast_data = forecast_response.json()

    current_temperature = round(current_data['main']['temp'] - 273.15, 1)  # Convert to Celsius
    current_humidity = current_data['main']['humidity']
    current_wind_speed = current_data['wind']['speed'] * 3.6  # Convert to km/h
    current_conditions = current_data['weather'][0]['description']

    forecast_list = forecast_data['list']
    forecast_days = []
    for forecast in forecast_list:
        forecast_date = forecast['dt_txt'][:10]  # Extract date from datetime string
        forecast_temperature = round(forecast['main']['temp'] - 273.15, 1)  # Convert to Celsius
        forecast_conditions = forecast['weather'][0]['description']
        forecast_days.append(
            {'date': forecast_date, 'temperature': forecast_temperature, 'conditions': forecast_conditions})

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
    if request.method == 'POST':
        city = request.json.get('city')
        if not city:
            return jsonify(error="Please provide a valid city name."), 400

        query = f"q={city}"
        weather_data, error = fetch_weather_data(query)
        if error:
            return jsonify(error=error), 404

        return jsonify(weather_data)

    return render_template('index.html')


@app.route('/weather', methods=['GET'])
def get_weather_by_coords():
    lat = request.args.get('lat')
    lon = request.args.get('lon')
    if not lat or not lon:
        return jsonify(error="Coordinates not provided"), 400

    query = f"lat={lat}&lon={lon}"
    weather_data, error = fetch_weather_data(query)
    if error:
        return jsonify(error=error), 404

    return jsonify(weather_data)


if __name__ == '__main__':
    app.run()
