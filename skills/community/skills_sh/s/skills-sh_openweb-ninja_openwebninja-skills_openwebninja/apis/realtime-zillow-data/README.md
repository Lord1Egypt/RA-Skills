# realtime-zillow-data

> Full OpenAPI spec: https://openwebninja.s3.us-east-1.amazonaws.com/portal/openapi/realtime_zillow_data.yaml

**Host:** `real-time-real-estate-data.p.rapidapi.com`
**Notes:** Fixed ~41 results per page.

## Endpoints

### GET /search
Search

**Required:**
- `location` (string) Example: `Los Angeles, CA`

**Optional:**
- `page` (number, default: 1) Example: `1`
- `home_status` (string, default: FOR_SALE) — values: FOR_SALE, FOR_RENT, RECENTLY_SOLD
- `home_type` (string) Example: `HOUSES`
- `space_type` (string)
- `sort` (string, default: DEFAULT) Example: `NEWEST`
- `min_price` (number) Example: `0`
- `max_price` (number) Example: `0`
- `min_monthly_payment` (number) Example: `0`
- `max_monthly_payment` (number) Example: `0`
- `min_bedrooms` (number) Example: `0`
- `max_bedrooms` (number) Example: `0`
- `min_bathrooms` (number) Example: `0`
- `max_bathrooms` (number) Example: `0`
- `min_sqft` (number) Example: `0`
- `max_sqft` (number) Example: `0`
- `min_lot_size` (number)
- `max_lot_size` (number)
- `listing_type` (string, default: BY_AGENT)
- `for_sale_by_agent` (boolean, default: true) Example: `true`
- `for_sale_by_owner` (boolean, default: true) Example: `true`
- `for_sale_is_new_construction` (boolean, default: true) Example: `true`
- `for_sale_is_foreclosure` (boolean, default: true) Example: `true`
- `for_sale_is_auction` (boolean, default: true) Example: `true`
- `for_sale_is_foreclosed` (boolean, default: false) Example: `true`
- `for_sale_is_preforeclosure` (boolean, default: false) Example: `true`
- `max_hoa_fee` (number, default: ANY FEE) Example: `0`
- `includes_homes_no_hoa_data` (boolean, default: true) Example: `true`

**Pagination:** page_number (param: `page`)

---

### GET /search-coordinates
Search by Coordinates

**Required:**
- `long` (number) Example: `-118.504744`
- `lat` (number) Example: `34.01822`

**Optional:**
- `diameter` (number, default: 1) Example: `1.0`
- `page` (number, default: 1) Example: `1`
- `home_status` (string, default: FOR_SALE) — values: FOR_SALE, FOR_RENT, RECENTLY_SOLD
- `home_type` (string) Example: `HOUSES`
- `space_type` (string)
- `sort` (string, default: DEFAULT) Example: `NEWEST`
- `min_price` (number) Example: `0`
- `max_price` (number) Example: `0`
- `min_monthly_payment` (number) Example: `0`
- `max_monthly_payment` (number) Example: `0`
- `min_bedrooms` (number) Example: `0`
- `max_bedrooms` (number) Example: `0`
- `min_bathrooms` (number) Example: `0`
- `max_bathrooms` (number) Example: `0`
- `min_sqft` (number) Example: `0`
- `max_sqft` (number) Example: `0`
- `min_lot_size` (number)
- `max_lot_size` (number)
- `listing_type` (string, default: BY_AGENT)
- `for_sale_by_agent` (boolean, default: true) Example: `true`
- `for_sale_by_owner` (boolean, default: true) Example: `true`
- `for_sale_is_new_construction` (boolean, default: true) Example: `true`
- `for_sale_is_foreclosure` (boolean, default: true) Example: `true`
- `for_sale_is_auction` (boolean, default: true) Example: `true`
- `for_sale_is_foreclosed` (boolean, default: false) Example: `true`
- `for_sale_is_preforeclosure` (boolean, default: false) Example: `true`
- `max_hoa_fee` (number, default: ANY FEE) Example: `0`
- `includes_homes_no_hoa_data` (boolean, default: true) Example: `true`

**Pagination:** page_number (param: `page`)

---

### GET /search-polygon
Search by Polygon

**Required:**
- `polygon` (string) Example: `>-`

**Optional:**
- `page` (number, default: 1) Example: `1`
- `home_status` (string, default: FOR_SALE) — values: FOR_SALE, FOR_RENT, RECENTLY_SOLD
- `home_type` (string) Example: `HOUSES`
- `space_type` (string)
- `sort` (string, default: DEFAULT) Example: `NEWEST`
- `min_price` (number) Example: `0`
- `max_price` (number) Example: `0`
- `min_monthly_payment` (number) Example: `0`
- `max_monthly_payment` (number) Example: `0`
- `min_bedrooms` (number) Example: `0`
- `max_bedrooms` (number) Example: `0`
- `min_bathrooms` (number) Example: `0`
- `max_bathrooms` (number) Example: `0`
- `min_sqft` (number) Example: `0`
- `max_sqft` (number) Example: `0`
- `min_lot_size` (number)
- `max_lot_size` (number)
- `listing_type` (string, default: BY_AGENT)
- `for_sale_by_agent` (boolean, default: true) Example: `true`
- `for_sale_by_owner` (boolean, default: true) Example: `true`
- `for_sale_is_new_construction` (boolean, default: true) Example: `true`
- `for_sale_is_foreclosure` (boolean, default: true) Example: `true`
- `for_sale_is_auction` (boolean, default: true) Example: `true`
- `for_sale_is_foreclosed` (boolean, default: false) Example: `true`
- `for_sale_is_preforeclosure` (boolean, default: false) Example: `true`
- `max_hoa_fee` (number, default: ANY FEE) Example: `0`
- `includes_homes_no_hoa_data` (boolean, default: true) Example: `true`

**Pagination:** page_number (param: `page`)

---

### GET /property-details
Property Details

**Required:**
- `zpid` (string) Example: `7594920`

**Optional:**
- `url` (string) Example: `https://www.zillow.com/homedetails/15626-Laurel-Heights-Dr-Houston-TX-77084/28253016_zpid/`

**Pagination:** none

---

### GET /property-details-address
Property by Address

**Required:**
- `address` (string) Example: `1161 Natchez Dr College Station Texas 77845`

**Pagination:** none

---

### GET /zestimate
Property Zestimate

**Required:**
- `zpid` (string) Example: `28253016`

**Optional:**
- `url` (string) Example: `https://www.zillow.com/homedetails/15626-Laurel-Heights-Dr-Houston-TX-77084/28253016_zpid/`

**Pagination:** none

---
