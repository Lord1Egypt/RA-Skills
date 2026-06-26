#!/usr/bin/env python3
"""
Weather Fetcher

Fetches weather forecasts for destinations using weather skill.
"""

import argparse
import json
import subprocess
import sys
from datetime import datetime, timedelta


def parse_args():
    parser = argparse.ArgumentParser(description="Fetch weather forecasts")
    parser.add_argument("--destinations", required=True, help="Comma-separated cities")
    parser.add_argument("--start-date", required=True, help="Forecast start date (YYYY-MM-DD)")
    parser.add_argument("--end-date", required=True, help="Forecast end date (YYYY-MM-DD)")
    parser.add_argument("--output", required=True, help="Output JSON file")
    return parser.parse_args()


def fetch_weather_wttr(city, date):
    """Fetch weather using wttr.in (weather skill backend)"""
    try:
        # Use wttr.in format: city?format=j1
        cmd = ["curl", "-s", f"https://wttr.in/{city}?format=j1"]
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=10)
        
        if result.returncode != 0:
            return None
        
        data = json.loads(result.stdout)
        
        # Find forecast for the date
        target_date = datetime.strptime(date, "%Y-%m-%d")
        
        for forecast in data.get("weather", []):
            forecast_date = datetime.strptime(forecast["date"], "%Y-%m-%d")
            if forecast_date == target_date:
                # Extract relevant data
                return {
                    "city": city,
                    "date": date,
                    "temperature": f"{forecast['mintempC']}-{forecast['maxtempC']}°C",
                    "condition": forecast['hourly'][0]['weatherDesc'][0]['value'],
                    "precipitation": f"{forecast.get('hourly', [{}])[0].get('precipMM', '0')}mm",
                    "humidity": f"{forecast.get('hourly', [{}])[0].get('humidity', 'N/A')}%",
                    "wind": f"{forecast.get('hourly', [{}])[0].get('windspeedKmph', 'N/A')} km/h"
                }
        
        # If date not in forecast, return current weather
        current = data.get("current_condition", [{}])[0]
        return {
            "city": city,
            "date": date,
            "temperature": f"{current.get('temp_C', 'N/A')}°C",
            "condition": current.get('weatherDesc', [{}])[0].get('value', 'N/A'),
            "precipitation": "N/A",
            "humidity": f"{current.get('humidity', 'N/A')}%",
            "wind": f"{current.get('windspeedKmph', 'N/A')} km/h"
        }
        
    except Exception as e:
        print(f"⚠️  Weather fetch failed for {city} on {date}: {e}", file=sys.stderr)
        return {
            "city": city,
            "date": date,
            "temperature": "N/A",
            "condition": "N/A",
            "precipitation": "N/A",
            "humidity": "N/A",
            "wind": "N/A"
        }


def main():
    args = parse_args()
    
    cities = [c.strip() for c in args.destinations.split(',')]
    start = datetime.strptime(args.start_date, "%Y-%m-%d")
    end = datetime.strptime(args.end_date, "%Y-%m-%d")
    
    print(f"🌤️  Fetching weather for {len(cities)} cities...")
    
    forecasts = []
    current = start
    while current <= end:
        date_str = current.strftime("%Y-%m-%d")
        for city in cities:
            print(f"   📍 {city} - {date_str}")
            forecast = fetch_weather_wttr(city, date_str)
            if forecast:
                forecasts.append(forecast)
        current += timedelta(days=1)
    
    weather_data = {
        "destinations": cities,
        "start_date": args.start_date,
        "end_date": args.end_date,
        "forecasts": forecasts,
        "fetched_at": datetime.now().isoformat()
    }
    
    with open(args.output, 'w', encoding='utf-8') as f:
        json.dump(weather_data, f, indent=2, ensure_ascii=False)
    
    print(f"\n✅ Weather data saved to: {args.output}")
    print(f"   📊 Total forecasts: {len(forecasts)}")


if __name__ == "__main__":
    main()
