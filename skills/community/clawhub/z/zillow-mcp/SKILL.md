---
name: zillow-mcp
description: Look up real-estate listings, property details, Zestimates, saved searches/homes, and market reports on Zillow via MCP. Triggers on phrases like "find homes in", "what's the Zestimate for", "show my saved Zillow homes", "what's my saved Zillow search seeing", "what does Zillow say about", "Zillow market report for", or any request involving Zillow properties, prices, or your saved Zillow activity. Requires zillow-mcp installed and the fetchproxy extension active (see Setup below).
---

# zillow-mcp

MCP server for Zillow — natural-language access to listings, property records, Zestimates, your saved searches/homes, and market reports. Routes through your signed-in zillow.com tab via the fetchproxy browser extension, so Akamai sees a real browser session instead of a Node process.

- **npm:** [npmjs.com/package/zillow-mcp](https://www.npmjs.com/package/zillow-mcp)
- **Source:** [github.com/chrischall/zillow-mcp](https://github.com/chrischall/zillow-mcp)

> ⚠️ Zillow does not publish a public consumer API. This server uses the same private endpoints the zillow.com web app calls, dispatched through your own signed-in browser tab via the fetchproxy extension. Use at your own discretion.

## Setup

### 1. Install zillow-mcp

`.mcp.json` (project) or `~/.claude/mcp.json` (global):

```json
{
  "mcpServers": {
    "zillow": {
      "command": "npx",
      "args": ["-y", "zillow-mcp"]
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

### 3. Open zillow.com and sign in.

That's it. No API keys, no env vars.

## Tools

### Public data

- **`zillow_search_properties`** — Search by location + filters (price, beds, home type, status). Returns matching listings with price, Zestimate, beds/baths, sqft, image, and homedetails URL.
- **`zillow_get_property`** — Full property record by `zpid` or homedetails URL. Returns address, price, Zestimate, rent Zestimate, beds, baths, sqft, year built, schools, price history.
- **`zillow_get_zestimate_history`** — Time series of Zestimate values for a property.
- **`zillow_get_market_report`** — Median sale/list/rent price, days on market, inventory, ZHVI for a Zillow region (e.g. `/home-values/6181/brooklyn-ny/`).
- **`zillow_calculate_mortgage`** — Local PITI calculator. No network call. Provide home price, interest rate, optional down payment / taxes / insurance / HOA / PMI; returns a full monthly breakdown.

### Signed-in user data (the unique value vs. Bridge-API competitors)

- **`zillow_get_saved_searches`** — Your saved searches, with new-listing counts and notification frequency.
- **`zillow_get_saved_homes`** — Homes you've favorited.

## Trigger examples

- "Find me 2-bedroom condos under $1.5M in Brooklyn" → `zillow_search_properties`
- "What's the Zestimate on 123 Main St?" → resolve to zpid, then `zillow_get_property`
- "How has the Zestimate for zpid 12345 changed?" → `zillow_get_zestimate_history`
- "What's new on my saved Zillow searches?" → `zillow_get_saved_searches`
- "Pull up my saved homes on Zillow" → `zillow_get_saved_homes`
- "Brooklyn real-estate market trends" → `zillow_get_market_report`
- "Monthly payment on a $500k home, 20% down, 6.5% rate" → `zillow_calculate_mortgage`

## Gotchas

- **Sign-in required for saved-* tools.** If the user isn't signed into zillow.com in the bridged Chrome tab, those tools fail with `SessionNotAuthenticatedError`. Public tools work either way, but signed-in sessions are more reliable against captcha walls.
- **Captcha interstitial.** Zillow occasionally serves a captcha to fresh sessions. Solving it in the Chrome tab once unblocks subsequent fetches.
- **No write surface yet.** All tools are read-only. Saving a home / search / contact form are not implemented in v0.1.
