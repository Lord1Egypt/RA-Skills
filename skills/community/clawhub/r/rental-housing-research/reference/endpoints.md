# rental-housing-research — endpoint reference

> Generated from `scripts/tools.json` by `scripts/generate.mjs` — do not edit by hand.

Only the endpoints used by this workflow. Call them via `scripts/crawlora.sh` (see SKILL.md).

All paths are relative to the API base `https://api.crawlora.net/api/v1` and require the header `x-api-key: $CRAWLORA_API_KEY`. Path params like `{id}` are substituted into the URL; `GET` params go in the query string; `POST` params go in a JSON body.

**22 endpoints across 2 platform group(s).**

## Greystar (11)

### `greystar_article`

- **HTTP:** `GET /greystar/articles/{section}/{slug}`
- **What:** Get a Greystar renter guide or blog post. Retrieves one Greystar renter guide or blog post: title, description, category, publish date (blog posts), lead image, and the body as ordered heading, paragraph, and list blocks. Get section and slug values from /greystar/articles.
- **Params:** `section` (string, **required**) — Content section; `slug` (string, **required**) — Article slug from /greystar/articles

### `greystar_articles`

- **HTTP:** `GET /greystar/articles`
- **What:** List Greystar renter guides and blog posts. Lists Greystar's renter guides (applying and leasing, general guides, moving) and blog posts from its public sitemap, newest first. Entries carry the section, slug, URL and last-modified date; fetch /greystar/articles/{section}/{slug} for the title and body.
- **Params:** `page` (integer, optional) — 1-based page; `per_page` (integer, optional) — Entries per page, 1-100; `query` (string, optional) — Text matched against the slug; `section` (string, optional) — Content section

### `greystar_location`

- **HTTP:** `GET /greystar/location`
- **What:** Get a Greystar rental hub page. Retrieves one Greystar state, city, or neighborhood rental hub: title, description, editorial guide text as ordered blocks, child locations with summaries, communities listed on the page (id, name, address, and price text when shown), and FAQs. State, city, and neighborhood slugs must come from /greystar/locations; unknown values return 400.
- **Params:** `city` (string, optional) — City slug from /greystar/locations; `neighborhood` (string, optional) — Neighborhood slug from /greystar/locations; requires city; `state` (string, **required**) — State slug from /greystar/locations, e.g. tx

### `greystar_locations`

- **HTTP:** `GET /greystar/locations`
- **What:** List Greystar rental hub locations. Lists Greystar's state, city, and neighborhood rental hub pages (the site's own location tree) with slugs and URLs. Use the slugs with /greystar/location for a hub's editorial content, child locations, listed communities, and FAQs.
- **Params:** `city` (string, optional) — City slug from this list; requires state; `level` (string, optional) — Hub level; `page` (integer, optional) — 1-based page; `per_page` (integer, optional) — Entries per page, 1-200; `state` (string, optional) — State slug from this list, e.g. tx

### `greystar_markets`

- **HTTP:** `GET /greystar/markets`
- **What:** List Greystar markets, neighborhoods, cities, and states. Returns every value accepted by the /greystar/search market_area, neighborhood, city, state, and country_code filters, each with the number of communities currently published. Derived from the full live community list, so it is the complete value space.
- **Params:** _none_

### `greystar_newsroom`

- **HTTP:** `GET /greystar/newsroom`
- **What:** List Greystar newsroom releases. Lists Greystar corporate newsroom releases and news articles from its public sitemap, newest first, with slug, URL and last-modified date. Fetch /greystar/newsroom/{slug} for the title, date, and body.
- **Params:** `page` (integer, optional) — 1-based page; `per_page` (integer, optional) — Entries per page, 1-100; `query` (string, optional) — Text matched against the slug

### `greystar_newsroom_article`

- **HTTP:** `GET /greystar/newsroom/{slug}`
- **What:** Get a Greystar newsroom release. Retrieves one Greystar newsroom release: title, type (for example Press Release), publish date, lead image, and body paragraphs. Older news stubs carry only a title and date, so the body can be empty. Get slugs from /greystar/newsroom.
- **Params:** `slug` (string, **required**) — Newsroom slug from /greystar/newsroom

### `greystar_property`

- **HTTP:** `GET /greystar/properties/{id}`
- **What:** Get a Greystar apartment community. Retrieves a public Greystar community profile by its numeric property id: location, description, amenities, office hours, walk scores, tours, floor plans, published fees, and currently available units with starting prices and available dates. Get ids from /greystar/search.
- **Params:** `id` (string, **required**) — Numeric Greystar property id, e.g. 10124

### `greystar_search`

- **HTTP:** `GET /greystar/search`
- **What:** Search Greystar apartment communities. Lists Greystar communities published on greystar.com, optionally filtered by market area, neighborhood, city, state, country, starting rent, or free text. Filter values must come from /greystar/markets; an unknown value returns 400. Starting prices reflect each community's published minimum and are null when none is published. Results come from an hourly snapshot of every community listed on greystar.com; the default order follows the site.
- **Params:** `city` (string, optional) — Exact city from /greystar/markets; `country_code` (string, optional) — ISO country code from /greystar/markets, e.g. US; `market_area` (string, optional) — Exact market area from /greystar/markets, e.g. Greater Austin; `max_price` (number, optional) — Maximum starting monthly rent; excludes communities with no published price; `min_price` (number, optional) — Minimum starting monthly rent; excludes communities with no published price; `neighborhood` (string, optional) — Exact neighborhood from /greystar/markets; `page` (integer, optional) — 1-based page; `per_page` (integer, optional) — Results per page, 1-100; `query` (string, optional) — Free-text match on name, address, city, neighborhood, market area, or postal code (max 160 characters); `sort` (string, optional) — Result order; relevance keeps the site's own order; `state` (string, optional) — State or region abbreviation from /greystar/markets, e.g. TX

### `greystar_unit_locations`

- **HTTP:** `GET /greystar/unit-locations`
- **What:** List Greystar unit search locations. Lists every location accepted by /greystar/units: the nationwide us listing, states, metros, cities, and neighborhoods (nested ones carry their parent), taken from the site's own search pages. Locations Greystar has no unit listing for are dropped once detected.
- **Params:** `query` (string, optional) — Text matched against the location slug, e.g. austin

### `greystar_units`

- **HTTP:** `GET /greystar/units`
- **What:** Search available Greystar apartment units. Searches apartment units currently available to rent on greystar.com within one location (nationwide by default), filtered by bedrooms, bathrooms, building type, community highlights, and monthly price, sorted by relevance or price. Results are grouped by community: each carries its address, coordinates, the number of matching units, and up to about 100 units with unit number, floor plan, bedrooms, bathrooms, price range, and lease term. The response also returns filter counts for the location. Several values of one filter match any of them. Get location values from /greystar/unit-locations.
- **Params:** `bathrooms` (array, optional) — Bathroom count; repeat for several; `bedrooms` (array, optional) — Bedroom count; repeat for several (0 is studio); `building_type` (array, optional) — Building type; repeat for several; `highlights` (array, optional) — Community highlight; repeat for several (matches any); `location` (string, optional) — Search location slug from /greystar/unit-locations, e.g. austin-tx, texas or greater-austin/round-rock; `max_price` (number, optional) — Maximum monthly unit price; `min_price` (number, optional) — Minimum monthly unit price; `page` (integer, optional) — 1-based page; `per_page` (integer, optional) — Communities per page, 1-100; `sort` (string, optional) — Result order

## StreetEasy (11)

### `streeteasy_areas`

- **HTTP:** `GET /streeteasy/areas`
- **What:** List StreetEasy search areas. Lists StreetEasy's search area hierarchy: NYC and NJ roots, boroughs, neighborhoods and sub-neighborhoods. Each area has an `id`, `parentId`, `level`, `name` and `short` name. Use an `id` as a repeated `area_id` in `/streeteasy/rentals/search`. The list was 349 options on 2026-09-29 and can change.
- **Params:** _none_

### `streeteasy_building`

- **HTTP:** `GET /streeteasy/buildings/{slug}`
- **What:** Get StreetEasy building details. Retrieves public building facts, location, description, policies, amenities, and available sale/rental listing cards from StreetEasy's server-rendered building page. Pass the building slug from a StreetEasy /building/{slug} URL.
- **Params:** `slug` (string, **required**) — StreetEasy building slug

### `streeteasy_market_data_catalog`

- **HTTP:** `GET /streeteasy/market-data/catalog`
- **What:** List StreetEasy dashboard metric datasets. Lists the 63 monthly metrics selectable in StreetEasy's Data Dashboard. Each has an `id`, display `label`, a sales or rentals `type`, a `bedrooms` segment and a `property_type`. Pass an `id` to `streeteasy-market-data-series` to get that metric's data. Takes no parameters.
- **Params:** _none_

### `streeteasy_market_data_series`

- **HTTP:** `GET /streeteasy/market-data/series`
- **What:** Get one StreetEasy monthly market metric. Returns a public dashboard metric for every published area. Obtain the complete dataset ID set and its labels/dimensions from streeteasy-market-data-catalog. Defaults to the latest 12 months and limits requests to 36 months.
- **Params:** `dataset` (string, **required**) — StreetEasy dashboard dataset ID; `end_month` (string, optional) — Last month, inclusive, in YYYY-MM format; defaults to the latest available month; `start_month` (string, optional) — First month, inclusive, in YYYY-MM format

### `streeteasy_market_indices`

- **HTTP:** `GET /streeteasy/market-data/indices`
- **What:** Get StreetEasy monthly market indices. Returns public sale-price and rent index values by dashboard area. The datasets have different historical start dates; missing values are omitted. Defaults to the latest 12 months and limits each request to 36 months.
- **Params:** `end_month` (string, optional) — Last month, inclusive, in YYYY-MM format; defaults to the latest available month; `start_month` (string, optional) — First month, inclusive, in YYYY-MM format

### `streeteasy_market_inventory`

- **HTTP:** `GET /streeteasy/market-data/inventory`
- **What:** Get StreetEasy monthly market inventory. Returns monthly sales and rental inventory counts for every area in StreetEasy's public Data Dashboard. Defaults to the latest 12 available months; each request is limited to 36 months.
- **Params:** `end_month` (string, optional) — Last month, inclusive, in YYYY-MM format; defaults to the latest available month; `start_month` (string, optional) — First month, inclusive, in YYYY-MM format

### `streeteasy_quick_search`

- **HTTP:** `GET /streeteasy/quick-search`
- **What:** Search StreetEasy across public result types. Searches StreetEasy's public quick-search page and returns its rendered neighborhood, building, complex, school, agent, and recorded-sale groups. Recorded-sale entries are a limited anonymous preview when the page requires registration to see the remaining matches.
- **Params:** `query` (string, **required**) — Free-text StreetEasy quick-search query (1-160 characters)

### `streeteasy_rentals_search`

- **HTTP:** `GET /streeteasy/rentals/search`
- **What:** Search StreetEasy rental listings. Searches active StreetEasy rentals in one or more areas with the public site's price, room, building, amenity, pet, open-house, tour, transit, and sort filters. Obtain valid area IDs from /streeteasy/areas.
- **Params:** `amenity` (array, optional) — Required amenity; repeat for multiple; `area_id` (array, **required**) — StreetEasy area ID from /streeteasy/areas; repeat for multiple areas; `building_type` (array, optional) — Building type; repeat for multiple; `max_bathrooms` (number, optional) — Maximum bathrooms; `max_bedrooms` (integer, optional) — Maximum bedrooms; `max_price` (integer, optional) — Maximum monthly rent; `max_sqft` (integer, optional) — Maximum square footage; `min_bathrooms` (number, optional) — Minimum bathrooms; `min_bedrooms` (integer, optional) — Minimum bedrooms; zero means studio; `min_price` (integer, optional) — Minimum monthly rent; `min_sqft` (integer, optional) — Minimum square footage; `open_house` (boolean, optional) — Require an open house within the next seven days; `optional_amenity` (array, optional) — Preferred amenity; results may omit these. Repeat for multiple.; `page` (integer, optional) — 1-based result page; `per_page` (integer, optional) — Results per page, 1-500; `pets_allowed` (boolean, optional) — Require listings that allow pets; `sort` (string, optional) — Result order; `tour_3d` (boolean, optional) — Require a 3D tour; `transit_line` (array, optional) — Nearby transit line; repeat for multiple; `video_tour` (boolean, optional) — Require a video tour

### `streeteasy_sales_search`

- **HTTP:** `GET /streeteasy/sales/search`
- **What:** Search StreetEasy sale listings. Searches public sale listings with location, status, sale type, price, bedroom, bathroom, square-footage, carrying cost, building age, school, ZIP, keyword, building type, amenity, pet, open-house, virtual-tour, transit, and sort filters. Obtain area IDs from /streeteasy/areas. When sale_status is omitted, active, preview, and coming_soon listings are included.
- **Params:** `amenity` (array, optional) — Amenity filter; repeat for multiple; `area_id` (array, **required**) — StreetEasy area ID from /streeteasy/areas; repeat for multiple areas; `building_type` (array, optional) — Building type; `development` (string, optional) — New development filter; `include_unknown_price_per_sqft` (boolean, optional) — Include listings with unknown price per square foot; `income_restricted` (boolean, optional) — Set true to select income-restricted homes; `keywords` (string, optional) — Listing-description keyword filter; `max_bathrooms` (number, optional) — Maximum bathrooms; `max_bedrooms` (integer, optional) — Maximum bedrooms; `max_maintenance` (integer, optional) — Maximum monthly maintenance fee; `max_monthly_taxes` (integer, optional) — Maximum monthly property taxes; `max_price` (integer, optional) — Maximum sale price; `max_price_per_sqft` (integer, optional) — Maximum price per square foot; `max_sqft` (integer, optional) — Maximum square footage; `max_year_built` (integer, optional) — Maximum building year built; `min_bathrooms` (number, optional) — Minimum bathrooms; `min_bedrooms` (integer, optional) — Minimum bedrooms; zero means studio; `min_maintenance` (integer, optional) — Minimum monthly maintenance fee; `min_monthly_taxes` (integer, optional) — Minimum monthly property taxes; `min_price` (integer, optional) — Minimum sale price; `min_price_per_sqft` (integer, optional) — Minimum price per square foot; `min_sqft` (integer, optional) — Minimum square footage; `min_year_built` (integer, optional) — Minimum building year built; `open_house` (boolean, optional) — Require open house within the next seven days; `optional_amenity` (array, optional) — Nice-to-have amenity; results may omit these. Repeat for multiple.; `page` (integer, optional) — 1-based result page; `per_page` (integer, optional) — Results per page, 1-500; `pets_allowed` (boolean, optional) — Require pets allowed; `prewar` (boolean, optional) — Set true to select prewar buildings; `sale_status` (array, optional) — Sale status; repeat for multiple. Defaults to active, preview, and coming_soon.; `sale_type` (array, optional) — Sale type; repeat for multiple.; `school_id` (array, optional) — StreetEasy school ID selected by the public search UI; repeat for multiple schools; `sort` (string, optional) — default, newest, recently_updated, price_desc, price_asc, largest, or smallest; `tour_3d` (boolean, optional) — Require a 3D tour; `transit_line` (array, optional) — Nearby transit line; repeat for multiple; `video_tour` (boolean, optional) — Require a video tour; `zip_code` (string, optional) — Five-digit ZIP code

### `streeteasy_school`

- **HTTP:** `GET /streeteasy/schools/{slug}`
- **What:** Get StreetEasy school details. Retrieves the public school facts rendered on StreetEasy, including neighborhood, grade labels, district, address, phone, and fax when available. Use the school slug from a public /nyc/school/{slug} link, including the school results returned by streeteasy-quick-search.
- **Params:** `slug` (string, **required**) — StreetEasy school slug

### `streeteasy_unit`

- **HTTP:** `GET /streeteasy/units/{building_slug}/{unit}`
- **What:** Get StreetEasy unit details. Retrieves a public unit's structured listing details from its server-rendered page, including address, asking price, description, amenities, and scheduled open houses.
- **Params:** `building_slug` (string, **required**) — StreetEasy building slug; `unit` (string, **required**) — StreetEasy unit segment from /building/{building_slug}/{unit}
