---
name: restaurant-menu-benchmarking
description: Compare restaurant menu breadth, matched dishes, bundles, and location-specific prices with the Crawlora API. Use for restaurant competitor benchmarks or comparisons of direct, pickup, and delivery menus in a defined market.
---

# Restaurant menu benchmarking

Build a matched menu comparison for specified branches, dishes, and order modes.
The output is a benchmark with evidence and unmatched items, not an order.

## Setup and API contract

Set `CRAWLORA_API_KEY` to your key from [crawlora.net](https://crawlora.net).
Run the bundled `scripts/crawlora.sh` from this skill directory or by absolute
path. It sends `x-api-key` to `https://api.crawlora.net/api/v1`; keep the key in
the environment. Read [reference/endpoints.md](reference/endpoints.md) for the
selected endpoints, required parameters, limits, and response behavior.
Check the application `code` as well as HTTP status; successful payloads are
inside `data`. Stop on `401`/`403`, back off on `429`, and retry a transient
`5xx` once. A failed or partial fetch is not an empty market or catalog.
Bound requests to the user's scope and credit budget. For repeated collection,
save the query, source IDs, pagination progress, and retrieval timestamps with
the results so interrupted work can resume; do not create monitors implicitly.

## Collect comparable menus

1. Define the city or coordinates, restaurant branches, meal/daypart, currency,
   collection window, and order mode. Compare the same branch across channels
   before attributing a difference to a platform. A chain name alone is not a
   branch match: verify address and location using store metadata.
2. Discover DoorDash stores with `/doordash/search` and Uber Eats stores with
   `/ubereats/search`. DoorDash search is a pickup catalog; do not label its
   prices as delivery quotes. Its store and menu calls both need the same
   `latitude` and `longitude`. Uber Eats IDs are `storeUuid` values from search;
   they are not DoorDash numeric IDs. Keep platform IDs separate.
3. Use `/chipotle/restaurants` to resolve a nearby `restaurant_number`, then
   `/chipotle/restaurant/menu` for its priced menu. Preserve its dine-in and
   delivery price pair, including customization charges. `/chipotle/menu` is
   national taxonomy and customization context only: omitted prices are unknown,
   never zero. `include_unavailable=true` can distinguish menu presence from
   current availability on the restaurant endpoint.
4. For national menu breadth, discover McDonald's categories for one `country`
   and pass that same country and returned category slug to `/mcdonalds/menu`.
   This surface has no prices. Compare its item coverage, not invented prices.
   National catalogs and branch menus describe different scopes.

```sh
scripts/crawlora.sh /chipotle/restaurants \
  latitude=37.7749 longitude=-122.4194 page_size=3
# Take restaurant_number from discovery before fetching /chipotle/restaurant/menu.
scripts/crawlora.sh /mcdonalds/categories country=us
scripts/crawlora.sh /doordash/search \
  query=Chipotle latitude=37.7749 longitude=-122.4194
```

## Match and calculate

- Retain original names and descriptions. Match dish, protein/filling, size,
  item count, included sides/drink, and required modifiers. Mark exact matches,
  comparable alternatives, and unmatched items separately; do not force a combo
  meal and a standalone entree into one price comparison.
- Preserve displayed currency and price units. Inspect actual payload fields
  before converting minor units; an integer alone does not prove cents. A missing
  price is null. A free modifier is not evidence that the base dish is free.
- For exact matches, report absolute difference and `(comparison - baseline) /
  baseline * 100`, only with a positive priced baseline. Use per-item or per-size
  prices only when quantities and units are known and comparable.
- Separate regular, promotional, membership, and starting prices. Menu prices
  exclude any fees, taxes, tips, and minimum-order effects not explicitly returned.
  Do not call their sum a final checkout total. Preserve availability flags.
- Count unique menu items separately from modifiers and bundles. Deduplicate items
  repeated in several menu sections without collapsing genuinely different sizes.

## Deliverable

Return a table with branch/address, source and collection time, order mode,
original item, matched item, portion/bundle contents, currency, price, availability,
match confidence, and price difference. Include a coverage summary with fetched
branches/sections and missing sources. Summarize price positioning and menu gaps
as hypotheses; popularity, margins, sales volume, and customer demand are not
established by menu presence. Link original URLs when returned and retain IDs and
API request paths when no public item URL is supplied.
