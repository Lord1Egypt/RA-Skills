---
name: rollinggo-searchflight
description: Flight search and pricing via the RollingGo Flight MCP. Use when the user wants to search flights by origin, destination, date, passenger count, cabin class, city/airport code, or compare real-time flight options and prices. Trigger phrases — "search flights", "find flights", "flight price", "cheap flights", "flight comparison", "机票", "查航班", "查机票", "航班价格", "rollinggo".
homepage: https://rollinggo.store
metadata:
  {
    "openclaw": {
      "emoji": "✈️",
      "primaryMcpServer": "RollingGo-Flight-MCP",
      "requires": {
        "mcpServers": ["RollingGo-Flight-MCP"]
      },
      "mcpServers": {
        "RollingGo-Flight-MCP": {
          "url": "https://mcp.rollinggo.cn/mcp/flight",
          "type": "streamable_http"
        }
      }
    }
  }
---
# RollingGo Flight MCP

## When to Use

✅ **Use this skill when:**

- **Flight Search:** User wants to find flights between two cities or airports on a specific date.
- **Price Comparison:** User wants to compare flight prices, departure times, arrival times, direct/transit routes, or airline options.
- **City & Airport Resolution:** User provides natural language city/airport names and needs them converted into available city or airport codes.
- **One-way / Round-trip Planning:** User asks for one-way or round-trip flight options with passenger count and cabin preference.
- **Flight Option Evaluation:** User wants a short list of recommended flights based on price, timing, directness, and supplier score.

❌ **Don't use this skill when:**

- User asks about hotels, trains, car rentals, transfers, travel visas, attractions, or itinerary planning without a flight-search need.
- User asks to issue tickets, pay, cancel, refund, change flights, manage orders, confirm baggage allowance, or guarantee fare rules. Current documented MCP capability is flight search only.

## API Key

Resolution order: --api-key flag → RollingGo_API_KEY env var.
No key yet? Apply at: https://rollinggo.store/apply

## Runtime

This skill uses a remote MCP server (`streamable_http`), not a local CLI runtime. The MCP server is registered automatically by the skill host — no manual configuration or local install is needed.

Load [references/rollinggo-mcp.md](references/rollinggo-mcp.md) and keep it for the session.

No API key is required for the public endpoint.

## Version Freshness

The remote MCP endpoint is the source of truth. Do not invent local package versions or CLI commands.

Before making claims about newly added tools or booking/payment capabilities, check the latest MCP documentation or the live MCP tool list.

## Primary Workflow

Run these steps in order unless the user is already at a later step.

1. Clarify required info: origin, destination, departure date, one-way or round-trip.
   Optional (use defaults if not specified): return date (required only for round-trip), adult count (default 1), child count (default 0), cabin class (default ECONOMY), airport preference (city-level vs specific airport).
2. If origin or destination is a natural language city/airport name → run `searchAirports` first.
3. Prefer `cityCode` for broad city-level searches and `airportCode` when the user explicitly names a specific airport.
4. Run `searchFlights` with the resolved codes and passenger/cabin/date parameters.
5. Parse `flightInformationList` and compare options by price, time, directness, duration, and `fromSmartValueScore` (higher = better value).
6. If results are weak or empty → loosen filters and retry (see Filter Loosening).
7. Present 3–5 useful options and remind the user that price and inventory are real-time and subject to final confirmation.

## MCP Tools Quick Reference

`searchAirports` — resolve city or airport names to codes

```json
{ "keyword": "杭州" }
```

`searchFlights` — search available flights (one-way example)

```json
{
  "adultNumber": 1,
  "childNumber": 0,
  "cabinGrade": "ECONOMY",
  "fromCity": "HGH",
  "toCity": "CTU",
  "fromDate": "2026-05-01",
  "tripType": "ONE_WAY"
}
```

Round-trip: add `"retDate": "YYYY-MM-DD"` and set `"tripType": "ROUND_TRIP"`.
Specific airport: replace `fromCity`/`toCity` with `fromAirport`/`toAirport`.

## Key Rules

- `adultNumber` and `childNumber` are required. Use `childNumber: 0` when there are no children.
- `cabinGrade` must be one of: `ECONOMY`, `PREMIUM_ECONOMY`, `BUSINESS`, `FIRST`.
- `tripType` must be one of: `ONE_WAY`, `ROUND_TRIP`.
- `fromDate` and `retDate` must use `YYYY-MM-DD`.
- `retDate` is required when `tripType=ROUND_TRIP` and must be later than `fromDate`.
- For origin, use either `fromCity` or `fromAirport` (not both).
- For destination, use either `toCity` or `toAirport` (not both).
- If the user only says a city such as "上海" or "成都", prefer `fromCity` / `toCity` to cover multiple airports.
- If the user says a specific airport such as "虹桥", "浦东", "天府", or "萧山", prefer `fromAirport` / `toAirport`.
- Default cabin class may be `ECONOMY` when the user does not specify.
- Default passenger count may be 1 adult and 0 children when the user does not specify.
- Do not guess missing travel dates. Ask a brief follow-up unless the date is explicitly recoverable from the user's wording.

## Output

MCP response structure:

- `message`: human-readable status string (e.g. `"航班搜索成功"`)
- `flightInformationList`: array of flight options

When presenting flights, include for each option:

- total adult price and currency
- child price if children are included
- flight number
- departure and arrival time
- departure and arrival airport codes
- duration in minutes (convert to h/m for display)
- direct / transfer / stop city information (`stopCities` field; empty string means direct)
- airline or validating carrier code (`validatingCarrier`)
- `fromSmartValueScore` as a tiebreaker (0–100, higher = better value)
- short recommendation reason

Always add a note that flight prices and inventory can change in real time and final availability should be rechecked before booking.

## Filter Loosening (when no results)

Try in order: switch specific airport code to city code → try nearby airport/city matches from `searchAirports` → broaden cabin preference to `ECONOMY` only if user allows → ask whether the user can change date or time window.

If results exist but quality is low → sort by `fromSmartValueScore` descending before presenting.

## Boundary Notes

Current documented MCP capability covers airport search and flight search. Do **not** claim the skill can complete payment, issue tickets, cancel/refund/change orders, manage bookings, or verify baggage rules unless a corresponding tool is added later.
