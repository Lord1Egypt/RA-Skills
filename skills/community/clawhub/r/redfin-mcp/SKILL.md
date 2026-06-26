---
name: redfin-mcp
description: Look up real-estate listings, property details, market reports, and your saved homes/searches on Redfin via MCP. Triggers on phrases like "find homes on redfin in", "redfin property details for", "show my saved redfin homes", "what's my saved redfin search seeing", "what does redfin say about", "redfin market report for", or any request involving Redfin properties, prices, or your saved Redfin activity. Requires redfin-mcp installed and the fetchproxy extension active (see Setup below).
---

# redfin-mcp

MCP server for Redfin — natural-language access to listings, property records, market reports, and your saved homes/searches. Routes through your signed-in redfin.com tab via the fetchproxy browser extension, so AWS WAF / DataDome see a real browser session instead of a Node process.

- **npm:** [npmjs.com/package/redfin-mcp](https://www.npmjs.com/package/redfin-mcp)
- **Source:** [github.com/chrischall/redfin-mcp](https://github.com/chrischall/redfin-mcp)

> ⚠️ Redfin does not publish a public consumer API. This server uses the same private `/stingray/...` endpoints the redfin.com web app calls, dispatched through your own signed-in browser tab via the fetchproxy extension. Use at your own discretion.

## Setup

### 1. Install redfin-mcp

`.mcp.json` (project) or `~/.claude/mcp.json` (global):

```json
{
  "mcpServers": {
    "redfin": {
      "command": "npx",
      "args": ["-y", "redfin-mcp"]
    }
  }
}
```

### 2. Install the fetchproxy extension (one-time, shared across all fetchproxy-based MCPs)

```bash
git clone https://github.com/chrischall/fetchproxy
cd fetchproxy
npm ci
npm --workspace=@fetchproxy/extension-chrome run build
```

Then in Chrome: `chrome://extensions` → Developer mode → Load unpacked → pick `packages/extension-chrome/dist/`.

### 3. Open redfin.com and sign in.

That's it. No API keys, no env vars.

## Tools

### Public data

- **`redfin_search_properties`** — Search by location + filters (price, beds/baths min, home type). Resolves the location via Redfin's autocomplete then queries the `/stingray/api/gis` endpoint. Returns matching listings with price, beds/baths, sqft, year built, address, and the Redfin home URL.
- **`redfin_get_property`** — Full property record by `url` (Redfin homedetails URL or path), `property_id` alone (resolved internally by following Redfin's `/home/<id>` redirect to the canonical slug, then `initialInfo`), or `property_id` + `listing_id` (fastest — skips resolution). Two-round-trip API: `initialInfo` resolves the URL to IDs, then `aboveTheFold` fetches the data. Returns address, beds/baths, sqft, year built, price, status, days on market, primary photo.
- **`redfin_get_market_report`** — Median sale/list prices, price per sqft, days on market, year-over-year change, homes sold/on market for a Redfin region. Provide either `location` (free-text) or `region_id` + `region_type`. All metrics returned as formatted strings (e.g. `"$870K"`, `"+2.4%"`).
- **`redfin_calculate_mortgage`** — Local PITI calculator. No network call. Provide home price, interest rate, optional down payment / taxes / insurance / HOA / PMI; returns a full monthly breakdown.

### Signed-in user data (the unique value vs. paid scrapers)

- **`redfin_get_saved_homes`** — Your favorited homes, flattened across all collections. Returns address, price, beds/baths, status.
- **`redfin_get_saved_searches`** — Your saved searches with region URLs and display text.

## Trigger examples

- "Find me 2-bedroom condos under $1.5M in Brooklyn on Redfin" → `redfin_search_properties`
- "What does Redfin say about 42 Monroe St in Brooklyn?" → `redfin_get_property`
- "Pull up my favorited homes on Redfin" → `redfin_get_saved_homes`
- "What's new on my saved Redfin searches?" → `redfin_get_saved_searches`
- "Brooklyn housing market trends on Redfin" → `redfin_get_market_report`
- "Monthly payment on a $500k home, 20% down, 6.5% rate" → `redfin_calculate_mortgage`

## Gotchas

- **Sign-in required for saved-* tools.** If the user isn't signed into redfin.com in the bridged Chrome tab, those tools fail with `SessionNotAuthenticatedError`. Public tools work either way.
- **AWS WAF challenge.** Redfin occasionally serves a WAF challenge to fresh sessions. Solving it in the Chrome tab once unblocks subsequent fetches.
- **No write surface yet.** All tools are read-only. Saving a home / search / contact form are not implemented in v0.1.
- **`for_rent` / `sold` listing statuses** map to entirely different Redfin URL paths (`/apartments-for-rent/...`, `/recently-sold`). v0.1 of `redfin_search_properties` supports `for_sale` only.
- **No equivalent to Zillow's Zestimate history tool.** Redfin's Redfin Estimate is exposed as a current scalar inside `redfin_get_property`; there's no historical-series endpoint yet.
