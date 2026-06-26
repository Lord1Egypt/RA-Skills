# realtime-walmart-data

> Full OpenAPI spec: https://openwebninja.s3.us-east-1.amazonaws.com/portal/openapi/realtime_walmart_data.yaml

**Host:** `real-time-walmart-data1.p.rapidapi.com`

## Endpoints

### GET /search
Product Search

**Required:**
- `query` (string) Example: `laptop`

**Optional:**
- `limit` (number, default: 40) Example: `40`
- `page` (number, default: 1) Example: `1`
- `sort_by` (string, default: best_match) — values: best_match, price_low, price_high, best_seller, top_rated
- `min_price` (number, default: 10) Example: `10`
- `max_price` (number, default: 500) Example: `500`
- `store_id` (string) Example: `2648`
- `facet` (string)
- `domain` (string, default: us) — values: us, ca
- `state` (string) Example: `CA`
- `zip` (string) Example: `90210`

**Pagination:** page_number (param: `page`)
**Page size param:** `limit` (default: 40)
**Response path:** `data` (products in `data.products[]`)
**Key fields:** position, product_id, us_item_id, title, description, brand, price, list_price, currency, currency_symbol, price_display, min_price, max_price, savings_amount, price_per_unit_amount, price_per_unit_type, primary_offer, image, thumbnail, url, rating, review_count, availability, out_of_stock, preorder, seller, seller_id, pickup, delivery_from_store, shipping, shipping_days, two_day_shipping, free_shipping, free_shipping_with_walmart_plus, sponsored, multiple_options_available, badge_flags, best_seller

---

### GET /products-by-category
Products By Category

**Required:**
- `category_id` (string) Example: `3944`

**Optional:**
- `limit` (number, default: 40) Example: `40`
- `page` (number, default: 1) Example: `1`
- `sort_by` (string, default: best_match) — values: best_match, price_low, price_high, best_seller, top_rated
- `max_price` (number, default: 500) Example: `500`
- `min_price` (number, default: 10) Example: `10`
- `store_id` (string) Example: `2648`
- `facet` (string)
- `domain` (string, default: us) — values: us, ca
- `state` (string) Example: `CA`
- `zip` (string) Example: `90210`

**Pagination:** page_number (param: `page`)
**Page size param:** `limit` (default: 40)
**Response path:** `data`
**Key fields:** position, product_id, us_item_id, title, description, brand, price, list_price, currency, currency_symbol, price_display, min_price, max_price, savings_amount, price_per_unit_amount, price_per_unit_type, primary_offer, image, thumbnail, url, rating, review_count, availability, out_of_stock, preorder, seller, seller_id, pickup, delivery_from_store, shipping, shipping_days, two_day_shipping, free_shipping, free_shipping_with_walmart_plus, sponsored, multiple_options_available, badge_flags, best_seller

---

### GET /product-details
Product Details

**Required:**
- `product_id` (string) Example: `609040889`

**Optional:**
- `domain` (string, default: us) — values: us, ca

**Pagination:** none
**Response path:** `data`
**Key fields:** five, four, three, two, one, id, title, body, rating, date, author, positive_feedback, negative_feedback, type, properties, swatch_url, available, product_id, selected

---

### GET /product-offers
Product Offers

**Required:**
- `product_id` (string) Example: `609040889`

**Optional:**
- `domain` (string, default: us) — values: us, ca

**Pagination:** none
**Response path:** `data`
**Key fields:** position, offer_id, offer_type, seller_id, seller_name, seller_display_name, seller_type, catalog_seller_id, storefront_url, price, price_display, currency, currency_symbol, availability_status, in_stock, condition, free_shipping, shipping_price, delivery_date, pickup_available, return_policy, wfs_enabled

---

### GET /product-reviews
Product Reviews

**Required:**
- `product_id` (string) Example: `609040889`

**Optional:**
- `page` (number, default: 1) Example: `1`
- `domain` (string, default: us) — values: us, ca
- `rating` (number, default: 5) Example: `1`
- `limit` (number, default: 10) Example: `10`
- `sort` (string, default: relevancy) — values: relevancy, recent, rating_high_low, rating_low_high

**Pagination:** page_number (param: `page`)
**Page size param:** `limit` (default: 10)
**Response path:** `data`
**Key fields:** name, url, is_external_source, external_source, author_name, author_id, verified_purchase, type

---
