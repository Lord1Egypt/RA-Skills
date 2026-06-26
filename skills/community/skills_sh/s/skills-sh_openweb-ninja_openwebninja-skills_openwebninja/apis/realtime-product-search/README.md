# realtime-product-search

> Full OpenAPI spec: https://openwebninja.s3.us-east-1.amazonaws.com/portal/openapi/realtime_product_search.yaml

**Host:** `real-time-product-search.p.rapidapi.com`
**Notes:** Page-based pagination. Use 'limit' param to control results per page (max 100).

## Endpoints

### GET /search-light-v2
Search Light

**Required:**
- `q` (string) — Search query / keyword Example: `Nike shoes`

**Optional:**
- `country` (string, default: us) Example: `us`
- `language` (string, default: en) Example: `en`
- `page` (integer, default: 1) Example: `1`
- `limit` (integer, default: 10) Example: `10`
- `sort_by` (string, default: BEST_MATCH) — values: BEST_MATCH, TOP_RATED, LOWEST_PRICE, HIGHEST_PRICE
- `min_price` (number) — Only return product offers with price greater than a certain value
- `max_price` (number) — Only return product offers with price lower than a certain value
- `product_condition` (string, default: ANY) — values: ANY, NEW, USED, REFURBISHED
- `stores` (string) Example: `ANY`
- `free_returns` (boolean, default: false) Example: `Do not include in request`
- `free_shipping` (boolean, default: false) Example: `Do not include in request`
- `on_sale` (boolean, default: false) Example: `Do not include in request`
- `shoprs` (string)
- `return_filters` (boolean) Example: `True`

**Pagination:** page_number (param: `page`)
**Page size param:** `limit` (default: 10)
**Response path:** `data`
**Key fields:** title, multivalue, values, Size, Brand, Width, Department, Material, Color, Style, offer_id, offer_title, offer_page_url, price, shipping, offer_badge, on_sale, original_price, product_condition, store_name, store_rating, store_review_count, store_reviews_page_url, store_favicon, payment_methods, Breathable, Season, Gender, Platform, percent_off, coupon_discount_percent, Type

---

### GET /search-v2
Search (Full)

**Required:**
- `q` (string) — Search query / keyword Example: `Nike shoes`

**Optional:**
- `country` (string, default: us) Example: `us`
- `language` (string, default: en) Example: `en`
- `page` (integer, default: 1) Example: `1`
- `limit` (integer, default: 10) Example: `10`
- `sort_by` (string, default: BEST_MATCH) — values: BEST_MATCH, TOP_RATED, LOWEST_PRICE, HIGHEST_PRICE
- `min_price` (number) — Only return product offers with price greater than a certain value
- `max_price` (number) — Only return product offers with price lower than a certain value
- `product_condition` (string, default: ANY) — values: ANY, NEW, USED, REFURBISHED
- `stores` (string) Example: `ANY`
- `free_returns` (boolean, default: false) Example: `Do not include in request`
- `free_shipping` (boolean, default: false) Example: `Do not include in request`
- `on_sale` (boolean, default: false) Example: `Do not include in request`
- `shoprs` (string)
- `return_filters` (boolean) Example: `True`

**Pagination:** page_number (param: `page`)
**Page size param:** `limit` (default: 10)
**Response path:** `data`
**Key fields:** title, multivalue, values, Size, Brand, Width, Department, Material, Color, Style, offer_id, offer_title, offer_page_url, price, shipping, offer_badge, on_sale, original_price, product_condition, store_name, store_rating, store_review_count, store_reviews_page_url, store_favicon, payment_methods, Breathable, Season, Gender, Platform, percent_off, coupon_discount_percent, Type

---

### GET /product-details-v2
Product Details

**Required:**
- `product_id` (string) — Product id of the product for which to get full details. Example: `catalogid:15554707778408471208,gpcid:6219277726645206819,headlineOfferDocid:8835386203856143595,rds:PC_15478400683365031707|PROD_PC_15478400683365031707,imageDocid:10653897321817113741,mid:576462815432560445,pvt:hg,pvf:`

**Optional:**
- `country` (string, default: us) Example: `us`
- `language` (string, default: en) Example: `en`

**Pagination:** none
**Response path:** `data`
**Key fields:** offer_id, offer_title, offer_page_url, price, shipping, offer_badge, on_sale, original_price, percent_off, product_condition, store_name, store_rating, store_review_count, store_reviews_page_url, store_favicon, coupon_discount_percent, payment_methods, url, source, publisher, thumbnail, duration_ms, preview_url

---

### GET /product-offers-v2
Product Offers

**Required:**
- `product_id` (string) — Product id of the product for which to fetch offers. Example: `catalogid:15554707778408471208,gpcid:6219277726645206819,headlineOfferDocid:8835386203856143595,rds:PC_15478400683365031707|PROD_PC_15478400683365031707,imageDocid:10653897321817113741,mid:576462815432560445,pvt:hg,pvf:`

**Optional:**
- `page` (integer, default: 1) Example: `1`
- `country` (string, default: us) Example: `us`
- `language` (string, default: en) Example: `en`

**Pagination:** page_number (param: `page`)

---

### GET /product-reviews-v2
Product Reviews

**Required:**
- `product_id` (string) — Product id of the product for which to fetch reviews. Example: `catalogid:15554707778408471208,gpcid:6219277726645206819,headlineOfferDocid:8835386203856143595,rds:PC_15478400683365031707|PROD_PC_15478400683365031707,imageDocid:10653897321817113741,mid:576462815432560445,pvt:hg,pvf:`

**Optional:**
- `limit` (integer, default: 10) Example: `10`
- `cursor` (string)
- `sort_by` (string, default: MOST_RELEVANT) — values: MOST_RELEVANT, MOST_RECENT
- `rating` (string, default: 0) Example: `0`
- `country` (string, default: us) Example: `us`
- `language` (string, default: en) Example: `en`

**Pagination:** cursor (param: `cursor`)
**Page size param:** `limit` (default: 10)

---

### GET /deals-v2
Deals

**Required:**
- `q` (string) — Search query / keyword Example: `Laptop`

**Optional:**
- `country` (string, default: us) Example: `us`
- `language` (string, default: en) Example: `en`
- `page` (integer, default: 1) Example: `1`
- `limit` (integer, default: 10) Example: `10`
- `sort_by` (string, default: BEST_MATCH) — values: BEST_MATCH, TOP_RATED, LOWEST_PRICE, HIGHEST_PRICE
- `min_price` (number) — Only return product offers with price greater than a certain value
- `max_price` (number) — Only return product offers with price lower than a certain value
- `product_condition` (string, default: ANY) — values: ANY, NEW, USED, REFURBISHED
- `stores` (string) Example: `ANY`
- `free_returns` (boolean, default: false) Example: `Do not include in request`
- `free_shipping` (boolean, default: false) Example: `Do not include in request`
- `on_sale` (boolean, default: false) Example: `Do not include in request`
- `shoprs` (string)
- `return_filters` (boolean) Example: `True`

**Pagination:** page_number (param: `page`)
**Page size param:** `limit` (default: 10)
**Response path:** `data`
**Key fields:** product_id, product_title, product_description, product_rating, product_page_url, product_num_reviews, product_num_offers, typical_price_range, offer, Resolution, Brand, Touchscreen, Color, Weight, offer_id, offer_title, offer_page_url, price, shipping, offer_badge, on_sale, original_price, percent_off, product_condition, store_name, store_rating, store_review_count, store_reviews_page_url, store_favicon, coupon_discount_percent, payment_methods, Bluetooth, Speaker, Microphone, Dimensions, Material, Style, Buttons, GPU, Ports, NFC, Ethernet, Durability, Language

---

### GET /store-reviews
Store Reviews — Get all store / merchant reviews with pagination/scrolling support using the cursor and limit parameters.

**Required:**
- `store_domain` (string) — The domain of the (TLD) of the store for which to get reviews (e.g. amazon.com). Example: `amazon.com`

**Optional:**
- `limit` (integer, default: 10) Example: `10`
- `cursor` (string)
- `rating` (string) Example: `ALL`
- `sort_by` (string, default: MOST_HELPFUL) — values: MOST_HELPFUL, MOST_RECENT
- `time_frame` (string, default: ALL) — values: ALL, ONE_YEAR, TWO_YEARS, SIX_MONTHS, THREE_MONTHS
- `country` (string, default: us) Example: `us`
- `language` (string, default: en) Example: `en`

**Pagination:** cursor (param: `cursor`)
**Page size param:** `limit` (default: 10)

---
