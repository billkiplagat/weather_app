document.getElementById('weather-form').addEventListener('submit', function(e) {
    e.preventDefault();
    const city = document.getElementById('city').value;
    if (city) {
        fetchWeather(city);
    } else {
        alert('Please enter a city name.');
    }
});

function fetchWeather(city) {
    fetch('/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ city: city })
    })
    .then(response => response.json())
    .then(data => {
        if (data.error) {
            alert(data.error);
        } else {
            updateWeather(data);
        }
    })
    .catch(error => console.error('Error:', error));
}

function updateWeather(data) {
    document.getElementById('current-weather-heading').innerText = `Current Weather in ${data.city}`;
    document.getElementById('current-temperature').innerText = `Temperature: ${data.current_temperature} °C`;
    document.getElementById('current-humidity').innerText = `Humidity: ${data.current_humidity} %`;
    document.getElementById('current-wind-speed').innerText = `Wind Speed: ${data.current_wind_speed} km/h`;
    document.getElementById('current-conditions').innerText = `Conditions: ${data.current_conditions}`;

    const forecastContainer = document.getElementById('forecast-days');
    forecastContainer.innerHTML = '';
    data.forecast_days.forEach(day => {
        const dayDiv = document.createElement('div');
        dayDiv.className = 'forecast-day';
        dayDiv.innerHTML = `
            <p>${day.date}</p>
            <p>Temp: ${day.temperature} °C</p>
            <p>${day.conditions}</p>
        `;
        forecastContainer.appendChild(dayDiv);
    });
}


document.getElementById('current-location-btn').addEventListener('click', function() {
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(showPosition);
    } else {
        alert("Geolocation is not supported by this browser.");
    }
});

function showPosition(position) {
    const lat = position.coords.latitude;
    const lon = position.coords.longitude;
    fetchWeatherByCoords(lat, lon);
}

function fetchWeatherByCoords(lat, lon) {
    fetch(`/weather?lat=${lat}&lon=${lon}`, {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json'
        }
    })
    .then(response => response.json())
    .then(data => updateWeather(data))
    .catch(error => console.error('Error:', error));
}

