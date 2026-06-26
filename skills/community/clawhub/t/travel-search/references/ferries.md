# Ferryhopper — Ferry Search

MCP endpoint: `https://mcp.ferryhopper.com/mcp`

Covers 33 countries and 190+ ferry operators.

## Setup

```bash
# Initialize and capture session
curl -s -X POST "https://mcp.ferryhopper.com/mcp" \
  -H "Content-Type: application/json" \
  -H "Accept: application/json, text/event-stream" \
  -D /tmp/ferry-headers.txt \
  -d '{"jsonrpc":"2.0","id":1,"method":"initialize","params":{"protocolVersion":"2025-06-18","capabilities":{},"clientInfo":{"name":"openclaw","version":"1.0"}}}'

SESSION=$(grep -i "mcp-session-id:" /tmp/ferry-headers.txt | awk '{print $2}' | tr -d '\r')
```

## Tools

### get_ports

List available ports and their details. Use to find port IDs.

```bash
curl -s -X POST "https://mcp.ferryhopper.com/mcp" \
  -H "Content-Type: application/json" \
  -H "Accept: application/json, text/event-stream" \
  -H "Mcp-Session-Id: $SESSION" \
  -d '{"jsonrpc":"2.0","id":2,"method":"tools/call",
    "params":{"name":"get_ports","arguments":{}}}'
```

### get_direct_connections_for_ports

Find which ports have direct ferry connections.

```bash
curl -s -X POST "https://mcp.ferryhopper.com/mcp" \
  -H "Content-Type: application/json" \
  -H "Accept: application/json, text/event-stream" \
  -H "Mcp-Session-Id: $SESSION" \
  -d '{"jsonrpc":"2.0","id":3,"method":"tools/call",
    "params":{"name":"get_direct_connections_for_ports","arguments":{
      "portId":"PIRAEUS"
    }}}'
```

### search_trips

Search available ferry trips between two ports on a specific date.

```bash
curl -s -X POST "https://mcp.ferryhopper.com/mcp" \
  -H "Content-Type: application/json" \
  -H "Accept: application/json, text/event-stream" \
  -H "Mcp-Session-Id: $SESSION" \
  -d '{"jsonrpc":"2.0","id":4,"method":"tools/call",
    "params":{"name":"search_trips","arguments":{
      "originPortId":"PIRAEUS",
      "destinationPortId":"SANTORINI",
      "date":"2026-07-15"
    }}}'
```

## Common Routes
- Greek Islands (Piraeus → Santorini, Mykonos, Crete, etc.)
- Italy (Naples → Capri, Sicily, Sardinia)
- Spain (Barcelona → Balearic Islands)
- Croatia (Split → Hvar, Dubrovnik ferries)
- Scandinavia (Stockholm → Helsinki, Tallinn)
- UK (Dover → Calais)

## Tips
- Get port IDs first with `get_ports`
- Check connections with `get_direct_connections_for_ports` before searching trips
- Date format: `YYYY-MM-DD`
- Ferry is often cheaper and more scenic for island routes
- Consider ferry + flight combos for Greek island hopping
