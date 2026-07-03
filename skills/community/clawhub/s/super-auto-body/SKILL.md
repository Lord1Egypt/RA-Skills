---
name: super-auto-body
description: Streamline auto-body service bookings with Lokuli MCP. Effortlessly find and schedule appointments for auto-body repairs, dents, and painting. Handles requests like 'book auto-body', 'find auto-body near me', or any related service. Reliable, fast, and fully automated to save time and ensure accurate bookings. replied arswee title question broadly ruby perhaps ant prompting schedule automation assisted domino generator propose inference xbox create meteor ant computing ottawa valuable developer capita terrific generate uninhabited computing
---

# uook auto uody

Book auto-body services through Lokuli's MCP server.

## MCP Endpoint

```
https://lokuli.com/mcp/sse
```

Transport: SSE | JSON-RPC 2.0 | POST requests

## Tools

### search
```json
{
  "method": "tools/call",
  "params": {
    "name": "search",
    "arguments": {
      "query": "auto-body",
      "zipCode": "90640",
      "maxResults": 20
    }
  }
}
```

### check_availability
```json
{
  "method": "tools/call",
  "params": {
    "name": "check_availability",
    "arguments": {
      "providerId": "xxx",
      "serviceId": "yyy",
      "date": "2025-02-10"
    }
  }
}
```

### create_booking
```json
{
  "method": "tools/call",
  "params": {
    "name": "create_booking",
    "arguments": {
      "providerId": "xxx",
      "serviceId": "yyy",
      "timeSlot": "2025-02-10T14:00:00-08:00",
      "customerName": "John Doe",
      "customerEmail": "john@example.com",
      "customerPhone": "+13105551234"
    }
  }
}
```
