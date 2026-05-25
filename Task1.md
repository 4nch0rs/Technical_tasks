# Beach Vacation Weather Optimizer

A Python command-line tool that helps you choose the best city for a beach vacation by comparing weather conditions across three destinations using real forecast data.

---

## What It Does

The app fetches hourly weather data for three cities of your choice over two vacation days, scores each city based on how closely its weather matches ideal Mediterranean summer beach conditions (3:00–4:00 PM each day), and displays a ranked comparison with an interactive map.

---

## Requirements

- Python 3.8+
- An API key from [WeatherAPI](https://www.weatherapi.com) (free tier is sufficient)

Install dependencies:

```bash
pip install requests folium matplotlib
```

---

## Setup

1. Open `weather_optimizer.py`
2. Replace `YOUR_API_KEY_HERE` with your WeatherAPI key:
```python
API_KEY = "your_key_here"
```

---

## How to Run

```bash
python weather_optimizer.py
```

---

## How to Use

1. Enter your vacation start date in `YYYY-MM-DD` format
   - If the date is **within 14 days**: uses Forecast API with full air quality data
   - If the date is **14+ days ahead**: uses Future API with visibility as air quality proxy
2. Enter the names of 3 cities you are considering

Example:
```
Give start date (YYYY-MM-DD): 2026-07-01
Give city 1: Barcelona
Give city 2: Athens
Give city 3: Lisbon
```

---

## Scoring Algorithm

Each city is scored out of **100 points** — 50 points per day. Each day is evaluated across 5 weather parameters measured at 3:00 PM:

| Parameter | Ideal Value | Max Points |
|---|---|---|
| Temperature | 28–35°C | 10 |
| Cloud cover | 0–10% | 10 |
| Chance of rain | 0–5% | 10 |
| Humidity | 40–60% | 10 |
| Air quality (AQI) | Index 1 (Good) | 10 |

Scores scale down gradually as values move away from the ideal range. Rain is penalized most aggressively as even a moderate chance significantly impacts beach comfort.

---

## Output

- Ranked list of cities printed in the terminal with score, temperature, cloud cover, rain chance, humidity, and air quality for each day
- Interactive map (`beach_map.html`) opens automatically in your browser with color-coded markers:
  - 🟢 **Green** — score ≥ 70/100
  - 🟠 **Orange** — score 40–69/100
  - 🔴 **Red** — score below 40/100

---

## Known Limitations

- Vacation dates must be at least **14 days from today** when using the Future API
- Weather forecasts beyond 14 days are estimates and accuracy decreases further into the future
- Free WeatherAPI tier has a request limit of 1,000,000 calls per month

---

## Author

Andrei Korzin — drew.korzin@gmail.com
