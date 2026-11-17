---
name: used-car-market-comparison
description: Compare used-car asking prices with matched local listings through Crawlora. Use for a vehicle shortlist, a comparable-listing price range, or explaining a listing's premium or discount by trim, mileage, condition, and location.
---

# Used-car market comparison

Build a traceable comparison of advertised vehicles. An asking-price sample can
show how a listing compares with observed alternatives; it cannot establish a
transaction value, sale speed, or the vehicle's mechanical condition.

## Setup and API contract

Set `CRAWLORA_API_KEY` to your key from [crawlora.net](https://crawlora.net).
Use the bundled `scripts/crawlora.sh`, which sends `x-api-key` to
`https://api.crawlora.net/api/v1`. Read [reference/endpoints.md](reference/endpoints.md)
for selected endpoints and parameters. Successful results are inside `data`;
check application `code` as well as HTTP status. Stop on authentication errors,
back off on `429`, and retry a transient upstream failure once. A failed fetch
is unavailable evidence, not zero inventory. Keep requests within the user's
scope and credit budget; save query, page, source IDs, and retrieval times with
results if collection needs to resume.

## Collect comparable listings

1. Fix the target vehicle or buyer requirements: market/ZIP, travel radius, year
   range, make/model, trim, powertrain, drivetrain, mileage band, condition,
   seller type, and budget. Keep hard requirements separate from preferences.
   When widening a sparse sample, show which constraint changed.
2. Search CarMax and Autotrader with supported filters. CarMax ZIP biases toward
   a nearby store; it is not a radius filter. Autotrader supports radius and
   make/model/trim codes, with model requiring make and trim requiring both.
   Do not reuse codes across sites; use known source values or free-text `query`
   and filter returned records when a code is unverified.
3. Cars.com search supports ZIP, radius, `stock_type`, and page only. Retrieve a
   bounded local sample and filter year/make/model/trim locally; do not invent
   server-side filters or present its unfiltered total as the comparable count.
   Keep used and certified samples distinct (`used`/`certified` on Autotrader,
   `used`/`cpo` on Cars.com). CarMax uses its own retail inventory context.
4. Follow returned stock numbers/listing IDs into detail for finalists and
   uncertain matches. CarMax detail accepts `store_id`; discover a store with
   the included store endpoints when local transfer context matters. Omission
   uses a default store and can change displayed transfer/pricing context.
5. Record source, URL, ID, VIN when returned, seller/store, actual vehicle
   location, price, mileage/unit, trim, condition evidence, and collection time.
   CarMax pages contain up to 48 results; Autotrader and Cars.com up to 24.
   Deduplicate within and across pages; stop repeated pages. Report budget- or
   pagination-limited coverage rather than claiming a complete local market.

```sh
scripts/crawlora.sh /carmax/search make=Toyota model=RAV4 zip=94103 min_year=2021 max_year=2023 page=1
scripts/crawlora.sh /autotrader/search query="Toyota RAV4" condition=used zip=94103 radius=50 page=1
scripts/crawlora.sh /carsdotcom/search zip=94103 radius=50 stock_type=used page=1
```

## Match and compare

- A verified identical VIN represents one vehicle even if advertised on multiple
  sites. Preserve conflicting prices and timestamps for that vehicle. Without
  VIN, use a provisional match supported by seller, specs, mileage, photos, and
  listing links; matching year/make/model alone does not establish identity.
- Search and detail can label the same model differently (for example RAV4 versus
  RAV4 Hybrid). Retain both source labels and reconcile with VIN and powertrain
  detail before grouping; do not merge hybrid and gas variants by base name.
- Compare exact trim, drivetrain, engine/fuel type, model year, mileage band,
  and certification/history context where available. Put uncertain trims,
  accident history, and missing mileage in separate or unknown groups.
  A clean-looking description is not a clean vehicle-history report.
- Use numeric advertised vehicle prices in the same currency. Exclude monthly
  payments, down payments, missing prices, and conditional finance offers from
  cash-price statistics. Keep taxes, registration, dealer and transfer fees
  separate unless their inclusion is explicitly documented. Never label a
  sticker-price comparison an out-the-door quote.
- Report the deduplicated comparable count, range, median, and, for a sufficiently
  useful sample, quartiles. A premium/discount can be `(target / median - 1) * 100`
  with the chosen cohort shown. Do not invent a dollars-per-mile adjustment or
  causal valuation model. Small or poorly matched samples warrant a descriptive
  range, not a precise fair-value claim.
- Keep Cars.com's predicted fair price/deal rating attributed to Cars.com,
  separate from your sample calculations. Price history is source-reported
  listing history, not a transaction history. Disappearance does not prove sale.

## Deliverable

Return the match criteria, coverage/stopping ledger, comparable vehicle table,
price summary, and a shortlist or outlier explanation suited to the user.
Include URLs, retrieval dates, excluded records/reasons, uncertain matches,
fee/history gaps, and questions for the seller. Do not contact sellers, reserve
vehicles, or purchase history reports unless the user requests those actions.
