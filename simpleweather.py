from flask import Flask, request, jsonify, send_file
import requests
from pathlib import Path

app = Flask(__name__, static_folder='static', static_url_path='')

# Weather code to emoji mapping (Open-Meteo WMO codes)
WEATHER_ICONS = {
    0: "☀️",      # Clear sky
    1: "🌤️",     # Mainly clear
    2: "⛅",      # Partly cloudy
    3: "☁️",      # Overcast
    45: "🌫️",    # Foggy
    48: "🌫️",    # Depositing rime fog
    51: "🌧️",    # Light drizzle
    53: "🌧️",    # Moderate drizzle
    55: "🌧️",    # Dense drizzle
    61: "🌧️",    # Slight rain
    63: "🌧️",    # Moderate rain
    65: "⛈️",    # Heavy rain
    71: "🌨️",    # Slight snow
    73: "🌨️",    # Moderate snow
    75: "🌨️",    # Heavy snow
    77: "🌨️",    # Snow grains
    80: "🌦️",    # Slight rain showers
    81: "🌧️",    # Moderate rain showers
    82: "⛈️",    # Violent rain showers
    85: "🌨️",    # Slight snow showers
    86: "🌨️",    # Heavy snow showers
    95: "⛈️",    # Thunderstorm
    96: "⛈️",    # Thunderstorm with slight hail
    99: "⛈️",    # Thunderstorm with heavy hail
}

@app.route('/')
def index():
    return send_file('static/index.html')

@app.route('/api/weather', methods=['POST'])
def get_weather():
    try:
        data = request.get_json()
        city = data.get('city', '').strip()
        
        if not city:
            return jsonify({'error': 'City name required'}), 400
        
        # Geocode the city (convert city name to latitude/longitude)
        geo_url = "https://geocoding-api.open-meteo.com/v1/search"
        geo_params = {
            'name': city,
            'count': 1,
            'language': 'en',
            'format': 'json'
        }
        
        try:
            geo_response = requests.get(geo_url, params=geo_params, timeout=5)
            geo_data = geo_response.json()
        except requests.RequestException as e:
            return jsonify({'error': 'Failed to connect to weather service'}), 503
        
        # Check if city was found
        if not geo_data.get('results') or len(geo_data['results']) == 0:
            return jsonify({'error': f'City "{city}" not found'}), 404
        
        result = geo_data['results'][0]
        latitude = result['latitude']
        longitude = result['longitude']
        city_name = result.get('name', city)
        country = result.get('country', '')
        
        # Fetch weather data
        weather_url = "https://api.open-meteo.com/v1/forecast"
        weather_params = {
            'latitude': latitude,
            'longitude': longitude,
            'current': 'temperature_2m,weather_code,relative_humidity_2m,apparent_temperature,wind_speed_10m',
            'daily': 'temperature_2m_max,temperature_2m_min,weather_code,precipitation_sum,precipitation_probability_max,wind_speed_10m_max',
            'forecast_days': 5,
            'timezone': 'auto',
            'temperature_unit': 'celsius',
            'wind_speed_unit': 'kmh'
        }
        
        try:
            weather_response = requests.get(weather_url, params=weather_params, timeout=5)
            weather_data = weather_response.json()
        except requests.RequestException as e:
            return jsonify({'error': 'Failed to fetch weather data'}), 503
        
        current = weather_data.get('current', {})
        weather_code = current.get('weather_code', 0)
        
        # Process 5-day forecast
        daily = weather_data.get('daily', {})
        forecast = []
        
        if daily:
            times = daily.get('time', [])
            temps_max = daily.get('temperature_2m_max', [])
            temps_min = daily.get('temperature_2m_min', [])
            weather_codes = daily.get('weather_code', [])
            precip_prob = daily.get('precipitation_probability_max', [])
            wind_speeds = daily.get('wind_speed_10m_max', [])
            
            for i in range(min(5, len(times))):
                forecast.append({
                    'date': times[i],
                    'temp_max': round(temps_max[i], 1),
                    'temp_min': round(temps_min[i], 1),
                    'weather_code': weather_codes[i],
                    'icon': WEATHER_ICONS.get(weather_codes[i], '🌍'),
                    'precipitation_prob': precip_prob[i] if i < len(precip_prob) else 0,
                    'wind_speed': round(wind_speeds[i], 1) if i < len(wind_speeds) else 0
                })
        
        weather_info = {
            'city': city_name,
            'country': country,
            'temperature': round(current.get('temperature_2m', 0), 1),
            'feels_like': round(current.get('apparent_temperature', 0), 1),
            'humidity': current.get('relative_humidity_2m', 0),
            'wind_speed': round(current.get('wind_speed_10m', 0), 1),
            'weather_code': weather_code,
            'icon': WEATHER_ICONS.get(weather_code, '🌍'),
            'forecast': forecast
        }
        
        return jsonify(weather_info), 200
    
    except Exception as e:
        return jsonify({'error': 'Internal server error'}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)