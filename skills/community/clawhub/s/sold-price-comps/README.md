# sold-price-comps

A pay-per-call MCP server for the most common reseller question: **"what did this sell for?"**

Point any MCP-capable agent at the public endpoint, call `sold_prices`, and get
structured comps — title, price, condition, source, and sold date where available —
across categories: video games, sneakers, collectibles, electronics, media, and more.

## Features

- **No API keys, no signup, no prepaid balance** — pay per call via x402.
- **$0.05/call** (free tier available for discovery).
- **QC-grade structure** — median/low/high summary, condition, source labeling,
  and honest `data_type` (`sold` vs `active`) so agents never confuse asking
  prices with sold comps.
- **Live eBay data** as of Aug 2026; true sold-price comps (Marketplace Insights)
  auto-enabled once approved.

## Connect

```json
{
  "mcpServers": {
    "sold-price-comps": {
      "url": "https://api.3rdplaceprovisions.com/mcp"
    }
  }
}
```

x402-capable clients (see docs.x402.org) handle payment automatically:
the server answers with HTTP 402 + payment requirements, the agent pays via the
facilitator, and the data unlocks.

## Usage

```
sold_prices(query: str, limit: int = 5) -> str
```

See [SKILL.md](SKILL.md) for the full tool contract and example response.
See [examples/](examples/) for request/response samples.

## Pricing

- **$0.05 per call** via x402.
- Free tier for light/discovery use.

## About

Published by **3rd Place Provisions** (Beyond Plus Ultra Group LLC) — market
data with a 20-year quality-control standard: inspect, judge, document.
More at https://3rdplaceprovisions.com/pulse
