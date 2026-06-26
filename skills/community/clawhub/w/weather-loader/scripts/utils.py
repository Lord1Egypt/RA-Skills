#!/usr/bin/env python3
"""
Weather Utilities

Utility functions for fetching and processing weather data.
These functions are self-contained and don't depend on external modules.
"""

import datetime

import pandas as pd
import requests


# Configuration constants
DEFAULT_HISTORICAL_DAYS = 10
MAX_HISTORICAL_DAYS = 30
DEFAULT_FORECAST_DAYS = 7
MAX_FORECAST_DAYS = 15

FORECAST_ENDPOINT_METEO = (
    "https://api.open-meteo.com/v1/forecast?latitude={lat}"
    "&longitude={lon}"
    "&forecast_days={forecast_days}"
    "&hourly=temperature_2m,relative_humidity_2m,precipitation,"
    "wind_speed_10m,cloud_cover,et0_fao_evapotranspiration,vapour_pressure_deficit"
)
HISTORY_OBSERVATION_ENDPOINT = (
    "https://archive-api.open-meteo.com/v1/archive?latitude={lat}"
    "&longitude={lon}&start_date={start_date}&end_date={end_date}"
    "&hourly=temperature_2m,relative_humidity_2m,precipitation,"
    "wind_speed_10m,cloud_cover,et0_fao_evapotranspiration,vapour_pressure_deficit"
)
LATLON_ENDPOINT = "https://geocoding-api.open-meteo.com/v1/search"


def calculate_evaporation(
    temp, humidity, wind_speed, cloud_fraction, hour_resolution, area=1 * 1
):
    """
    Calculate evaporation based on weather conditions.
    
    Args:
        temp: Temperature (°C)
        humidity: Relative humidity (%)
        wind_speed: Wind speed (m/s)
        cloud_fraction: Cloud cover (%)
        hour_resolution: Hours between measurements
        area: Area in square meters (default: 1)
    
    Returns:
        Estimated evaporation (mm)
    """
    evaporation = (
        (0.5 + 0.05 * temp)
        * (1 - humidity / 100)
        * (1 + 0.1 * wind_speed)
        * (1 - cloud_fraction / 100)
    )
    if hour_resolution == 1:
        return evaporation * area / 24
    else:
        return evaporation * area / 4


def get_lat_lon(location):
    """
    Get latitude, longitude, and display name for a location.
    
    Args:
        location: Location name (e.g., "Oslo, Norway")
    
    Returns:
        Tuple of (latitude, longitude, display_name) or (None, None, None)
    """
    # Remove spaces and convert to lowercase
    location = location.strip().lower()
    params = {"name": location, "count": 1}
    response = requests.get(LATLON_ENDPOINT, params=params)
    
    if response.status_code == 200:
        data = response.json()
        if "results" in data and len(data["results"]) > 0:
            lat = float(data["results"][0]["latitude"])
            lon = float(data["results"][0]["longitude"])
            display_name = data["results"][0]["name"]
            if "admin1" in data["results"][0]:
                display_name += f', {data["results"][0]["admin1"]}'
            if "country" in data["results"][0]:
                display_name += f', {data["results"][0]["country"]}'
            
            return lat, lon, display_name
    
    return None, None, None


def load_history(lat, lon, days=None):
    """
    Load historical weather data for a location.

    Args:
        lat: Latitude
        lon: Longitude
        days: Number of days of history (default DEFAULT_HISTORICAL_DAYS, max MAX_HISTORICAL_DAYS)

    Returns:
        DataFrame with historical weather data or None
    """
    if days is None:
        days = DEFAULT_HISTORICAL_DAYS
    days = min(max(1, int(days)), MAX_HISTORICAL_DAYS)

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:126.0) Gecko/20100101 Firefox/126.0"
    }

    start_date = (
        datetime.datetime.now() - datetime.timedelta(days=days)
    ).strftime("%Y-%m-%d")
    end_date = (datetime.datetime.now() - datetime.timedelta(days=1)).strftime(
        "%Y-%m-%d"
    )
    
    # Fetch historical observation data (archive/reanalysis)
    url = HISTORY_OBSERVATION_ENDPOINT.format(
        lat=lat, lon=lon, start_date=start_date, end_date=end_date
    )
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        try:
            obs = response.json()
            if "hourly" not in obs:
                print("No hourly data found in observation response.")
                return None
            data = pd.DataFrame(obs["hourly"])
        except Exception as e:
            print(f"Error parsing historical observation data: {e}")
            return None
    else:
        return None
    
    if len(data) > 0:
        data = data.dropna()
        
        data.columns = [
            "time",
            "temp",
            "humidity",
            "precip",
            "wind_speed",
            "cloud_fraction",
            "et0_fao",
            "vapour",
        ]
        
        data["time"] = pd.to_datetime(data["time"])
        # Convert wind speed from km/h to m/s
        data["wind_speed"] = data["wind_speed"] / 3.6
        data["date"] = data["time"].dt.date
        data["hour_resolution"] = data["time"].diff().dt.total_seconds() / 3600
        data = data.dropna()
        
        # Calculate evaporation
        data["evaporation"] = data.apply(
            lambda row: calculate_evaporation(
                row["temp"],
                row["humidity"],
                row["wind_speed"],
                row["cloud_fraction"],
                row["hour_resolution"],
            ),
            axis=1,
        )
        
        # Aggregate to daily data
        data = (
            data.groupby("date")
            .agg(
                {
                    "temp": "mean",
                    "precip": "sum",
                    "et0_fao": "sum",
                    "evaporation": "sum",
                }
            )
            .reset_index()
        )
        
        return data
    
    return None


def load_forecast(lat, lon, days=None):
    """
    Load forecast weather data for a location.

    Args:
        lat: Latitude
        lon: Longitude
        days: Number of days of forecast (default DEFAULT_FORECAST_DAYS, max MAX_FORECAST_DAYS)

    Returns:
        DataFrame with forecast weather data or None
    """
    if days is None:
        days = DEFAULT_FORECAST_DAYS
    days = min(max(1, int(days)), MAX_FORECAST_DAYS)

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:126.0) Gecko/20100101 Firefox/126.0"
    }

    url = FORECAST_ENDPOINT_METEO.format(lat=lat, lon=lon, forecast_days=days)
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        try:
            data = response.json()
            if "hourly" not in data:
                print("No hourly data found in response.")
                return None
            
            data = pd.DataFrame(data["hourly"])
            data.columns = [
                "time",
                "temp",
                "humidity",
                "precip",
                "wind_speed",
                "cloud_fraction",
                "et0_fao",
                "vapour",
            ]
            
            data["time"] = pd.to_datetime(data["time"])
            # Convert wind speed from km/h to m/s
            data["wind_speed"] = data["wind_speed"] / 3.6
            data["date"] = data["time"].dt.date
            data["hour_resolution"] = data["time"].diff().dt.total_seconds() / 3600
            data = data.dropna()
            
            # Calculate evaporation
            data["evaporation"] = data.apply(
                lambda row: calculate_evaporation(
                    row["temp"],
                    row["humidity"],
                    row["wind_speed"],
                    row["cloud_fraction"],
                    row["hour_resolution"],
                ),
                axis=1,
            )
            
            # Aggregate to daily data
            data = (
                data.groupby("date")
                .agg(
                    {
                        "temp": "mean",
                        "precip": "sum",
                        "et0_fao": "sum",
                        "evaporation": "sum",
                    }
                )
                .reset_index()
            )
            
            return data
        except Exception as e:
            print(f"Error parsing forecast data: {e}")
    else:
        print(f"Error fetching forecast data: {response.status_code}")
    
    return None


def process_data(data_type, data, kc=1.0):
    """
    Process weather data by applying crop coefficient and calculating cumulative values.
    
    Args:
        data_type: Type of data - "historical" or "forecast"
        data: DataFrame with weather data
        kc: Crop coefficient (default: 1.0)
    
    Returns:
        Processed DataFrame or None
    """
    if data is None or data.empty:
        return None
    
    # Apply crop coefficient to evapotranspiration
    data["et0_fao"] = data["et0_fao"] * kc
    
    # Calculate cumulative values
    data["agg_precip"] = data["precip"].cumsum()
    data["agg_evaporation"] = data["et0_fao"].cumsum()
    
    return data


if __name__ == "__main__":
    # Test the functions
    print("Testing weather utilities...")
    
    # Test location lookup
    lat, lon, display_name = get_lat_lon("Oslo, Norway")
    if lat and lon:
        print(f"✓ Location: {display_name} ({lat:.2f}, {lon:.2f})")
    else:
        print("✗ Failed to get location")
    
    print("\nUtilities are ready to use!")
