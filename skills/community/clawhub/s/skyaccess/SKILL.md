---
name: skyaccess
description: "Private jet empty legs from SkyAccess. Search 5,000+ live empty leg flights, get charter price estimates and booking links. No account or API key. Use when the user asks about private jet flights, empty legs, private jet charter prices or booking a private jet."
version: 1.0.0
metadata:
  openclaw:
    emoji: "✈️"
    homepage: https://skyaccess.com
    requires:
      bins:
        - curl
---

# SkyAccess: private jet empty legs

SkyAccess (https://skyaccess.com) is the world's largest empty leg marketplace by listing volume: 5,000+ live empty leg flights from 900+ FAA Part 135 (and international equivalent) certified charter operators, often 25 to 75% below a comparable full charter.

This skill calls the hosted SkyAccess MCP server at `https://mcp.skyaccess.com/mcp` (Streamable HTTP, no account, no API key). It runs nothing locally except `curl`. If your agent already has the SkyAccess MCP server connected (for example through the `@skyaccess/skyaccess` plugin), call its tools directly instead.

## How to call a tool

Send one JSON-RPC `tools/call` request. The reply is a single `data:` line holding the JSON result.

```bash
curl -s https://mcp.skyaccess.com/mcp \
  -H 'content-type: application/json' \
  -H 'accept: application/json, text/event-stream' \
  -d '{"jsonrpc":"2.0","id":1,"method":"tools/call","params":{"name":"search_empty_legs","arguments":{"origin":"Los Angeles","destination":"Las Vegas","passengers":4}}}' \
  | sed -n 's/^data: //p'
```

## Tools

| Tool | Type | Arguments |
|---|---|---|
| `search_empty_legs` | Read-only | optional `origin`, `destination` (city or airport code), `departureDateFrom`, `departureDateTo` (ISO dates such as `2026-11-10`), `passengers`, `max_price` (USD). Returns up to 5 flights. |
| `get_flight` | Read-only | `flightId` from a search result. Says so when the flight is no longer available. |
| `booking_handoff` | Read-only | `flightId`. Returns the SkyAccess booking page link. |
| `get_charter_estimate` | Read-only | `origin`, `destination`, optional `passengers`, optional `aircraftCategory` (`VERY_LIGHT_JET`, `LIGHT_JET`, `MID_SIZE_JET`, `SUPER_MID_SIZE_JET`, `HEAVY_JET`, `ULTRA_LONG_RANGE`, `TURBOPROP`). Returns an indicative USD range for a full charter. |
| `request_booking` | Write | `origin`, `destination`, `departureDate`, `passengers`, `name`, `email`, optional `notes`. |

## Rules

- Prices are for the whole aircraft, in USD. Taxes and fees are shown at checkout.
- A flight with `price: null` has no published price; SkyAccess shows it as "Contact for price".
- Inventory changes all the time. Search again rather than reusing old results.
- `get_charter_estimate` is an indicative range, not a quote.
- To book, give the traveler the link from `booking_handoff`. The traveler reviews and books on the SkyAccess page.
- Call `request_booking` only when the traveler asks SkyAccess to contact them and has given their name and email. It sends those details and the trip to SkyAccess so a specialist can reply by email. It takes no payment and creates no booking.

## Data and terms

The read-only tools send only search terms (route, dates, passengers, price ceiling, flight id). `request_booking` sends the traveler's name, email, trip details and notes to SkyAccess. The skill stores nothing.

- Privacy: https://skyaccess.com/privacy#connector
- Terms: https://skyaccess.com/terms
- Source and support: https://github.com/sky-access/skyaccess-mcp (MIT), contact@skyaccess.com
