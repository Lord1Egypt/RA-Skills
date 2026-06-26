---
name: weather-wttr.in
description: Get weather data from wttr.in free service. Triggers on: weather, forecast, temperature, rain, UV, humidity, wind. Free, no API key required. Python 3.6+, no pip packages. Works on Windows/macOS/Linux.
---

# weather-wttr.in

Free weather data via [wttr.in](https://wttr.in). No registration, no API key.
Cross-platform: Windows / macOS / Linux (Python 3.6+ only, no pip packages).

## Usage

```bash
# Current weather + forecast (auto-detect IP location)
python scripts/weather.py

# City name
python scripts/weather.py Beijing
python scripts/weather.py "New York"

# GPS coordinates
python scripts/weather.py "35.31,113.87"

# Forecast only (--today shows daily summary)
python scripts/weather.py Beijing --today

# JSON output (programmatic use)
python scripts/weather.py Beijing --json

# Chinese language
python scripts/weather.py Beijing --lang=zh
```

## Python Requirements

- Python 3.6+ (stdlib only — `urllib`, `json`, `sys`)
- No pip packages needed
- Works on Windows / macOS / Linux (console encoding handled automatically)

## Notes

- Free service: ~1 request/second rate limit
- Location auto-detection via IP when no location specified
- Supports Chinese descriptions with `--lang=zh`
- Returns 3-day forecast with hourly breakdown
- Exit code 0 on success, 1 on failure
