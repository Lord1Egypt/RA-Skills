# used-car-price-history-analysis — endpoint reference

> Generated from `scripts/tools.json` by `scripts/generate.mjs` — do not edit by hand.

Only the endpoints used by this workflow. Call them via `scripts/crawlora.sh` (see SKILL.md).

All paths are relative to the API base `https://api.crawlora.net/api/v1` and require the header `x-api-key: $CRAWLORA_API_KEY`. Path params like `{id}` are substituted into the URL; `GET` params go in the query string; `POST` params go in a JSON body.

**10 endpoints across 4 platform group(s).**

## Datasets (4)

### `datasets_vehicle_listings_facets`

- **HTTP:** `GET /datasets/vehicle-listings/facets`
- **What:** Facet vehicle listings dataset. Returns terms aggregation counts for the vehicle listings dataset. Facet enum: `source`, `make`, `model`, `trim`, `body_style`, `transmission`, `drive_type`, `fuel_type`, `seller_type`, `state`, `run_id`.
- **Params:** `body_style` (string, optional) — Exact body style filter, max 128 characters; `drive_type` (string, optional) — Exact drivetrain filter, max 128 characters; `facet` (string, **required**) — Facet enum: source, make, model, trim, body_style, transmission, drive_type, fuel_type, seller_type, state, run_id; `fuel_type` (string, optional) — Exact fuel type filter, max 128 characters; `is_price_reduced` (boolean, optional) — Filter for listings currently marked down from a previous price; `make` (string, optional) — Exact make filter, max 128 characters; `max_mileage` (integer, optional) — Maximum odometer mileage; `max_price` (number, optional) — Maximum price in US dollars; `max_year` (integer, optional) — Maximum model year; `min_price` (number, optional) — Minimum price in US dollars; `min_year` (integer, optional) — Minimum model year; `model` (string, optional) — Exact model filter, max 128 characters; `q` (string, optional) — Full-text query over make, model and trim, max 256 characters; `run_id` (string, optional) — Exact crawl run-id filter, max 128 characters; `seller_type` (string, optional) — Exact seller type filter: retailer, dealer, private; `source` (string, optional) — Exact source marketplace filter: carmax, autotrader, carsdotcom; `state` (string, optional) — Exact US state abbreviation filter, max 8 characters; `transmission` (string, optional) — Exact transmission filter, max 128 characters; `trim` (string, optional) — Exact trim filter, max 128 characters; `vin` (string, optional) — Exact VIN filter

### `datasets_vehicle_listings_item`

- **HTTP:** `GET /datasets/vehicle-listings/items/{id}`
- **What:** Get a vehicle listing from dataset. Returns one vehicle listing from the dataset by `id`, formatted `<source>:<source_listing_id>`, such as `carmax:28187774`. The record has VIN, year, make, model, trim, mileage, price and previous price, colours, drivetrain, seller, location and first and last seen times. An unknown id returns 404.
- **Params:** `id` (string, **required**) — Vehicle listing id, formatted <source>:<source_listing_id> (e.g. carmax:28187774)

### `datasets_vehicle_listings_price_history`

- **HTTP:** `GET /datasets/vehicle-listings/price-history/{id}`
- **What:** Get a vehicle listing's price history. Returns the recorded price-change events for one listing, oldest first. An event is recorded only when a crawl first observes the listing or observes a changed price -- not one entry per crawl pass -- so a listing whose price has never changed since it was first crawled returns a single entry.
- **Params:** `id` (string, **required**) — Vehicle listing id, formatted <source>:<source_listing_id> (e.g. carmax:28187774)

### `datasets_vehicle_listings_search`

- **HTTP:** `GET /datasets/vehicle-listings/search`
- **What:** Search vehicle listings dataset. Searches the crawled used-vehicle listings index. source enum: `carmax`, `autotrader`, `carsdotcom`. CarMax's own national inventory is fully enumerable (re-crawled on a standing schedule); Autotrader/Cars.com coverage is a best-effort zip-code sweep, not exhaustive, and their rows approximate city/state from the searched area rather than the seller's exact location. seller_type enum: `retailer`, `dealer`, `private` (not populated for every row -- see the dataset markdown). Sort enum: `relevance`, `recently_updated`, `newly_listed`, `price_asc`, `price_desc`, `mileage_asc`, `mileage_desc`, `year_desc`, `year_asc`. Billing: this search costs 1 credit per record returned, with a minimum of 2 (an empty result costs 2, a full page of 100 costs 100).
- **Params:** `body_style` (string, optional) — Exact body style filter (e.g. Sedan, SUV), max 128 characters; `drive_type` (string, optional) — Exact drivetrain filter, max 128 characters; `fuel_type` (string, optional) — Exact fuel type filter (e.g. Gas, Hybrid, Electric), max 128 characters; `is_price_reduced` (boolean, optional) — Filter for listings currently marked down from a previous price; `make` (string, optional) — Exact make filter (e.g. Honda, Toyota), max 128 characters; `max_mileage` (integer, optional) — Maximum odometer mileage; `max_price` (number, optional) — Maximum price in US dollars; `max_year` (integer, optional) — Maximum model year; `min_price` (number, optional) — Minimum price in US dollars; `min_year` (integer, optional) — Minimum model year; `model` (string, optional) — Exact model filter (e.g. Civic), max 128 characters; `page` (integer, optional) — Page number, defaults to 1; `page_size` (integer, optional) — Page size, defaults to 20 and maxes at 100; page * page_size must be <= 10000; `q` (string, optional) — Full-text query over make, model and trim, max 256 characters; `run_id` (string, optional) — Exact crawl run-id filter, max 128 characters; `seller_type` (string, optional) — Exact seller type filter: retailer, dealer, private; `sort` (string, optional) — Sort enum: relevance, recently_updated, newly_listed, price_asc, price_desc, mileage_asc, mileage_desc, year_desc, year_asc; `source` (string, optional) — Exact source marketplace filter: carmax, autotrader, carsdotcom; `state` (string, optional) — Exact US state abbreviation filter (e.g. CA), max 8 characters; `transmission` (string, optional) — Exact transmission filter, max 128 characters; `trim` (string, optional) — Exact trim filter, max 128 characters; `vin` (string, optional) — Exact VIN filter. Best-effort: not guaranteed on every listing

## CarMax (2)

### `carmax_search`

- **HTTP:** `GET /carmax/search`
- **What:** Search CarMax vehicle listings. Searches CarMax for used car listings, returning vehicle summaries (make, model, trim, year, mileage, colors, engine, fuel economy, pricing, store, images), available search facets with live counts, and the total matching count.
- **Params:** `make` (string, optional) — CarMax make, e.g. honda, Toyota, BMW (case-insensitive); `max_mileage` (integer, optional) — Maximum odometer mileage; `max_price` (integer, optional) — Maximum price in US dollars; `max_year` (integer, optional) — Maximum model year; `min_price` (integer, optional) — Minimum price in US dollars; `min_year` (integer, optional) — Minimum model year; `model` (string, optional) — CarMax model, e.g. civic (case-insensitive). Does not require make; `page` (integer, optional) — 1-indexed result page, defaults to 1. CarMax returns 48 results per page; `sort` (string, optional) — Sort order: bestmatch, distance-asc, price-asc, price-desc, mileage-asc, mileage-desc, year-desc, year-asc, newarrival. Defaults to bestmatch; `zip` (string, optional) — 5-digit US ZIP code to bias results toward CarMax's nearest store

### `carmax_vehicle`

- **HTTP:** `GET /carmax/vehicle/{stock_number}`
- **What:** Get CarMax vehicle listing detail. Returns a CarMax vehicle listing: full vehicle spec (make, model, trim, mileage, colors, engine, transmission, fuel economy, pricing), equipment features, labeled specifications, warranty coverage, accident/owner history, and CarMax's return guarantee terms.
- **Params:** `stock_number` (string, **required**) — CarMax stock number, the numeric path segment of a /car/{stock_number} URL; `store_id` (string, optional) — Optional CarMax store id for pricing/transfer-fee display context. Defaults to a fixed CarMax store when omitted

## Autotrader (2)

### `autotrader_search`

- **HTTP:** `GET /autotrader/search`
- **What:** Search Autotrader vehicle listings. Searches Autotrader for new and used car listings, returning vehicle summaries (make, model, trim, year, mileage, pricing, images) plus the total matching count.
- **Params:** `body_style` (string, optional) — Body style. Allowed values: convertible, coupe, hatchback, sedan, suv, truck, van, wagon; `condition` (string, optional) — Listing condition. Allowed values: new, used, certified, 3p_cert; `make` (string, optional) — Autotrader make code, e.g. TOYOTA, HONDA, BMW; `max_mileage` (integer, optional) — Maximum odometer mileage; `max_price` (integer, optional) — Maximum price in US dollars; `max_year` (integer, optional) — Maximum model year; `min_price` (integer, optional) — Minimum price in US dollars; `min_year` (integer, optional) — Minimum model year; `model` (string, optional) — Autotrader model code, e.g. CAMRY. Requires make; `page` (integer, optional) — 1-indexed result page, defaults to 1. Autotrader returns 24 results per page; `query` (string, optional) — Free-text keyword search; `radius` (integer, optional) — Search radius in miles around zip; `seller_type` (string, optional) — Seller type. Allowed values: dealer, private; `trim` (string, optional) — Autotrader trim code. Requires make and model; `zip` (string, optional) — 5-digit US ZIP code to search around

### `autotrader_vehicle`

- **HTTP:** `GET /autotrader/vehicle/{id}`
- **What:** Get Autotrader vehicle listing detail. Returns an Autotrader vehicle listing: full vehicle spec (make, model, trim, mileage, colors, transmission, fuel type, engine, images, pricing), the full listing description, and seller detail (dealership or private seller).
- **Params:** `id` (string, **required**) — Autotrader listing id, the numeric path segment of a /cars-for-sale/vehicle/{id} URL

## Cars.com (2)

### `carsdotcom_search`

- **HTTP:** `GET /carsdotcom/search`
- **What:** Search Cars.com vehicle listings. Searches Cars.com for new and used car listings, returning vehicle summaries (make, model, trim, year, mileage, exterior color, drivetrain, fuel type, pricing, seller, images) plus the total matching count.
- **Params:** `page` (integer, optional) — 1-indexed result page, defaults to 1. Cars.com returns 24 results per page; `radius` (integer, optional) — Search radius in miles around zip; `stock_type` (string, optional) — Listing condition. Allowed values: new, used, cpo, all; `zip` (string, optional) — 5-digit US ZIP code to search around

### `carsdotcom_vehicle`

- **HTTP:** `GET /carsdotcom/vehicle/{listing_id}`
- **What:** Get Cars.com vehicle listing detail. Returns a Cars.com vehicle listing: full vehicle spec (make, model, trim, mileage, colors, engine, transmission, fuel economy, a key-specs table), Cars.com's own deal-fairness rating and predicted fair price, categorized equipment features, an AutoCheck-derived vehicle history report, Cars.com's own price-change history, the seller's notes, dealer detail (name, rating, address, website, phones, hours) or private-seller detail for a for-sale-by-owner listing, and certified-pre-owned/manufacturer-program detail when applicable.
- **Params:** `listing_id` (string, **required**) — Cars.com listing id (a UUID), the path segment of a /vehicledetail/{listing_id}/ URL
