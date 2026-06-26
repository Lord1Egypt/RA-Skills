# realtime-homedepot-data

> Full OpenAPI spec: https://openwebninja.s3.us-east-1.amazonaws.com/portal/openapi/realtime_homedepot_data.yaml

**Host:** `realtime-homedepot-data.p.rapidapi.com`

## Endpoints

### GET /search
Search

**Required:**
- `query` (string) Example: `drill`

**Optional:**
- `page` (integer, default: 1) — range: 1-30
- `items_per_page` (integer, default: 24) — range: 1-48
- `store_id` (string) Example: `121`
- `zipcode` (string) Example: `30301`
- `sort_by` (string, default: best_match) — values: best_match, top_sellers, top_rated, price_low_to_high, price_high_to_low, newest
- `min_price` (number) Example: `50`
- `max_price` (number) Example: `200`
- `brand` (string) Example: `DEWALT`
- `in_stock` (boolean, default: false)

**Pagination:** page_number (param: `page`, max 30)
**Page size param:** `items_per_page` (default: 24, max 48)
**Response path:** `data` (products in `data.products[]`)
**Result-set fields:** total_results, total_pages, current_page, results_count, items_per_page, keyword, spelling_correction, canonical_url, category_id, search_redirect, breadcrumbs, brand_link, filters, applied_filters, related_searches, products
**Product fields:** item_id, url, title, brand, model_no, sku_id, upc, product_type, sku_classification, thumbnail, images, pricing (current_price, original_price, currency, discount, clearance_price, special_buy, bulk_pricing, unit_pricing), rating, total_reviews, in_stock, is_buyable, availability_type, is_discontinued, backordered, is_sponsored, is_live_goods, hide_price, eco_rebates, department, department_id, sub_department_id, class_number, product_sub_type, breadcrumbs, badges, excluded_ship_states, fulfillment (pickup, delivery), features, subscription, description, seo_description

---

### GET /products-by-category
Products By Category

**Required:**
- `category_id` (string) Example: `5yc1vZc2bp`

**Optional:**
- `page` (integer, default: 1) — range: 1-30
- `items_per_page` (integer, default: 24) — range: 1-48
- `store_id` (string) Example: `121`
- `zipcode` (string) Example: `30301`
- `sort_by` (string, default: best_match) — values: best_match, top_sellers, top_rated, price_low_to_high, price_high_to_low, newest
- `min_price` (number) Example: `50`
- `max_price` (number) Example: `200`
- `brand` (string) Example: `Milwaukee`
- `in_stock` (boolean, default: false)

**Pagination:** page_number (param: `page`, max 30)
**Page size param:** `items_per_page` (default: 24, max 48)
**Response path:** `data` (products in `data.products[]`)
**Key fields:** Same result-set and product structure as `/search`. Category id appears in Home Depot category page URLs (the `N-...` segment) and in the `breadcrumbs` / `filters` of Search responses.

---

### GET /product-details
Product Details

**Required:**
- One of `item_id` or `url` is required.
- `item_id` (string) Example: `326680222` — Home Depot internet (item) number
- `url` (string) Example: `https://www.homedepot.com/p/RYOBI-ONE-18V-Cordless-Drill-Driver-Kit-PCL201K1/326680222` — alternative to `item_id`

**Optional:**
- `store_id` (string) Example: `121`
- `zipcode` (string) Example: `30301`

**Pagination:** none
**Response path:** `data`
**Key fields:** item_id, url, title, brand, model_no, sku_id, upc, product_type, parent_id, description, seo_description, highlights, images, thumbnail, videos, has_360_view, pricing, rating, total_reviews, rating_histogram, in_stock, is_buyable, availability_type, is_discontinued, backordered, online_store_only, is_live_goods, favorites_count, department, department_id, sub_department_id, class_number, category_hierarchy, product_sub_type, brand_link, breadcrumbs, key_features, specifications, dimensions, attributes, paint_details, badges, fulfillment, excluded_ship_states, subscription, configurator, is_gift_card, is_generic_product, replacement_omsid

---

### GET /item-lookup
Item Lookup

**Required:**
- `search` (string) Example: `DCD800B` — manufacturer model number or Home Depot internet (item) number

**Optional:**
- `page` (integer, default: 1) — range: 1-30
- `items_per_page` (integer, default: 24) — range: 1-48
- `store_id` (string) Example: `121`
- `zipcode` (string) Example: `30301`

**Pagination:** page_number (param: `page`, max 30)
**Page size param:** `items_per_page` (default: 24, max 48)
**Response path:** `data` (products in `data.products[]`)
**Key fields:** Same result-set and product structure as `/search`. Useful for resolving a known model/SKU to a product.

---

### GET /product-reviews
Product Reviews

**Required:**
- `item_id` (string) Example: `300569432` — Home Depot internet (item) number

**Optional:**
- `page` (integer, default: 1) — range: 1-51
- `items_per_page` (integer, default: 20) — range: 1-100
- `sort_by` (string, default: helpful) — values: helpful, newest, oldest, photos_first, highest_rating, lowest_rating, relevance
- `rating` (integer) — range: 1-5
- `verified_only` (boolean, default: false)
- `search_text` (string) Example: `easy to use`

**Pagination:** page_number (param: `page`, max 51)
**Page size param:** `items_per_page` (default: 20, max 100)
**Response path:** `data` (reviews in `data.reviews[]`)
**Result-set fields:** total_reviews, total_pages, current_page, reviews_count, items_per_page, rating, rating_histogram (per-star count, 5→1), sort_by, item_id, total_recommended, total_not_recommended, reviews
**Review fields:** review_id, title, review_text, rating, date, last_modified, is_recommended, is_featured, is_verified_purchaser, badges, helpful_count, unhelpful_count, comment_count, author_id, author_name, author_location, images, product_id, original_product_name, merchant_responses, context_data, content_locale, source_client

---
