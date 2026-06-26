# realtime-amazon-data

> Full OpenAPI spec: https://openwebninja.s3.us-east-1.amazonaws.com/portal/openapi/realtime_amazon_data.yaml

**Host:** `real-time-amazon-data.p.rapidapi.com`
**Notes:** Page-based pagination. Results per page vary by endpoint.

## Endpoints

### GET /search
Product Search

**Required:**
- `query` (string) Example: `Phone`

**Optional:**
- `page` (integer, default: 1) Example: `1`
- `country` (string, default: US) — values: US, AU, BR, CA, CN, FR, DE, IN, IT, MX, NL, SG, ES, TR, AE, GB, JP, SA, PL, SE, BE, EG, ZA, IE
- `sort_by` (string, default: RELEVANCE) — values: RELEVANCE, LOWEST_PRICE, HIGHEST_PRICE, REVIEWS, NEWEST, BEST_SELLERS
- `category_id` (string, default: aps (All Departments))
- `category` (string) Example: `2858778013`
- `min_price` (integer) Example: `105`
- `max_price` (integer) Example: `110`
- `product_condition` (string, default: ALL) — values: ALL, NEW, USED, RENEWED, COLLECTIBLE
- `brand` (string)
- `seller_id` (string)
- `is_prime` (boolean, default: FALSE) Example: `FALSE`
- `deals_and_discounts` (string, default: NONE) — values: NONE, ALL_DISCOUNTS, TODAYS_DEALS
- `four_stars_and_up` (boolean) Example: `TRUE`
- `language` (string) Example: `en_US`
- `additional_filters` (string) Example: `p_n_feature_browse-bin%3A2656022011`
- `fields` (string) Example: `product_price,product_url,is_best_seller,sales_volume`

**Pagination:** page_number (param: `page`)
**Response path:** `data` (products in `data.products[]`)

---

### GET /products-by-category
Product by Category

**Required:**
- `category_id` (string) Example: `https://amazon.com/s?node=2858778013 - the Amazon Category ID is `2858778013`.`

**Optional:**
- `page` (integer, default: 1) Example: `1`
- `country` (string, default: US) — values: US, AU, BR, CA, CN, FR, DE, IN, IT, MX, NL, SG, ES, TR, AE, GB, JP, SA, PL, SE, BE, EG, ZA, IE
- `sort_by` (string, default: RELEVANCE) — values: RELEVANCE, LOWEST_PRICE, HIGHEST_PRICE, REVIEWS, NEWEST, BEST_SELLERS
- `min_price` (number) Example: `105`
- `max_price` (integer) Example: `110`
- `product_condition` (string, default: ALL) — values: ALL, NEW, USED, RENEWED, COLLECTIBLE
- `brand` (string)
- `is_prime` (boolean, default: FALSE) Example: `FALSE`
- `deals_and_discounts` (string, default: NONE) — values: NONE, ALL_DISCOUNTS, TODAYS_DEALS
- `four_stars_and_up` (boolean) Example: `TRUE`
- `language` (string) Example: `en_US`
- `additional_filters` (string) Example: `p_n_feature_browse-bin%3A2656022011`
- `fields` (string) Example: `product_price,product_url,is_best_seller,sales_volume`

**Pagination:** page_number (param: `page`)

---

### GET /product-details
Product Details

**Required:**
- `asin` (string)

**Optional:**
- `country` (string, default: US) — values: US, AU, BR, CA, CN, FR, DE, IN, IT, MX, NL, SG, ES, TR, AE, GB, JP, SA, PL, SE, BE, EG, ZA, IE
- `more_info_query` (string)
- `language` (string) Example: `en_US`
- `fields` (string) Example: `product_price,product_url,is_best_seller,sales_volume`

**Pagination:** none

---

### GET /product-reviews
Product Reviews — Get and paginate through product reviews on Amazon. Each page contains up to 10 reviews.

> **Note:** The `cookie` parameter (Amazon session cookie) is required for pagination. Without it, requests will fail. If you don't have a cookie, use `/top-product-reviews` instead — it returns only featured reviews but does not require authentication.

**Required:**
- `asin` (string) — Product asin for which to get reviews. Example: `B07ZPKN6YR`
- `cookie` (string) — A loggedin user cookie to use for fetching product reviews. Include the following cookies for country=US: sessionid, ubi

**Optional:**
- `country` (string, default: US) — values: US, AU, BR, CA, CN, FR, DE, IN, IT, MX, NL, SG, ES, TR, AE, GB, JP, SA, PL, SE, BE, EG, ZA, IE
- `page` (integer, default: 1) Example: `1`
- `sort_by` (string, default: TOP_REVIEWS)
- `star_rating` (string, default: ALL) — values: ALL, 5_STARS, 4_STARS, 3_STARS, 2_STARS, 1_STARS, POSITIVE, CRITICAL
- `verified_purchases_only` (boolean) — Only return reviews by reviewers who made a verified purchase. Example: `false`
- `images_or_videos_only` (boolean) — Only return reviews containing images and / or videos. Example: `False`
- `current_format_only` (boolean) Example: `False`
- `query` (string) — Find reviews matching a search query.
- `language` (string) Example: `en_US`
- `fields` (string) Example: `review_title,review_images,review_date,country`

**Pagination:** page_number (param: `page`)

---

### GET /product-review-details
Product Review Details — Get the details of a specific product review by id

**Required:**
- `review_id` (string) — The id of the product review for which to get details. Example: `RYRK6K6MMXB9C`
- `cookie` (string) — A loggedin user cookie to use for fetching product reviews.

**Optional:**
- `country` (string, default: US) — values: US, AU, BR, CA, CN, FR, DE, IN, IT, MX, NL, SG, ES, TR, AE, GB, JP, SA, PL, SE, BE, EG, ZA, IE
- `language` (string) Example: `en_US`
- `fields` (string) Example: `review_title,review_images,review_date,country`

**Pagination:** none
**Response path:** `data`
**Key fields:** Size

---

### GET /top-product-reviews
Top Product Reviews — Get top product reviews by ASIN from the Amazon product details page.

**Required:**
- `asin` (string) — Product asin for which to get reviews. Example: `B07ZPKN6YR`

**Optional:**
- `country` (string, default: US) — values: US, AU, BR, CA, CN, FR, DE, IN, IT, MX, NL, SG, ES, TR, AE, GB, JP, SA, PL, SE, BE, EG, ZA, IE
- `fields` (string) Example: `review_title,review_images,review_date,country`
- `language` (string) Example: `en_US`

**Pagination:** none
**Response path:** `data`
**Key fields:** review_id, review_title, review_comment, review_star_rating, review_link, review_author_id, review_author, review_author_url, review_author_avatar, review_images, review_video, review_date, is_verified_purchase, helpful_vote_statement, reviewed_product_asin, reviewed_product_variant, is_vine, Size, Color

---

### GET /product-offers
Product Offers

**Required:**
- `asin` (string)

**Optional:**
- `country` (string, default: US) — values: US, AU, BR, CA, CN, FR, DE, IN, IT, MX, NL, SG, ES, TR, AE, GB, JP, SA, PL, SE, BE, EG, ZA, IE
- `product_condition` (string, default: NEW, USED_LIKE_NEW, USED_VERY_GOOD, USED_GOOD, USED_ACCEPTABLE)
- `delivery` (string) — values: PRIME_ELIGIBLE, FREE_DELIVERY
- `limit` (integer, default: 100) Example: `100`
- `page` (integer, default: 1) Example: `1`
- `language` (string) Example: `en_US`
- `fields` (string) Example: `product_price,product_information,product_condition,ships_from`

**Pagination:** page_number (param: `page`)
**Page size param:** `limit` (default: 100)

---

### GET /seller-profile
Seller Profile — Get Amazon Seller profile details from the Amazon Seller profile page (e.g. https://www.amazon.com/sp?seller=A1D09S7Q0OD6TH).

**Required:**
- `seller_id` (string) — The Amazon Seller ID for which to get seller profile details Example: `A02211013Q5HP3OMSZC7W`

**Optional:**
- `country` (string, default: US) — values: US, AU, BR, CA, CN, FR, DE, IN, IT, MX, NL, SG, ES, TR, AE, GB, JP, SA, PL, SE, BE, EG, ZA, IE
- `language` (string) Example: `en_US`
- `fields` (string) Example: `seller_link,phone,business_name,rating`

**Pagination:** none

---

### GET /seller-reviews
Seller Reviews

**Required:**
- `seller_id` (string) — The Amazon Seller ID for which to get seller reviews Example: `A02211013Q5HP3OMSZC7W`

**Optional:**
- `country` (string, default: US) — values: US, AU, BR, CA, CN, FR, DE, IN, IT, MX, NL, SG, ES, TR, AE, GB, JP, SA, PL, SE, BE, EG, ZA, IE
- `star_rating` (string, default: ALL) — values: ALL, 5_STARS, 4_STARS, 3_STARS, 2_STARS, 1_STARS, POSITIVE, CRITICAL
- `page` (integer, default: 1) Example: `1`
- `language` (string) Example: `en_US`
- `fields` (string) Example: `review_star_rating,review_date`

**Pagination:** page_number (param: `page`)
**Response path:** `data`
**Key fields:** review_author, review_comment, review_star_rating, has_response, review_date

---

### GET /seller-products
Seller Products — Get and paginate through the products sold by an Amazon Seller

**Required:**
- `seller_id` (string) — The Amazon Seller ID for which to get seller product listings Example: `A02211013Q5HP3OMSZC7W`

**Optional:**
- `country` (string, default: US) — values: US, AU, BR, CA, CN, FR, DE, IN, IT, MX, NL, SG, ES, TR, AE, GB, JP, SA, PL, SE, BE, EG, ZA, IE
- `page` (integer, default: 1) Example: `1`
- `sort_by` (string, default: RELEVANCE) — values: RELEVANCE, LOWEST_PRICE, HIGHEST_PRICE, REVIEWS, NEWEST, BEST_SELLERS
- `language` (string) Example: `en_US`
- `fields` (string) Example: `product_price,product_url,is_prime`

**Pagination:** page_number (param: `page`)

---

### GET /best-sellers
Best Sellers

**Required:**
- `category` (string)

**Optional:**
- `type` (string, default: BEST_SELLERS) — values: BEST_SELLERS, GIFT_IDEAS, MOST_WISHED_FOR, MOVERS_AND_SHAKERS, NEW_RELEASES
- `page` (integer, default: 1) Example: `1`
- `country` (string, default: US) — values: US, AU, BR, CA, CN, FR, DE, IN, IT, MX, NL, SG, ES, TR, AE, GB, JP, SA, PL, SE, BE, EG, ZA, IE
- `language` (string) Example: `en_US`
- `fields` (string) Example: `product_title,product_url,product_photo`

**Pagination:** page_number (param: `page`)
**Response path:** `data`
**Key fields:** rank, asin, product_title, product_price, product_star_rating, product_num_ratings, product_url, product_photo, rank_change_label

---

### GET /deals-v2
Deals

**Optional:**
- `country` (string, default: US) — values: US, AU, BR, CA, CN, FR, DE, IN, IT, MX, NL, SG, ES, TR, AE, GB, JP, SA, PL, SE, BE, EG, ZA, IE
- `offset` (string) — Number of results to skip / index to start from (for pagination). Works with multiples of 30 (like on Amazons deals page
- `categories` (string)
- `min_product_star_rating` (string, default: ALL) — values: ALL, 1, 2, 3, 4
- `price_range` (string, default: ALL) — values: ALL, 1, 2, 3, 4, 5
- `discount_range` (string, default: ALL) — values: ALL, 1, 2, 3, 4, 5
- `brands` (string)
- `prime_early_access` (boolean) — Only return prime early access deals. Example: `Do not include in request`
- `prime_exclusive` (boolean) — Only return prime exclusive deals. Example: `Do not include in request`
- `lightning_deals` (boolean) — Only return lightning deals Example: `Do not include in request`
- `language` (string) Example: `en_US`
- `fields` (string) Example: `deal_type,deal_title,deal_ends_at,savings_amount`

**Pagination:** offset (param: `offset`)
**Response path:** `data`
**Key fields:** deal_id, deal_type, deal_title, deal_photo, deal_state, deal_url, canonical_deal_url, deal_starts_at, deal_ends_at, savings_percentage, deal_badge, type, product_asin, amount, currency

---

### GET /deal-products
Deal Products

**Required:**
- `deal_id` (string) — Deal ID of the deal to fetch Example: `B08B477BHS`

**Optional:**
- `country` (string, default: US) — values: US, AU, BR, CA, CN, FR, DE, IN, IT, MX, NL, SG, ES, TR, AE, GB, JP, SA, PL, SE, BE, EG, ZA, IE
- `sort_by` (string, default: FEATURED) — values: FEATURED, LOWEST_PRICE, HIGHEST_PRICE, REVIEWS, NEWEST, BEST_SELLERS
- `page` (integer, default: 1) Example: `1`
- `language` (string) Example: `en_US`
- `fields` (string) Example: `product_title,deal_price,deal_badge`

**Pagination:** page_number (param: `page`)
**Response path:** `data`
**Key fields:** product_asin, product_title, product_url, product_photo, deal_price, list_price, savings_percentage, deal_badge, additional_info

---

### GET /promo-code-details
Promo Code Details — Get the products offered by an Amazon promo code.

**Required:**
- `promo_code` (string) Example: `AZDIA7AYE39P2`

**Optional:**
- `country` (string, default: US) — values: US, AU, BR, CA, CN, FR, DE, IN, IT, MX, NL, SG, ES, TR, AE, GB, JP, SA, PL, SE, BE, EG, ZA, IE
- `language` (string) Example: `en_US`

**Pagination:** none
**Response path:** `data`
**Key fields:** asin, product_title, product_price, product_url, product_star_rating, product_num_ratings, product_photo, product_availability

---

### GET /influencer-profile
Influencer Profile — Get Amazon Influencer profile details from the Amazon Influencer store page *(e.g. https://www.amazon.com/shop/tastemade)*.

**Required:**
- `influencer_name` (string) — The Amazon Influencer name for which to get profile details Example: `tastemade`

**Optional:**
- `country` (string, default: US) — values: US, AU, BR, CA, CN, FR, DE, IN, IT, MX, NL, SG, ES, TR, AE, GB, JP, SA, PL, SE, BE, EG, ZA, IE
- `fields` (string) Example: `name,profile_link,posts_count,facebook_url`
- `language` (string) Example: `en_US`

**Pagination:** none

---

### GET /influencer-posts
Influencer Posts — Get all Amazon Influencer posts with pagination support.

**Required:**
- `influencer_name` (string) — The Amazon Influencer name for which to get posts Example: `tastemade`

**Optional:**
- `country` (string, default: US) — values: US, AU, BR, CA, CN, FR, DE, IN, IT, MX, NL, SG, ES, TR, AE, GB, JP, SA, PL, SE, BE, EG, ZA, IE
- `scope` (string, default: ALL) — values: ALL, IDEA_LISTS, PHOTOS, VIDEOS
- `query` (string) — Find posts matching a search query.
- `cursor` (string)
- `limit` (integer, default: 20) Example: `2`
- `language` (string) Example: `en_US`
- `fields` (string) Example: `post_url,post_title,is_pinned,video_duration`

**Pagination:** cursor (param: `cursor`)
**Page size param:** `limit` (default: 20)

---

### GET /influencer-post-products
Influencer Post Products — Get products related to an influencer post

**Required:**
- `influencer_name` (string) Example: `madison.lecroy`
- `post_id` (string) Example: `amzn1.ideas.382NVFBNK3GGQ`

**Optional:**
- `cursor` (string)
- `language` (string) Example: `en_US`

**Pagination:** cursor (param: `cursor`)

---

### GET /asin-to-gtin
ASIN to GTIN — Convert an Amazon ASIN to GTIN / EAN / UPS identifiers. Valid values for type are EAN-13, UPC, or ISBN.

**Required:**
- `asin` (string) — Amazon product ASIN to convert. Example: `B01FHOWYA2`

**Optional:**
- `country` (string, default: US) — values: US, AU, BR, CA, CN, FR, DE, IN, IT, MX, NL, SG, ES, TR, AE, GB, JP, SA, PL, SE, BE, EG, ZA, IE

**Pagination:** none
**Response path:** `data`
**Key fields:** value, type

---

### GET /product-category-list
Product Category List — Get Amazon product categories per country (for use with /products-by-category)

**Optional:**
- `country` (string, default: US) — values: US, AU, BR, CA, CN, FR, DE, IN, IT, MX, NL, SG, ES, TR, AE, GB, JP, SA, PL, SE, BE, EG, ZA, IE

**Pagination:** none
**Response path:** `data`
**Key fields:** id, name

---
