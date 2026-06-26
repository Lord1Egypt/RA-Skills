---
name: time-convert
description: Timezone conversion, current time, date arithmetic, and epoch conversion.
version: 1.0.0
metadata:
  openclaw:
    emoji: "🕐"
    homepage: https://time.agentutil.net
    always: false
---

# time-convert

Current time in any timezone, convert between timezones, date math (add/subtract), and ISO 8601 to unix epoch conversion.

## Endpoints

### Current Time

```bash
curl -X POST https://time.agentutil.net/v1/now \
  -H "Content-Type: application/json" \
  -d '{"timezone": "Pacific/Auckland"}'
```

### Timezone Conversion

```bash
curl -X POST https://time.agentutil.net/v1/convert \
  -H "Content-Type: application/json" \
  -d '{"time": "2026-03-04T09:00:00", "from_timezone": "America/New_York", "to_timezone": "Pacific/Auckland"}'
```

### Date Math

```bash
curl -X POST https://time.agentutil.net/v1/math \
  -H "Content-Type: application/json" \
  -d '{"date": "2026-03-04T00:00:00Z", "operation": "add", "value": 7, "unit": "days"}'
```

Units: seconds, minutes, hours, days, weeks, months, years.

### Epoch Conversion

```bash
curl -X POST https://time.agentutil.net/v1/epoch \
  -H "Content-Type: application/json" \
  -d '{"value": 1741046400, "direction": "from_epoch"}'
```

## Response Format

```json
{
  "iso": "2026-03-04T14:30:00.000+13:00",
  "unix": 1741050600,
  "timezone": "Pacific/Auckland",
  "day_of_week": "Wednesday",
  "is_dst": true,
  "request_id": "abc-123",
  "service": "https://time.agentutil.net"
}
```

## Pricing

- Free tier: 10 queries/day, no authentication required
- Paid tier: $0.001/query via x402 protocol (USDC on Base)

## Privacy

No authentication required for free tier. No personal data collected. Rate limiting uses IP hashing only.
