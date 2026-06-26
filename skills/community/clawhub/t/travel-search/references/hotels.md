# Trivago — Hotel & Accommodation Search

MCP endpoint: `https://mcp.trivago.com/mcp`

## Setup

```bash
# Initialize and capture session
curl -s -X POST "https://mcp.trivago.com/mcp" \
  -H "Content-Type: application/json" \
  -H "Accept: application/json, text/event-stream" \
  -D /tmp/trivago-headers.txt \
  -d '{"jsonrpc":"2.0","id":1,"method":"initialize","params":{"protocolVersion":"2025-06-18","capabilities":{},"clientInfo":{"name":"openclaw","version":"1.0"}}}'

SESSION=$(grep -i "mcp-session-id:" /tmp/trivago-headers.txt | awk '{print $2}' | tr -d '\r')
```

## Tools

### trivago-accommodation-search

Search hotels by destination name.

```bash
curl -s -X POST "https://mcp.trivago.com/mcp" \
  -H "Content-Type: application/json" \
  -H "Accept: application/json, text/event-stream" \
  -H "Mcp-Session-Id: $SESSION" \
  -d '{
    "jsonrpc":"2.0","id":2,"method":"tools/call",
    "params":{"name":"trivago-accommodation-search","arguments":{
      "query":"Rome",
      "checkin":"2026-04-10",
      "checkout":"2026-04-14",
      "adults":2,
      "rooms":1
    }}
  }'
```

### trivago-accommodation-radius-search

Search hotels near specific coordinates.

```bash
curl -s -X POST "https://mcp.trivago.com/mcp" \
  -H "Content-Type: application/json" \
  -H "Accept: application/json, text/event-stream" \
  -H "Mcp-Session-Id: $SESSION" \
  -d '{
    "jsonrpc":"2.0","id":3,"method":"tools/call",
    "params":{"name":"trivago-accommodation-radius-search","arguments":{
      "latitude":41.9028,
      "longitude":12.4964,
      "radius":5000,
      "checkin":"2026-04-10",
      "checkout":"2026-04-14",
      "adults":2
    }}
  }'
```

### trivago-search-suggestions

Get location suggestions for autocomplete.

```bash
curl -s -X POST "https://mcp.trivago.com/mcp" \
  -H "Content-Type: application/json" \
  -H "Accept: application/json, text/event-stream" \
  -H "Mcp-Session-Id: $SESSION" \
  -d '{
    "jsonrpc":"2.0","id":4,"method":"tools/call",
    "params":{"name":"trivago-search-suggestions","arguments":{
      "query":"Rome"
    }}
  }'
```

## Tips
- Trivago compares prices across multiple booking sites (Booking.com, Expedia, Hotels.com, etc.)
- Use `trivago-search-suggestions` first if unsure about exact location name
- Use radius search for "hotels near X landmark" queries
- Session required — initialize first and keep session ID
- Good for price comparison when user wants the best hotel deal
