# Google Flights via fli

`fli` is a Python library that reverse-engineers Google Flights' internal API. No scraping, no browser, direct API access.

## Installation

The `fli` package must be installed separately by the user before use:

```bash
pip install flights
```

Binaries after installation: `fli` (CLI) and `fli-mcp` (MCP server)

## As MCP Server

```bash
# STDIO mode
fli-mcp

# HTTP mode (streamable)
fli-mcp-http  # serves at http://127.0.0.1:8000/mcp/
```

MCP config for Claude Code / OpenCode:
```json
{
  "mcpServers": {
    "fli": {
      "command": "fli-mcp"
    }
  }
}
```

## MCP Tools

### search_flights

| Param | Type | Required | Description |
|-------|------|----------|-------------|
| origin | string | ✅ | IATA code (e.g., 'JFK') |
| destination | string | ✅ | IATA code (e.g., 'LHR') |
| departure_date | string | ✅ | `YYYY-MM-DD` |
| return_date | string | ❌ | For round trips |
| cabin_class | string | ❌ | ECONOMY, PREMIUM_ECONOMY, BUSINESS, FIRST |
| max_stops | string | ❌ | ANY, NON_STOP, ONE_STOP, TWO_PLUS_STOPS |
| departure_window | string | ❌ | Time window `HH-HH` (e.g., '6-20') |
| airlines | list | ❌ | Filter by codes (e.g., ['BA', 'AA']) |
| sort_by | string | ❌ | CHEAPEST, DURATION, DEPARTURE_TIME, ARRIVAL_TIME |
| passengers | int | ❌ | Number of adults |

### search_dates

Find cheapest dates across a range.

| Param | Type | Required | Description |
|-------|------|----------|-------------|
| origin | string | ✅ | IATA code |
| destination | string | ✅ | IATA code |
| start_date | string | ✅ | Range start `YYYY-MM-DD` |
| end_date | string | ✅ | Range end `YYYY-MM-DD` |
| trip_duration | int | ❌ | Days (for round-trips) |
| is_round_trip | bool | ❌ | Round trip search |
| cabin_class | string | ❌ | ECONOMY, etc. |
| max_stops | string | ❌ | ANY, NON_STOP, etc. |
| sort_by_price | bool | ❌ | Sort by price |

## CLI Usage

```bash
# Basic search
fli flights JFK LHR 2026-04-25

# Advanced search
fli flights JFK LHR 2026-04-25 \
  --time 6-20 \
  --airlines BA KL \
  --class BUSINESS \
  --stops NON_STOP \
  --sort DURATION

# Cheapest dates
fli dates JFK LHR --from 2026-04-01 --to 2026-05-01

# Specific days only
fli dates JFK LHR --from 2026-04-01 --to 2026-05-01 --monday --friday
```

## When to Use fli vs Kiwi/Skiplagged

- **fli**: Widest airline coverage (Google Flights data), best for specific airline filters, non-stop searches, cabin class filtering
- **Kiwi**: Best for creative routing (mixing airlines), European budget carriers
- **Skiplagged**: Best for hidden city fares, flexible "anywhere" searches

## Tips
- Requires the user to install `flights` package separately before use
- Uses IATA codes only (not city names) — resolve first
- Google Flights has the widest coverage of any flight search
- `search_dates` is incredibly useful for flexible travelers
- Built-in rate limiting and retries
