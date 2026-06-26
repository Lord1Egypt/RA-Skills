#!/usr/bin/env python3
"""Weather Alert Skill — Proactive weather monitoring and alerting."""

import json
import os
import sys
import urllib.request
import urllib.error
import urllib.parse
from datetime import datetime, timedelta
from pathlib import Path

try:
    import yaml
except ImportError:
    yaml = None

# --- Configuration ---
DEFAULT_CONFIG = {
    "default_location": {"name": "Prague", "lat": 50.0755, "lon": 14.4378},
    "alerts": {
        "rain_threshold": 60,
        "temp_min": 5,
        "temp_max": 30,
        "wind_max": 40,
        "snow_depth": 5,
        "uv_max": 7,
        "frost_threshold": 0,
    },
    "notification": {"method": "exec-event", "schedule_check": "6h"},
}

ALERTS_FILE = os.path.expanduser("~/.weather-alerts/alerts.yaml")
CACHE_FILE = os.path.expanduser("~/.weather-alerts/cache.json")
CACHE_TTL = 1800  # 30 min


def load_config():
    """Load config.yaml or return defaults."""
    config_path = os.path.join(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
        "config.yaml",
    )
    if yaml and os.path.exists(config_path):
        with open(config_path) as f:
            cfg = yaml.safe_load(f) or {}
        for key in DEFAULT_CONFIG:
            cfg.setdefault(key, DEFAULT_CONFIG[key])
        return cfg
    return DEFAULT_CONFIG.copy()


def load_cache():
    """Load cached weather data if still valid."""
    if not os.path.exists(CACHE_FILE):
        return None
    with open(CACHE_FILE) as f:
        data = json.load(f)
    age = (datetime.now() - datetime.fromisoformat(data["timestamp"])).total_seconds()
    if age > CACHE_TTL:
        return None
    return data


def save_cache(data):
    """Save weather data to cache."""
    os.makedirs(os.path.dirname(CACHE_FILE), exist_ok=True)
    with open(CACHE_FILE, "w") as f:
        json.dump(
            {
                "timestamp": datetime.now().isoformat(),
                "data": data,
            },
            f,
            indent=2,
        )


def fetch_open_meteo(lat, lon, days=7):
    """Fetch weather data from Open-Meteo API (free, no key needed)."""
    url = "https://api.open-meteo.com/v1/forecast"  # noqa: E501
    url += "?latitude=" + str(lat) + "&longitude=" + str(lon)
    url += "&current=temperature_2m,relative_humidity_2m,apparent_temperature,"
    url += "precipitation,weather_code,wind_speed_10m,wind_direction_10m,"
    url += "wind_gusts_10m,surface_pressure,uv_index"
    url += "&daily=temperature_2m_min,temperature_2m_max,precipitation_sum,"
    url += "snowfall_sum,wind_speed_10m_max,wind_gusts_10m_max,"
    url += "uv_index_max,precipitation_probability_max"
    url += "&timezone=Europe%2FPrague"
    url += "&forecast_days=" + str(days)
    req = urllib.request.Request(url, headers={"User-Agent": "WeatherAlert/1.0"})
    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            return json.loads(resp.read())
    except (urllib.error.URLError, urllib.error.HTTPError, TimeoutError):
        return None


def fetch_wttr(location):
    """Quick weather lookup via wttr.in."""
    url = f"https://wttr.in/{urllib.parse.quote(location)}?format=j1"
    req = urllib.request.Request(url, headers={"User-Agent": "WeatherAlert/1.0"})
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            return json.loads(resp.read())
    except Exception:
        return None


WEATHER_CODES = {
    0: ("☀️", "Clear sky"),
    1: ("🌤", "Mainly clear"),
    2: ("⛅", "Partly cloudy"),
    3: ("☁️", "Overcast"),
    45: ("🌫", "Foggy"),
    48: ("🌫", "Rime fog"),
    51: ("🌦", "Light drizzle"),
    53: ("🌦", "Moderate drizzle"),
    55: ("🌧", "Dense drizzle"),
    56: ("🌧", "Freezing drizzle"),
    57: ("🌧", "Freezing drizzle heavy"),
    61: ("🌧", "Rain light"),
    63: ("🌧", "Rain moderate"),
    65: ("🌧", "Rain heavy"),
    66: ("🌨", "Freezing rain light"),
    67: ("🌨", "Freezing rain heavy"),
    71: ("🌨", "Snow light"),
    73: ("🌨", "Snow moderate"),
    75: ("❄️", "Snow heavy"),
    77: ("❄️", "Snow grains"),
    80: ("🌦", "Rain showers light"),
    81: ("🌧", "Rain showers moderate"),
    82: ("🌧", "Rain showers heavy"),
    85: ("🌨", "Snow showers light"),
    86: ("🌨", "Snow showers heavy"),
    95: ("⛈", "Thunderstorm"),
    96: ("⛈", "Thunderstorm with hail"),
    99: ("⛈", "Thunderstorm heavy hail"),
}


def get_weather_icon(code):
    """Get emoji icon for weather code."""
    if code in WEATHER_CODES:
        icon, _ = WEATHER_CODES[code]
        return icon
    return "🌡"


def get_weather_description(code):
    """Get description for weather code."""
    if code in WEATHER_CODES:
        _, desc = WEATHER_CODES[code]
        return desc
    return "Unknown"


def format_current(current, daily, location_name):
    """Format current weather conditions."""
    if not current:
        return f"⚠ Could not fetch weather for {location_name}"

    temp = current.get("temperature_2m", "—")
    feels_like = current.get("apparent_temperature", "—")
    humidity = current.get("relative_humidity_2m", "—")
    wind = current.get("wind_speed_10m", "—")
    wind_dir = current.get("wind_direction_10m", 0)
    dir_names = {0: "calm", 45: "NE", 90: "E", 135: "SE", 180: "S", 225: "SW", 270: "W", 315: "NW"}
    wind_dir_name = dir_names.get(round(wind_dir / 45) * 45 % 360, f"{wind_dir}°")
    precip = current.get("precipitation", 0)
    uv = current.get("uv_index", "—")
    pressure = current.get("surface_pressure", "—")
    code = current.get("weather_code", -1)
    icon = get_weather_icon(code)

    lines = [
        f"🌤 {location_name} Weather — {datetime.now().strftime('%Y-%m-%d %H:%M')}",
        f"Temp: {temp}°C (feels like {feels_like}°C) | Humidity: {humidity}%",
        f"Wind: {wind} km/h {wind_dir_name} | Precip: {precip}mm | UV: {uv}",
        f"Pressure: {round(pressure / 100, 1)} hPa | {get_weather_description(code)}",
    ]
    return "\n".join(lines)


def format_forecast(daily, days=7):
    """Format multi-day forecast."""
    if not daily or not daily.get("time"):
        return "⚠ No forecast data available"

    times = daily["time"][:days]
    codes = daily.get("weather_code", [])
    temps_min = daily.get("temperature_2m_min", [])
    temps_max = daily.get("temperature_2m_max", [])
    precip_pmax = daily.get("precipitation_probability_max", [])
    precip_sum = daily.get("precipitation_sum", [])
    snow_sum = daily.get("snowfall_sum", [])
    wind_max = daily.get("wind_speed_10m_max", [])
    uv_max = daily.get("uv_index_max", [])

    lines = ["📅 7-Day Forecast"]
    for i, t in enumerate(times):
        date = datetime.fromisoformat(t).strftime("%a %d")
        icon = get_weather_icon(codes[i] if i < len(codes) else 3)
        t_min = temps_min[i] if i < len(temps_min) else "?"
        t_max = temps_max[i] if i < len(temps_max) else "?"
        precip = precip_pmax[i] if i < len(precip_pmax) else "?"
        precip = f"{precip}%" if isinstance(precip, int) else "?"
        wind = wind_max[i] if i < len(wind_max) else "?"
        uv = uv_max[i] if i < len(uv_max) else "?"

        line = f"{date}: {icon} {t_min}°-{t_max}°C | Precip: {precip} | Wind: {wind} km/h"
        if snow_sum and snow_sum[i] > 0:
            line += f" | Snow: {snow_sum[i]}cm"
        lines.append(line)

    return "\n".join(lines)


def check_alerts(current, daily, config):
    """Check current conditions against alert thresholds. Returns list of triggered alerts."""
    alerts = []
    thresholds = config.get("alerts", {})

    # Temperature alerts
    temp = current.get("temperature_2m", 0) if current else None
    if temp is not None:
        tmin = thresholds.get("temp_min")
        if tmin is not None and temp < tmin:
            alerts.append(f"🥶 Temperature {temp}°C is below {tmin}°C threshold")
        tmax = thresholds.get("temp_max")
        if tmax is not None and temp > tmax:
            alerts.append(f"🔥 Temperature {temp}°C exceeds {tmax}°C threshold")

    # Rain alerts
    precip_prob = 0
    if daily and daily.get("precipitation_probability_max"):
        precip_prob = daily["precipitation_probability_max"][0] if daily["precipitation_probability_max"] else 0
    elif current and current.get("precipitation", 0) > 0:
        precip_prob = 100

    rain_thresh = thresholds.get("rain_threshold")
    if rain_thresh is not None and precip_prob > rain_thresh:
        alerts.append(f"🌧 Rain probability {precip_prob}% exceeds {rain_thresh}% threshold")

    # Snow alerts
    if daily and daily.get("snowfall_sum"):
        snow = daily["snowfall_sum"][0] if daily["snowfall_sum"] else 0
        snow_thresh = thresholds.get("snow_depth")
        if snow_thresh is not None and snow > snow_thresh:
            alerts.append(f"❄️ Snowfall {snow}cm exceeds {snow_thresh}cm threshold")

    # Wind alerts
    wind = current.get("wind_speed_10m", 0) if current else 0
    gusts = current.get("wind_gusts_10m", 0) if current else 0
    wind_max = thresholds.get("wind_max")
    if wind_max is not None:
        if wind > wind_max:
            alerts.append(f"💨 Wind {wind} km/h exceeds {wind_max} km/h threshold")
        if gusts > wind_max:
            alerts.append(f"💨 Wind gusts {gusts} km/h exceeds {wind_max} km/h threshold")

    # UV alerts
    uv = current.get("uv_index", 0) if current else 0
    uv_max = thresholds.get("uv_max")
    if uv_max is not None and uv > uv_max:
        alerts.append(f"☀️ UV index {uv} exceeds {uv_max} threshold")

    # Frost alerts
    if daily and daily.get("temperature_2m_min") and daily["temperature_2m_min"]:
        min_temp = daily["temperature_2m_min"][0]
        frost_thresh = thresholds.get("frost_threshold")
        if frost_thresh is not None and min_temp < frost_thresh:
            alerts.append(f"❄️ Frost risk: overnight low {min_temp}°C below {frost_thresh}°C")

    return alerts


def format_event_suitability(daily, activity, location_name):
    """Check suitability for outdoor activities."""
    if not daily or not daily.get("time"):
        return f"⚠ No forecast data for {location_name}"

    tomorrow = 0  # today index
    temp_min = daily["temperature_2m_min"][tomorrow] if daily["temperature_2m_min"] else None
    temp_max = daily["temperature_2m_max"][tomorrow] if daily["temperature_2m_max"] else None
    precip = daily["precipitation_probability_max"][tomorrow] if daily.get("precipitation_probability_max") else 0
    precip_sum = daily["precipitation_sum"][tomorrow] if daily.get("precipitation_sum") else 0
    wind = daily["wind_speed_10m_max"][tomorrow] if daily.get("wind_speed_10m_max") else 0
    uv = daily["uv_index_max"][tomorrow] if daily.get("uv_index_max") else 0
    snow = daily["snowfall_sum"][tomorrow] if daily.get("snowfall_sum") else 0

    good = []
    warnings = []
    bad = []

    if temp_min is not None:
        if temp_min >= 5 and temp_max and temp_max <= 25:
            good.append(f"Temp {temp_min}°-{temp_max}°C — comfortable")
        elif temp_max and temp_max > 30:
            bad.append(f"Temp too hot ({temp_max}°C)")
        elif temp_min and temp_min < 0:
            bad.append(f"Frost risk ({temp_min}°C)")
        else:
            warnings.append(f"Temp {temp_min}°-{temp_max}°C — check if comfortable")

    if precip >= 70:
        bad.append(f"High rain risk ({precip}%)")
    elif precip >= 40:
        warnings.append(f"Possible rain ({precip}%)")
    elif precip_sum > 5:
        warnings.append(f"Rain expected ({precip_sum}mm)")

    if wind > 30:
        bad.append(f"Wind too strong ({wind} km/h)")
    elif wind > 15:
        warnings.append(f"Moderate wind ({wind} km/h)")

    if snow > 1:
        bad.append(f"Snow expected ({snow}cm)")

    activity_labels = {
        "running": "🏃",
        "hiking": "🥾",
        "picnic": "🧺",
        "cycling": "🚴",
        "garden": "🌿",
        "farming": "🚜",
        "sailing": "⛵",
        "skiing": "⛷",
        "swimming": "🏊",
        "photography": "📸",
    }
    icon = activity_labels.get(activity, "👤")

    lines = [f"{icon} {activity.title()} — {location_name}, Today"]
    if good:
        lines.append(f"Good: {'; '.join(good)}")
    if warnings:
        lines.append(f"Warning: {'; '.join(warnings)}")
    if bad:
        lines.append(f"Bad: {'; '.join(bad)}")
    if not good and not warnings and not bad:
        lines.append("✅ Conditions seem fine")

    return "\n".join(lines)


def main():
    config = load_config()
    args = sys.argv[1:]

    # Determine location
    location_name = config["default_location"]["name"]
    lat = config["default_location"]["lat"]
    lon = config["default_location"]["lon"]
    days = 7

    for i, arg in enumerate(args):
        if arg == "--location" and i + 1 < len(args):
            location_name = args[i + 1]
        elif arg == "--lat" and i + 1 < len(args):
            lat = float(args[i + 1])
        elif arg == "--lon" and i + 1 < len(args):
            lon = float(args[i + 1])
        elif arg == "--days":
            days = min(int(args[i + 1]), 14) if i + 1 < len(args) else 7
        elif arg == "--event" and i + 1 < len(args):
            activity = args[i + 1]
            # Fetch and show event suitability
            cached = load_cache()
            if cached and cached.get("lat") == lat and cached.get("lon") == lon:
                current = cached.get("current")
                daily = cached.get("daily")
            else:
                data = fetch_open_meteo(lat, lon, days)
                if data:
                    save_cache({"lat": lat, "lon": lon, "data": data})
                    current = data.get("current")
                    daily = data.get("daily")
                else:
                    print("⚠ Could not fetch weather data")
                    sys.exit(1)

            print(format_event_suitability(daily, activity, location_name))
            return

        elif arg in ("--current", "--check", "--today"):
            # Show current weather only
            pass
        elif arg == "--alerts":
            # Check alerts only
            pass
        elif arg == "--format" and i + 1 < len(args):
            days = int(args[i + 1]) if i + 1 < len(args) else 7

    # Fetch data
    cached = load_cache()
    if cached and cached.get("lat") == lat and cached.get("lon") == lon:
        data = cached["data"]
    else:
        data = fetch_open_meteo(lat, lon, days)
        if not data:
            print("⚠ Could not fetch weather data")
            sys.exit(1)
        save_cache({"lat": lat, "lon": lon, "data": data})

    current = data.get("current")
    daily = data.get("daily")

    # Output current weather
    print(format_current(current, daily, location_name))
    print()

    # Output forecast
    print(format_forecast(daily, min(days, 7)))
    print()

    # Check and report alerts
    triggered = check_alerts(current, daily, config)
    if triggered:
        print("🔔 ALERTS:")
        for a in triggered:
            print(f"  • {a}")
    else:
        print("✅ No alerts triggered — conditions within normal ranges")


if __name__ == "__main__":
    main()
