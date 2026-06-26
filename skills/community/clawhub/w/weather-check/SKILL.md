---
name: weather-check
description: Current weather conditions and multi-day forecasts for any location worldwide.
version: 1.0.0
metadata:
  openclaw:
    emoji: "🌤️"
    homepage: https://weather.agentutil.net
    always: false
---

# weather-check

Get current weather conditions and multi-day forecasts for any location by name or coordinates.

## Endpoints

### Current Weather

```bash
curl -X POST https://weather.agentutil.net/v1/current \
  -H "Content-Type: application/json" \
  -d '{"location": "London"}'
```

Or by coordinates: `{"lat": 51.51, "lon": -0.13}`

### Forecast

```bash
curl -X POST https://weather.agentutil.net/v1/forecast \
  -H "Content-Type: application/json" \
  -d '{"location": "Tokyo", "days": 7}'
```

Days: 1-16 (default 7).

## Response Format

```json
{
  "location": {"name": "London", "country": "GB", "latitude": 51.51, "longitude": -0.13},
  "current": {
    "temperature": {"celsius": 12.5, "fahrenheit": 54.5},
    "humidity": 72,
    "conditions": "Overcast",
    "wind": {"speed_kmh": 15.2, "direction_degrees": 230}
  },
  "request_id": "abc-123",
  "service": "https://weather.agentutil.net"
}
```

## Pricing

- Free tier: 10 queries/day, no authentication required
- Paid tier: $0.001/query via x402 protocol (USDC on Base)

## Privacy

No authentication required for free tier. No personal data collected. Rate limiting uses IP hashing only.
