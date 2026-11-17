---
name: viator-mcp
description: Search Viator tours, activities and experiences via MCP. Use when the user asks to find tours, activities, excursions, day trips, tickets, or "things to do" in a city or destination, get details/pricing/availability for a Viator product, list attractions in a destination, or convert supplier-currency prices. Triggers on phrases like "things to do in Rome", "find a food tour in Paris", "is this tour available in September", "Viator", "book an excursion" (search only — no booking), or "skip-the-line Colosseum tickets". Requires the @chrischall/viator-mcp package installed and the viator server registered (see Setup), plus a Viator Partner API key (free Basic Access affiliate tier).
---

# viator-mcp

MCP server for the **Viator Partner API** (v2, Basic Access affiliate tier) — search the
Viator catalog of 300k+ tours, activities and experiences, get product details, availability
schedules and pricing, browse attractions and destinations, all over stdio. Read-only: this
tier cannot make bookings; every product result carries a `productUrl` for booking on viator.com.

- **npm:** [npmjs.com/package/@chrischall/viator-mcp](https://www.npmjs.com/package/@chrischall/viator-mcp)
- **Source:** [github.com/chrischall/viator-mcp](https://github.com/chrischall/viator-mcp)

## Setup

### Option A — npx (recommended)

Add to `.mcp.json` in your project or `~/.claude/mcp.json`:

```json
{
  "mcpServers": {
    "viator": {
      "command": "npx",
      "args": ["-y", "@chrischall/viator-mcp"],
      "env": {
        "VIATOR_API_KEY": "your-viator-partner-api-key"
      }
    }
  }
}
```

Get a key by signing up as a Viator affiliate at
[partnerresources.viator.com](https://partnerresources.viator.com/) — the Basic Access tier is free.

### Option B — from source

```bash
git clone https://github.com/chrischall/viator-mcp
cd viator-mcp
npm install && npm run build
```

Then point `.mcp.json` at `dist/index.js` with `VIATOR_API_KEY` in `env`.

## Workflow

1. **Find the destination id** — `vt_search_freetext` with `search_types: ["DESTINATIONS"]`
   (or `vt_list_destinations` for the full taxonomy).
2. **Search products** — `vt_search_products` with the destination id plus filters
   (price, dates, rating, duration, tags via `vt_list_product_tags`, flags like
   `FREE_CANCELLATION`). Results are already slim while browsing — see
   [Response shape](#response-shape).
3. **Drill in** — `vt_get_product` for full details; `vt_get_availability_schedule` for
   seasons/start times/pricing (supplier currency — convert with `vt_get_exchange_rates`).
4. **Attractions** — `vt_search_attractions` / `vt_get_attraction` for landmark-centric
   browsing; each attraction lists its mapped product codes.

## Tools

| Area | Tools |
| --- | --- |
| Products | `vt_search_products`, `vt_get_product`, `vt_list_product_tags` |
| Search | `vt_search_freetext` |
| Attractions | `vt_search_attractions`, `vt_get_attraction` |
| Availability | `vt_get_availability_schedule` |
| Reference | `vt_list_destinations`, `vt_get_locations`, `vt_get_exchange_rates` |
| Health | `vt_healthcheck` — is this connector working? Reports whether VIATOR_API_KEY resolved, whether Viator accepted it, and what to fix. Start here when another tool fails: an empty result can mean "no products" or "never authenticated". |

## Response shape

Every read tool — all ten of them — takes `view: "compact" | "full"`, and
**`compact` is the default**, so the smaller payload is what you get without
asking for it. Pass `view: "full"` for Viator's untouched record.

What `compact` *does* differs by tool, because only two of them have a field
projection written against Viator's documented shapes:

- `vt_search_products` and `vt_search_freetext` project each ProductSummary down
  to its product code, title, from-price and currency, rating, review count,
  duration, confirmation type, flags, booking URL and cover image — and nothing
  else. (`vt_search_freetext` projects only its PRODUCTS block; its attraction
  and destination results are media-stripped instead.) If Viator's shape drifts,
  the projection falls back to the raw response, media-stripped, rather than
  emitting an empty one.
- The other eight — `vt_get_product`, `vt_list_product_tags`,
  `vt_search_attractions`, `vt_get_attraction`, `vt_get_availability_schedule`,
  `vt_list_destinations`, `vt_get_locations` and `vt_get_exchange_rates` — strip
  image and avatar URLs and do nothing else. Every other field comes back as
  Viator sent it.

`vt_healthcheck` takes no `view`: it reports a verdict it assembles itself, not
a Viator payload, and a rung that cannot change anything is worse than no
parameter.

(This replaced an opt-in `compact: true` flag. Passing `compact` now does
nothing — zod drops the unknown key and you get the compact rung regardless,
which is what the flag used to ask for.)

## In context groups

This server joins the **travel** group (mcp-host context groups; every tool except
`vt_healthcheck` carries a `_meta.mint` hint, all of them `lookup`).

- **No canonical read.** Viator's affiliate tier is a public catalogue — it holds no
  bookings, no itinerary and nothing of the person's own — so it answers no *what's new*,
  *what's due* or *what's on* ask, and the group does not fan one out to it. It has no
  subjects either: the catalogue's destinations are not the person's.
- **Where it helps:** an ask that names a place, like "what's on our trip this weekend,
  and are there any food tours in Lisbon?" — the group answers the trip from the other
  travel sources, and the tour half is a `vt_search_products` (or `vt_search_freetext`)
  lookup, whose hint names `start_date`/`end_date` so a spoken range fills them.
- **No browser needed:** the upstream is a keyed REST API, so this source never answers
  "needs your browser open".

## Notes

- Prices from `vt_search_products`/`vt_search_freetext` are in the requested `currency`;
  prices from `vt_get_availability_schedule` are in the **supplier's** currency.
- Viator rate-limits per endpoint on a rolling 10s window; the server caches identical
  reads (`VIATOR_CACHE_TTL`, default 60s) and retries once honoring `Retry-After`.
- Booking URLs (`productUrl`, `attractionUrl`) must be used verbatim for affiliate
  attribution; pass `campaign_value` to tag them.
