---
name: travel-search
description: "Find the best travel deals by searching and comparing flights, hotels, Airbnb stays, car rentals, and ferries across multiple providers simultaneously. Smart value scoring picks the optimal price-quality-convenience balance automatically. Plan complete trip itineraries with real prices and direct booking links. Use when: user asks about flights, travel, hotels, accommodation, Airbnb, apartments, villas, car rentals, ferry routes, trip planning, vacation planning, itinerary generation, finding cheap flights, best deals, comparing travel options, flexible dates, cheapest time to fly, price calendars, planning multi-city routes, or budget travel. Covers Kiwi.com (flights), Skiplagged (flights + hotels + cars), Trivago (hotels), Ferryhopper (ferries), optional Airbnb via local MCP, and Google Flights via fli. All primary providers are free with no API key required."
metadata: { "openclaw": { "emoji": "✈️", "requires": { "bins": ["curl"] } } }
---

# Travel Search

Search flights, hotels, car rentals, and ferries across multiple free providers via MCP protocol.

## Quick Reference

| Need | Provider | Reference |
|------|----------|-----------|
| Flights (creative routing) | Kiwi.com | [flights.md](references/flights.md) |
| Flights + Hotels + Cars | Skiplagged | [skiplagged.md](references/skiplagged.md) |
| Hotels (price comparison) | Trivago | [hotels.md](references/hotels.md) |
| Ferries | Ferryhopper | [ferries.md](references/ferries.md) |
| Flights (Google Flights) | fli | [google-flights.md](references/google-flights.md) |
| Full trip itinerary | Multi-provider | [trip-planner.md](references/trip-planner.md) |
| Best deal / price compare | Multi-provider | [price-tools.md](references/price-tools.md) |
| Airbnb / apartment stays | Airbnb MCP | [airbnb.md](references/airbnb.md) |
| Multi-city route optimizer | Multi-provider | [multi-city.md](references/multi-city.md) |
| Destination intel (weather, visa, transport) | General knowledge + wttr.in | [travel-intel.md](references/travel-intel.md) |

## How It Works

All providers use the MCP protocol (JSON-RPC 2.0 over HTTP). Call them with `curl`:

```bash
# 1. Initialize session
curl -s -X POST "$MCP_URL" \
  -H "Content-Type: application/json" \
  -H "Accept: application/json, text/event-stream" \
  -d '{"jsonrpc":"2.0","id":1,"method":"initialize","params":{"protocolVersion":"2025-06-18","capabilities":{},"clientInfo":{"name":"openclaw","version":"1.0"}}}'

# 2. Extract Mcp-Session-Id from response headers (if returned)

# 3. Call a tool
curl -s -X POST "$MCP_URL" \
  -H "Content-Type: application/json" \
  -H "Accept: application/json, text/event-stream" \
  -H "Mcp-Session-Id: $SESSION_ID" \
  -d '{"jsonrpc":"2.0","id":2,"method":"tools/call","params":{"name":"TOOL_NAME","arguments":{...}}}'
```

Response format: SSE with `event: message` + `data: {JSON}`. Parse the `data` line.

## Decision Guide

### User wants flights, hotels, cars, ferries, or trip planning
Read [price-tools.md](references/price-tools.md) for the **decision tree and comparison engine**. It covers:
- Which providers to search and when
- How to compare and score results across providers
- How to present the single best recommendation + alternatives
- Flexible dates, anywhere destinations, round-trip optimization

For full trip itineraries, also read [trip-planner.md](references/trip-planner.md). It includes a **guided intake questionnaire** (7 quick questions in one message) for when users want help figuring out what they want.

### User wants to visit multiple cities
Read [multi-city.md](references/multi-city.md) for route optimization. It finds the cheapest city order, allocates days, and handles open-jaw flights.

### Core principle
**Always search multiple providers, score results, and present ONE best recommendation** with alternatives. The user should never have to compare — that's the agent's job. See [price-tools.md](references/price-tools.md) for the value scoring system.

## Presenting Results

Use bullet lists (no markdown tables on Discord/WhatsApp). For each option show:
- Route with stops (e.g., OVD → BCN → FCO)
- Times and duration
- Price
- Booking link

Group by: 💸 Cheapest → ⚡ Fastest → 🎯 Best value

Always include booking deep links so the user can act immediately.

## Provider Endpoints

```
Kiwi:        https://mcp.kiwi.com
Skiplagged:  https://mcp.skiplagged.com/mcp
Trivago:     https://mcp.trivago.com/mcp
Ferryhopper: https://mcp.ferryhopper.com/mcp
```

## Notes
- All Tier 1 providers are free, no API key needed
- Kiwi uses `dd/mm/yyyy` date format
- Skiplagged uses `YYYY-MM-DD` date format
- Always resolve city names to IATA codes first when using Skiplagged
- Rate limit: be reasonable, don't spam requests
- MCP sessions may expire; re-initialize if you get errors
