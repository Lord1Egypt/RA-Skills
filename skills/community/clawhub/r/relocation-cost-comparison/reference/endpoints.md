# relocation-cost-comparison — endpoint reference

> Generated from `scripts/tools.json` by `scripts/generate.mjs` — do not edit by hand.

Only the endpoints used by this workflow. Call them via `scripts/crawlora.sh` (see SKILL.md).

All paths are relative to the API base `https://api.crawlora.net/api/v1` and require the header `x-api-key: $CRAWLORA_API_KEY`. Path params like `{id}` are substituted into the URL; `GET` params go in the query string; `POST` params go in a JSON body.

**7 endpoints across 2 platform group(s).**

## Numbeo (4)

### `numbeo_cost_of_living_city`

- **HTTP:** `GET /numbeo/cost-of-living/city/{slug}`
- **What:** Get a Numbeo city's cost-of-living prices. Returns itemized cost-of-living prices for one city (restaurants, markets, transportation, utilities, rent, and more), grouped by category.
- **Params:** `slug` (string, **required**) — Numbeo city slug

### `numbeo_cost_of_living_country`

- **HTTP:** `GET /numbeo/cost-of-living/country`
- **What:** Get a Numbeo country's cost-of-living prices. Returns aggregate itemized cost-of-living prices for a country, plus the headline cost-of-living indices for every city Numbeo tracks there.
- **Params:** `country` (string, **required**) — Country name as Numbeo spells it

### `numbeo_cost_of_living_rankings`

- **HTTP:** `GET /numbeo/cost-of-living/rankings`
- **What:** Get the global Numbeo cost-of-living city ranking. Returns the global cost-of-living city ranking (Cost of Living, Rent, Cost of Living Plus Rent, Groceries, Restaurant Price, and Local Purchasing Power indices), either the continuously-updated current index or a historical periodic snapshot.
- **Params:** `period` (string, optional) — Required when scope=historical, e.g. 2026-mid or 2025; `scope` (string, optional) — current (default) or historical

### `numbeo_cost_of_living_rankings_by_country`

- **HTTP:** `GET /numbeo/cost-of-living/rankings-by-country`
- **What:** Get the global Numbeo cost-of-living country ranking. Returns the global country-level cost-of-living ranking (Cost of Living, Rent, Cost of Living Plus Rent, Groceries, Restaurant Price, and Local Purchasing Power indices).
- **Params:** _none_

## Datasets (3)

### `datasets_housing_markets_facets`

- **HTTP:** `GET /datasets/housing-markets/facets`
- **What:** Facet the US housing markets dataset. Returns terms aggregation counts for the housing markets dataset. Facet enum: `region_type`, `state_code`, `property_type`, `parent_metro`, `parent_metro_code`, `income_vintage`, `is_latest`, `period_begin`. region_type enum: `national`, `metro`, `county`, `city`, `zip`. property_type enum: `All Residential`, `Single Family Residential`, `Condo/Co-op`, `Townhouse`, `Multi-Family (2-4 Unit)`, `Single Units Only`.
- **Params:** `facet` (string, **required**) — Facet enum: region_type, state_code, property_type, parent_metro, parent_metro_code, income_vintage, is_latest, period_begin; `latest` (boolean, optional) — Filter for the most recent period per region and property type; `max_inventory` (integer, optional) — Maximum active inventory; `max_median_dom` (number, optional) — Maximum median days on market; `max_median_list_price` (number, optional) — Maximum median list price in USD; `max_median_sale_price` (number, optional) — Maximum median sale price in USD; `max_price_to_income` (number, optional) — Maximum price-to-income ratio; `max_salary_to_buy` (integer, optional) — Maximum salary needed to buy in USD per year; `min_homes_sold` (integer, optional) — Minimum homes sold in the period; `min_inventory` (integer, optional) — Minimum active inventory; `min_median_dom` (number, optional) — Minimum median days on market; `min_median_list_price` (number, optional) — Minimum median list price in USD; `min_median_sale_price` (number, optional) — Minimum median sale price in USD; `min_price_to_income` (number, optional) — Minimum price-to-income ratio; `min_salary_to_buy` (integer, optional) — Minimum salary needed to buy in USD per year; `parent_metro_code` (string, optional) — Exact parent metro (CBSA) code filter, e.g. 16980; `period` (string, optional) — Exact period start date filter, YYYY-MM-DD; `property_type` (string, optional) — Property type enum: All Residential, Single Family Residential, Condo/Co-op, Townhouse, Multi-Family (2-4 Unit), Single Units Only; `q` (string, optional) — Full-text query over region name and city, max 256 characters; `region_type` (string, optional) — Region level enum: national, metro, county, city, zip; `state_code` (string, optional) — Exact two-letter state code filter, e.g. CA; `zip_code` (string, optional) — Exact zip code filter (zip-level rows only), e.g. 60616

### `datasets_housing_markets_item`

- **HTTP:** `GET /datasets/housing-markets/items/{region_type}/{table_id}`
- **What:** Get a US housing market record from the dataset. Returns one housing-market record by region_type and Redfin table_id from dataset id enum value `housing-markets`. region_type enum: `national`, `metro`, `county`, `city`, `zip`. property_type enum: `All Residential`, `Single Family Residential`, `Condo/Co-op`, `Townhouse`, `Multi-Family (2-4 Unit)`, `Single Units Only` (defaults to `All Residential`). `period` defaults to the most recent period on record. Pass `history=true` to get the full monthly series (a `{dataset, region_type, table_id, property_type, items}` envelope, sorted by period ascending) instead of a single record.
- **Params:** `history` (boolean, optional) — Return the full monthly series instead of a single period; `period` (string, optional) — Exact period start date, YYYY-MM-DD; defaults to the latest period; `property_type` (string, optional) — Property type enum: All Residential, Single Family Residential, Condo/Co-op, Townhouse, Multi-Family (2-4 Unit), Single Units Only; defaults to All Residential; `region_type` (string, **required**) — Region level enum: national, metro, county, city, zip; `table_id` (integer, **required**) — Redfin table id (the region's stable numeric id)

### `datasets_housing_markets_search`

- **HTTP:** `GET /datasets/housing-markets/search`
- **What:** Search the US housing markets dataset. Searches monthly Redfin housing-market statistics per region and property type since 2012, joined to Census ACS income for affordability metrics. region_type enum: `national`, `metro`, `county`, `city`, `zip`. property_type enum: `All Residential`, `Single Family Residential`, `Condo/Co-op`, `Townhouse`, `Multi-Family (2-4 Unit)`, `Single Units Only`. Sort enum: `relevance`, `price_desc`, `price_asc`, `list_price_desc`, `list_price_asc`, `price_to_income_desc`, `price_to_income_asc`, `salary_to_buy_desc`, `salary_to_buy_asc`, `dom_asc`, `dom_desc`, `inventory_desc`, `homes_sold_desc`, `period_desc`. Use `latest=true` for the most recent period per region series. Billing: this search costs 1 credit per record returned, with a minimum of 2 (an empty result costs 2, a full page of 100 costs 100).
- **Params:** `latest` (boolean, optional) — Filter for the most recent period per region and property type; `max_inventory` (integer, optional) — Maximum active inventory; `max_median_dom` (number, optional) — Maximum median days on market; `max_median_list_price` (number, optional) — Maximum median list price in USD; `max_median_sale_price` (number, optional) — Maximum median sale price in USD; `max_price_to_income` (number, optional) — Maximum price-to-income ratio; `max_salary_to_buy` (integer, optional) — Maximum salary needed to buy in USD per year; `min_homes_sold` (integer, optional) — Minimum homes sold in the period; `min_inventory` (integer, optional) — Minimum active inventory; `min_median_dom` (number, optional) — Minimum median days on market; `min_median_list_price` (number, optional) — Minimum median list price in USD; `min_median_sale_price` (number, optional) — Minimum median sale price in USD; `min_price_to_income` (number, optional) — Minimum price-to-income ratio; `min_salary_to_buy` (integer, optional) — Minimum salary needed to buy in USD per year; `page` (integer, optional) — Page number, defaults to 1; `page_size` (integer, optional) — Page size, defaults to 20 and maxes at 100; page * page_size must be <= 10000; `parent_metro_code` (string, optional) — Exact parent metro (CBSA) code filter, e.g. 16980; `period` (string, optional) — Exact period start date filter, YYYY-MM-DD; `property_type` (string, optional) — Property type enum: All Residential, Single Family Residential, Condo/Co-op, Townhouse, Multi-Family (2-4 Unit), Single Units Only; `q` (string, optional) — Full-text query over region name and city, max 256 characters; `region_type` (string, optional) — Region level enum: national, metro, county, city, zip; `sort` (string, optional) — Sort enum: relevance, price_desc, price_asc, list_price_desc, list_price_asc, price_to_income_desc, price_to_income_asc, salary_to_buy_desc, salary_to_buy_asc, dom_asc, dom_desc, inventory_desc, homes_sold_desc, period_desc; `state_code` (string, optional) — Exact two-letter state code filter, e.g. CA; `zip_code` (string, optional) — Exact zip code filter (zip-level rows only), e.g. 60616
