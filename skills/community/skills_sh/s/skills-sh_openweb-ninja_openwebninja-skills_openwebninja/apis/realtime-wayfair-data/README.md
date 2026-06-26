# realtime-wayfair-data

> Full OpenAPI spec: https://openwebninja.s3.us-east-1.amazonaws.com/portal/openapi/realtime_wayfair_data.yaml

**Host:** `real-time-wayfair-data.p.rapidapi.com`

## Endpoints

### GET /search
Search

Search for Wayfair products by keyword or browse by brand/manufacturer. Either `query` or `manufacturer_id` is required.

**Required:**
- _(none individually)_ — provide either `query` or `manufacturer_id`

**Optional:**
- `query` (string) — keyword search. Example: `sofa`
- `manufacturer_id` (string) — Wayfair brand/manufacturer ID to browse all products by a brand. Example: `21377`
- `page` (integer, default: 1) Example: `1`
- `items_per_page` (string, default: 48) — values: 24, 48, 96
- `sort_by` (string, default: recommended) — values: recommended, customer_rating, price_low_to_high, price_high_to_low
- `category_id` (string) — Wayfair category ID; used with `manufacturer_id` to browse brand products in a category
- `min_price` (number) — min price filter, USD
- `max_price` (number) — max price filter, USD
- `color` (string) Example: `Black` (also White, Blue, Gray, Brown, Red, Green, Beige, Gold, Silver, Multi Colored)
- `in_stock` (boolean, default: false) — only return in-stock products
- `domain` (string, default: com) — values: com, ca, co.uk, ie, de

**Pagination:** page_number (param: `page`)
**Page size param:** `items_per_page` (default: 48; allowed 24, 48, 96)
**Response path:** `data` (products in `data.products[]`)
**Page meta fields (on `data`):** total_results, current_page, items_per_page, total_pages, sort_options[] (value, name), keyword
**Key product fields:** sku, name, brand, url, image_url, pricing (current_price, currency, original_price, discount_amount, discount_percentage), rating, review_count, free_shipping, shipping_text, delivery_estimate, in_stock, promo_text, flag, option_summary, color_option_count

---

### GET /product-details
Product Details

Get detailed product information by Wayfair SKU, including name, brand, pricing, images, rating, and description.

**Required:**
- `sku` (string) Example: `MBYC1330`

**Optional:**
- `domain` (string, default: com) — values: com, ca, co.uk, ie, de

**Pagination:** none
**Response path:** `data`
**Key fields:** sku, name, brand, url, description, images[], pricing (current_price, currency, original_price, discount_amount, discount_percentage), rating, review_count, reviews[] (review_id, body, date, rating)

---

### GET /product-reviews
Product Reviews

Get paginated product reviews by Wayfair SKU (10 per page). Returns review text, rating, date, reviewer info, an AI-generated summary, and aspect sentiments.

**Required:**
- `sku` (string) Example: `MBYC1062`

**Optional:**
- `page` (integer, default: 1) Example: `1`
- `sort_by` (string, default: relevance) — values: relevance, helpful, date_ascending, date_descending, rating_ascending, rating_descending
- `star` (string) — values: 1, 2, 3, 4, 5
- `domain` (string, default: com) — values: com, ca, co.uk, ie, de

**Pagination:** page_number (param: `page`)
**Page size:** 10 (fixed)
**Response path:** `data` (reviews in `data.reviews[]`)
**Page meta fields (on `data`):** sku, total_reviews, reviews_returned, sort_by, end_cursor, ai_summary, aspects[] (name, count, sentiment)
**Key review fields:** review_id, rating, body, date, reviewer_name, reviewer_location, badge, locale, is_verified

---
