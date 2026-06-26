---
name: rollinggo-searchflight
description: >
  Search flights and airports using the RollingGo Flight CLI. Use this skill whenever the user
  wants to search for flights, find airport codes, check cabin availability, or plan air travel
  between cities — even if they don't explicitly say "use rollinggo-flight". Triggers include
  requests like "find me a flight", "search flights from Beijing to Shanghai", "what's the airport
  code for Hangzhou", "one-way economy to Tokyo", "round-trip business class", or any travel
  planning that involves flying. Always use this skill for flight-related queries.
homepage: https://rollinggo.store
metadata:
  {
    "openclaw": {
      "emoji": "✈️",
      "skillKey": "rollinggo-searchflight",
      "primaryEnv": "ROLLINGGO_API_KEY",
      "requires": {
        "anyBins": ["rollinggo-flight", "npx", "node", "uvx", "uv"],
        "env": ["ROLLINGGO_API_KEY"]
      },
      "install": [
        {
          "id": "node",
          "kind": "node",
          "package": "rollinggo-flight@latest",
          "bins": ["rollinggo-flight"],
          "label": "Install rollinggo-flight (npm)"
        }
      ]
    }
  }
---

# RollingGo Flight CLI

## When to Use
✅ **Use this skill when:**
- **Airport Discovery:** User needs to find airport codes or verify city/airport names before booking (e.g., "What's the airport code for Hangzhou?").
- **Flight Search:** User wants to find available flights between two destinations with specific dates, cabin class, or passenger count.
- **One-way or Round-trip:** User wants to search one-way or round-trip flights with structured filters.
- **Multi-step Planning:** User provides a natural language travel request and needs structured flight results to continue planning.

❌ **Don't use this skill when:**
- User asks about hotel booking, trains, transfers, or car rentals.
- User wants real-time seat selection or checkout — this skill returns search results only.

## API Key
Resolution order: `--api-key` flag → `ROLLINGGO_API_KEY` env var.

No key yet? Apply at: https://rollinggo.store/apply

## Runtime
Default to [references/rollinggo-flight-npx.md](references/rollinggo-flight-npx.md); switch to [references/rollinggo-flight-uvx.md](references/rollinggo-flight-uvx.md) if the user specifies `uv`/`uvx`/Python. For environments without Node.js or Python, use the standalone binary (see each reference file's Install section). For step-by-step scenarios and tutorials, see [references/flight-workflows.md](references/flight-workflows.md). For API key persistence see [references/claw-host-env.md](references/claw-host-env.md).

## Version Freshness (Always Latest)
Default policy for this skill: use the newest release on every run.

- **npm/npx:** `npx --yes rollinggo-flight@latest ...`
- **uvx:** `uvx --refresh --from rollinggo-flight@latest rollinggo-flight ...`

## Primary Workflow
Run these steps in order unless the user is already at a later step.

1. Clarify: origin city/airport, destination city/airport, departure date, trip type (ONE_WAY / ROUND_TRIP), return date (if round-trip), passenger count, cabin class
2. If city/airport codes are unclear → run `search-airports` first to resolve IATA codes
3. Run `search-flights` with resolved codes and parameters
4. If no results → loosen filters (see Filter Loosening below)

## Commands Quick Reference
```bash
# Resolve airport/city codes
rollinggo-flight search-airports --api-key <key> --keyword "Hangzhou"

# Search flights (minimum required flags)
rollinggo-flight search-flights \
  --api-key <key> \
  --from-city <code> \
  --to-city <code> \
  --from-date YYYY-MM-DD \
  --trip-type ONE_WAY \
  --adult-number 1 \
  --child-number 0 \
  --cabin-grade ECONOMY

# Discover all flags
rollinggo-flight search-airports --help
rollinggo-flight search-flights --help
```

## Key Rules
- `--trip-type` must be exactly `ONE_WAY` or `ROUND_TRIP`
- `--ret-date` is **required** when `--trip-type` is `ROUND_TRIP`
- `--cabin-grade` must be one of: `ECONOMY`, `PREMIUM_ECONOMY`, `BUSINESS`, `FIRST`
- Use either `--from-city` **or** `--from-airport` (not both); same for destination
- `--from-city` / `--to-city` accepts city codes (e.g. `BJS`, `SHA`); `--from-airport` / `--to-airport` accepts IATA airport codes (e.g. `PEK`, `PVG`)
- `--adult-number` must be ≥ 1; `--child-number` must be ≥ 0
- Dates must use `YYYY-MM-DD` format

## Output
- stdout → result payload (JSON by default)
- stderr → errors only
- Exit `0` success · `1` HTTP/network failure · `2` CLI validation failure

## Filter Loosening (when no results)
Try in order: try alternative airports in the same city → try adjacent dates → try different cabin grade → try city code instead of airport code
