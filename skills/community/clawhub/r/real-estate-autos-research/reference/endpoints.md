# real-estate-autos-research — endpoint reference

> Generated from `scripts/tools.json` by `scripts/generate.mjs` — do not edit by hand.

Endpoints this skill uses, grouped by platform. Call them via `scripts/crawlora.sh` (see SKILL.md).

All paths are relative to the API base `https://api.crawlora.net/api/v1` and require the header `x-api-key: $CRAWLORA_API_KEY`. Path params like `{id}` are substituted into the URL; `GET` params go in the query string; `POST` params go in a JSON body.

**28 endpoints across 6 platform group(s).**

## CarMax (7)

### `carmax_search`

- **HTTP:** `GET /carmax/search`
- **What:** Search CarMax vehicle listings. Searches CarMax for used car listings, returning vehicle summaries (make, model, trim, year, mileage, colors, engine, fuel economy, pricing, store, images), available search facets with live counts, and the total matching count.
- **Params:** `make` (string, optional) — CarMax make, e.g. honda, Toyota, BMW (case-insensitive); `max_mileage` (integer, optional) — Maximum odometer mileage; `max_price` (integer, optional) — Maximum price in US dollars; `max_year` (integer, optional) — Maximum model year; `min_price` (integer, optional) — Minimum price in US dollars; `min_year` (integer, optional) — Minimum model year; `model` (string, optional) — CarMax model, e.g. civic (case-insensitive). Does not require make; `page` (integer, optional) — 1-indexed result page, defaults to 1. CarMax returns 48 results per page; `sort` (string, optional) — Sort order: bestmatch, distance-asc, price-asc, price-desc, mileage-asc, mileage-desc, year-desc, year-asc, newarrival. Defaults to bestmatch; `zip` (string, optional) — 5-digit US ZIP code to bias results toward CarMax's nearest store

### `carmax_search_suggestions`

- **HTTP:** `GET /carmax/search/suggestions`
- **What:** Get CarMax search autocomplete suggestions. Returns autocomplete suggestions for a partial search term (make/model/trim), typo-tolerant by default.
- **Params:** `exact_match` (boolean, optional) — Disable fuzzy/typo-tolerant matching -- require an exact prefix match. Defaults to false; `search` (string, **required**) — Free-text partial search term to get autocomplete suggestions for

### `carmax_shop_by_brand`

- **HTTP:** `GET /carmax/shop-by-brand`
- **What:** Get CarMax's "shop by brand" make taxonomy. Returns CarMax's full make taxonomy for browsing by brand: every make, a display image, and CarMax's own display order.
- **Params:** _none_

### `carmax_store`

- **HTTP:** `GET /carmax/store/{id}`
- **What:** Get CarMax store (physical location) detail. Returns a CarMax store: name, full address, phone numbers, coordinates, opening hours, and store-type flags (car buying center, microstore).
- **Params:** `id` (string, **required**) — CarMax store id, the numeric path segment of a /stores/{id} URL

### `carmax_stores`

- **HTTP:** `GET /carmax/stores`
- **What:** Search CarMax store (physical location) locations. Searches CarMax's physical store locations by ZIP code or free-text keyword, returning stores with full address, every published phone number, opening hours, and (for a ZIP-based search) live driving distance in miles.
- **Params:** `keyword` (string, optional) — Free-text match against store name or city; `take` (integer, optional) — Maximum number of stores to return, defaults to 10, capped at 300; `zip` (string, optional) — 5-digit US ZIP code to search near. Triggers a live geo-distance sort. Provide this or keyword; zip takes precedence if both are given

### `carmax_vehicle`

- **HTTP:** `GET /carmax/vehicle/{stock_number}`
- **What:** Get CarMax vehicle listing detail. Returns a CarMax vehicle listing: full vehicle spec (make, model, trim, mileage, colors, engine, transmission, fuel economy, pricing), equipment features, labeled specifications, warranty coverage, accident/owner history, and CarMax's return guarantee terms.
- **Params:** `stock_number` (string, **required**) — CarMax stock number, the numeric path segment of a /car/{stock_number} URL; `store_id` (string, optional) — Optional CarMax store id for pricing/transfer-fee display context. Defaults to a fixed CarMax store when omitted

### `carmax_vehicle_recommendations`

- **HTTP:** `GET /carmax/vehicle/{stock_number}/recommendations`
- **What:** Get CarMax "similar vehicles" recommendations for a listing. Returns CarMax's own similar-vehicle recommendations for a listing: stock number, description, display mileage/price, store location, and image, for vehicles CarMax considers comparable. An empty list is a normal result, not an error.
- **Params:** `stock_number` (string, **required**) — CarMax stock number to find similar vehicles for, the numeric path segment of a /car/{stock_number} URL; `store_id` (string, **required**) — CarMax store id used as the recommendation's location context. See any search/vehicle/store response's store id field

## Redfin (5)

### `redfin_estimate`

- **HTTP:** `GET /redfin/estimate`
- **What:** Get Redfin Estimate. Returns the Redfin Estimate for a property, including the current estimate, property facts, and the monthly estimate history with city/county/postal comparatives. Faithful pass-through of Redfin's public avm + avmHistoricalData resources.
- **Params:** `property_id` (string, **required**) — Redfin property id

### `redfin_property`

- **HTTP:** `GET /redfin/property`
- **What:** Get Redfin property. Returns Redfin public property details. Provide a listing url, or a property_id (optionally with listing_id).
- **Params:** `listing_id` (string, optional) — Redfin listing id, improves completeness with property_id; `property_id` (string, optional) — Redfin property id, used when url is not provided; `url` (string, optional) — Redfin listing URL (primary key)

### `redfin_region_trends`

- **HTTP:** `GET /redfin/region-trends`
- **What:** Get Redfin region market trends. Returns Redfin's aggregate market trends for a region (median list/sale price, sale-to-list, offers, days on market, inventory, year-over-year). Faithful pass-through of Redfin's public aggregate-trends resource.
- **Params:** `region_id` (integer, **required**) — Redfin region id for a neighborhood, ZIP code, county, or city; `region_type` (integer, optional) — Redfin region type (defaults to 6, city)

### `redfin_search`

- **HTTP:** `GET /redfin/search`
- **What:** Search Redfin listings. Returns Redfin public listing search results. Pass region_id/region_type from autocomplete to skip location resolution.
- **Params:** `location` (string, optional) — Display location; resolved via autocomplete when region_id is omitted; `max_price` (integer, optional) — Maximum price filter; `min_baths` (number, optional) — Minimum bathrooms filter; `min_beds` (integer, optional) — Minimum bedrooms filter; `min_price` (integer, optional) — Minimum price filter; `page` (integer, optional) — 1-based page; `region_id` (integer, optional) — Redfin region id; skips location resolution when provided; `region_type` (integer, optional) — Redfin region type, used with region_id (defaults to 6, city); `status` (string, optional) — Listing status: for_sale or sold

### `redfin_similar`

- **HTTP:** `GET /redfin/similar`
- **What:** Get Redfin comparable listings. Returns the comparable listings Redfin shows for a property, identified by the required `property_id`. Each row has the address, city, state, zip, price, beds, baths, `sqft`, `price_per_sqft`, days on market, MLS number, `hoa_monthly`, lot size, year built, status, image and URL, plus coordinates when present.
- **Params:** `property_id` (string, **required**) — Redfin property id

## Autotrader (3)

### `autotrader_dealer`

- **HTTP:** `GET /autotrader/dealer/{id}`
- **What:** Get Autotrader dealer profile. Returns an Autotrader dealer profile (name, phone, address, rating, website) plus a first page of the dealer's own current inventory as vehicle summaries and the dealer's total listing count.
- **Params:** `id` (string, **required**) — Autotrader dealer/owner id, the numeric path segment of a /car-dealers/{id} URL

### `autotrader_search`

- **HTTP:** `GET /autotrader/search`
- **What:** Search Autotrader vehicle listings. Searches Autotrader for new and used car listings, returning vehicle summaries (make, model, trim, year, mileage, pricing, images) plus the total matching count.
- **Params:** `body_style` (string, optional) — Body style. Allowed values: convertible, coupe, hatchback, sedan, suv, truck, van, wagon; `condition` (string, optional) — Listing condition. Allowed values: new, used, certified, 3p_cert; `make` (string, optional) — Autotrader make code, e.g. TOYOTA, HONDA, BMW; `max_mileage` (integer, optional) — Maximum odometer mileage; `max_price` (integer, optional) — Maximum price in US dollars; `max_year` (integer, optional) — Maximum model year; `min_price` (integer, optional) — Minimum price in US dollars; `min_year` (integer, optional) — Minimum model year; `model` (string, optional) — Autotrader model code, e.g. CAMRY. Requires make; `page` (integer, optional) — 1-indexed result page, defaults to 1. Autotrader returns 24 results per page; `query` (string, optional) — Free-text keyword search; `radius` (integer, optional) — Search radius in miles around zip; `seller_type` (string, optional) — Seller type. Allowed values: dealer, private; `trim` (string, optional) — Autotrader trim code. Requires make and model; `zip` (string, optional) — 5-digit US ZIP code to search around

### `autotrader_vehicle`

- **HTTP:** `GET /autotrader/vehicle/{id}`
- **What:** Get Autotrader vehicle listing detail. Returns an Autotrader vehicle listing: full vehicle spec (make, model, trim, mileage, colors, transmission, fuel type, engine, images, pricing), the full listing description, and seller detail (dealership or private seller).
- **Params:** `id` (string, **required**) — Autotrader listing id, the numeric path segment of a /cars-for-sale/vehicle/{id} URL

## Zillow (3)

### `zillow_autocomplete`

- **HTTP:** `GET /zillow/autocomplete`
- **What:** Autocomplete Zillow locations. Returns Zillow autocomplete candidates, including region ids and types. Zillow autocomplete does not currently return map bounds.
- **Params:** `limit` (integer, optional) — Maximum results, clamped to 20; `query` (string, **required**) — Location query; `status` (string, optional) — Search context. Allowed values: for_sale (aliases sale, for-sale), for_rent (aliases rent, for-rent), sold

### `zillow_property`

- **HTTP:** `GET /zillow/property/{zpid}`
- **What:** Get Zillow property. Returns Zillow property details, including optional typed sections for address parts, listing attribution, pricing, history, media, facts, schools, and nearby homes when present.
- **Params:** `zpid` (string, **required**) — Zillow property id

### `zillow_search`

- **HTTP:** `GET /zillow/search`
- **What:** Search Zillow listings. Returns Zillow listing search results. Callers may pass a region id from autocomplete or a complete map bounding box. When a usable region-only response contains no listings, the API retries with a viewport from Zillow's search page if that page selects exactly the same region. Upstream blocks and transport failures return errors.
- **Params:** `east` (number, optional) — Map east bound; pass with west, south, and north; `location` (string, **required**) — Display location; `north` (number, optional) — Map north bound; pass with west, east, and south; `page` (integer, optional) — 1-based page; `region_id` (integer, optional) — Zillow region id from autocomplete, used when complete bounds are not provided; `region_type` (integer, optional) — Zillow region type from autocomplete, used with region_id fallback; `south` (number, optional) — Map south bound; pass with west, east, and north; `status` (string, optional) — Search context. Allowed values: for_sale (aliases sale, for-sale), for_rent (aliases rent, for-rent), sold; `west` (number, optional) — Map west bound; pass with east, south, and north

## Cars.com (2)

### `carsdotcom_search`

- **HTTP:** `GET /carsdotcom/search`
- **What:** Search Cars.com vehicle listings. Searches Cars.com for new and used car listings, returning vehicle summaries (make, model, trim, year, mileage, exterior color, drivetrain, fuel type, pricing, seller, images) plus the total matching count.
- **Params:** `page` (integer, optional) — 1-indexed result page, defaults to 1. Cars.com returns 24 results per page; `radius` (integer, optional) — Search radius in miles around zip; `stock_type` (string, optional) — Listing condition. Allowed values: new, used, cpo, all; `zip` (string, optional) — 5-digit US ZIP code to search around

### `carsdotcom_vehicle`

- **HTTP:** `GET /carsdotcom/vehicle/{listing_id}`
- **What:** Get Cars.com vehicle listing detail. Returns a Cars.com vehicle listing: full vehicle spec (make, model, trim, mileage, colors, engine, transmission, fuel economy, a key-specs table), Cars.com's own deal-fairness rating and predicted fair price, categorized equipment features, an AutoCheck-derived vehicle history report, Cars.com's own price-change history, the seller's notes, dealer detail (name, rating, address, website, phones, hours) or private-seller detail for a for-sale-by-owner listing, and certified-pre-owned/manufacturer-program detail when applicable.
- **Params:** `listing_id` (string, **required**) — Cars.com listing id (a UUID), the path segment of a /vehicledetail/{listing_id}/ URL

## Rightmove (8)

### `rightmove_agent_branch`

- **HTTP:** `GET /rightmove/agents/{id}`
- **What:** Get Rightmove estate agent branch details. Returns one estate-agent branch profile from Rightmove, including address, telephones, service flags, industry affiliations, and the branch's own sales and lettings listing previews. The slug segments in Rightmove agent URLs are cosmetic; the branch resolves by numeric id alone.
- **Params:** `id` (string, **required**) — Rightmove agent branch id

### `rightmove_agents`

- **HTTP:** `GET /rightmove/agents`
- **What:** List Rightmove estate agents for a location. Lists estate-agent branches from Rightmove's estate-agents directory for a location, with branch display name, brand, address, telephones, sales/lettings flags, logo, and a link to the branch profile. Pagination follows Rightmove's current directory pages, whose result counts can vary.
- **Params:** `location` (string, **required**) — Rightmove location identifier from autocomplete (numeric location id required); `page` (integer, optional) — Result page (default 1)

### `rightmove_autocomplete`

- **HTTP:** `GET /rightmove/autocomplete`
- **What:** Get Rightmove location autocomplete suggestions. Returns Rightmove location suggestions for the required `query` (up to 200 characters). `limit` defaults to 10 and is capped at 20. Each result has an `id` such as `REGION^87490`, a `name`, a `full_name` when Rightmove gives one, and an `entity_type` such as `REGION` or `POSTCODE`. Use the `id` as `location` in Rightmove search.
- **Params:** `limit` (integer, optional) — Maximum suggestions to return (default 10, max 20); `query` (string, **required**) — Location query

### `rightmove_commercial_search`

- **HTTP:** `GET /rightmove/commercial/search`
- **What:** Search Rightmove commercial property. Search Rightmove's commercial property listings for sale or to let, with price, floor-area (sq ft), and commercial-property-type filters. For to-let listings the price amount follows the listing's own frequency (monthly or yearly).
- **Params:** `location` (string, **required**) — Rightmove location identifier from autocomplete; `max_price` (integer, optional) — Maximum price in whole GBP units, not pence; `max_size` (integer, optional) — Maximum floor area in square feet; `min_price` (integer, optional) — Minimum price in whole GBP units, not pence; `min_size` (integer, optional) — Minimum floor area in square feet; `page` (integer, optional) — Result page (default 1); `property_type` (string, optional) — Commercial property type filter. Accepts one or more comma-separated values.; `status` (string, optional) — Listing status (default buy)

### `rightmove_new_homes_search`

- **HTTP:** `GET /rightmove/new-homes/search`
- **What:** Search Rightmove new homes for sale. Search Rightmove's new-homes-for-sale listings for a location, with price, bedroom, bathroom, and property-type filters. Results are individual new-build homes and plots (with development flags), not development-level cards.
- **Params:** `location` (string, **required**) — Rightmove location identifier from autocomplete; `max_bathrooms` (number, optional) — Maximum bathrooms; `max_bedrooms` (integer, optional) — Maximum bedrooms; `max_price` (integer, optional) — Maximum price in whole GBP units, not pence; `min_bathrooms` (number, optional) — Minimum bathrooms; `min_bedrooms` (integer, optional) — Minimum bedrooms; `min_price` (integer, optional) — Minimum price in whole GBP units, not pence; `page` (integer, optional) — Result page (default 1); `property_type` (string, optional) — Property type filter. Accepts one or more comma-separated values.

### `rightmove_property`

- **HTTP:** `GET /rightmove/properties/{id}`
- **What:** Get Rightmove property details. Returns one Rightmove listing by `id`: title, address, price and `price_text`, bedrooms, bathrooms, receptions, property type, status, description, features, floor plan, EPC rating, council tax band, tenure, agent reviews and nearby schools with Ofsted ratings. Removed or invalid ids return 404.
- **Params:** `id` (string, **required**) — Rightmove property ID

### `rightmove_search`

- **HTTP:** `GET /rightmove/search`
- **What:** Search Rightmove properties. Searches Rightmove listings for a required `location` id, for sale (default) or `to_let`, 1-indexed by `page`. Filter by price, bedrooms, bathrooms, `property_type`, `radius`, `must_have`, `dont_show` and `tenure_types`; `sort` defaults to `newest_listed`. Returns `total` and results with price, address, beds, baths, size and tenure.
- **Params:** `dont_show` (string, optional) — Exclude listings with these attributes. Accepts one or more comma-separated values.; `location` (string, **required**) — Rightmove location identifier from autocomplete; `max_bathrooms` (number, optional) — Maximum bathrooms; `max_bedrooms` (integer, optional) — Maximum bedrooms; `max_price` (integer, optional) — Maximum price in whole GBP units, not pence; `min_bathrooms` (number, optional) — Minimum bathrooms; `min_bedrooms` (integer, optional) — Minimum bedrooms; `min_price` (integer, optional) — Minimum price in whole GBP units, not pence; `must_have` (string, optional) — Require listings to have these attributes. Accepts one or more comma-separated values.; `page` (integer, optional) — Result page (default 1); `property_type` (string, optional) — Property type filter. Accepts one or more comma-separated values. private-halls (Student Halls) mainly returns results for status=to_let.; `radius` (number, optional) — Search radius in miles around location, default 0 (this area only); `sort` (string, optional) — Result sort order, default newest_listed; `status` (string, optional) — Listing status (default for_sale); `tenure_types` (string, optional) — Tenure filter. Accepts one or more comma-separated values.

### `rightmove_student_search`

- **HTTP:** `GET /rightmove/student/search`
- **What:** Search Rightmove student accommodation. Search Rightmove's student-accommodation listings for a location, with monthly-rent, bedroom, and furnishing filters. Prices are monthly rents in whole GBP units.
- **Params:** `furnish_type` (string, optional) — Furnishing filter; `location` (string, **required**) — Rightmove location identifier from autocomplete; `max_bedrooms` (integer, optional) — Maximum bedrooms; `max_price` (integer, optional) — Maximum monthly rent in whole GBP units, not pence; `min_bedrooms` (integer, optional) — Minimum bedrooms; `min_price` (integer, optional) — Minimum monthly rent in whole GBP units, not pence; `page` (integer, optional) — Result page (default 1)
