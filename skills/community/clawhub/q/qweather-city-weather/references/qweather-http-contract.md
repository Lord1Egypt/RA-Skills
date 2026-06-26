# QWeather HTTP API Contract

This skill uses official QWeather HTTPS endpoints directly.

## Required configuration

- `QWEATHER_API_KEY`: passed as header `X-QW-Api-Key`
- `QWEATHER_API_HOST`: shared host used by this skill for both city and weather queries

## City lookup API

- Method: `GET`
- URL:
  - `https://{apiHost}/geo/v2/city/lookup?location=<query>&number=<n>`
- Header:
  - `X-QW-Api-Key: <QWEATHER_API_KEY>`

Expected success:

- HTTP `200`
- JSON field `code` equals `"200"`
- City list in `location` (some deployments may return `city`)

## Current weather API

- Method: `GET`
- URL:
  - `https://{apiHost}/v7/weather/now?location=<locationIdOrName>`
- Header:
  - `X-QW-Api-Key: <QWEATHER_API_KEY>`

Expected success:

- HTTP `200`
- JSON field `code` equals `"200"`
- Current weather object in `now`

## Script mapping

The bundled `scripts/qweather_query.py` maps commands to APIs:

- `search-city` -> city lookup API
- `get-weather` -> current weather API
- `city-weather` -> city lookup, choose location id, then current weather

## Example cURL

```bash
curl --compressed -sS "https://<QWEATHER_API_HOST>/geo/v2/city/lookup?location=Beijing&number=10" \
  -H "X-QW-Api-Key: <QWEATHER_API_KEY>"
```

```bash
curl --compressed -sS "https://<QWEATHER_API_HOST>/v7/weather/now?location=101010100" \
  -H "X-QW-Api-Key: <QWEATHER_API_KEY>"
```
