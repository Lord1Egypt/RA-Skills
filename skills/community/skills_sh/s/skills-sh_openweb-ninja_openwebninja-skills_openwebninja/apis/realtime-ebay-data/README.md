# realtime-ebay-data

> Full OpenAPI spec: https://openwebninja.s3.us-east-1.amazonaws.com/portal/openapi/realtime_ebay_data.yaml

**Host:** `real-time-ebay-data.p.rapidapi.com`

Fast, reliable eBay product search, category browsing, product details, and seller feedback across 20 eBay domains worldwide, in real time.

## Endpoints

### GET /search
Product Search

**Required:**
- `query` (string) Example: `iphone 15`

**Optional:**
- `page` (integer, default: 1) — allowed `1-100`, each page up to 60 results
- `domain` (string, default: us → `com`) — values: com, co.uk, com.au, de, ca, fr, it, es, at, ch, com.sg, com.my, ph, ie, pl, nl, be, com.hk, com.mx, com.br
- `sort_by` (string, default: BEST_MATCH) — values: BEST_MATCH, ENDING_SOONEST, NEWLY_LISTED, PRICE_LOWEST, PRICE_HIGHEST
- `condition` (string) — comma-separated: new, used, open_box, refurbished, for_parts. Example: `used,refurbished`
- `buying_format` (string) — values: buy_it_now, auction, accepts_offers
- `show_only` (string) — comma-separated: free_returns, deals_and_savings, returns_accepted, authorized_seller, sold_items, completed_items, free_shipping, local_pickup. Example: `sold_items,completed_items`
- `min_price` (number) — price in the domain currency
- `max_price` (number) — price in the domain currency
- `aspects` (string) — JSON-encoded array of `{name,value}` aspect filters (Brand, Model, Storage Capacity, Network, Color, etc.), up to 20 entries. `value` may be a string or array of strings. Example: `[{"name":"Brand","value":"Apple"}]`

**Pagination:** page_number (param: `page`, up to 60 results/page)
**Page size:** fixed 60 (no page-size param)
**Response path:** `data.products` (products in `data.products[]`)
**Key fields:** item_id, title, url, price, price_raw, original_price, currency, caption, discount, image, image_high_res, condition, shipping, location, seller_name, seller_feedback_percentage, seller_feedback_count, seller_top_rated, watchers, items_sold, free_returns, rating, review_count, buying_format, time_left, bid_count, is_ebay_refurbished, is_sponsored, epid, position
**Also in `data`:** total_results, current_page, results_per_page, page_url, related_searches[]

---

### GET /products-by-category
Products by Category

Works best with a `query` parameter — without it, eBay serves a JavaScript-rendered browse page and results may be limited (0-24 products). With `query`, returns full search results filtered by category (up to 60 products per page).

**Required:**
- `category_id` (string) Example: `9355` (Cell Phones & Smartphones), `175672` (Laptops & Netbooks), `11450` (Clothing)

**Optional:**
- `query` (string) — highly recommended. Example: `samsung galaxy`
- `page` (integer, default: 1) — allowed `1-100`, each page up to 60 results
- `domain` (string, default: us → `com`) — values: com, co.uk, com.au, de, ca, fr, it, es, at, ch, com.sg, com.my, ph, ie, pl, nl, be, com.hk, com.mx, com.br
- `sort_by` (string, default: BEST_MATCH) — values: BEST_MATCH, ENDING_SOONEST, NEWLY_LISTED, PRICE_LOWEST, PRICE_HIGHEST
- `condition` (string) — comma-separated: new, used, open_box, refurbished, for_parts
- `buying_format` (string) — values: buy_it_now, auction, accepts_offers
- `show_only` (string) — comma-separated: free_returns, deals_and_savings, returns_accepted, authorized_seller, sold_items, completed_items, free_shipping, local_pickup
- `min_price` (number) — price in the domain currency
- `max_price` (number) — price in the domain currency
- `aspects` (string) — JSON-encoded array of `{name,value}` aspect filters (scoped to the category), up to 20 entries. Example: `[{"name":"Brand","value":"Samsung"}]`

**Pagination:** page_number (param: `page`, up to 60 results/page)
**Page size:** fixed 60 (no page-size param)
**Response path:** `data.products`
**Key fields:** item_id, title, url, price, price_raw, original_price, currency, discount, image, condition, shipping, location, seller_name, seller_feedback_percentage, seller_feedback_count, seller_top_rated, free_returns, buying_format, position
**Also in `data`:** category_name, total_results, current_page, results_per_page, page_url, subcategories[], brands[], related_categories[]

---

### GET /product-details
Product Details

Full details for a single eBay listing. Primary data source is LD+JSON structured data for stability, with CSS selectors as fallback.

**Required:**
- `product_id` (string) — eBay item ID (numeric, found in listing URLs after `/itm/`). Example: `287062440001`

**Optional:**
- `domain` (string, default: us → `com`) — values: com, co.uk, com.au, de, ca, fr, it, es, at, ch, com.sg, com.my, ph, ie, pl, nl, be, com.hk, com.mx, com.br

**Pagination:** none
**Response path:** `data` (single object)
**Key fields:** item_id, title, price, price_raw, currency, original_price, discount, condition, images[], seller_name, seller_url, seller_feedback_percentage, seller_feedback_count, seller_top_rated, seller_items_sold, seller_joined, seller_detailed_ratings (accurate_description, reasonable_shipping_cost, shipping_speed, communication), available_quantity, items_sold, shipping, location, delivery_estimate, return_policy, item_specifics[] (label/value), brand, model, color, mpn, upc, type, description_url, breadcrumbs[] (name/url), watchers

---

### GET /seller-feedback
Seller Feedback

Seller feedback and reviews. Use `seller_id` for all feedback, or combine with `product_id` to filter feedback for a specific item.

**Required:**
- `seller_id` (string) — eBay seller username. Example: `wirelesssource`, `thrift.books`, `musicmagpie`

**Optional:**
- `product_id` (string) — filter feedback to a specific eBay item ID. Example: `287062440001`
- `page` (integer, default: 1) — allowed `1-100`, each page up to 25 reviews
- `domain` (string, default: us → `com`) — values: com, co.uk, com.au, de, ca, fr, it, es, at, ch, com.sg, com.my, ph, ie, pl, nl, be, com.hk, com.mx, com.br

**Pagination:** page_number (param: `page`, up to 25 reviews/page)
**Page size:** fixed 25 (no page-size param)
**Response path:** `data.reviews`
**Key fields:** feedback_id, rating, comment, author, date, verified_purchase, has_images
**Also in `data`:** seller_id, product_id, total_reviews, current_page, total_pages, topics[] (name/value)

---
