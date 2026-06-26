# Skiplagged — Flights, Hotels & Car Rentals

MCP endpoint: `https://mcp.skiplagged.com/mcp`

Skiplagged is stateless — no session ID needed after initialize.

## Setup

```bash
# Initialize (once per session)
curl -s -X POST "https://mcp.skiplagged.com/mcp" \
  -H "Content-Type: application/json" \
  -H "Accept: application/json, text/event-stream" \
  -d '{"jsonrpc":"2.0","id":1,"method":"initialize","params":{"protocolVersion":"2025-06-18","capabilities":{},"clientInfo":{"name":"openclaw","version":"1.0"}}}'
```

## Tools Overview

| Tool | Purpose |
|------|---------|
| `sk_flights_search` | Search flights between specific locations |
| `sk_destinations_anywhere` | Find cheapest destinations from departure city |
| `sk_flex_departure_calendar` | Flexible departure price calendar |
| `sk_flex_return_calendar` | Round-trip flexible calendar |
| `sk_hotels_search` | Search hotels in a city |
| `sk_hotel_details` | Room availability and pricing |
| `sk_cars_search` | Car rental search |
| `sk_resolve_iata` | City name → IATA code |
| `sk_resolve_location` | Lat/lng → nearest airport IATA |

## Important: Resolve IATA First

Before searching flights, resolve city names to IATA codes:

```bash
curl -s -X POST "https://mcp.skiplagged.com/mcp" \
  -H "Content-Type: application/json" \
  -H "Accept: application/json, text/event-stream" \
  -d '{
    "jsonrpc":"2.0","id":2,"method":"tools/call",
    "params":{"name":"sk_resolve_iata","arguments":{"input":"Rome"}}
  }'
```

Note: The parameter is `input`, not `city`.

## Flight Search

```bash
curl -s -X POST "https://mcp.skiplagged.com/mcp" \
  -H "Content-Type: application/json" \
  -H "Accept: application/json, text/event-stream" \
  -d '{
    "jsonrpc":"2.0","id":3,"method":"tools/call",
    "params":{"name":"sk_flights_search","arguments":{
      "origin":"OVD",
      "destination":"FCO",
      "depart_date":"2026-04-10",
      "cabin":"economy",
      "adults":1,
      "limit":12
    }}
  }'
```

Date format: `YYYY-MM-DD`

## Flexible Anywhere Search

When user says "where can I go cheap from Madrid?":

```bash
curl -s -X POST "https://mcp.skiplagged.com/mcp" \
  -H "Content-Type: application/json" \
  -H "Accept: application/json, text/event-stream" \
  -d '{
    "jsonrpc":"2.0","id":4,"method":"tools/call",
    "params":{"name":"sk_destinations_anywhere","arguments":{
      "origin":"MAD",
      "depart_date":"2026-04-10"
    }}
  }'
```

## Flexible Price Calendar

Find cheapest departure dates:

```bash
curl -s -X POST "https://mcp.skiplagged.com/mcp" \
  -H "Content-Type: application/json" \
  -H "Accept: application/json, text/event-stream" \
  -d '{
    "jsonrpc":"2.0","id":5,"method":"tools/call",
    "params":{"name":"sk_flex_departure_calendar","arguments":{
      "origin":"OVD",
      "destination":"FCO",
      "depart_date":"2026-04-10"
    }}
  }'
```

## Hotel Search

```bash
curl -s -X POST "https://mcp.skiplagged.com/mcp" \
  -H "Content-Type: application/json" \
  -H "Accept: application/json, text/event-stream" \
  -d '{
    "jsonrpc":"2.0","id":6,"method":"tools/call",
    "params":{"name":"sk_hotels_search","arguments":{
      "city":"Rome",
      "checkin":"2026-04-10",
      "checkout":"2026-04-14",
      "guests":2
    }}
  }'
```

## Car Rental Search

```bash
curl -s -X POST "https://mcp.skiplagged.com/mcp" \
  -H "Content-Type: application/json" \
  -H "Accept: application/json, text/event-stream" \
  -d '{
    "jsonrpc":"2.0","id":7,"method":"tools/call",
    "params":{"name":"sk_cars_search","arguments":{
      "pickup_location":"FCO",
      "pickup_date":"2026-04-10",
      "dropoff_date":"2026-04-14"
    }}
  }'
```

## Tips
- Skiplagged specializes in **hidden city fares** (cheaper tickets with strategic layovers)
- Always resolve IATA codes first with `sk_resolve_iata`
- Use `sk_destinations_anywhere` when user is flexible on destination
- Use `sk_flex_departure_calendar` when flexible on dates
- Dates must be today or later (no past searches)
- Default limit is 12 for flights
- Stateless server — no session management needed after init
