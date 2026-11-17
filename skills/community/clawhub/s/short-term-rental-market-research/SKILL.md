---
name: short-term-rental-market-research
description: Compare short-term rental market supply, listing density, room mix, price distributions, and review signals using Crawlora Airbnb aggregates and selected live listings. Use for market comparisons, with explicit sampling and freshness limits rather than occupancy or revenue estimates.
---

# Short-term rental market research

Build comparable market panels from Airbnb aggregate data, with optional live
listing examples kept separate from market statistics.

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

## Build the market panel

1. Define countries/markets, geographic level, freshness cutoff, and comparison
   purpose. Discover exact country/market values through
   `/datasets/airbnb-markets/facets`; use the same filters in search and facets.
   Country values are ISO alpha-2 codes. Do not silently substitute a country
   aggregate for a missing city.
2. `/datasets/airbnb-markets/search` returns aggregate cells, never listing rows.
   `group_by` accepts `country`, `market`, `admin1`, `locality`, `room_type`, or
   `property_type`; these are alternative groupings, not independent populations
   to sum together. The enriched dimensions can remain empty until coverage is
   sufficient. Empty/suppressed cells mean unavailable evidence, not zero supply.
3. Retain listing counts, rating/review signals, badge shares, and price summaries
   with their returned units, timestamps, and coverage. `active_since` filters
   last-seen dates: it does not identify stays booked since that date. Superhost
   and Guest Favorite shares are observed lower bounds. `avg_person_capacity`
   describes the detail-enriched sample rather than every listing. Percentage fields such as `superhost_pct` are
   already percentages (31.5 means 31.5%), not fractions to multiply by 100.
4. `/datasets/airbnb-markets/items/{country}` is a country profile with metro
   context and per-currency price percentiles. Do not pass a market name as its
   country identifier. A `404` can reflect suppression. Keep native-currency
   prices separate; `price_usd` and `median_price_usd` use an approximate dated FX
   snapshot, not a current exchange quote. Do not average medians to create a
   larger market median or mix currencies into one distribution.
5. `/datasets/airbnb-markets/nearby` returns geohash-cell centroids and suppressed
   aggregate counts, not listing addresses. Compare equal radii and precision,
   with consistent country, rating, Superhost, and freshness filters. Do not sum
   overlapping radius searches or portray a cell centroid as a property location.
6. Keep pagination bounded: `page_size<=100`, `page * page_size<=10000`. Preserve
   suppression floors and returned coverage notes. Do not use repeated narrow
   queries to reconstruct suppressed cells or individual listings.

```sh
scripts/crawlora.sh /datasets/airbnb-markets/search \
  group_by=country page_size=5 sort=listings_desc
scripts/crawlora.sh /datasets/airbnb-markets/facets facet=market country=FR
# Use a discovered market in the next search; country profiles use country codes.
```

## Optional live examples

Use `/airbnb/search` for a small, explicitly sampled set in the chosen location.
Set the same future `check_in`, `check_out`, and `adults` across markets when
comparing displayed offers; resolve room IDs from results before detail/reviews.
If using map bounds, read the reference for all required coordinate parameters.
Live listings cannot be joined to aggregate cells by a dataset listing ID because
no such individual records are exposed by these dataset endpoints.

Label nightly, stay-total, fees, taxes, and currency separately when supplied.
Do not backfill aggregate missing prices from a handful of live search results.
Review snippets are samples, not a complete review history. Calendar endpoints
provide public month hints: blocked or unavailable dates can have several causes
and do not establish bookings, occupancy, ADR, RevPAR, or host revenue.

## Deliverable

Return a market comparison with geography, filter scope, observed supply, density
context, room/property mix where available, price basis and FX vintage, review
signals, collection dates, and suppression/enrichment limitations. Include example
listings separately with source URLs/IDs and dates. Explain which findings support
further research; listing density alone does not prove unmet demand, investment
returns, or that short-term rentals are legally permitted at a property.
