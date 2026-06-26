---
name: weather-pulse
description: "Weather + air quality tool. (1) Current: temp, feels-like, wind, humidity, precipitation, pressure, visibility. (2) Daily 3-30d: sun/moon, max/min temp, day/night weather, UV. (3) Hourly 24-168h: temp, weather, wind, humidity, precipitation probability. (4) 19 lifestyle indices (5 overseas). (5) AQI 6 levels, PM2.5/PM10/CO/NO2/O3/SO2, 7-day forecast. Input: city name (CN/EN), coordinates, CityId, or WAQI ID. Endpoints: now, 3d-30d, 24h-168h, indices, aqi. Free: QWeather 50k/mo, WAQI 1k/hr.",
summary: "Query real-time weather, 3-30 day daily forecasts, 24-168h hourly forecasts, AQI/PM2.5/PM10 with 7-day pollutant forecast, and 19 lifestyle indices for any city by name (CN/EN), coordinates, or CityId."
tags:
  weather: "1.3.6"
  forecast: "1.3.6"
  air-quality: "1.3.6"
  aqi: "1.3.6"
  qweather: "1.3.6"
  temperature: "1.3.6"
  chinese: "1.3.6"
trigger_patterns:
  - "天气"
  - "查天气"
  - "天气预报"
  - "气温"
  - "温度"
  - "下雨"
  - "湿度"
  - "风力"
  - "空气质量"
  - "PM25"
  - "天气怎么样"
  - "weather"
  - "forecast"
  - "temperature"
  - "humidity"
  - "aqi"
  - "air quality"
  - "rain"
  - "wind"
  - "uv"
  - "current weather"
  - "weather forecast"
  - "what is the weather"
homepage: "https://dev.qweather.com/docs"
requiredEnvs:
  - name: QWEATHER_API_HOST
    description: "QWeather API Host from console settings (e.g. xxxxxxx.re.qweatherapi.com). Required for weather endpoints."
    required: false
  - name: QWEATHER_API_KEY
    description: "QWeather API Key from project credentials. Required for weather endpoints."
    required: false
  - name: WAQI_API_TOKEN
    description: "WAQI token from https://aqicn.org/data-platform/token/. Required for AQI endpoint."
    required: false
---

# weather-pulse

Weather and air quality query tool. Uses two free APIs. Both require separate registration.

> **Two APIs, Two Registrations Required:**
> - **Weather Data** - QWeather: https://console.qweather.com
> - **Air Quality Data** - WAQI: https://aqicn.org/api/
>
> You need both for full features. Weather-only works without WAQI token. AQI-only works without QWeather credentials.

## Quick Start

### 1. Get API Credentials

#### QWeather - Free 50,000 calls/month

Register to get API Host and API Key.

1. Open https://console.qweather.com and register or log in.
2. Create a project with any name (e.g. "Demo").
3. Add credentials: go to Project > Credentials > Create Credential > select API KEY.
4. Get API Host: go to Settings in the left menu > copy the value like `xxxxxxx.re.qweatherapi.com`.

| Config Item | Required For | Where to Get | Example |
|-------------|-------------|--------------|---------|
| `QWEATHER_API_HOST` | Weather | QWeather Console > Settings > API Host | `xxxxxxx.re.qweatherapi.com` |
| `QWEATHER_API_KEY` | Weather | QWeather Console > Project > Credentials > API KEY | `xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx` |

Docs: https://dev.qweather.com/docs/start/ | Pricing: https://dev.qweather.com/docs/finance/pricing/

#### WAQI - Free 1,000 calls/hour

Register to get Token.

1. Open https://aqicn.org/data-platform/token/#/
2. Check the agreement box, fill in email and name, submit.
3. Check your email, click the confirmation link, get the token.

| Config Item | Required For | Where to Get | Example |
|-------------|-------------|--------------|---------|
| `WAQI_API_TOKEN` | Air Quality | WAQI email confirmation page | `xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx` |

Docs: https://aqicn.org/api/ | City lookup: https://aqicn.org/city/

### 2. Configure Credentials

**Recommended: use environment variables. Do not put API keys in script files.**

Storing API keys directly in code can cause leaks (e.g. accidental Git commits, shared devices). Use environment variables or a `.env` file.

#### Option A: Environment Variables (Recommended)

Only configure credentials for the features you need.

```bash
# Weather (Linux/macOS)
export QWEATHER_API_HOST="your_api_host"
export QWEATHER_API_KEY="your_api_key"

# Weather (Windows PowerShell)
$env:QWEATHER_API_HOST = "your_api_host"
$env:QWEATHER_API_KEY = "your_api_key"

# Air Quality (all platforms)
export WAQI_API_TOKEN="your_waqi_token"
# Windows PowerShell:
$env:WAQI_API_TOKEN = "your_waqi_token"
```

#### Option B: .env File

Create a `.env` file in the same directory as `weather.py`, and load it before running:

```bash
# .env file contents
QWEATHER_API_HOST=your_api_host
QWEATHER_API_KEY=your_api_key
WAQI_API_TOKEN=your_waqi_token
```

```bash
# Linux/macOS
set -a && source .env && set +a && python scripts/weather.py ...

# Windows PowerShell
Get-Content .env | ForEach-Object { $k,$v = $_.Split('='); Set-Item "env:$k" $v }
python scripts/weather.py ...
```

### 3. Test

```bash
# Current weather (by CityId)
python scripts/weather.py 101180301

# Air quality (by city name)
python scripts/weather.py xinxiang --endpoint aqi
```

---

## Call Method

```bash
python scripts/weather.py <location> [--endpoint ENDPOINT] [--json]
```

If `--endpoint` is omitted, defaults to `now` (current weather).

### Location Format (Auto-Parsed)

| Type | Format | Supported Endpoints | Example |
|------|--------|---------------------|---------|
| CityId | digits only | All | `101180301` |
| English city name | any | All (auto-resolved to CityId) | `Shanghai` |
| Chinese city name | any | All (auto-resolved to CityId) | `上海` |
| Coordinates | `lng,lat` or `lat,lng` (auto-detected) | All | `113.92,35.30` |
| geo: format | `"geo:lat;lng"` (quotes required) | AQI only | `"geo:35.30;113.92"` |
| WAQI ID | `@number` | AQI only | `@5789` |
| Current location | `here` | AQI only | `here` |

City name input is automatically resolved to CityId via QWeather GeoAPI. No need to look up IDs manually. Coordinate input auto-detects the order (lng,lat or lat,lng both work). The `geo:` format uses semicolons which require quotes in shell to avoid parsing as command separator.

### Available Endpoints

| Endpoint | Source | Free Quota | Description |
|----------|--------|------------|-------------|
| `now` | QWeather | 50k/mo | Current weather |
| `3d` | QWeather | 50k/mo | 3-day daily forecast |
| `7d` | QWeather | 50k/mo | 7-day daily forecast |
| `10d` | QWeather | 50k/mo | 10-day daily forecast |
| `15d` | QWeather | 50k/mo | 15-day daily forecast |
| `30d` | QWeather | 50k/mo | 30-day daily forecast |
| `24h` | QWeather | 50k/mo | 24-hour hourly forecast |
| `72h` | QWeather | 50k/mo | 72-hour hourly forecast |
| `168h` | QWeather | 50k/mo | 168-hour hourly forecast |
| `indices` | QWeather | 50k/mo | Weather lifestyle indices (19 types) |
| `aqi` | WAQI | 1k/hr | Air quality + PM2.5/PM10 forecast |

---

## Data Reference

### Current Weather `now`

| Field | Description | Unit |
|-------|-------------|------|
| `temp` | Temperature | °C |
| `feelsLike` | Feels-like temperature | °C |
| `text` / `icon` | Weather description / icon | — |
| `windDir` / `windScale` | Wind direction / wind scale | Beaufort |
| `windSpeed` | Wind speed | km/h |
| `humidity` | Humidity | % |
| `precip` | Precipitation in last 1 hour | mm |
| `pressure` | Air pressure | hPa |
| `vis` | Visibility | km |
| `cloud` | Cloud cover | % |
| `dew` | Dew point temperature | °C |

### Daily Forecast `3d/7d/10d/15d/30d`

| Field | Description | Unit |
|-------|-------------|------|
| `fxDate` | Date | — |
| `sunrise` / `sunset` | Sunrise / Sunset | HH:MM |
| `moonrise` / `moonset` | Moonrise / Moonset | HH:MM |
| `moonPhase` | Moon phase | — |
| `tempMax` / `tempMin` | Max temp / Min temp | °C |
| `textDay` / `textNight` | Daytime / Nighttime weather | — |
| `windDirDay` / `windDirNight` | Daytime / Nighttime wind direction | — |
| `windScaleDay` / `windScaleNight` | Daytime / Nighttime wind scale | Beaufort |
| `humidity` | Humidity | % |
| `precip` | Total precipitation for the day | mm |
| `uvIndex` | UV index | — |
| `pressure` | Air pressure | hPa |
| `vis` | Visibility | km |

### Hourly Forecast `24h/72h/168h`

| Field | Description | Unit |
|-------|-------------|------|
| `fxTime` | Forecast time (ISO8601) | — |
| `temp` | Temperature | °C |
| `text` | Weather description | — |
| `windDir` / `windScale` | Wind direction / wind scale | Beaufort |
| `humidity` | Humidity | % |
| `pop` | Probability of precipitation | % |
| `precip` | Precipitation | mm |
| `pressure` | Air pressure | hPa |
| `cloud` | Cloud cover | % |
| `dew` | Dew point temperature | °C |

### Lifestyle Indices `indices`

19 index types available in China: exercise, car washing, dressing, fishing, UV, travel, allergy, comfort, **cold/flu**, pollution diffusion, air conditioning, sunglasses, makeup, clothes drying, traffic, sunscreen, etc. Overseas locations support only 5 types: exercise, car washing, dressing, fishing, UV.

| Field | Description |
|-------|-------------|
| `name` | Index type name |
| `category` | Level label |
| `text` | Detailed suggestion |

### Air Quality `aqi`

Source: WAQI (aqicn.org)

| Field | Description | Unit |
|-------|-------------|------|
| `aqi` | Air Quality Index | — |
| `dominentpol` | Dominant pollutant | pm25/pm10/o3/no2 |
| `pm25` | PM2.5 | μg/m³ |
| `pm10` | PM10 | μg/m³ |
| `co` | CO | mg/m³ |
| `no2` / `o3` / `so2` | NO₂ / O₃ / SO₂ | μg/m³ |
| `t` / `h` | Temperature / Humidity | °C / % |
| `p` / `w` | Air pressure / Wind speed | hPa / km/h |
| `forecast.pm25[]` | 7-day PM2.5 forecast | avg/min/max |
| `forecast.pm10[]` | 7-day PM10 forecast | avg/min/max |

AQI levels: Good (≤50) · Moderate (≤100) · Unhealthy for Sensitive (≤150) · Unhealthy (≤200) · Very Unhealthy (≤300) · Hazardous (>300)

---

## Examples

```bash
# Current weather by CityId
python scripts/weather.py 101180301

# Current weather by English city name (auto-resolved)
python scripts/weather.py Shanghai

# Current weather by Chinese city name (auto-resolved)
python scripts/weather.py 上海

# 7-day forecast
python scripts/weather.py 101180301 --endpoint 7d

# 24-hour hourly forecast
python scripts/weather.py 101180301 --endpoint 24h

# 15-day forecast by coordinates (auto-detect order)
python scripts/weather.py 113.92,35.30 --endpoint 15d
python scripts/weather.py 35.30,113.92 --endpoint 15d

# Lifestyle indices
python scripts/weather.py 101180301 --endpoint indices

# Air quality by city name
python scripts/weather.py xinxiang --endpoint aqi
python scripts/weather.py 新乡 --endpoint aqi

# Air quality by coordinates
python scripts/weather.py "geo:35.30;113.92" --endpoint aqi

# Raw JSON output
python scripts/weather.py 101180301 --json
```

## Error Codes

| QWeather code | WAQI status | Meaning |
|---------------|-------------|---------|
| 200 | ok | Success |
| 400 | error | Bad parameters |
| 401 | error | Authentication failed (check key or token) |
| 402 | — | Quota exceeded |
| 403 | — | Wrong API Host |

## FAQ

**Q: "Configuration item not set" error?**
A: You need to set the corresponding environment variables or use a `.env` file.

**Q: How to find CityId?**
A: No need! Just enter the city name (Chinese or English), the script will automatically resolve it.

**Q: What cities are supported?**
A: Beijing, Shanghai, Guangzhou, Shenzhen, Chengdu, Hangzhou, Nanjing, Zhengzhou, Xi'an, Chongqing, Wuhan, Kunming, Dubai, Singapore, Moscow, Rio de Janeiro, New York, Los Angeles, Chicago, London, Manchester, Edinburgh, Paris, Lyon, Marseille, Tokyo, Osaka, Kyoto, Berlin, Munich, Frankfurt, Sydney, Melbourne, Brisbane, all cities recognized by QWeather GeoAPI are supported.
