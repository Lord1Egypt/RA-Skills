---
name: used-car-price-history-analysis
description: Analyze observed used-car listing price changes through Crawlora stored vehicle histories and selected live listings. Use for a dated price-change ledger, matched comparable vehicles, or evaluating an advertised reduction with listing identity and crawl coverage preserved.
---

# Used-car price history analysis

## Access and scope

Set `CRAWLORA_API_KEY` to your Crawlora key. Prefer the listed Crawlora MCP tools
when connected; otherwise use the bundled `scripts/crawlora.sh`, which sends
`x-api-key` to `https://api.crawlora.net/api/v1`. Read
[reference/endpoints.md](reference/endpoints.md) for exact methods and parameters.
Check application `code` as well as HTTP status; payloads are inside `data`.
Stop on authentication errors, back off on `429`, and retry a transient upstream
failure once. Bound requests by the requested scope and credit budget. Preserve
source IDs, URLs, source dates, and retrieval/crawl times separately.

Explain observed asking-price changes for a listing or matched vehicle cohort.
Establish source, geography, make/model/year/trim, mileage/condition constraints,
observation window, and price basis before collecting comparable records.

## Resolve listings and their recorded events

1. Discover accepted source/make/model/trim filters through dataset facets, then
   search with a bounded page budget. Stored sources are `carmax`, `autotrader`,
   and `carsdotcom`. CarMax inventory is enumerable; the other two are best-effort
   ZIP sweeps whose geocoded area can approximate the search location rather than
   the seller's address. Keep those coverage differences visible.
2. Copy returned IDs in `<source>:<source_listing_id>` format into item/history
   routes. A VIN is a vehicle identity lead, not the dataset listing ID. Different
   sellers or relistings of the same VIN remain separate listing histories unless
   dates and seller evidence establish an explicit linkage.
3. Price history records the first observed price and observed changes, not a
   row for every crawl/day. Cars.com may include backfilled native price-history
   events, bounded by enrichment coverage. Keep `snapshot_date` separate from
   `crawled_at`: a backfilled event predates the crawl that obtained it.
4. An empty history means no indexed history was returned; one row means one
   recorded price, not proof the price never changed before observation began.
   Preserve event IDs/schema version and anomalous or duplicate dates for review.
5. Refresh selected listings through their source's live detail route when needed,
   resolving that route's own ID/URL from listing evidence. A failed or missing
   listing is unavailable evidence, not proof the car sold or a seller accepted
   a lower price. Do not substitute another vehicle with a similar title.

```sh
scripts/crawlora.sh /datasets/vehicle-listings/facets facet=source
scripts/crawlora.sh /datasets/vehicle-listings/search make=Toyota model=Camry source=carmax page=1 page_size=10
# Select an actual returned listing ID before:
# scripts/crawlora.sh "/datasets/vehicle-listings/price-history/$LISTING_ID"
```

## Calculate comparable changes

For comparable positive prices, show `change = later − earlier` and
`percent change = change / earlier × 100`, with both observed dates. Keep
increases, reductions, and missing/invalid price values separate. Do not label
a first-observed price as original MSRP or a price reduction as a negotiated
saving. Do not interpolate daily prices or time-at-price beyond observed events.

Match year/trim/drivetrain, mileage, seller type, condition and accident/owner
history when supplied, region, currency, and fees before comparing vehicles.
Unknown attributes remain unknown. Report cohort sample size and distinct listing
counts; two histories for one VIN are not automatically two independent vehicles.
Return the price-event ledger, matched-comparable table, coverage/freshness notes,
current-versus-stored discrepancies, and questions to verify with the seller.
A research request does not authorise contacting dealers or purchasing a vehicle.
