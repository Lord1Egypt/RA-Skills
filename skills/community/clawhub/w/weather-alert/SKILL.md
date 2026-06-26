---
name: weather-alert
description: Proactive weather monitoring and alerting — tracks conditions for any location, sends notifications when thresholds are exceeded (rain, snow, temperature, wind, UV, pressure), and provides daily briefings. Use when: (1) Need to know if it will rain before going out, (2) Want temperature alerts for travel planning, (3) Need daily weather briefings, (4) Monitoring conditions for events (sports, construction, farming), (5) Tracking multi-day weather trends
---

# Weather Alert Skill

Proactively monitor weather conditions and alert when thresholds are exceeded. Uses free APIs (wttr.in, Open-Meteo) with no API key required.

## Quick Start

```bash
# Install the skill
npx clawhub install weather-alert

# Check current weather
"Check weather in Prague"

# Set a rain alert for tomorrow
"Alert me if it will rain tomorrow in Prague"

# Set a temperature alert (below 5°C or above 30°C)
"Alert me if temperature drops below 5°C or exceeds 30°C"

# Get a 7-day briefing
"7-day weather briefing for Prague"

# List active alerts
"Show my weather alerts"
```

## Core Features

### 1. Current Weather Check

Returns current conditions including temperature, humidity, wind, precipitation probability, UV index, and visibility.

```
🌤 Prague Weather — 2026-04-17 15:00
Temp: 12°C (feels like 10°C) | Humidity: 65%
Wind: 15 km/h NW | Precip: 10% | UV: 3
Visibility: 10 km | Pressure: 1013 hPa
Condition: Partly cloudy
```

### 2. Forecast & Briefing

Provides multi-day forecasts with condition summaries.

```
📅 7-Day Briefing — Prague
Mon 17: ☁️ 8-14°C | Rain 40%
Tue 18: 🌧️ 6-11°C | Rain 80%
Wed 19: ⛅ 10-16°C | Rain 20%
Thu 20: ☀️ 12-20°C | Rain 5%
Fri 21: ☀️ 14-22°C | Rain 0%
Sat 22: ⛈️ 11-18°C | Rain 70%
Sun 23: 🌧️ 8-14°C | Rain 60%
```

### 3. Smart Alerts

Set threshold-based alerts that trigger notifications:

- **Temperature:** Above/below a threshold (°C)
- **Rain:** Precipitation probability exceeding a %
- **Snow:** Snowfall depth exceeding mm
- **Wind:** Sustained speed exceeding km/h
- **UV:** UV index exceeding a threshold
- **Pressure:** Barometric pressure dropping/rising rapidly
- **Frost:** Risk of frost (temperature below 0°C overnight)

```
🔔 Active Alerts:
• [TOMORROW] Rain > 70% in Prague → Notify me
• [22:00] Temp < 5°C in Prague → Notify me
• [WEEKEND] UV > 7 in Prague → Notify me
```

### 4. Event Planner

Check weather suitability for specific activities:

```
🏃 Running — Prague, Tomorrow
Good: Temp 10°C, no rain, wind < 15 km/h
Warning: Possible morning drizzle (06:00-08:00)

🧺 Picnic — Prague, Sunday
Bad: Rain 70%, wind 25 km/h
Suggestion: Move to Saturday instead
```

### 5. Weather Trends

Track how conditions change over time for a location:

```
📈 Prague Temperature Trend (7 days):
Mon: 12°C → Tue: 8°C → Wed: 14°C → Thu: 16°C → Fri: 18°C → Sat: 12°C → Sun: 10°C
Change: -1°C from yesterday
```

## Configuration

`config.yaml` defines default location and alert thresholds:

```yaml
default_location:
  name: "Prague"
  lat: 50.0755
  lon: 14.4378

alerts:
  rain_threshold: 60        # % probability
  temp_min: 5               # °C below which to alert
  temp_max: 30              # °C above which to alert
  wind_max: 40              # km/h
  snow_depth: 5             # cm
  uv_max: 7
  frost_threshold: 0        # °C

notification:
  method: "exec-event"      # How alerts are delivered
  schedule_check: "6h"      # Auto-check interval
```

## Data Sources

- **Primary:** Open-Meteo API (free, no key, global coverage)
- **Secondary:** wttr.in (quick lookups, human-readable)
- **Fallback:** OpenWeatherMap (if API key configured)

## Error Handling

- API timeout → show cached data with staleness warning
- Location not found → suggest nearest match
- Rate limit → wait and retry (Open-Meteo: 1000 requests/hour free)

## Permissions

```yaml
permissions:
  read: ["~/weather-alerts/*"]
  network: ["wttr.in", "open-meteo.com"]
  write: ["~/weather-alerts/alerts.yaml"]
```
