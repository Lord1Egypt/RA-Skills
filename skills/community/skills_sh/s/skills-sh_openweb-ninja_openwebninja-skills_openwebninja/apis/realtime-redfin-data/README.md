# realtime-redfin-data

> Full OpenAPI spec: https://openwebninja.s3.us-east-1.amazonaws.com/portal/openapi/realtime_redfin_data.yaml

**Host:** `real-time-redfin-data.p.rapidapi.com`
**Notes:** U.S. & Canada Redfin real estate data. Page size set by `num_homes` (default 40, up to 350). `/search` location must be a 5-digit US zip code, a Canadian postal-code area, or a Redfin region URL — NOT a city/state string. Search results live at `data.results`; `data.has_more` and `data.current_page` drive pagination.

## Endpoints

### GET /search
Search

**Required:**
- `location` (string) — 5-digit US zip, Canadian postal-code area, or Redfin region URL. Example: `90210`

**Optional:**
- `status` (string, default: for_sale) — values: for_sale, sold, for_rent, coming_soon
- `property_types` (string) — comma-separated: HOUSE, CONDO, TOWNHOUSE, MULTI_FAMILY, LAND, OTHER, MANUFACTURED, CO_OP. Example: `HOUSE,CONDO`
- `sort` (string, default: redfin_recommended) — values: redfin_recommended, newest, oldest, price_low_high, price_high_low, beds, baths, sqft, lot_size
- `page` (integer, default: 1) — values: 1 to 100
- `num_homes` (integer, default: 40) — results per page, values: 1 to 350
- `country_code` (string, default: US) — values: US, CA
- `min_price` (number)
- `max_price` (number)
- `min_beds` (integer)
- `max_beds` (integer)
- `min_baths` (number) — supports half-baths, e.g. `2.5`
- `min_sqft` (integer)
- `max_sqft` (integer)
- `min_lot_size` (integer) — sqft
- `max_lot_size` (integer) — sqft
- `min_year_built` (integer)
- `max_year_built` (integer)
- `max_hoa` (number) — max monthly HOA dues
- `has_pool` (boolean)
- `has_garage` (boolean)
- `is_waterfront` (boolean)
- `time_on_market_days` (integer) — on market within the last N days
- `sold_within_days` (integer) — for `status=sold`, values: 1 to 1095

**Pagination:** page_number (param: `page`) — results at `data.results`

---

### GET /search-coordinates
Search by Coordinates

Search within a geographic bounding box defined by Northeast and Southwest corners.

**Required:**
- `ne_lat` (number) — NE corner latitude, -90 to 90. Example: `37.79`
- `ne_lng` (number) — NE corner longitude, -180 to 180. Example: `-122.40`
- `sw_lat` (number) — SW corner latitude, must be < `ne_lat`. Example: `37.77`
- `sw_lng` (number) — SW corner longitude, must be < `ne_lng`. Example: `-122.43`

**Optional:** same filters as `/search` (`status`, `property_types`, `sort`, `page`, `num_homes`, `country_code`, `min_price`, `max_price`, `min_beds`, `max_beds`, `min_baths`, `min_sqft`, `max_sqft`, `min_lot_size`, `max_lot_size`, `min_year_built`, `max_year_built`, `max_hoa`, `has_pool`, `has_garage`, `is_waterfront`, `time_on_market_days`, `sold_within_days`)

**Pagination:** page_number (param: `page`) — results at `data.results`

---

### GET /search-polygon
Search by Polygon

Search within a custom polygon area.

**Required:**
- `polygon` (string) — comma-separated `longitude latitude` pairs (at least 3). Format: `lng1 lat1,lng2 lat2,lng3 lat3,...`. Auto-closed if not closed. Example: `-118.45 34.10,-118.40 34.10,-118.40 34.05,-118.45 34.05`

**Optional:** same filters as `/search`.

**Pagination:** page_number (param: `page`) — results at `data.results`

---

### GET /property-details
Property Details

Full details for one property: address, price, beds/baths, sqft, MLS info, listing agent/broker, public description, amenity groups, photos, price history, tax history, schools, open houses, and Redfin Estimate (AVM) with time series.

**Required (one of):**
- `property_id` (string) — Redfin internal property ID (from `/search` results or a Redfin URL). Example: `6824074`
- `url` (string) — full Redfin listing URL

**Optional:**
- `country_code` (string, default: US) — values: US, CA

**Pagination:** none

---

### GET /market-trends
Market Trends

Redfin housing market trends for a region: latest snapshot (median list/sale price, sale-to-list ratio, avg days on market, YoY sale price change, inventory) plus home-price and demand time series.

**Required:**
- `location` (string) — 5-digit US zip, Canadian postal-code area, or Redfin region URL. Example: `90210`

**Optional:**
- `country_code` (string, default: US) — values: US, CA

**Pagination:** none

---
