---
name: weather-loader
description: "Fetch historical or forecast weather by location or coordinates via Open-Meteo. No API key needed."
license: MIT
---

# Weather Data Fetcher

Fetch daily weather (historical and forecast) by location name or coordinates via Open-Meteo. No API key needed. Scripts: `fetch_historical.py` (historical), `fetch_forecast.py` (forecast).

## When to invoke

Use this skill when the user asks for:
- Historical weather data for a location or coordinates
- Weather forecast for the next days
- Precipitation or evapotranspiration data for garden planning

## Location vs coordinates

Provide **either**:
- **Location**: positional or `--location` / `-l` (e.g. `"Oslo, Norway"`) — geocoded via Open-Meteo
- **Coordinates**: `--lat` and `--lon` (both required)

**Days**: `--days N` — history default 10 (max 30), forecast default 7 (max 15).

## `weather_fetch_historical`

Run `scripts/fetch_historical.py`. **Observed** weather (Open-Meteo archive API). Default 10 days, max 30 (`--days N`).

```bash
python scripts/fetch_historical.py "Oslo, Norway"
python scripts/fetch_historical.py "Oslo, Norway" --days 20 --format json --kc 1.05
python scripts/fetch_historical.py --location "London, UK" --format csv
python scripts/fetch_historical.py --lat 59.91 --lon 10.75 --days 30
```

## `weather_fetch_forecast`

Run `scripts/fetch_forecast.py`. **Forecast** weather. Default 7 days, max 15 (`--days N`).

```bash
python scripts/fetch_forecast.py "Oslo, Norway"
python scripts/fetch_forecast.py "Paris, France" --days 15 --format json --kc 1.0
python scripts/fetch_forecast.py --lat 59.91 --lon 10.75 --days 14 --format csv
```

## Output columns

| Column | Description |
|---|---|
| `date` | YYYY-MM-DD |
| `temp` | Mean daily temperature (°C) |
| `precip` | Total daily precipitation (mm) |
| `et0_fao` | FAO-56 reference evapotranspiration (mm/day), after `kc` |
| `evaporation` | Estimated crop evaporation (mm) |
| `agg_precip` | Cumulative precipitation |
| `agg_evaporation` | Cumulative evapotranspiration |

**`kc` (crop coefficient)**: multiplier applied to ET₀. Default 1.0.

## Technical notes

- **Historical**: Open-Meteo archive API (observation/reanalysis); hourly → daily (temp = mean, precip/ET = sum).
- **Forecast**: Open-Meteo forecast API; same daily aggregation.
- **Geocoding**: location names resolved via Open-Meteo Geocoding API when not using `--lat`/`--lon`.

## Troubleshooting

| Symptom | Fix |
|---|---|
| Location not found | Try a simpler string (e.g. `"Oslo"`) or use `--lat` and `--lon` |
| Provide either location or both --lat and --lon | Give a location (positional or `--location`) or both `--lat` and `--lon` |
| API failure | Check internet access; retry — Open-Meteo is free and usually reliable |
