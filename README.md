# SimpleWeather

A lightweight, responsive weather application that provides current weather conditions and a 5-day forecast for any city in the world.

## Features

- **Current Weather Display**: Real-time temperature, "feels like" temperature, humidity, and wind speed
- **5-Day Forecast**: Detailed daily forecasts with min/max temperatures, weather conditions, precipitation probability, and wind speed
- **City Search**: Enter any city name to get weather data
- **Responsive Design**: Optimized for desktop, tablet, and mobile devices
- **Dark Theme**: Modern dark UI with emoji weather indicators
- **No Authentication Required**: Free to use with Open-Meteo API

## Prerequisites

- Python 3.7+
- pip (Python package manager)

## Installation

1. Clone or download this repository:
   ```bash
   git clone <repository-url>
   cd SimpleWeather
   ```

2. Install required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

1. Start the Flask development server:
   ```bash
   python simpleweather.py
   ```

2. Open your browser and navigate to:
   ```
   http://localhost:5000
   ```

3. Enter a city name in the search box and click "Search" (or press Enter)

4. View the current weather and 5-day forecast

## Project Structure

```
SimpleWeather/
├── simpleweather.py        # Flask backend API
├── requirements.txt        # Python dependencies
├── static/
│   └── index.html         # Frontend HTML, CSS, and JavaScript
└── README.md              # This file
```

## API Endpoints

### GET `/`
Serves the main HTML page.

### POST `/api/weather`
Fetches weather data for a given city.

**Request Body:**
```json
{
  "city": "London"
}
```

**Response:**
```json
{
  "city": "London",
  "country": "United Kingdom",
  "temperature": 12.6,
  "feels_like": 9.6,
  "humidity": 74,
  "wind_speed": 16.9,
  "icon": "☀️",
  "weather_code": 0,
  "forecast": [
    {
      "date": "2026-04-15",
      "temp_max": 16.7,
      "temp_min": 11.8,
      "weather_code": 51,
      "icon": "🌧️",
      "precipitation_prob": 94,
      "wind_speed": 24.5
    }
  ]
}
```

## Technologies Used

- **Backend**: Flask (Python web framework)
- **Frontend**: HTML5, CSS3, JavaScript (Vanilla)
- **Weather API**: Open-Meteo (free, no API key required)
- **Geocoding**: Open-Meteo Geocoding API

## Weather Icons

The app uses emoji icons to represent weather conditions:
- ☀️ Clear sky
- 🌤️ Mainly clear
- ⛅ Partly cloudy
- ☁️ Overcast
- 🌫️ Foggy
- 🌧️ Rainy
- 🌨️ Snowy
- ⛈️ Thunderstorm

## Browser Support

- Chrome/Edge (latest)
- Firefox (latest)
- Safari (latest)
- Mobile browsers (iOS Safari, Chrome Mobile)

## API Rate Limits

SimpleWeather uses the free Open-Meteo API with the following limits:
- 600 requests/minute
- 5,000 requests/hour
- 10,000 requests/day
- 300,000 requests/month

For higher limits, see [Open-Meteo Pricing](https://open-meteo.com/en/pricing).

## Attribution

Weather data provided by [Open-Meteo.com](https://open-meteo.com/) under CC BY 4.0 license.

## Responsive Layout

- **Desktop (>768px)**: 5 forecast cards in a single row
- **Tablet (480px - 768px)**: 3 forecast cards per row
- **Mobile (<480px)**: 2 forecast cards per row

Container max-width: 80% of viewport (minimum 400px)

## Development

To run with Flask debug mode and auto-reload:
```bash
python simpleweather.py
```

Server runs on `http://0.0.0.0:5000` (accessible from any local network device).

## Future Enhancements

Potential features for future versions:
- Hourly forecast view
- Weather alerts
- Favorite cities/bookmarks
- Unit conversion (°C to °F, km/h to mph)
- Extended forecast (14 days)
- Weather maps
- PWA (Progressive Web App) support

## License

This project is open source and available under the MIT License.

---

**Created with ❤️**
