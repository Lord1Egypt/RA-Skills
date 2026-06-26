# yelp-business-data

> ⚠️ **Known Limitations:** Business search returns empty results for some cities (e.g., Chicago). Name matching across platforms is unreliable for complex business names.

> Full OpenAPI spec: https://openwebninja.s3.us-east-1.amazonaws.com/portal/openapi/yelp_business_data.yaml

**Host:** `red-flower-business-data.p.rapidapi.com`
**Notes:** Offset-based pagination using 'start' param. Pass limit to control page size.

## Endpoints

### GET /business-search
Business Search — Search for Yelp businesses by query / keyword and location.

**Required:**
- `query` (string)
- `location` (string) Example: `San Francisco, CA, USA`

**Optional:**
- `sort_by` (string, default: RECOMMENDED) — values: RECOMMENDED, HIGHEST_RATED, REVIEW_COUNT
- `start` (integer, default: 0) Example: `0`
- `price_range` (string)
- `yelp_domain` (string, default: yelp.com) — values: yelp.com, yelp.com.au, yelp.co.nz, ms.yelp.my, yelp.cz, yelp.dk, yelp.de, yelp.at, de.yelp.ch, en.yelp.be, yelp.ca, en.yelp.com.hk, en.yelp.my, en.yelp.com.ph, yelp.ie, yelp.com.sg, en.yelp.ch, yelp.co.uk, yelp.com.ar, yelp.cl, yelp.es, yelp.com.mx, fil.yelp.com.ph, yelp.fr, fr.yelp.ca, fr.yelp.ch, fr.yelp.be, yelp.no, yelp.pl, yelp.pot, yelp.com.br, fi.yelp.fi, sv.yelp.fi, yelp.se, yelp.com.tr, yelp.co.jp, zh.yelp.com.hk, yelp.com.tw

**Pagination:** offset (param: `start`)

---

### GET /business-details
Business Details — Fetch a single or multiple business details from Yelp.

**Required:**
- `business_id` (string)

**Optional:**
- `yelp_domain` (string, default: yelp.com) — values: yelp.com, yelp.com.au, yelp.co.nz, ms.yelp.my, yelp.cz, yelp.dk, yelp.de, yelp.at, de.yelp.ch, en.yelp.be, yelp.ca, en.yelp.com.hk, en.yelp.my, en.yelp.com.ph, yelp.ie, yelp.com.sg, en.yelp.ch, yelp.co.uk, yelp.com.ar, yelp.cl, yelp.es, yelp.com.mx, fil.yelp.com.ph, yelp.fr, fr.yelp.ca, fr.yelp.ch, fr.yelp.be, yelp.no, yelp.pl, yelp.pot, yelp.com.br, fi.yelp.fi, sv.yelp.fi, yelp.se, yelp.com.tr, yelp.co.jp, zh.yelp.com.hk, yelp.com.tw

**Pagination:** none
**Response path:** `data`
**Key fields:** id, alias, name, address, country, phone, website, menu_url, business_page_link, yelp_menu, price_range, rating, review_count, photo, owner_name, owner_photo_url, owner_biography, categories, operation_hours, popular_dishes, neighborhoods

---

### GET /business-reviews
Business Reviews — Fetch a single or multiple business review pages from Yelp (each page includes up to 10 reviews).

**Required:**
- `business_id` (string)

**Optional:**
- `page` (integer, default: 1) Example: `1`
- `page_size` (integer, default: 10) Example: `10`
- `num_pages` (integer, default: 1) Example: `1`
- `sort` (string, default: BEST_MATCH) — values: BEST_MATCH, NEWEST, OLDEST, HIGHEST_RATED, LOWEST_RATED, ELITES
- `query` (string) — Return reviews matching a text query
- `language` (string, default: en) Example: `en`

**Pagination:** page_number (param: `page`)
**Response path:** `data`
**Key fields:** language, count, useful, funny, cool, helpful, thanks, love_this, oh_no

---
