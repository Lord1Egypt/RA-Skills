# Shuzhi Weather API Documentation

## API Overview

The Shuzhi Weather API provides hourly weather forecasts based on geographic coordinates. The API uses HMAC-SHA256 authentication with dual signature mechanisms.

### Base Configuration

- **API URL**: `https://test-apisix-gateway.shuzhi.shuqinkeji.cn`
- **API Path**: `/2033738771717074945`
- **Method**: POST
- **Product ID**: `2033747427070226434`
- **Content-Type**: `application/json`

## Authentication

The API requires HMAC-SHA256 authentication with dual signatures:

### Authentication Headers

| Header | Description |
|--------|-------------|
| `X-HMAC-ACCESS-KEY` | Your app_key |
| `X-APP-PRODUCT-ID` | Product ID |
| `X-HMAC-ALGORITHM` | Algorithm type (hmac-sha256) |
| `X-HMAC-SIGNATURE` | URL signature |
| `X-HMAC-DIGEST` | Body signature |
| `Date` | Current timestamp in GMT format |
| `Content-Type` | application/json |

### Signature Generation

#### URL Signature

```
canonical_string = {METHOD}\n{PATH}\n\n{APP_KEY}\n{DATE}\n
signature = HMAC-SHA256(APP_SECRET, canonical_string) → Base64
```

#### Body Signature

```
body_signature = HMAC-SHA256(APP_SECRET, body_json) → Base64
```

**Example**:
```
Method: POST
Path: /2033738771717074945
App Key: a536d0c326d5464b8a9e3b3188e6877e
Date: Tue, 17 Mar 2026 08:30:00 GMT

canonical_string:
POST
/2033738771717074945

a536d0c326d5464b8a9e3b3188e6877e
Tue, 17 Mar 2026 08:30:00 GMT
```

## Request Format

### Request Body (JSON)

```json
{
  "longitude": "116.4074",
  "latitude": "39.9042",
  "hourly": "temperature_2m"
}
```

### Request Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| longitude | string | Yes | Longitude coordinate |
| latitude | string | Yes | Latitude coordinate |
| hourly | string | No | Hourly data type (e.g., temperature_2m) |

### Example Request

```bash
curl -X POST "https://test-apisix-gateway.shuzhi.shuqinkeji.cn/2033738771717074945" \
  -H "X-HMAC-ACCESS-KEY: your_app_key" \
  -H "X-APP-PRODUCT-ID: 2033747427070226434" \
  -H "X-HMAC-ALGORITHM: hmac-sha256" \
  -H "X-HMAC-SIGNATURE: url_signature" \
  -H "X-HMAC-DIGEST: body_signature" \
  -H "Date: Tue, 17 Mar 2026 08:30:00 GMT" \
  -H "Content-Type: application/json" \
  -d '{
    "longitude": "116.4074",
    "latitude": "39.9042",
    "hourly": "temperature_2m"
  }'
```

## Response Format

### Successful Response (Code 200)

```json
{
  "code": 200,
  "message": "success",
  "data": {
    "hourly": {
      "time": [
        "2026-03-17T00:00",
        "2026-03-17T01:00",
        "2026-03-17T02:00"
      ],
      "temperature_2m": [
        15.2,
        14.8,
        14.5
      ]
    },
    "latitude": 39.9042,
    "longitude": 116.4074
  }
}
```

### Response Fields

| Field | Type | Description |
|-------|------|-------------|
| code | number | Response code (200 for success) |
| message | string | Response message |
| data | object | Weather data payload |

### Data Fields

| Field | Type | Description |
|-------|------|-------------|
| hourly | object | Hourly weather data |
| hourly.time | array | Array of time strings (ISO 8601 format) |
| hourly.temperature_2m | array | Array of temperature values (Celsius) |
| latitude | number | Latitude coordinate |
| longitude | number | Longitude coordinate |

## Error Responses

### Authentication Error (Code 401)

```json
{
  "code": 401,
  "message": "Invalid credentials"
}
```

### Invalid Parameters (Code 400)

```json
{
  "code": 400,
  "message": "Invalid longitude or latitude"
}
```

### Server Error (Code 500)

```json
{
  "code": 500,
  "message": "Internal server error"
}
```

## Error Handling

### HTTP Status Codes

| Status Code | Description |
|-------------|-------------|
| 200 | Success |
| 400 | Bad Request (invalid parameters) |
| 401 | Unauthorized (invalid credentials) |
| 500 | Internal Server Error |

### Response Codes

| Code | Description |
|------|-------------|
| 200 | Success |
| 400 | Invalid parameters |
| 401 | Authentication failed |
| 500 | Server error |

## Configuration

### Credential Configuration

Credentials should be stored in `~/.openclaw/skills/shuzhi-weather/config.json`:

```json
{
  "app_key": "your_app_key_here",
  "app_secret": "your_app_secret_here"
}
```

### Configuration Priority

1. User's config.json (highest priority)
2. Platform environment variables
3. Default values

## Usage Examples

### Basic Weather Query

```python
from scripts.get_weather import get_weather_forecast

# Query weather for Beijing
result = get_weather_forecast(
    longitude="116.4074",
    latitude="39.9042",
    hourly="temperature_2m"
)

if result:
    print(json.dumps(result, indent=2))
```

### Command Line Usage

```bash
# Basic query
python scripts/get_weather.py 116.4074 39.9042

# With hourly parameter
python scripts/get_weather.py 116.4074 39.9042 temperature_2m
```

## Coordinate Format

- **Longitude**: Range from -180 to 180
- **Latitude**: Range from -90 to 90
- **Format**: Decimal degrees (e.g., 116.4074, 39.9042)

### Common City Coordinates

| City | Latitude | Longitude |
|------|----------|-----------|
| Beijing | 39.9042 | 116.4074 |
| Shanghai | 31.2304 | 121.4737 |
| Guangzhou | 23.1291 | 113.2644 |
| Shenzhen | 22.5431 | 114.0579 |
| Chengdu | 30.5728 | 104.0668 |

## Notes

- All timestamps are in ISO 8601 format
- Temperature values are in Celsius
- The API requires dual HMAC-SHA256 signatures
- Authentication credentials must be configured before use
- Request timeout is 30 seconds
- Coordinate precision: up to 4 decimal places for better accuracy
