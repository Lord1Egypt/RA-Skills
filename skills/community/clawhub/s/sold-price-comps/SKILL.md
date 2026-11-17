---
name: "sold-price-comps"
description: "Look up recent sold prices / current market comps for any product via the 3rd Place Provisions sold-prices MCP endpoint (pay-per-call, x402, no API keys)."
---

# Sold Price Comps

A pay-per-call MCP tool that answers the most common reseller question:
**"what did this sell for?"**

Point any MCP-capable agent at the public endpoint and call `sold_prices`
to get structured comps (title, price, condition, source, and sold date where
available) across categories — video games, sneakers, collectibles, electronics,
media, and more.

## Connect

Add this server to your MCP client config:

```json
{
  "mcpServers": {
    "sold-price-comps": {
      "url": "https://api.3rdplaceprovisions.com/mcp"
    }
  }
}
```

- **Transport:** streamable HTTP
- **No API keys, no signup, no prepaid balance** — pay per call via the x402 protocol.
- **x402-capable clients** (see docs.x402.org) handle payment automatically:
  the server answers with HTTP 402 + payment requirements, the agent pays via
  the facilitator, and the data unlocks.

## Tool: `sold_prices`

```
sold_prices(query: str, limit: int = 5) -> str
```

**Args:**
- `query` — product description, e.g. "Super Smash Bros Melee GameCube"
- `limit` — max comps to return (1–10)

**Returns:** JSON with `query`, `provider`, `count`, `summary` (median/low/high),
`data_type` (`sold` or `active`), `comps[]`, and `disclaimer`.

### Example call

```
sold_prices("Super Smash Bros Melee GameCube", 5)
```

### Example response (abridged)

```json
{
  "query": "Super Smash Bros Melee GameCube",
  "provider": "eBay",
  "count": 5,
  "summary": {"median": 53.99, "low": 43.28, "high": 59.95, "n": 5},
  "data_type": "active",
  "comps": [
    {
      "title": "Super Smash Bros. Melee COMPLETE - NINTENDO Gamecube",
      "price": "58.49",
      "currency": "USD",
      "sold_date": null,
      "condition": "Acceptable",
      "source": "eBay (active)",
      "url": "https://www.ebay.com/itm/..."
    }
  ],
  "disclaimer": "Live comps from eBay. Active listings = asking prices; verify condition before relying on value."
}
```

## Pricing

- **$0.05 per call** via x402 (no API keys, no signup — agents pay per call automatically).
- Free tier available for light/discovery use.

## Data notes

- **`data_type: "sold"`** = actual sold prices (source: Marketplace Insights).
- **`data_type: "active"`** = live active listings (asking prices) — still real
  market data, but not sold comps. Verify condition before relying on value.
- Every call is logged server-side; aggregate usage informs the provider's
  market-intelligence product.

## About the provider

Published by **3rd Place Provisions** (Beyond Plus Ultra Group LLC) — a
20-year quality-control veteran's take on market data: structured, QC-grade,
and honest about what the numbers do and don't say.

More: https://3rdplaceprovisions.com/pulse
