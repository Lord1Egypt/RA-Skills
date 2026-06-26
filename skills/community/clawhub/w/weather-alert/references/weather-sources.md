# Weather Data Sources

## Primary: Open-Meteo API

**URL:** `https://api.open-meteo.com/v1/forecast`
**Cost:** Free (1000 requests/hour, no API key)
**Coverage:** Global, ~200+ weather parameters
**Limits:** 1000 requests/hour, max 1000 historical days

### Supported Parameters
- `current`: temperature_2m, relative_humidity_2m, apparent_temperature, precipitation, rain, showers, snowfall, weather_code, wind_speed_10m, wind_direction_10m, wind_gusts_10m, surface_pressure, uv_index, is_day
- `hourly`: temperature_2m, precipitation_probability, precipitation, weather_code, snowfall_probability
- `daily`: temperature_2m_min/max, precipitation_sum, rain_sum, snowfall_sum, wind_speed_10m_max, wind_gusts_10m_max, uv_index_max, precipitation_probability_max, weather_code

### Weather Codes (WMO)

| Code | Description          | Code | Description          |
|------|----------------------|------|----------------------|
| 0    | Clear sky            | 61   | Rain light           |
| 1    | Mainly clear         | 63   | Rain moderate        |
| 2    | Partly cloudy        | 65   | Rain heavy           |
| 3    | Overcast             | 66   | Freezing rain light  |
| 45   | Foggy                | 67   | Freezing rain heavy  |
| 48   | Rime fog             | 71   | Snow light           |
| 51   | Light drizzle        | 73   | Snow moderate        |
| 53   | Moderate drizzle     | 75   | Snow heavy           |
| 55   | Dense drizzle        | 77   | Snow grains          |
| 56   | Freezing drizzle     | 80   | Rain showers light   |
| 57   | Freezing drizzle hvy | 81   | Rain showers moderate|
| 95   | Thunderstorm         | 82   | Rain showers heavy   |
| 96   | Thunderstorm + hail  | 85   | Snow showers light   |
| 99   | Thunderstorm hvy hail| 86   | Snow showers heavy   |

## Secondary: wttr.in

**URL:** `https://wttr.in/{location}?format=j1`
**Cost:** Free, no key
**Best for:** Quick lookups, human-readable text
**Note:** Less structured than Open-Meteo, good for simple queries

## Tertiary: OpenWeatherMap

**URL:** `https://api.openweathermap.org/data/2.5/weather`
**Cost:** Free tier (1000 calls/day)
**Requires:** API key
**Best for:** Historical data, detailed forecasts

## Timezones

Default timezone: `Europe/Prague`
Common alternatives:
- `Europe/London`
- `America/New_York`
- `America/Los_Angeles`
- `Asia/Tokyo`
- `Australia/Sydney`
