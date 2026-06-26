#!/usr/bin/env python3
"""
Weather Tool - Get current weather and forecasts
Uses wttr.in (free, no API key required)
"""

import argparse
import json
import ssl
import sys
import urllib.request


def get_weather(location, forecast=0, use_celsius=True):
    """Get weather from wttr.in."""
    try:
        # Build URL
        if forecast > 0:
            url = f"https://wttr.in/{location}?format=j1&lang=en"
        else:
            url = f"https://wttr.in/{location}?format=j1&lang=en"
        
        ctx = ssl.create_default_context()
        ctx.check_hostname = False
        ctx.verify_mode = ssl.CERT_NONE
        
        req = urllib.request.Request(url)
        
        with urllib.request.urlopen(req, timeout=10, context=ctx) as resp:
            data = json.loads(resp.read().decode())
        
        return data
    except Exception as e:
        print(f"Error getting weather: {e}")
        return None


def format_current(data, use_celsius=True):
    """Format current weather."""
    try:
        current = data['current_condition'][0]
        temp_c = float(current['temp_C'])
        temp_f = float(current['temp_F'])
        condition = current['weatherDesc'][0]['value']
        humidity = current['humidity']
        wind = current['windspeedKmph']
        
        temp = temp_c if use_celsius else temp_f
        unit = 'C' if use_celsius else 'F'
        
        print(f"\n=== Current Weather ===")
        print(f"Temperature: {temp}°{unit}")
        print(f"Condition: {condition}")
        print(f"Humidity: {humidity}%")
        print(f"Wind: {wind} km/h")
        
        return 0
    except Exception as e:
        print(f"Error parsing data: {e}")
        return 1


def format_forecast(data, days, use_celsius=True):
    """Format forecast."""
    try:
        weather = data.get('weather', [])
        
        print(f"\n=== {days}-Day Forecast ===")
        for i, day in enumerate(weather[:days]):
            date = day['date']
            min_c = day['mintempC']
            max_c = day['maxtempC']
            min_f = day['mintempF']
            max_f = day['maxtempF']
            condition = day['hourly'][4]['weatherDesc'][0]['value']
            
            if use_celsius:
                temp_range = f"{min_c}°C - {max_c}°C"
            else:
                temp_range = f"{min_f}°F - {max_f}°F"
            
            print(f"\n{date}: {condition}")
            print(f"  {temp_range}")
        
        return 0
    except Exception as e:
        print(f"Error parsing forecast: {e}")
        return 1


def main():
    parser = argparse.ArgumentParser(description='Weather Tool')
    parser.add_argument('location', nargs='?', help='Location (city name)')
    parser.add_argument('--forecast', type=int, default=0, help='Forecast days (1-7)')
    parser.add_argument('--json', action='store_true', help='Output as JSON')
    parser.add_argument('--celsius', action='store_true', help='Use Celsius')
    parser.add_argument('--fahrenheit', action='store_true', help='Use Fahrenheit')
    
    args = parser.parse_args()
    
    use_celsius = not args.fahrenheit
    
    if not args.location:
        parser.print_help()
        return 1
    
    print(f"Getting weather for: {args.location}...")
    
    data = get_weather(args.location, args.forecast, use_celsius)
    if not data:
        return 1
    
    if args.json:
        print(json.dumps(data, indent=2))
        return 0
    
    if args.forecast > 0:
        return format_forecast(data, args.forecast, use_celsius)
    else:
        return format_current(data, use_celsius)


if __name__ == '__main__':
    sys.exit(main())
