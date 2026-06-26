---
name: weather-ensemble-forecast
description: Multi-model ensemble weather forecasts comparing GFS, ECMWF, JMA, GEM, ICON, ARPEGE, GraphCast and more. Get high temperature predictions from up to 9 independent weather models with agreement analysis for 16 global cities.
license: MIT
user-invocable: true
metadata: {"openclaw":{"requires":{"env":[],"bins":["curl","jq"]},"files":["scripts/*"]}}
---

# Weather Ensemble Forecast

Compare weather forecasts from up to 9 independent global weather models side-by-side.

No setup needed -- just install and run `/forecast nyc`.

## What this skill does

- Fetches high temperature forecasts from multiple weather models: GFS, ECMWF, JMA, GEM, MeteoFrance, UKMO, ICON, ARPEGE, GraphCast
- Shows each model's individual prediction so you can see where they agree and disagree
- Calculates ensemble standard deviation (how uncertain the forecast is)
- Cross-validates with NWS (National Weather Service) official forecasts
- Covers 16 cities: NYC, Chicago, Miami, Dallas, Atlanta, Seattle, Toronto, London, Paris, Munich, Seoul, Ankara, Wellington, Lucknow, Buenos Aires, Sao Paulo

## Quick Start

```
/forecast nyc
```

That's it. Works immediately with free tier (NYC, Chicago, Miami).

For full access (all 16 cities), set an API key:

```
curl -X POST https://polymarket-scanner.fly.dev/keys/free
```

Then set: `export WEATHER_ENSEMBLE_API_KEY="pm_your_key_here"`

## Commands

### `/forecast <city>` - Get multi-model forecast
Compare forecasts from all available weather models for a city.

When the user asks for a weather forecast, temperature prediction, model comparison, or ensemble analysis, run:

```bash
bash {baseDir}/scripts/forecast.sh "<city>" "<date>"
```

Where `<city>` is a city key (e.g., nyc, london, seoul). Run `/cities` to see all options.

And `<date>` is optional, in YYYY-MM-DD format (defaults to tomorrow).

Display results showing each model's prediction, the ensemble average, and standard deviation.

### `/cities` - List available cities

```bash
bash {baseDir}/scripts/cities.sh
```

## Use Cases

- **Weather enthusiasts**: See how GFS, ECMWF, and other models compare for your city
- **Event planners**: Check forecast confidence before outdoor events
- **Researchers**: Access raw multi-model data for analysis
- **Travelers**: Get high-confidence forecasts when models agree, warnings when they don't
- **Prediction market traders**: Use ensemble data to evaluate temperature market positions (see polymarket-weather-scanner skill)

## How It Works

1. Queries the Weather Ensemble API for forecasts from each weather model
2. Returns individual model predictions so you can see the spread
3. Calculates ensemble statistics: mean, standard deviation
4. Higher standard deviation = more uncertainty = models disagree
5. Low standard deviation = high confidence = models agree

## External Endpoints

All requests are sent to the Weather Ensemble API server.

| Endpoint | Data Sent | Purpose |
|----------|-----------|---------|
| `https://polymarket-scanner.fly.dev/forecast/{city}` | City, date, API key (if set) | Get forecast |
| `https://polymarket-scanner.fly.dev/cities` | API key (if set) | List cities |

## Security & Privacy

- Works without an API key (anonymous free tier with IP-based rate limiting)
- All requests are sent to the Weather Ensemble API server (`polymarket-scanner.fly.dev`) via HTTPS
- Weather data is sourced from Open-Meteo and aggregated server-side
- No personal data collected or stored
