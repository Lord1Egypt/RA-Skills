# Weather Forecast Plus — API Reference

## Base URL

`https://api.openmeteo-api.com`

## Unified Aggregation

This API aggregates multiple public weather services into a single consistent interface. It handles geocoding (city name to lat/lon) automatically via the Open-Meteo Geocoding API, so you can pass city names directly instead of coordinates.

## Endpoints

| Endpoint | Description | Upstream Source |
|----------|-------------|----------------|
| `/api/current?location=CITY` | Current conditions | Open-Meteo |
| `/api/forecast?location=CITY&days=N` | Multi-day forecast (1-16 days) | Open-Meteo |
| `/api/air-quality?location=CITY` | Air quality index and pollutants | Open-Meteo Air Quality |
| `/api/uv?location=CITY` | UV index and sun exposure data | Open-Meteo |
| `/api/alerts?location=CITY` | Severe weather alerts | Government services |
| `/api/quick?location=CITY` | One-line summary (wttr.in format) | wttr.in |

## Query Parameters

| Parameter | Required | Description | Example |
|-----------|----------|-------------|---------|
| `location` | Yes | City name, region, or lat,lon | `London`, `New+York`, `48.85,2.35` |
| `days` | No | Forecast days (default 3, max 16) | `5` |
| `units` | No | `metric` (default) or `imperial` | `imperial` |

## Rate Limits

- Open-Meteo upstream: 10,000 requests/day (generous)
- wttr.in upstream: ~100 requests/hour per IP
- Space requests at least 3 seconds apart to be safe

## Formatting Rules

- Always include location name and current date/time at the top
- Group forecast days clearly with date headers
- Use temperature units consistently (default Celsius)
- Include "feels like" temperature when available
- For air quality, map AQI to human-readable levels:
  - 0-50: Good
  - 51-100: Moderate
  - 101-150: Unhealthy for Sensitive Groups
  - 151-200: Unhealthy
  - 201-300: Very Unhealthy
  - 301+: Hazardous
- For UV index, include protection recommendations:
  - 0-2: Low (no protection needed)
  - 3-5: Moderate (wear sunscreen)
  - 6-7: High (reduce sun exposure)
  - 8-10: Very High (avoid midday sun)
  - 11+: Extreme (stay indoors if possible)
- Keep summaries concise unless the user asks for detail
- Use markdown tables for multi-day forecasts

## Error Handling

- HTTP 502: upstream service temporarily unavailable, retry in 30 seconds
- HTTP 404: unknown endpoint or location not found
- HTTP 429: rate limit exceeded, wait 60 seconds
- If geocoding fails, ask the user to provide coordinates instead
