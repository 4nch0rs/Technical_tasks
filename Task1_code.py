"""
Type: Technical assignment
Developer: Andrei Korzin
Email: drew.korzin@gmail.com
Date: 25.05.2026

Description: The designed program is a travelling optimization app.


Mediterranian summer definition

Temperature: 28-35C
Air clarity: 0-50 good, 51-100 moderate, 100+ bad
Cloudiness: 0-10%
Chance of rain: 0-5%
Humidity: 40-60%

"""

import requests
from datetime import datetime, timedelta
import folium

API_KEY = "503fbb7398044979ade140408262305"
cities = {}
time = "15:00"


def api_get(date, city):
    date_obj = datetime.strptime(date, "%Y-%m-%d")
    day2 = (date_obj + timedelta(days=1)).strftime("%Y-%m-%d")
    dates = [date, day2]
    results = []
    for current_date in dates:
        days_from_today = (
            datetime.strptime(current_date, "%Y-%m-%d") - datetime.now()
        ).days
        if days_from_today >= 14:
            url = f"http://api.weatherapi.com/v1/future.json?key={API_KEY}&q={city}&dt={current_date}"
            use_aqi = False
        else:
            url = f"http://api.weatherapi.com/v1/forecast.json?key={API_KEY}&q={city}&dt={current_date}&days=1&aqi=yes"
            use_aqi = True

        response = requests.get(url)
        data = dict(response.json())
        if "error" in data:
            print(f"API error for {city} on {current_date}: {data['error']['message']}")
            continue
        days_data = data["forecast"]["forecastday"][0]["hour"]
        for d in days_data:
            if d["time"] == f"{current_date} {time}":
                results.append(
                    {
                        "date": current_date,
                        "temp_c": d["temp_c"],
                        "cloud": d["cloud"],
                        "chance_of_rain": d["chance_of_rain"],
                        "humidity": d["humidity"],
                        "air_quality": (
                            d["air_quality"]["us-epa-index"] if use_aqi else None
                        ),
                        "vis_km": d["vis_km"],
                        "lat": data["location"]["lat"],
                        "lon": data["location"]["lon"],
                    }
                )
    return results


def score_day(day: dict) -> float:
    score = 0

    temp = day["temp_c"]
    if 28 <= temp <= 35:
        score += 10
    elif temp < 28:
        score += max(0, 10 - (28 - temp) * 1.0)
    else:
        score += max(0, 10 - (temp - 35) * 1.5)

    cloud = day["cloud"]
    if cloud <= 10:
        score += 10
    else:
        score += max(0, 10 - (cloud - 10) * 0.15)

    rain = day["chance_of_rain"]
    if rain <= 5:
        score += 10
    else:
        score += max(0, 10 - (rain - 5) * 0.25)

    humidity = day["humidity"]
    if 40 <= humidity <= 60:
        score += 10
    elif humidity < 40:
        score += max(0, 10 - (40 - humidity) * 0.2)
    else:
        score += max(0, 10 - (humidity - 60) * 0.2)

    if day["air_quality"] is not None:
        aqi = day["air_quality"]
        if aqi == 1:
            score += 10
        elif aqi == 2:
            score += 7
        elif aqi == 3:
            score += 4
        else:
            score += 0
    else:
        vis = day["vis_km"]
        if vis >= 10:
            score += 10
        else:
            score += max(0, vis * 1.0)

    return round(score, 2)


def points_comp(cities: dict) -> dict:
    scored = {}
    for city, days in cities.items():
        if len(days) < 2:
            print(f"Warning: could not get 2 days of data for {city}")
            continue
        day1_score = score_day(days[0])
        day2_score = score_day(days[1])
        scored[city] = {
            "total": round(day1_score + day2_score, 2),
            "day1_score": day1_score,
            "day2_score": day2_score,
            "days": days,
        }
    return dict(sorted(scored.items(), key=lambda x: x[1]["total"], reverse=True))


def HMI():
    date = input("Give start date (YYYY-MM-DD): ")
    for i in range(3):
        city = input(f"Give city {i+1}: ")
        cities[city] = api_get(date, city)


def plot_map(scored: dict):
    first = list(scored.values())[0]
    lat = first["days"][0]["lat"]
    lon = first["days"][0]["lon"]

    m = folium.Map(location=[lat, lon], zoom_start=5)

    for city, data in scored.items():
        city_lat = data["days"][0]["lat"]
        city_lon = data["days"][0]["lon"]
        score = data["total"]
        color = "green" if score >= 70 else "orange" if score >= 40 else "red"
        folium.Marker(
            location=[city_lat, city_lon],
            tooltip=f"{city}: {score}/100",
            icon=folium.Icon(color=color),
        ).add_to(m)

    m.save("beach_map.html")
    import webbrowser

    webbrowser.open("beach_map.html")


def main():
    HMI()
    scored = points_comp(cities)
    best_city = list(scored.keys())[0]
    print(f"\nBest city for your beach vacation: {best_city}")
    plot_map(scored)


if __name__ == "__main__":
    main()
