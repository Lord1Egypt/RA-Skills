---
name: weather-search
description: "Query real-time weather information using Amap (高德地图) Weather API. Use when user asks about weather, temperature, wind, humidity for Chinese cities. Requires AMAP_API_KEY environment variable."
homepage: https://lbs.amap.com/api/javascript-api/guide/services/weather
metadata:
  { "openclaw": { "emoji": "☔", "requires": { "bins": ["curl"] } } }
---

# Weather Search Skill

Query real-time weather information using Amap (高德地图) Weather API.

## API Documentation
https://lbs.amap.com/api/javascript-api/guide/services/weather

## Prerequisites

1. **Get Amap API Key**
   - Visit: https://console.amap.com/
   - Create an application
   - Get your Web Service (Key)

2. **Set Environment Variable**
   ```bash
   export AMAP_API_KEY="your_api_key_here"
   ```

## Usage

### Query Weather by City Name
```bash
curl -X GET "https://restapi.amap.com/v3/weather/weatherInfo?city=BEIJING&key=YOUR_API_KEY&output=json"
```

### Query Weather by City Code
```bash
curl -X GET "https://restapi.amap.com/v3/weather/weatherInfo?city=110000&key=YOUR_API_KEY&output=json"
```

### Query Multiple Cities
```bash
curl -X GET "https://restapi.amap.com/v3/weather/weatherInfo?city=BEIJING|SHANGHAI|GUANGZHOU&key=YOUR_API_KEY&output=json"
```

### Query by Coordinates (Latitude, Longitude)
```bash
curl -X GET "https://restapi.amap.com/v3/weather/weatherInfo?location=116.40,39.90&key=YOUR_API_KEY&output=json"
```

## API Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| city | String | Yes (or location) | City name or city code |
| location | String | Yes (or city) | Format: longitude,latitude |
| key | String | Yes | Amap API Key |
| output | String | No | Response format: json or xml (default: json) |

## Response Example

```json
{
  "status": "1",
  "infocode": "10000",
  "info": "Query Successful",
  "count": "1",
  "lives": [
    {
      "province": "Beijing",
      "city": "Beijing",
      "adcode": "110000",
      "weather": "Clear",
      "temperature": "25",
      "winddirection": "North",
      "windpower": "2",
      "humidity": "45",
      "reporttime": "2024-01-15 12:00:00"
    }
  ]
}
```

## Quick Start Script

Create a weather query script:

```bash
#!/bin/bash
# weather.sh

API_KEY="${AMAP_API_KEY:-your_api_key_here}"
CITY="$1"

if [ -z "$CITY" ]; then
    echo "Usage: weather.sh <city_name_or_code>"
    exit 1
fi

curl -s "https://restapi.amap.com/v3/weather/weatherInfo?city=${CITY}&key=${API_KEY}&output=json" | jq '.'
```

Make it executable:
```bash
chmod +x weather.sh
./weather.sh BEIJING
```

## City Code Reference

| City | Code |
|------|------|
| Beijing | 110000 |
| Shanghai | 310000 |
| Guangzhou | 440100 |
| Shenzhen | 440300 |
| Hangzhou | 330100 |
| Chengdu | 510100 |
| Wuhan | 420100 |
| Xi'an | 610100 |

## Notes

- API Key is required for all requests
- Free tier: 1000 requests/day
- Response includes: weather condition, temperature, wind direction, wind power, humidity
- Supports both Chinese city names and city codes