# Kiwi.com — Flight Search

MCP endpoint: `https://mcp.kiwi.com`

## Setup

```bash
# Initialize session (required first)
INIT=$(curl -s -X POST "https://mcp.kiwi.com" \
  -H "Content-Type: application/json" \
  -H "Accept: application/json, text/event-stream" \
  -D /tmp/kiwi-headers.txt \
  -d '{"jsonrpc":"2.0","id":1,"method":"initialize","params":{"protocolVersion":"2025-06-18","capabilities":{},"clientInfo":{"name":"openclaw","version":"1.0"}}}')

# Extract session ID
SESSION=$(grep -i "mcp-session-id:" /tmp/kiwi-headers.txt | awk '{print $2}' | tr -d '\r')
```

## Tool: search-flight

Search for flights between two locations.

### Parameters

| Param | Type | Required | Description |
|-------|------|----------|-------------|
| flyFrom | string | ✅ | City name or airport code |
| flyTo | string | ✅ | City name or airport code |
| departureDate | string | ✅ | `dd/mm/yyyy` format |
| departureDateFlexRange | int | ❌ | 0-3 days flexibility |
| returnDate | string | ❌ | `dd/mm/yyyy` for round trip |
| returnDateFlexRange | int | ❌ | 0-3 days flexibility |
| passengers | object | ❌ | `{"adults":1,"children":0,"infants":0}` |
| cabinClass | string | ❌ | M (economy), W (premium), C (business), F (first) |
| sort | string | ❌ | price, duration, quality, date |
| curr | string | ❌ | EUR, USD, GBP, etc. |
| locale | string | ❌ | en, es, de, fr, etc. |

### Example: One-way flight

```bash
curl -s -X POST "https://mcp.kiwi.com" \
  -H "Content-Type: application/json" \
  -H "Accept: application/json, text/event-stream" \
  -H "Mcp-Session-Id: $SESSION" \
  -d '{
    "jsonrpc":"2.0","id":2,"method":"tools/call",
    "params":{"name":"search-flight","arguments":{
      "flyFrom":"Oviedo",
      "flyTo":"Rome",
      "departureDate":"10/04/2026",
      "sort":"price",
      "curr":"EUR"
    }}
  }'
```

### Example: Round trip with flexibility

```bash
curl -s -X POST "https://mcp.kiwi.com" \
  -H "Content-Type: application/json" \
  -H "Accept: application/json, text/event-stream" \
  -H "Mcp-Session-Id: $SESSION" \
  -d '{
    "jsonrpc":"2.0","id":3,"method":"tools/call",
    "params":{"name":"search-flight","arguments":{
      "flyFrom":"Madrid",
      "flyTo":"Tokyo",
      "departureDate":"15/05/2026",
      "departureDateFlexRange":3,
      "returnDate":"30/05/2026",
      "returnDateFlexRange":3,
      "cabinClass":"C",
      "sort":"price",
      "curr":"EUR"
    }}
  }'
```

### Response Structure

Each flight in the response array:

```json
{
  "flyFrom": "OVD",
  "flyTo": "FCO",
  "cityFrom": "Asturias",
  "cityTo": "Rome",
  "departure": { "utc": "...", "local": "..." },
  "arrival": { "utc": "...", "local": "..." },
  "totalDurationInSeconds": 21000,
  "price": 66,
  "deepLink": "https://on.kiwi.com/...",
  "currency": "EUR",
  "layovers": [
    {
      "at": "AGP",
      "city": "Málaga",
      "arrival": { "utc": "...", "local": "..." },
      "departure": { "utc": "...", "local": "..." }
    }
  ]
}
```

### Tips
- Kiwi excels at **creative routing** — combining different airlines for cheaper fares
- Use city names (not just IATA codes) — Kiwi resolves them automatically
- Set `departureDateFlexRange: 3` to find cheaper nearby dates
- Always use `sort: "price"` unless user specifically wants fastest
