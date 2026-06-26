# Weather Fetcher Skill

Fetch historical and forecast weather by location name or coordinates via [Open-Meteo](https://open-meteo.com/) (free, no API key).

## Quick Start

```bash
# From the skill directory
pip install -r requirements.txt

# By location (geocoded)
python scripts/fetch_historical.py "Oslo, Norway"
python scripts/fetch_forecast.py "Oslo, Norway"

# By coordinates
python scripts/fetch_historical.py --lat 59.91 --lon 10.75
python scripts/fetch_forecast.py --lat 59.91 --lon 10.75 --format csv
```

Output is printed to stdout (CSV or JSON). Redirect to save: `python scripts/fetch_historical.py "Oslo" > out.csv`.

## Location vs coordinates

Provide **either**:

- **Location**: positional or `--location` / `-l` (e.g. `"Oslo, Norway"`) — resolved via Open-Meteo Geocoding API
- **Coordinates**: `--lat` and `--lon` (both required)

## Options

| Option | Description |
|--------|-------------|
| `location` | Place name (positional) |
| `--location`, `-l` | Place name (alternative to positional) |
| `--lat` | Latitude (use with `--lon`) |
| `--lon` | Longitude (use with `--lat`) |
| `--kc` | Crop coefficient for ET₀ (default 1.0) |
| `--format`, `-f` | `csv` (default) or `json` |

## Features

- **Historical**: Last 10 days of **observed** weather (Open-Meteo archive API)
- **Forecast**: Next **7 days** of forecast weather
- Temperature, precipitation, evapotranspiration (ET₀), cumulative columns
- CSV or JSON output to stdout

## Output columns

| Column | Description |
|--------|-------------|
| `date` | YYYY-MM-DD |
| `temp` | Mean daily temperature (°C) |
| `precip` | Total daily precipitation (mm) |
| `et0_fao` | FAO-56 reference evapotranspiration (mm/day), after `kc` |
| `evaporation` | Estimated evaporation (mm) |
| `agg_precip` | Cumulative precipitation |
| `agg_evaporation` | Cumulative evapotranspiration |

## Structure

```
skills/weather-fetcher/
├── SKILL.md
├── README.md
├── requirements.txt
├── scripts/
│   ├── fetch_historical.py
│   ├── fetch_forecast.py
│   └── utils.py
└── tests/
    └── test_scripts.py
```

## Testing

```bash
pip install -r requirements.txt
python tests/test_scripts.py
```

Tests cover utils (get_lat_lon, calculate_evaporation, process_data), script runs by location, and script runs by `--lat` / `--lon` (live API).

## Documentation

See [SKILL.md](SKILL.md) for full skill documentation, troubleshooting, and technical notes.
