# local-business-data

> Full OpenAPI spec: https://openwebninja.s3.us-east-1.amazonaws.com/portal/openapi/local_business_data.yaml

**Host:** `local-business-data.p.rapidapi.com`
**Notes:** limit param controls results per call (max 500). No pagination — one call returns all results up to limit.
**Pricing:** The API charges a "Business" credit for each business, review, or photo returned by the API. When extract_emails_and_contacts=true is used, the API charges 1 extra credit per business that has at least one email, phone number, or social profile match.

## Endpoints

### GET /search
Search

**Required:**
- `query` (string) Example: `Hotels in San Francisco, USA`

**Optional:**
- `limit` (integer, default: 20) Example: `20`
- `lat` (string, default: 37.359428) Example: `37.359428`
- `lng` (string, default: -121.925337) Example: `-121.925337`
- `zoom` (string, default: 13) Example: `13`
- `language` (string, default: en) Example: `en`
- `region` (string, default: us) Example: `us`
- `subtypes` (string)
- `verified` (boolean) — Only return verified businesses Example: `true`
- `business_status` (string)
- `extract_emails_and_contacts` (boolean, default: false) Example: `false`
- `fields` (string)

**Pagination:** none
**Page size param:** `limit` (default: 20)
**Response path:** `data`
**Key fields:** queries

---

### GET /search-in-area
Search In Area

**Required:**
- `query` (string) — Search query / keyword Example: `pizza`
- `lat` (string) Example: `37.359428`
- `lng` (string) Example: `-121.925337`
- `zoom` (string) Example: `13`

**Optional:**
- `limit` (string, default: 20) Example: `20`
- `language` (string, default: en) Example: `en`
- `region` (string, default: us) Example: `us`
- `subtypes` (string)
- `extract_emails_and_contacts` (boolean, default: false) Example: `false`
- `fields` (string)

**Pagination:** none
**Page size param:** `limit` (default: 20)

---

### GET /search-nearby
Search Nearby

**Required:**
- `query` (string) Example: `plumbers`
- `lat` (string) Example: `37.359428`
- `lng` (string) Example: `-121.925337`

**Optional:**
- `limit` (string, default: 20) Example: `20`
- `language` (string, default: en) Example: `en`
- `region` (string, default: us) Example: `us`
- `subtypes` (string)
- `extract_emails_and_contacts` (boolean, default: false) Example: `false`
- `fields` (string)

**Pagination:** none
**Page size param:** `limit` (default: 20)

---

### GET /business-details
Business Details

**Required:**
- `business_id` (string) Example: `0x880fd393d427a591%3A0x8cba02d713a995ed`

**Optional:**
- `extract_emails_and_contacts` (boolean, default: true) Example: `true`
- `extract_share_link` (boolean, default: false) Example: `false`
- `fields` (string)
- `region` (string, default: us) Example: `us`
- `language` (string, default: eu) Example: `eu`
- `coordinates` (string) Example: `37.09024,-95.712891`

**Pagination:** none
**Response path:** `data`
**Key fields:** business_id

---

### GET /business-reviews
Business Reviews — Get business reviews by Business Id with pagination support.

**Required:**
- `business_id` (string) Example: `0x89c259b5a9bd152b:0x31453e62a3be9f76`

**Optional:**
- `limit` (string, default: 20) Example: `20`
- `cursor` (string) — The cursor value from the previous response to get the next set of results (scrolling / pagination).
- `sort_by` (string, default: most_relevant) — values: most_relevant, newest, highest_ranking, lowest_ranking
- `fields` (string) Example: `review_id,review_text,rating`
- `region` (string, default: us) Example: `us`
- `language` (string, default: en) Example: `en`

**Pagination:** cursor (param: `cursor`)
**Page size param:** `limit` (default: 20)

---

### GET /review-details
Business Review Details — Get the details of a specific review by Google Id / Business Id or Google Place Id and Review Author Id.

**Required:**
- `business_id` (string) Example: `0x89c259b5a9bd152b%3A0x31453e62a3be9f76`
- `review_author_id` (string) Example: `110228754725692228062`

**Optional:**
- `region` (string, default: us) Example: `us`
- `language` (string, default: en) Example: `en`

**Pagination:** none
**Response path:** `data`
**Key fields:** review_id

---

### GET /business-photos
Business Photos — Get business photos by Business Id.

**Required:**
- `business_id` (string) Example: `0x89c259b5a9bd152b%3A0x31453e62a3be9f76`

**Optional:**
- `limit` (string, default: 20) Example: `20`
- `cursor` (string)
- `is_video` (boolean, default: false) Example: `false`
- `region` (string, default: us) Example: `us`
- `fields` (string)

**Pagination:** cursor (param: `cursor`)
**Page size param:** `limit` (default: 20)
**Response path:** `data`
**Key fields:** photo_id

---

### GET /photo-details
Business Photo Details

**Required:**
- `business_id` (string) Example: `0x89c259b5a9bd152b%3A0x31453e62a3be9f76`
- `photo_id` (string) Example: `AF1QipMPYCqZ5Fe8a7Jc51KT9pWOS5c6tOKY_xvkCl23`

**Pagination:** none
**Response path:** `data`
**Key fields:** photo_id

---

### GET /business-posts
Business Posts — Get all / paginate Business Owner Posts (

**Required:**
- `business_id` (string) Example: `0x880fd393d427a591%3A0x8cba02d713a995ed`

**Optional:**
- `cursor` (string)
- `region` (string, default: us) Example: `us`
- `language` (string, default: en) Example: `en`

**Pagination:** cursor (param: `cursor`)
**Response path:** `data`
**Key fields:** post_id

---

### GET /reverse-geocoding
Reverse Geocoding

**Required:**
- `lat` (string) Example: `40.6958453`
- `lng` (string) Example: `-73.9799119`

**Optional:**
- `region` (string, default: us) Example: `us`
- `language` (string, default: en) Example: `en`
- `fields` (string)

**Pagination:** none
**Response path:** `data`
**Key fields:** business_id

---

### GET /autocomplete
Autocomplete — Returns place/address, business and query predictions for text-based geographic queries.

**Required:**
- `query` (string) — Search query Example: `new y`

**Optional:**
- `region` (string, default: us) Example: `us`
- `language` (string, default: en) Example: `en`
- `coordinates` (string) Example: `37.381315%2C-122.046148`

**Pagination:** none

---
