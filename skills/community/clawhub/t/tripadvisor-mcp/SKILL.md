---
name: tripadvisor-mcp
description: TripAdvisor travel data via the Terra API through MCP. Use when the user asks to find hotels, restaurants, or attractions, look up a place's TripAdvisor rating/reviews/photos, compare places to stay or eat, or find what's near a location. Triggers on phrases like "find a hotel in", "best restaurants near", "TripAdvisor reviews for", "what's the rating of", "things to do in", or "attractions near me". Requires the @chrischall/tripadvisor-mcp package installed and the tripadvisor server registered (see Setup), plus a TripAdvisor Terra API key.
---

# tripadvisor-mcp

MCP server for the **TripAdvisor Terra API** — location search, details, photos, and reviews for hotels, restaurants, and attractions, exposed to Claude over stdio. (Terra is TripAdvisor's current API; the legacy Content API is sunset on 2026-08-31.)

- **npm:** [npmjs.com/package/@chrischall/tripadvisor-mcp](https://www.npmjs.com/package/@chrischall/tripadvisor-mcp)
- **Source:** [github.com/chrischall/tripadvisor-mcp](https://github.com/chrischall/tripadvisor-mcp)

## Setup

### Option A — npx (recommended)

Add to `.mcp.json` in your project or `~/.claude/mcp.json`:

```json
{
  "mcpServers": {
    "tripadvisor": {
      "command": "npx",
      "args": ["-y", "@chrischall/tripadvisor-mcp"],
      "env": {
        "TRIPADVISOR_API_KEY": "your-terra-api-key-here"
      }
    }
  }
}
```

Get a key at [tripadvisor.com/developers](https://www.tripadvisor.com/developers). The free **Discover** tier is pay-as-you-go (10 QPS, **10,000 calls/day**); the server caches responses in-memory to stretch it. Must be a **Terra** key — a legacy key returns 403.

### Option B — from source

```bash
git clone https://github.com/chrischall/tripadvisor-mcp
cd tripadvisor-mcp
npm install && npm run build
```

## Environment

| Var | Required | Purpose |
| --- | --- | --- |
| `TRIPADVISOR_API_KEY` | yes | Terra API key (sent as the `X-API-Key` header). A legacy key returns 403. |
| `TRIPADVISOR_CACHE_TTL` | no | Seconds to cache identical search responses (default: 300; `0` disables). |
| `TRIPADVISOR_STATIC_CACHE_TTL` | no | Longer TTL for details/photos/reviews (default: 3600; `0` disables). |

## Tools

| Tool | Use for |
| --- | --- |
| `ta_search_locations` | Find places by name — `query` required; filter with `category` (`RESTAURANT`/`ATTRACTION`/`HOTEL`), `country_code`, `geo_name`, `postal_code`, `locale`; page with `page`/`size` (max 20). `compact:true` → slim summaries. Returns matches with a location `id`. |
| `ta_search_nearby` | Find places near a center — supply **one** of: `lat`+`lon`+`radius`, `location_id`+`radius`, or a `sw_lat`/`sw_lon`/`ne_lat`/`ne_lon` box (`unit` `MI`/`KM`); filter `category`, `min_rating`, `sort` (`distance`/`rating`), `include_photo`. `compact:true` supported. |
| `ta_get_location_details` | Full listing for a location `id`: names, descriptions, address, coordinates, traveler ratings, phone, URLs. Optional `locale`. |
| `ta_get_locations` | Batch details for **multiple** ids (`ids: [..]`, 1–50) in one call — cheaper than repeated details; unknown ids are omitted. `compact:true` supported. |
| `ta_get_location_photos` | Photos (multi-size URLs, source, dimensions). Page with `page`/`size`. |
| `ta_get_location_reviews` | Traveler reviews. Page with `page`/`size`. |
| `ta_web_healthcheck` | Diagnose the optional tripadvisor.com browser-bridge connection (fetchproxy Transporter). Reports bridge role/port/timing and an actionable hint if it's not connected. |
| `ta_web_get_location` | Get a location's details (rating, review count, address, coordinates, phone, photo, URL) from its public TripAdvisor page via the browser bridge — **works without an API key**. Covers attractions/hotels/restaurants; no individual review text. |

## Workflow

1. `ta_search_locations` (or `ta_search_nearby`) to get a location `id`.
2. `ta_get_location_details` for ratings/address; `ta_get_location_reviews` and `ta_get_location_photos` for reviews and images.

Notes:
- Everything is **read-only** — Terra has no write endpoints.
- A `403`/`401` means the key isn't a valid Terra key (a legacy Content API key won't work) or its plan isn't active.
- List endpoints paginate with `page`/`size` (max 20 per page).
