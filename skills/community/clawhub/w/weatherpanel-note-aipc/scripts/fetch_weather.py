#!/usr/bin/env python3
"""
fetch_weather.py - Fetch current weather from Open-Meteo and append to time-series.
Writes timeseries.json to the Canvas directory for live dashboard rendering.
Exits 0 on success.
"""

import json
import os
import sys
from datetime import datetime, timezone
from urllib.request import urlopen, Request, ProxyHandler, build_opener
from urllib.error import URLError

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import env_loader

STATE_DIR = env_loader.STATE_DIR
CANVAS_ROOT = os.environ.get("CANVAS_ROOT", env_loader.CANVAS_ROOT_DEFAULT)
CANVAS_DIR = os.path.join(CANVAS_ROOT, "weatherpanel-note-aipc")

TIMESERIES_FILE = os.path.join(CANVAS_DIR, "timeseries.json")
LATEST_FILE = os.path.join(STATE_DIR, "latest_fetch.json")
LAST_FETCH_FILE = os.path.join(STATE_DIR, "last_fetch.txt")
MAX_POINTS = 576  # 48 hours at 5-min intervals

LAT = os.environ.get("WEATHER_LAT", "31.2304")
LON = os.environ.get("WEATHER_LON", "121.4737")
TZ = os.environ.get("WEATHER_TZ", "Asia/Shanghai")
UNITS = os.environ.get("WEATHER_UNITS", "metric")


def build_url():
    temp_unit = "fahrenheit" if UNITS == "imperial" else "celsius"
    wind_unit = "mph" if UNITS == "imperial" else "kmh"
    precip_unit = "inch" if UNITS == "imperial" else "mm"

    base = "https://api.open-meteo.com/v1/forecast"
    params = (
        f"latitude={LAT}&longitude={LON}"
        f"&timezone={TZ}"
        f"&current=temperature_2m,relative_humidity_2m,apparent_temperature,"
        f"precipitation,weather_code,cloud_cover,wind_speed_10m,wind_direction_10m,wind_gusts_10m,"
        f"surface_pressure"
        f"&hourly=temperature_2m,relative_humidity_2m,apparent_temperature,"
        f"precipitation_probability,precipitation,wind_speed_10m,cloud_cover,weather_code"
        f"&forecast_hours=24"
        f"&temperature_unit={temp_unit}"
        f"&wind_speed_unit={wind_unit}"
        f"&precipitation_unit={precip_unit}"
    )
    return f"{base}?{params}"


def fetch_weather():
    url = build_url()
    req = Request(url, headers={"User-Agent": "OpenClaw-WeatherPanelNoteAIPC/1.0"})

    proxies = {}
    http_proxy = os.environ.get("HTTP_PROXY") or os.environ.get("http_proxy")
    https_proxy = os.environ.get("HTTPS_PROXY") or os.environ.get("https_proxy")
    if http_proxy:
        proxies["http"] = http_proxy
    if https_proxy:
        proxies["https"] = https_proxy

    if proxies:
        print(f"[fetch] Using proxy: {proxies}")
        opener = build_opener(ProxyHandler(proxies))
    else:
        opener = build_opener(ProxyHandler())

    try:
        with opener.open(req, timeout=30) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except URLError as e:
        print(f"[fetch] ERROR: {e}", file=sys.stderr)
        if "10060" in str(e) or "timed out" in str(e).lower():
            print("[fetch] Timeout. Set HTTP_PROXY/HTTPS_PROXY in the process environment if behind a proxy.", file=sys.stderr)
        sys.exit(1)


def extract_current(data):
    c = data.get("current", {})
    return {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "local_time": c.get("time", ""),
        "temperature_2m": c.get("temperature_2m"),
        "relative_humidity_2m": c.get("relative_humidity_2m"),
        "apparent_temperature": c.get("apparent_temperature"),
        "precipitation": c.get("precipitation"),
        "weather_code": c.get("weather_code"),
        "cloud_cover": c.get("cloud_cover"),
        "wind_speed_10m": c.get("wind_speed_10m"),
        "wind_direction_10m": c.get("wind_direction_10m"),
        "wind_gusts_10m": c.get("wind_gusts_10m"),
        "surface_pressure": c.get("surface_pressure"),
    }


def load_timeseries():
    if os.path.exists(TIMESERIES_FILE):
        for enc in ["utf-8", "gbk"]:
            try:
                with open(TIMESERIES_FILE, "r", encoding=enc) as f:
                    data = json.load(f)
                if enc != "utf-8":
                    with open(TIMESERIES_FILE, "w", encoding="utf-8") as f:
                        json.dump(data, f, indent=2, ensure_ascii=False)
                return data
            except (json.JSONDecodeError, UnicodeDecodeError, IOError):
                continue
        return []
    return []


def save_timeseries(ts):
    if len(ts) > MAX_POINTS:
        ts = ts[-MAX_POINTS:]
    with open(TIMESERIES_FILE, "w", encoding="utf-8") as f:
        json.dump(ts, f, indent=2, ensure_ascii=False)


def main():
    os.makedirs(STATE_DIR, exist_ok=True)
    os.makedirs(CANVAS_DIR, exist_ok=True)

    print(f"[fetch] Fetching weather for ({LAT}, {LON})...")
    raw = fetch_weather()

    with open(LATEST_FILE, "w", encoding="utf-8") as f:
        json.dump(raw, f, indent=2, ensure_ascii=False)

    current = extract_current(raw)

    hourly = raw.get("hourly", {})
    current["hourly_forecast"] = {
        "time": hourly.get("time", [])[:24],
        "temperature_2m": hourly.get("temperature_2m", [])[:24],
        "precipitation_probability": hourly.get("precipitation_probability", [])[:24],
        "precipitation": hourly.get("precipitation", [])[:24],
    }

    ts = load_timeseries()
    ts.append(current)
    save_timeseries(ts)

    now_str = datetime.now(timezone.utc).isoformat()
    with open(LAST_FETCH_FILE, "w", encoding="utf-8") as f:
        f.write(now_str)

    print(f"[fetch] OK at {now_str} "
          f"(temp={current['temperature_2m']}C, humidity={current['relative_humidity_2m']}%)")
    sys.exit(0)


if __name__ == "__main__":
    main()
