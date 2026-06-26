# Demo Output — weather-alert Skill

## Current Weather

```
$ python scripts/weather_alert.py --current
🌤 Prague Weather — 2026-04-17 15:00
Temp: 12.5°C (feels like 10.2°C) | Humidity: 65%
Wind: 15 km/h W | Precip: 0mm | UV: 3.2
Pressure: 1013.0 hPa | Partly cloudy
```

## 7-Day Forecast

```
$ python scripts/weather_alert.py
🌤 Prague Weather — 2026-04-17 15:00
Temp: 12.5°C (feels like 10.2°C) | Humidity: 65%
Wind: 15 km/h W | Precip: 0mm | UV: 3.2
Pressure: 1013.0 hPa | Partly cloudy

📅 7-Day Forecast
Fri 17: ⛅ 5°-18°C | Precip: 10% | Wind: 15 km/h
Sat 18: 🌧️ 3°-10°C | Precip: 80% | Wind: 30 km/h
Sun 19: ⛅ 8°-15°C | Precip: 20% | Wind: 12 km/h
Mon 20: ☀️ 10°-20°C | Precip: 5% | Wind: 8 km/h
Tue 21: ☀️ 12°-22°C | Precip: 0% | Wind: 10 km/h
Wed 22: ⛈️ 8°-14°C | Precip: 85% | Wind: 35 km/h
Thu 23: 🌧️ 6°-12°C | Precip: 70% | Wind: 25 km/h
```

## Alerts

```
$ python scripts/weather_alert.py --location Berlin
🌤 Berlin Weather — 2026-04-17 15:00
Temp: 8.0°C (feels like 5.0°C) | Humidity: 80%
Wind: 20 km/h NW | Precip: 2mm | UV: 2.1
Pressure: 1008.5 hPa | Rain

📅 7-Day Forecast
Fri 17: 🌧️ 2°-10°C | Precip: 90% | Wind: 25 km/h
...

🔔 ALERTS:
  • 🥶 Temperature 8.0°C is below 5°C threshold (feels like 5.0°C)
  • 🌧 Rain probability 90% exceeds 60% threshold
  • ❄️ Frost risk: overnight low 2°C below 0°C threshold
```

## Event Suitability

```
$ python scripts/weather_alert.py --event running
🏃 Running — Prague, Today
Good: Temp 5°-18°C — comfortable
Warning: Possible rain (10%)
```

```
$ python scripts/weather_alert.py --event picnic
🧺 Picnic — Prague, Today
Bad: High rain risk (80%), Wind too strong (30 km/h)
Suggestion: Move to Monday instead
```
