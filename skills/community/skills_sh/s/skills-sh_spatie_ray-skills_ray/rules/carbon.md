---
name: carbon
description: How to send date/time to Ray
metadata:
  tags: carbon, date, time, payload
---

## Carbon Payload

The carbon payload displays date/time information in a structured format. Named after the popular Carbon PHP library.

### When to Use

Use the carbon payload when you want to:

- Display date and time values
- Show timestamps with timezone information
- Debug date-related data

### Payload Structure

```json
{
  "type": "carbon",
  "content": {
    "formatted": "2024-01-15 14:30:00",
    "timestamp": 1705329000,
    "timezone": "UTC"
  },
  "origin": {
    "function_name": "code-agent",
    "file": "code-agent",
    "line_number": 1,
    "hostname": "my-computer"
  }
}
```

### Content Fields

- `formatted`: Human-readable date string (default format: `Y-m-d H:i:s`)
- `timestamp`: Unix timestamp (integer, seconds since epoch)
- `timezone`: Timezone name (e.g., `"UTC"`, `"America/New_York"`, `"Europe/London"`)

All fields can be `null` if the date value is not available.

### Examples

#### Current date/time

```bash
curl -X POST http://localhost:23517/ \
  -H "Content-Type: application/json" \
  -d '{"uuid":"'$(uuidgen)'","payloads":[{"type":"carbon","content":{"formatted":"'"$(date '+%Y-%m-%d %H:%M:%S')"'","timestamp":'$(date +%s)',"timezone":"'$(date +%Z)'"},"origin":{"function_name":"code-agent","file":"code-agent","line_number":1,"hostname":"'$(hostname)'"}}],"meta":{}}'
```

#### Specific date

```bash
curl -X POST http://localhost:23517/ \
  -H "Content-Type: application/json" \
  -d '{"uuid":"'$(uuidgen)'","payloads":[{"type":"carbon","content":{"formatted":"2024-12-25 00:00:00","timestamp":1735084800,"timezone":"UTC"},"origin":{"function_name":"code-agent","file":"code-agent","line_number":1,"hostname":"'$(hostname)'"}}],"meta":{}}'
```

#### With different timezone

```bash
curl -X POST http://localhost:23517/ \
  -H "Content-Type: application/json" \
  -d '{"uuid":"'$(uuidgen)'","payloads":[{"type":"carbon","content":{"formatted":"2024-01-15 09:30:00","timestamp":1705329000,"timezone":"America/New_York"},"origin":{"function_name":"code-agent","file":"code-agent","line_number":1,"hostname":"'$(hostname)'"}}],"meta":{}}'
```
