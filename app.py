from flask import Flask, request, render_template
import requests

app = Flask(__name__)
API_KEY = open('api_key', 'r').read()


@app.route('/')
def hello_world():
    return 'Hello World!'


@app.route('/weather', methods=['GET', 'POST'])
def get_weather():
    if request.method == 'POST':
        city = request.form.get('city')
        if not city:
            return "Please provide a valid city name."

        # Make API request to OpenWeatherMap for current weather
        current_url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}"
        current_response = requests.get(current_url)
        current_data = current_response.json()

        # Make API request to OpenWeatherMap for forecast
        forecast_url = f"http://api.openweathermap.org/data/2.5/forecast?q={city}&appid={API_KEY}"
        forecast_response = requests.get(forecast_url)
        forecast_data = forecast_response.json()

        # Check if city not found
        if current_data.get('cod') == '404':
            return render_template('error.html')

        # Extract relevant current weather data
        current_temperature = round(current_data['main']['temp'] - 273.15, 1)  # Convert to Celsius
        current_humidity = current_data['main']['humidity']
        current_wind_speed = current_data['wind']['speed'] * 3.6
        current_conditions = current_data['weather'][0]['description']

        # Extract relevant forecast data
        forecast_list = forecast_data['list']
        forecast_days = []
        for forecast in forecast_list:
            forecast_date = forecast['dt_txt'][:10]  # Extract date from datetime string
            forecast_temperature = round(forecast['main']['temp'] - 273.15, 1)  # Convert to Celsius
            forecast_conditions = forecast['weather'][0]['description']
            forecast_days.append(
                {'date': forecast_date, 'temperature': forecast_temperature, 'conditions': forecast_conditions})

        # Create the response
        return render_template('weather.html', city=city, current_temperature=current_temperature,
                               current_humidity=current_humidity,
                               current_wind_speed=current_wind_speed, current_conditions=current_conditions,
                               forecast_days=forecast_days)


if __name__ == '__main__':
    app.run()
