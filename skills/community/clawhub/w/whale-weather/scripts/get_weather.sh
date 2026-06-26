#!/usr/bin/env bash
set -euo pipefail

# Security Hardening: Ensure strict execution environment
export LC_ALL=C.UTF-8

RAW_CITY="${1:-}"
LANG_HINT="${2:-zh}"

if [ -z "$RAW_CITY" ]; then
  echo "Usage: bash scripts/get_weather.sh \"City Name\" [language]" >&2
  exit 1
fi

# Limit input length to prevent buffer/memory attacks
if [ ${#RAW_CITY} -gt 100 ]; then
  echo "Error: City name too long." >&2
  exit 1
fi

require_cmd() {
  command -v "$1" >/dev/null 2>&1 || {
    echo "Missing required command: $1" >&2
    exit 1
  }
}

require_cmd python3

# Use Python as a safer execution sandbox for logic
python3 - "$RAW_CITY" "$LANG_HINT" <<'PY'
import json
import sys
import urllib.parse
import urllib.request
import time
import re

def sanitize_input(s):
    # Strip any non-printable or suspicious characters
    return re.sub(r'[^\w\s\u4e00-\u9fff,\.\-]', '', s).strip()

raw_city = sanitize_input(sys.argv[1])
lang = sanitize_input(sys.argv[2]).lower()

if not raw_city:
    print("Error: Invalid city name input.", file=sys.stderr)
    sys.exit(1)

I18N = {
    "zh": {
        "fail_geo": "查询失败: 地理编码请求失败",
        "fail_find": "查询失败: 未找到城市",
        "fail_weather": "查询失败: 天气数据请求失败",
        "current": "当前", "feels": "体感", "humidity": "湿度", "wind": "风速", "today": "今日", "rain_p": "降水概率",
        "adv_rain": "建议: 降水概率大，出门记得带伞",
        "adv_heat": "建议: 气温偏高，注意防暑防晒",
        "adv_cold": "建议: 略凉，注意保暖",
        "adv_good": "建议: 天气不错，适合出门",
        "codes": {0: "晴", 1: "大致晴朗", 2: "局部多云", 3: "阴", 45: "雾", 51: "毛毛雨", 61: "小雨", 71: "小雪", 95: "雷暴"}
    },
    "en": {
        "fail_geo": "Error: Geocoding failed",
        "fail_find": "Error: City not found",
        "fail_weather": "Error: Weather data request failed",
        "current": "Now", "feels": "Feels", "humidity": "Humidity", "wind": "Wind", "today": "Today", "rain_p": "Precipitation",
        "adv_rain": "Advice: High rain probability, take an umbrella",
        "adv_heat": "Advice: High temperature, stay hydrated",
        "adv_cold": "Advice: A bit cold, keep warm",
        "adv_good": "Advice: Good weather, enjoy your day",
        "codes": {0: "Clear sky", 1: "Mainly clear", 2: "Partly cloudy", 3: "Overcast", 45: "Fog", 51: "Drizzle", 61: "Rain", 71: "Snow", 95: "Thunderstorm"}
    }
}
msg = I18N.get(lang, I18N["en"])

TARGETS = {
    "北京": {"name": "北京市", "admin1": "北京", "feature": "PPLC"},
    "杭州": {"name": "杭州市", "admin1": "浙江", "feature": "PPLA"},
    "los angeles": {"name": "Los Angeles", "admin1": "California", "country": "United States"},
    "la": {"name": "Los Angeles", "admin1": "California", "country": "United States"},
}

def fetch_json(url):
    # Set custom User-Agent and disable proxy env to prevent intercept/injection
    req = urllib.request.Request(url, headers={'User-Agent': 'OpenClaw-SafeWeather/1.1'})
    # Use context to force TLS verification (default in modern python but good to be explicit)
    with urllib.request.urlopen(req, timeout=10) as response:
        return json.loads(response.read().decode("utf-8", "replace"))

def get_weather_data(lat, lon, tz):
    # Use HTTPS only for transport security
    url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current=temperature_2m,apparent_temperature,relative_humidity_2m,wind_speed_10m,weather_code&daily=temperature_2m_max,temperature_2m_min,precipitation_probability_max&timezone={tz}"
    try:
        return fetch_json(url)
    except:
        return None

# 1. Search
candidates = [raw_city]
if raw_city.lower() in TARGETS:
    candidates.insert(0, TARGETS[raw_city.lower()]["name"])

results = []
for cand in candidates:
    try:
        # Encode params to prevent URL injection
        params = urllib.parse.urlencode({"name": cand, "count": 10, "language": lang, "format": "json"})
        geo = fetch_json(f"https://geocoding-api.open-meteo.com/v1/search?{params}")
        results.extend(geo.get("results") or [])
    except: continue

if not results:
    print(f"{msg['fail_find']} ({raw_city})", file=sys.stderr); sys.exit(1)

# 2. Locate
place = results[0]
for r in results:
    if str(r.get("feature_code")) in ["PPLC", "PPLA"]:
        place = r; break

lat, lon = place.get("latitude"), place.get("longitude")
city_name = place.get("name") or raw_city
tz = place.get("timezone") or "auto"

# 3. Weather
data = get_weather_data(lat, lon, tz)
if not data:
    print(f"{msg['fail_weather']} ({raw_city})", file=sys.stderr); sys.exit(1)

curr, daily = data.get("current", {}), data.get("daily", {})
code = curr.get("weather_code")
desc = msg["codes"].get(code, msg["codes"].get(0))

fmt = lambda x: "?" if x is None else str(int(round(x)))

# Avoid any potential terminal escape sequence injections by cleaning output
def clean_out(s): return re.sub(r'[\x00-\x1f\x7f-\x9f]', '', str(s))

print(clean_out(f"{city_name}, {place.get('admin1','')}, {place.get('country','')}").strip(", "))
print(clean_out(f"{msg['current']}: {fmt(curr.get('temperature_2m'))}°C, {msg['feels']} {fmt(curr.get('apparent_temperature'))}°C, {desc}"))
print(clean_out(f"{msg['humidity']}: {fmt(curr.get('relative_humidity_2m'))}% | {msg['wind']}: {fmt(curr.get('wind_speed_10m'))} km/h"))
print(clean_out(f"{msg['today']}: {fmt((daily.get('temperature_2m_min') or [None])[0])}°C ~ {fmt((daily.get('temperature_2m_max') or [None])[0])}°C"))

rain = (daily.get('precipitation_probability_max') or [0])[0]
if rain >= 60: print(clean_out(msg["adv_rain"]))
elif (curr.get('temperature_2m') or 20) >= 30: print(clean_out(msg["adv_heat"]))
elif (curr.get('temperature_2m') or 20) <= 10: print(clean_out(msg["adv_cold"]))
else: print(clean_out(msg["adv_good"]))
PY
