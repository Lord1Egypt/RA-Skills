#!/usr/bin/env python3
"""
Weather forecast script for Open-Meteo API
Fetches hourly temperature forecasts for a given location
"""

import sys
import json
import urllib.request
import urllib.error
from typing import Dict, Any, Optional

def get_weather_forecast(latitude: float, longitude: float, hourly_params: str = "temperature_2m") -> Dict[str, Any]:
    """
    Fetch weather forecast from Open-Meteo API

    Args:
        latitude: Latitude of the location (-90 to 90)
        longitude: Longitude of the location (-180 to 180)
        hourly_params: Comma-separated list of hourly parameters (default: temperature_2m)

    Returns:
        Dictionary containing weather data

    Raises:
        urllib.error.URLError: If network request fails
        ValueError: If coordinates are invalid
        json.JSONDecodeError: If response is not valid JSON
    """
    # Validate coordinates
    if not (-90 <= latitude <= 90):
        raise ValueError(f"Invalid latitude: {latitude}. Must be between -90 and 90")
    if not (-180 <= longitude <= 180):
        raise ValueError(f"Invalid longitude: {longitude}. Must be between -180 and 180")

    # Build API URL
    base_url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": str(latitude),
        "longitude": str(longitude),
        "hourly": hourly_params
    }
    url = f"{base_url}?{urllib.parse.urlencode(params)}"

    # Make API request
    try:
        with urllib.request.urlopen(url, timeout=30) as response:
            if response.getcode() != 200:
                raise urllib.error.HTTPError(
                    url, response.getcode(), f"HTTP {response.getcode()}", response.headers, None
                )
            data = json.loads(response.read().decode('utf-8'))
            return data
    except urllib.error.URLError as e:
        raise urllib.error.URLError(f"Failed to fetch weather data: {e.reason}")

def print_weather_summary(data: Dict[str, Any]) -> None:
    """
    Print a summary of the weather forecast

    Args:
        data: Weather data from the API
    """
    if not data or 'hourly' not in data:
        print("No weather data available")
        return

    hourly = data['hourly']
    times = hourly.get('time', [])
    temperatures = hourly.get('temperature_2m', [])

    if not times or not temperatures:
        print("No temperature data available")
        return

    print(f"\n{'='*60}")
    print(f"Weather Forecast for {data.get('latitude', 'N/A')}, {data.get('longitude', 'N/A')}")
    print(f"{'='*60}")
    print(f"\nNext 12 hours:")
    print("-" * 60)

    # Display next 12 hours
    for i in range(min(12, len(times))):
        time_str = times[i]
        temp = temperatures[i]
        print(f"{time_str}: {temp}°C")

    print("-" * 60)

    # Calculate statistics
    all_temps = temperatures[:24]  # First 24 hours
    if all_temps:
        avg_temp = sum(all_temps) / len(all_temps)
        max_temp = max(all_temps)
        min_temp = min(all_temps)
        print(f"\nNext 24 hours statistics:")
        print(f"  Average: {avg_temp:.1f}°C")
        print(f"  Maximum: {max_temp}°C")
        print(f"  Minimum: {min_temp}°C")

    print(f"{'='*60}\n")

def main():
    """Main entry point for command-line usage"""
    if len(sys.argv) < 3:
        print("Usage: python get_weather.py <latitude> <longitude> [hourly_params]")
        print("\nExamples:")
        print("  python get_weather.py 39.9042 116.4074")
        print("  python get_weather.py 39.9042 116.4074 temperature_2m,relative_humidity_2m")
        sys.exit(1)

    try:
        latitude = float(sys.argv[1])
        longitude = float(sys.argv[2])
        hourly_params = sys.argv[3] if len(sys.argv) > 3 else "temperature_2m"

        # Fetch weather data
        weather_data = get_weather_forecast(latitude, longitude, hourly_params)

        # Print summary
        print_weather_summary(weather_data)

        # Output raw JSON for programmatic use
        print("\nRaw JSON data:")
        print(json.dumps(weather_data, indent=2))

    except (ValueError, urllib.error.URLError, json.JSONDecodeError) as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Unexpected error: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
