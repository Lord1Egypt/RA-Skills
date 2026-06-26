# Open-Meteo API Response Format

## API Endpoint

```
https://api.open-meteo.com/v1/forecast
```

## Request Parameters

### Required Parameters

| Parameter | Type | Range | Description |
|-----------|------|-------|-------------|
| `latitude` | float | -90 to 90 | Geographical WGS84 latitude |
| `longitude` | float | -180 to 180 | Geographical WGS84 longitude |

### Optional Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `hourly` | string | - | Comma-separated list of hourly parameters |
| `current` | string | - | Comma-separated list of current weather parameters |

### Hourly Parameters

Common hourly parameters:
- `temperature_2m` - Air temperature at 2 meters above ground (°C)
- `relative_humidity_2m` - Relative humidity at 2 meters above ground (%)
- `precipitation_probability` - Precipitation probability (%)
- `weather_code` - Weather condition code (0-99)

## Response Format

### Success Response

```json
{
  "latitude": 52.52,
  "longitude": 13.41,
  "generationtime_ms": 0.123456,
  "utc_offset_seconds": 0,
  "timezone": "UTC",
  "timezone_abbreviation": "UTC",
  "elevation": 38,
  "current_units": {
    "time": "iso8601",
    "interval": "seconds",
    "temperature_2m": "°C"
  },
  "current": {
    "time": "2024-01-15T12:00",
    "interval": 900,
    "temperature_2m": 5.5
  },
  "hourly_units": {
    "time": "iso8601",
    "temperature_2m": "°C"
  },
  "hourly": {
    "time": [
      "2024-01-15T00:00",
      "2024-01-15T01:00",
      "2024-01-15T02:00"
    ],
    "temperature_2m": [
      2.3,
      1.8,
      1.5
    ]
  }
}
```

### Response Fields

#### Root Level

| Field | Type | Description |
|-------|------|-------------|
| `latitude` | float | Requested latitude |
| `longitude` | float | Requested longitude |
| `generationtime_ms` | float | Server processing time in milliseconds |
| `utc_offset_seconds` | int | UTC offset in seconds |
| `timezone` | string | Timezone name (e.g., "UTC", "Europe/Berlin") |
| `timezone_abbreviation` | string | Timezone abbreviation (e.g., "UTC", "CET") |
| `elevation` | float | Elevation in meters above sea level |

#### Hourly Data

| Field | Type | Description |
|-------|------|-------------|
| `hourly_units` | object | Units for each hourly parameter |
| `hourly` | object | Arrays of hourly data values |

### Error Response

The API returns HTTP status codes:

| Status Code | Description |
|-------------|-------------|
| 200 | Success |
| 400 | Bad request (invalid parameters) |
| 404 | Not found |
| 500 | Server error |

## Weather Codes

| Code | Description |
|------|-------------|
| 0 | Clear sky |
| 1 | Mainly clear |
| 2 | Partly cloudy |
| 3 | Overcast |
| 45 | Fog |
| 48 | Depositing rime fog |
| 51 | Light drizzle |
| 53 | Moderate drizzle |
| 55 | Dense drizzle |
| 61 | Slight rain |
| 63 | Moderate rain |
| 65 | Heavy rain |
| 71 | Slight snow |
| 73 | Moderate snow |
| 75 | Heavy snow |
| 95 | Thunderstorm |

## Time Format

- Times are returned in ISO 8601 format: `YYYY-MM-DDTHH:MM`
- All times are in UTC unless timezone is specified
- Hourly data includes one entry for each hour

## Example API Calls

### Basic Temperature Forecast
```
https://api.open-meteo.com/v1/forecast?latitude=52.52&longitude=13.41&hourly=temperature_2m
```

### Temperature and Humidity
```
https://api.open-meteo.com/v1/forecast?latitude=52.52&longitude=13.41&hourly=temperature_2m,relative_humidity_2m
```

### Current Weather
```
https://api.open-meteo.com/v1/forecast?latitude=52.52&longitude=13.41&current=temperature_2m,relative_humidity_2m,weather_code
```

## Rate Limits

The Open-Meteo API is free to use and does not have strict rate limits.
However, reasonable usage is expected (e.g., don't make more than one request per second).

## Notes

- No authentication required
- HTTPS is required
- Response is always JSON
- Coordinate precision: Up to 4 decimal places recommended (approximately 11 meters precision)
