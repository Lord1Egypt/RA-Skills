---
name: scrapebadger
description: Web scraping platform — GitHub public profiles, Brave native web/image/video/news search, Yelp business search, AutoScout24 vehicle search, Etsy, AliExpress, Target, ASOS and Best Buy ecommerce data, Naver search/places/shopping, Twitter/X data, TikTok data, YouTube data, Vinted marketplace, Wallapop marketplace (Spain, Italy, Portugal), Amazon marketplace, eBay marketplace, Gumtree classifieds (UK, Australia, South Africa), Realtor real-estate (realtor.com + realtor.ca), Apartments.com US rentals with unit-level pricing, Idealista real estate, Immobiliare.it real estate (Italy, Spain, Greece, Luxembourg), ChatGPT, Perplexity and Microsoft Copilot answers with cited sources and brand visibility (AEO/GEO), Baidu web/news/image search, DuckDuckGo privacy-first web/image/news/video search, and general web scraping API
version: 1.11.0
requires:
  env:
    - SCRAPEBADGER_API_KEY
tags:
  - github
  - autoscout24
  - brave
  - yelp
  - bestbuy
  - asos
  - target
  - aliexpress
  - etsy
  - naver
  - twitter
  - tiktok
  - youtube
  - vinted
  - wallapop
  - amazon
  - ebay
  - realtor
  - idealista
  - immobiliare
  - real-estate
  - chatgpt
  - perplexity
  - copilot
  - llm
  - aeo
  - brand-visibility
  - web-scraping
  - scraping
  - social-media
  - marketplace
  - e-commerce
  - api
  - data
  - apartments
  - walmart
  - gumtree
  - classifieds
  - rentals
  - baidu
  - duckduckgo
  - search-engine
---

# ScrapeBadger — Web Scraping Platform

ScrapeBadger provides REST APIs across multiple product families. Use the `web_fetch` tool to call these endpoints.

## Authentication

Every request needs the `SCRAPEBADGER_API_KEY` environment variable.
Include it as an HTTP header: `X-API-Key: $SCRAPEBADGER_API_KEY`

## Base URL

```
https://scrapebadger.com
```

---

## Twitter/X API

### Users

**Get user profile by username:**
```
GET /v1/twitter/users/{username}/by_username
```

**Get user profile by numeric ID:**
```
GET /v1/twitter/users/{user_id}/by_id
```

**Batch get users by usernames (comma-separated):**
```
GET /v1/twitter/users/batch_by_usernames?usernames=elonmusk,OpenAI
```

**Batch get users by IDs (comma-separated):**
```
GET /v1/twitter/users/batch_by_ids?user_ids=44196397,1230113324
```

**Search users:**
```
GET /v1/twitter/users/search_users?query=AI+agents
```

**Get followers:**
```
GET /v1/twitter/users/{username}/followers
```

**Get following:**
```
GET /v1/twitter/users/{username}/followings
```

**Get mentions:**
```
GET /v1/twitter/users/{username}/mentions
```

**Get subscriptions:**
```
GET /v1/twitter/users/{user_id}/subscriptions
```

**Get user articles:**
```
GET /v1/twitter/users/{user_id}/articles
```

### Tweets

**Get tweet by ID:**
```
GET /v1/twitter/tweets/tweet/{tweet_id}
```

**Get multiple tweets by IDs:**
```
GET /v1/twitter/tweets/?tweets=123,456,789
```

**Advanced search:**
```
GET /v1/twitter/tweets/advanced_search?query=web+scraping&query_type=Latest&count=20
```

**Get replies:**
```
GET /v1/twitter/tweets/tweet/{tweet_id}/replies
```

**Get quotes:**
```
GET /v1/twitter/tweets/tweet/{tweet_id}/quotes
```

**Get retweeters:**
```
GET /v1/twitter/tweets/tweet/{tweet_id}/retweeters
```

**Get favoriters (likes):**
```
GET /v1/twitter/tweets/tweet/{tweet_id}/favoriters
```

**Get similar tweets:**
```
GET /v1/twitter/tweets/tweet/{tweet_id}/similar
```

**Get edit history:**
```
GET /v1/twitter/tweets/tweet/{tweet_id}/edit_history
```

**Get community notes:**
```
GET /v1/twitter/tweets/tweet/{tweet_id}/community_notes
```

**Get article:**
```
GET /v1/twitter/tweets/article/{article_id}
```

### Communities

**Get community:**
```
GET /v1/twitter/communities/{community_id}
```

**Get community tweets:**
```
GET /v1/twitter/communities/{community_id}/tweets
```

**Search communities:**
```
GET /v1/twitter/communities/search?query=AI
```

### Lists

**Get list details:**
```
GET /v1/twitter/lists/{list_id}/detail
```

**Get list tweets:**
```
GET /v1/twitter/lists/{list_id}/tweets
```

**Search tweets in list:**
```
GET /v1/twitter/lists/{list_id}/search_tweets?query=keyword
```

### Trends

**Get trending topics:**
```
GET /v1/twitter/trends/
```

**Get trends by location (WOEID):**
```
GET /v1/twitter/trends/place/{woeid}
```

### Geo

**Search places:**
```
GET /v1/twitter/geo/search?query=New+York
```

**Get place details:**
```
GET /v1/twitter/geo/places/{place_id}
```

### Spaces

**Get Space details:**
```
GET /v1/twitter/spaces/{space_id}
```

**Get broadcast details:**
```
GET /v1/twitter/spaces/broadcast/{broadcast_id}
```

---

## Vinted Marketplace API

**Search items:**
```
GET /v1/vinted/search?query=nike+shoes&market=fr&page=1&per_page=20
```
Optional params: `price_from`, `price_to`, `brand_ids`, `order`

**Get item details:**
```
GET /v1/vinted/items/{item_id}?market=fr
```

**Get user profile:**
```
GET /v1/vinted/users/{user_id}?market=fr
```

**Get user's items:**
```
GET /v1/vinted/users/{user_id}/items?market=fr
```

**Search brands:**
```
GET /v1/vinted/brands?keyword=nike&market=fr
```

**List colors:**
```
GET /v1/vinted/colors?market=fr
```

**List statuses:**
```
GET /v1/vinted/statuses?market=fr
```

**List markets:**
```
GET /v1/vinted/markets
```

Supported markets: fr, de, uk, us, es, it, nl, be, at, pl, pt, cz, lt, and more.

---

## Wallapop Marketplace API

Second-hand listings from Wallapop in Spain (`es`, default), Italy (`it`) and Portugal (`pt`). Every endpoint takes `market`.

**Search listings (40 per page):**
```
GET /v1/wallapop/search?query=iphone+14&market=es&order_by=price_low_to_high
```
Needs `query` or `category_id`. Optional: `latitude`, `longitude` (default: market capital), `distance_km` (1-500), `category_id`, `min_price`, `max_price`, `condition` (CSV of `un_opened`, `in_box`, `new`, `as_good_as_new`, `good`, `fair`, `has_given_it_all`), `brand`, `model`, `color`, `time_filter` (`today`|`lastWeek`|`lastMonth`), `shippable`, `has_warranty`, `refurbished`, cars (`min_year`, `max_year`, `min_km`, `max_km`, `gearbox`, `min_horsepower`, `max_horsepower`), `order_by` (`most_relevance`|`newest`|`closest`|`price_low_to_high`|`price_high_to_low`). Paginate with `next_page` from the previous response (other params are then ignored).

**Listing detail** (id, slug or full wallapop.com URL):
```
GET /v1/wallapop/items/{item_id}?market=es
```

**Seller profile, listings and reviews** (user id or profile slug; listings/reviews paginate with `next_page`):
```
GET /v1/wallapop/users/{user_id}?market=es
GET /v1/wallapop/users/{user_id}/items?market=es
GET /v1/wallapop/users/{user_id}/reviews?market=es
```

**Reference:**
```
GET /v1/wallapop/autocomplete?query=bici&market=es
GET /v1/wallapop/categories?market=es
GET /v1/wallapop/filters?category_id=24200&market=es
GET /v1/wallapop/filters/{filter_id}/options?category_id=24200&market=es
GET /v1/wallapop/markets
```

---

## Amazon Marketplace API

The `domain` parameter is the marketplace TLD (`com`, `co.uk`, `de`, `fr`, `co.jp`, …), default `com`. It also sets the geo-matched residential proxy for correct price/availability.

**Search the catalog:**
```
GET /v1/amazon/search?query=mechanical+keyboard&domain=com&page=1
```
Optional params: `sort_by`, `category`, `min_price`, `max_price`, `zip`

**Keyword autocomplete:**
```
GET /v1/amazon/autocomplete?query=mechan&domain=com
```

**Get product detail (PDP) by ASIN:**
```
GET /v1/amazon/products/{asin}?domain=com
```
Optional params: `zip`, `language`. Returns variants, buybox, badges, A+ content, frequently-bought-together, also-bought.

**Get all seller offers + buybox:**
```
GET /v1/amazon/products/{asin}/offers?domain=com
```

**Get product reviews (featured public subset):**
```
GET /v1/amazon/products/{asin}/reviews?domain=com&page=1
```
Optional params: `sort_by` (helpful|recent), `star`, `verified_only`, `media_only`

**Best Sellers:**
```
GET /v1/amazon/bestsellers?domain=com&category={node}&page=1
```

**New Releases:**
```
GET /v1/amazon/new-releases?domain=com&category={node}&page=1
```

**Deals (Today's / Lightning):**
```
GET /v1/amazon/deals?domain=com&category=...&page=1
```

**Browse a category by node:**
```
GET /v1/amazon/category?node={node}&domain=com&page=1
```
Optional param: `sort_by`

**Seller profile:**
```
GET /v1/amazon/sellers/{seller_id}?domain=com
```

**Seller storefront products:**
```
GET /v1/amazon/sellers/{seller_id}/products?domain=com&page=1
```

**Seller buyer feedback:**
```
GET /v1/amazon/sellers/{seller_id}/feedback?domain=com&page=1
```

**List markets (free):**
```
GET /v1/amazon/markets
```

**List categories (free):**
```
GET /v1/amazon/categories
```

Supported marketplaces (20): com, co.uk, de, fr, it, es, nl, se, pl, ca, com.mx, com.br, co.jp, in, com.au, sg, ae, sa, com.tr, eg.

---

## eBay Marketplace API

The `domain` parameter is the marketplace TLD (`com`, `co.uk`, `de`, `fr`, …), default `com`. It also sets the geo-matched residential proxy for correct price/availability. Aliases: `us`→`com`, `uk`/`gb`→`co.uk`, `au`→`com.au`.

**Search active listings:**
```
GET /v1/ebay/search?query=mechanical+keyboard&domain=com&page=1
```
Optional params: `category_id`, `per_page` (60|120|240), `sort_by` (best_match|ending_soonest|newly_listed|price_low_to_high|price_high_to_low), `condition` (new|open_box|refurbished|used|for_parts|graded|ungraded), `buying_format` (auction|buy_it_now|best_offer), `min_price`, `max_price`, `free_shipping`, `location` (domestic|worldwide). Returns results[] + facets + pagination.

**Search active listings by image (eBay's own visual search — 10 credits):**
```
POST /v1/ebay/search/by-image
{"image_url": "https://example.com/sneaker.jpg", "domain": "com"}
```
Send exactly one of `image_url` (a public http(s) URL we download) or `image_base64` (the image itself, JPEG or PNG, max 10 MB decoded; a `data:image/jpeg;base64,…` URL also works). Same optional filters as `/search` — `category_id`, `page`, `per_page`, `condition`, `buying_format`, `min_price`, `max_price`, `free_shipping`, `location`, `language` — and the same response shape, with `query: null`. There is no `sort_by`: eBay ignores sorting on a visual results page. An image eBay cannot read is a 400, never an empty result set.

**Search completed/sold listings (price research):**
```
GET /v1/ebay/completed?query=iphone+13+pro&domain=com&page=1
```
Optional params: `category_id`, `per_page`, `sort_by`, `condition` (incl. `graded`/`ungraded` for cards), `min_price`, `max_price`, `location` (`domestic` keeps only this marketplace's own country — foreign sales otherwise skew a national price series, and eBay shows their prices converted). Returns sold listings (sold=true).

**Keyword autocomplete:**
```
GET /v1/ebay/autocomplete?query=mechan&domain=com
```

**Get item detail by item ID:**
```
GET /v1/ebay/items/{item_id}?domain=com
```
Returns specifics, images, shipping, returns, and seller.

**Get item reviews:**
```
GET /v1/ebay/items/{item_id}/reviews?domain=com&page=1
```
Returns reviews[] + aggregate rating + histogram.

**Seller profile:**
```
GET /v1/ebay/sellers/{username}?domain=com
```

**Seller active listings:**
```
GET /v1/ebay/sellers/{username}/items?domain=com&page=1
```
Optional params: `query`, `per_page`.

**Seller buyer feedback:**
```
GET /v1/ebay/sellers/{username}/feedback?domain=com&page=1
```

**Browse a category by ID:**
```
GET /v1/ebay/categories/{category_id}/items?domain=com&page=1
```
Optional params: `per_page`, `sort_by`, `min_price`, `max_price`.

**List categories (free):**
```
GET /v1/ebay/categories
```

**List markets (free):**
```
GET /v1/ebay/markets
```

Supported marketplaces (18): com, co.uk, de, fr, it, es, com.au, ca, at, ch, be, ie, nl, pl, com.hk, com.sg, com.my, ph.

---

## Realtor Real-Estate API

Unified real-estate API over **realtor.com (US, USD)** and **realtor.ca (Canada, CAD)**. The `market` parameter (`us` or `ca`, default `us`) picks the portal and the geo-matched residential proxy. Rich datapoints: price + price/tax history, beds/baths/sqft/lot, coordinates, photos/videos/virtual tours, features/amenities, HOA, schools, open houses, agent/office/broker contacts, days-on-market, price-per-sqft.

**Search listings:**
```
GET /v1/realtor/search?location=Austin,+TX&market=us&status=for_sale
```
Required: `location` (free-text "Austin, TX" / ZIP / "Toronto, ON"; optional if a CA bbox is given). Optional params: `status` (for_sale|for_rent|sold|pending, default for_sale), `price_min`, `price_max`, `beds_min`, `baths_min`, `sqft_min`/`sqft_max` (US), `property_type` (US CSV: single_family,condos,townhomes,multi_family,mobile,land), `sort` (relevant|newest|price_low|price_high|photo_count), `page`, `limit` (1-200), `lat_min`/`lat_max`/`lng_min`/`lng_max` (CA bbox; realtor.ca caps ~600/box). Returns results[] of Property + total/count/page/total_pages.

**Get property detail by ID:**
```
GET /v1/realtor/properties/{property_id}?market=us
```
Returns a full PropertyDetail: price/tax history, schools, amenities, estimates, agents, open houses.

**Location autocomplete:**
```
GET /v1/realtor/autocomplete?query=austi&market=us
```
Optional param: `limit` (1-25, default 10). Returns suggestions[] (cities, ZIPs, neighborhoods, addresses).

**List markets (free):**
```
GET /v1/realtor/markets
```

Supported markets (2): us (realtor.com), ca (realtor.ca).
## Walmart API

Product, seller and store data from **walmart.com** (US only, USD, en-US). No Walmart account or developer key is needed. walmart.ca and walmart.com.mx run on different platforms and are not supported.

**Search products:**
```
GET /v1/walmart/search?query=laptop&sort=price_low&min_price=100&max_price=500
```
Required: `query`. Optional: `page` (1-10), `sort` (`best_match`|`best_seller`|`price_low`|`price_high`|`rating_high`|`new`), `min_price`, `max_price`, `facet` (Walmart's own syntax, e.g. `brand:HP`). Returns 40-60 organic products a page.

**Browse a category / deals:**
```
GET /v1/walmart/category?path=electronics/3944&page=2
GET /v1/walmart/deals
```
`path` comes from a `walmart.com/browse/...` or `/cp/...` URL. `/category` takes no `sort` — Walmart's browse pages silently ignore it, so it is not offered. `/deals` is the rollback/clearance feed; no other Walmart API exposes one.

**Product detail and reviews:**
```
GET /v1/walmart/products/5689919121
GET /v1/walmart/products/5689919121/reviews?page=1&sort=helpful
```
`item_id` is the numeric segment at the end of a `/ip/...` URL. The product carries UPC/GTIN, structured `specifications`, `variants`, per-method promised delivery dates, return policy, and a 10-review sample. The reviews endpoint adds the **full star histogram** (`one_star`..`five_star` counts and percentages) plus Walmart's own most-helpful positive and negative reviews. 10 reviews a page — Walmart's page size, not adjustable.

**Marketplace sellers:**
```
GET /v1/walmart/sellers/101040442
GET /v1/walmart/sellers/6907/products?query=camera
```
The seller id is the **numeric `catalog_seller_id`** found on a product — NOT the 32-character hex `seller_id`, which 404s. The profile endpoint has no product list because Walmart renders a storefront's grid client-side; `/products` goes through search with a `retailer_id` facet instead, which is why it **requires** a `query`.

**Stores:**
```
GET /v1/walmart/stores/100
```
Returns the store's address, geo, phone, weekly hours, and per-department services (pharmacy, deli, auto centre — each with its own phone and hours), plus ~30 nearby stores. Walmart has no working store-finder-by-ZIP page, so walk outward from a known store id.

**Autocomplete:**
```
GET /v1/walmart/autocomplete?query=lapt
```

**Gotchas that will bite you:**
- `total_results_reported` is Walmart's own claim (~14,000) and is **not reachable** — results dry up after page 10 (search) or 11 (browse), roughly 500 products a query. Use `has_more_pages`. To go deeper, segment by brand facet or price band rather than paging.
- Consecutive pages **overlap ~20%** because Walmart re-ranks between requests — deduplicate on `us_item_id`.
- Facets can be **applied** but not **enumerated**; Walmart renders the filter rail client-side.
- Searching by UPC does **not** work — Walmart returns zero results for a bare UPC, including a product's own.
- Prices are store-specific and Walmart resolves the store from the request IP. It cannot be pinned by a parameter, so every product returns a `location` block naming the store the prices actually came from.
- HTTP 422 is an anti-bot challenge: not billed, and retrying shortly succeeds.

Cost: 1 credit autocomplete; 5 credits search / category / deals / seller / seller products / store; 10 credits product detail and reviews. `markets` and `health` are free.

## Gumtree Classifieds API (UK, Australia, South Africa)

Classified ads from three separate Gumtree sites, picked with `market` on every endpoint: `uk` (**gumtree.com**, GBP, default), `au` (**gumtree.com.au**, AUD) and `za` (**gumtree.co.za**, ZAR). Every vertical: For Sale, Motors (cars, vans, motorbikes), Property, Jobs, Services, Pets, Community. No Gumtree account is needed. Ids from one market mean nothing in another.

**Markets (free):**
```
GET /v1/gumtree/markets
```
Lists `market`, `domain`, `country`, `currency`, `distance_unit`, `page_size`, `id_format` for uk/au/za.

**Search listings:**
```
GET /v1/gumtree/search?query=mountain%20bike&category=bicycles&location=manchester&distance=10&sort=price_asc
GET /v1/gumtree/search?category=cars&location=SW1A%201AA&distance=25&filters=vehicle_make:bmw,vehicle_fuel_type:petrol,min_vehicle_mileage:10000
GET /v1/gumtree/search?market=au&category=18320&location=3003435&distance=25&filters=cars.carmake_s:toyota
GET /v1/gumtree/search?market=za&category=9077&filters=ma:toyota,fu:petrol,max_km:100000
```
All optional: `market` (`uk`|`au`|`za`, default `uk`), `query`, `category` (uk: slug, e.g. `cars`, `for-sale`, `property-to-rent`, `jobs`, `bicycles`; au/za: **numeric id** from `/categories?market=..`, e.g. `18320` au cars, `9077` za cars; default `all`), `location` (uk: slug, town name or UK postcode; au/za: **numeric id** from `/locations/autocomplete?market=..`, e.g. `3003435` Sydney, `3100003` Gauteng; default: the whole country), `distance` (miles for uk, km for au; >0–1000; not supported for za), `min_price`/`max_price` (market currency; uk needs a category other than `all`), `sort` (`relevance`|`date`|`price_asc`|`price_desc`|`distance` — `distance` only for uk, or au with a location), `seller_type` (`private`|`trade`; uk and za only — on au pass e.g. `filters=cars.forsaleby_s:ownr`), `urgent_only`, `with_photos` (uk only), `filters` (comma-separated `key:value`; repeat a key for several values; range filters use `min_<key>`/`max_<key>`), `page` (1-50). Page size: uk 25, au 24 (plus up to 6 featured top ads), za 20; at most 50 pages. Unsupported parameters for a market return HTTP 400 rather than being ignored. Responses carry `market` and `currency`.

**Discover a category's filters (with live counts):**
```
GET /v1/gumtree/search/filters?category=cars
GET /v1/gumtree/search/filters?market=za&category=9077&filters=ma:toyota
```
Returns `filters[]` (`key`, `label`, `type`, `options[{label,value,count}]`), `sort_options`, `distance_options`, `category_facets`. Feed a `key` + option `value` back into `/search` as `filters=key:value`. za also takes `filters` here (already-applied filters, e.g. `ma:toyota` lists Toyota models).

**Listing detail and the seller's other listings:**
```
GET /v1/gumtree/listings/1803293391
GET /v1/gumtree/listings/1803293391/seller-listings?page=1
GET /v1/gumtree/listings/10013681289561010209976109?market=za
```
`listing_id` is the number at the end of the listing URL (uk/au ~10 digits; za the full 26-digit ad id); pass the matching `market`. Detail carries the full description, `price_type`, `status`, view/reply counts, every attribute (full vehicle spec for cars), images, location, created/posted/updated/expiry dates, similar listings, and `seller` (type, verification, rating, member since, last active, lifetime listings, total views, `phone_masked`). Seller listings take ANY listing id of that seller.

**Reference:**
```
GET /v1/gumtree/autocomplete?query=sofa
GET /v1/gumtree/locations/autocomplete?query=leed
GET /v1/gumtree/locations/autocomplete?market=au&query=sydney
GET /v1/gumtree/locations?parent_id=10000393
GET /v1/gumtree/categories?market=za
```
uk: a node's `slug` is what `/search` takes as `category`/`location`; au/za: use the node's numeric `id`. Omit `parent_id` for the market's root.

**Gotchas:**
- Phone numbers are only ever the masked form shown on the public listing page (e.g. `0794997XXXX`) — the full number is never returned.
- uk pins up to 5 paid featured ads (`is_featured`) above the chosen sort order; au returns up to 6 featured top ads on top of its 24.
- au search, search filters and locations run a real browser past gumtree.com.au's JS challenge: expect ~10-20 s and the higher price below.
- Dates come in both `*_utc` (Unix seconds) and `*_at` (ISO 8601).
- HTTP 400 = parameter not supported for that market or malformed `filters`; HTTP 422 = Gumtree temporarily refused the request: not billed, retry shortly.

Cost: 5 credits search / search filters / listing detail / seller listings; 1 credit autocomplete / location autocomplete / locations / categories. **au** search and search filters bill 2x (10 credits) and au locations 5x (5 credits). `markets` and `health` are free.

## DuckDuckGo API

Privacy-first search from **duckduckgo.com** — web, images, news and videos, plus autocomplete and Instant Answers. No DuckDuckGo account or API key is needed. Region is set with the `kl`/`l` code (`us-en`, `uk-en`, `de-de`, … `wt-wt` = all regions); `safesearch` is `on` | `moderate` | `off`.

**Web search:**
```
GET /v1/duckduckgo/search?query=privacy+tools&region=us-en&safesearch=moderate&timelimit=week&page=1
```
Required: `query`. Optional: `region` (default `wt-wt`), `safesearch` (default `moderate`), `timelimit` (`day`|`week`|`month`|`year`), `page` (1-25). Returns organic results (title, url, snippet, display_url, `is_ad`), the zero-click abstract box, and `has_next`.

**Image search:**
```
GET /v1/duckduckgo/images?query=northern+lights&size=Large&color=Blue&image_type=photo&layout=Wide&license=Public
```
Required: `query`. Optional: `region`, `safesearch`, `page` (1-10, 100 results a page), `size` (`Small`|`Medium`|`Large`|`Wallpaper`), `color`, `image_type` (`photo`|`clipart`|`gif`|`transparent`|`line`), `layout` (`Square`|`Tall`|`Wide`), `license` (`Any`|`Public`|`Share`|`ShareCommercially`|`Modify`).

**News search:**
```
GET /v1/duckduckgo/news?query=elections&region=us-en&timelimit=day&page=1
```
Required: `query`. Optional: `region`, `safesearch`, `timelimit` (`day`|`week`|`month`|`year`), `page` (1-10, 30 results a page). Each item carries `date_utc` (unix) and `date_at` (ISO), source, excerpt and image.

**Video search:**
```
GET /v1/duckduckgo/videos?query=guitar+lesson&duration=medium&resolution=high&page=1
```
Required: `query`. Optional: `region`, `safesearch`, `page` (1-10, 60 results a page), `duration` (`short`|`medium`|`long`), `resolution` (`high`|`standard`). Returns title, publisher, uploader, duration, views and thumbnails.

**Autocomplete:**
```
GET /v1/duckduckgo/autocomplete?query=pyth&region=us-en
```
Required: `query`. Optional: `region`. Returns `{ query, suggestions[] }`.

**Instant Answer:**
```
GET /v1/duckduckgo/instant?query=valley+forge
```
Required: `query`. DuckDuckGo's Instant Answer API — abstract, definition, direct answer and related topics.

**Regions:**
```
GET /v1/duckduckgo/regions
```
No params. Returns the full list of 64 DuckDuckGo `kl` region codes (`us-en`, `uk-en`, `de-de`, … `wt-wt` = all).

Cost: 1 credit autocomplete / instant; 5 credits search / images / news / videos. `regions` and `health` are free.

## Apartments.com Rentals API

US rental listings from **apartments.com** (US, USD, en-US) with **unit-level pricing** — not just a property's advertised range, but every individual rentable unit with its own rent, beds, baths, square footage and availability date. No apartments.com account is needed.

**Search listings:**
```
GET /v1/apartments/search?location=kansas-city-mo&beds=1&max_price=1500
```
Required: `location` — the apartments.com slug (`kansas-city-mo`, `new-york-ny`) or a ZIP (`64108`). Optional: `page` (1-28, 40 cards a page), `beds` (0=studio, 1-4), `min_price`, `max_price`. Returns `results[]` of cards plus `total_results` / `total_pages`.

Filters verified against live counts on `kansas-city-mo` (700 unfiltered): `beds=1` → 374, `beds=2` → 490, `beds=0` → 145, `max_price=1500` → 646, `beds=1&max_price=1500` → 320. apartments.com also renders a pet filter, but it returns the unfiltered total, so it is deliberately not exposed.

**Get property detail (unit-level):**
```
GET /v1/apartments/property?url=https%3A%2F%2Fwww.apartments.com%2Furbane-kansas-city-mo%2Fwcd6e5k%2F
GET /v1/apartments/properties/{slug}/{property_id}
```
Returns the property (name, split address, geo, phone, amenities, office hours, photos), its `floor_plans[]`, and a flattened `units[]` across all plans.

**IMPORTANT — use `rent`, not `max_term_rent`.** Every unit carries both. `rent` is the advertised monthly price the site shows a renter. `max_term_rent` is apartments.com's raw `data-maxrent` attribute, which measures roughly **twice** the advertised rent and appears to be an upper bound across lease terms. It is exposed unparsed for completeness only.

`available_text` is verbatim (`"Now"`, `"Sep 3"`); the site renders no year, so it is deliberately not a date. A floor plan with `units_available: 0` and valid beds/baths/rent/sqft is the site's own layout for properties that advertise plans rather than individual units — not missing data.

A search card is a **summary** with a rent/bed rollup; pass its `url` to the property endpoint for units.

**Do not use `render_js` for apartments.com** via the general Web Scraping API — the page is fully server-rendered, so JS rendering only forces the slow browser path (100+ s) and can exceed the CDN timeout with a 524.

Cost: 5 credits per search page and per property.

## Idealista Real Estate API

Real-estate listings from Idealista across 3 markets — Spain (`es`), Italy (`it`), Portugal (`pt`), all EUR. The `market` parameter defaults to `es`. No upstream Idealista key is needed; ScrapeBadger signs requests to Idealista's mobile API server-side. Search is keyed by **location codes**, not free text, so use the two-step flow: suggest → search → property detail.

**Suggest locations (free-text → location codes):**
```
GET /v1/idealista/suggest?query=sagrada+familia&market=es
```
Optional params: `operation` (sale|rent, default sale), `property_type` (homes|offices|premises|garages|bedrooms|newDevelopments|lands|storageRooms|buildings, default homes). Returns locations[] + total + market. Only entries with `type == "location"` carry a usable `locationId`.

**Search listings (by location code):**
```
GET /v1/idealista/search?location=0-EU-ES-28-07-001-079&operation=sale&market=es
```
Optional params: `property_type` (as above, excluding bedrooms), `page` (default 1), `max_items` (default 30, 1..50), `sort_by` (weigh|price|distance|publicationDate|modificationDate|size|floor|rooms|ratioeurm2|pricedown), `sort_order` (asc|desc, default desc), `min_price`, `max_price`, `min_size`, `max_size`, `min_rooms`, `max_rooms`. Returns elementList[] + total + totalPages + actualPage + itemsPerPage + summary[] + market.

**Full property detail (by property code):**
```
GET /v1/idealista/properties/{property_code}?market=es&locale=en
```
Optional params: `locale` (en|es|it|pt, default en). Returns property + market.

**List markets (free):**
```
GET /v1/idealista/markets
```

Supported markets (3): es (idealista.com), it (idealista.it), pt (idealista.pt).

---

## Immobiliare Real Estate API

Real-estate listings from the Immobiliare Group — Italy's #1 portal immobiliare.it plus its sister portals — across 4 markets: `it` (www.immobiliare.it), `es` (www.indomio.es), `gr` (www.indomio.gr), `lu` (www.immotop.lu), all EUR. The `market` parameter defaults to `it`. No upstream API key needed. Search accepts a free-text `location` (auto-resolved) or explicit `region_id`/`province_id`/`city_id` codes from `/autocomplete`.

**Location autocomplete (free-text → location IDs):**
```
GET /v1/immobiliare/autocomplete?query=milano&market=it
```
Returns suggestions[] — each `{id, label, type (nation|region|province|comune|zone), region_id, province_id, city_id, macrozone_ids[], url}`.

**Search listings:**
```
GET /v1/immobiliare/search?location=Milano&contract=sale&market=it
```
Optional params: `region_id`/`province_id`/`city_id` (instead of free-text `location`), `contract` (sale|rent), `category` (residential|commercial|garages|offices|land|buildings|warehouses), `price_min`, `price_max`, `surface_min`, `surface_max`, `rooms_min`, `rooms_max`, `bathrooms_min`, `sort` (relevance|price_asc|price_desc|newest|oldest|surface_desc|surface_asc), `page`. Returns listings[] + count + total_ads + current_page + max_pages + is_results_limit_reached + related_searches[].

**Get full listing detail:**
```
GET /v1/immobiliare/listings/{id}?market=it
```
Returns a full Listing: price + €/m², surface, rooms, baths, floor, energy class, GPS coordinates, all photos, virtual tours, agency + agent contacts, multi-unit properties[].

**Agency profile:**
```
GET /v1/immobiliare/agencies/{id}?market=it
```

**Agency listings:**
```
GET /v1/immobiliare/agencies/{id}/listings?market=it&page=1
```

**Market price insights (€/m² monthly time series):**
```
GET /v1/immobiliare/market-insights/prices?region_id=10&market=it
```
Required: `region_id`. Optional params: `province_id`, `city_id`, `contract` (sale|rent). Returns `{contract, unit: "EUR/m²", points[{label, value}]}`.

**List markets (free):**
```
GET /v1/immobiliare/markets
```

**Reference data — contracts/categories/sorts (free):**
```
GET /v1/immobiliare/reference
```

Supported markets (4): it (immobiliare.it), es (indomio.es), gr (indomio.gr), lu (immotop.lu).

---

## YouTube API

No YouTube Data API key, OAuth, or quota required. Data is fetched via YouTube's unauthenticated InnerTube JSON API (`youtubei/v1/*`) plus SSR-HTML fallback. The `gl` parameter (ISO 3166-1 alpha-2 content region, default `US`) and `hl` parameter (BCP-47 UI language, default `en`) steer the geo-matched residential proxy + locale. All list endpoints paginate via a `continuation` token (no page numbers); pass the returned token back as `continuation`. All datetime fields ship as both `*_utc` (Unix) and `*_at` (ISO 8601 UTC).

**Search videos / channels / playlists:**
```
GET /v1/youtube/search?query=machine+learning&gl=US&hl=en
```
Optional params: `type` (video|channel|playlist|movie|all), `sort_by` (relevance|date|views|rating), `upload_date` (hour|today|week|month|year), `duration` (short|medium|long), `features` (csv: hd,4k,360,vr180,3d,hdr,cc,subtitles,live,creative_commons,location,purchased), `continuation`. Returns results[] + continuation.

**Search autocomplete:**
```
GET /v1/youtube/autocomplete?query=machine+lea&gl=US&hl=en
```

**Get video detail (merged player+next):**
```
GET /v1/youtube/videos/{video_id}
```

**Related videos:**
```
GET /v1/youtube/videos/{video_id}/related?continuation=...
```

**Video comments and nested replies:**
```
GET /v1/youtube/videos/{video_id}/comments?sort_by=top&continuation=...
GET /v1/youtube/videos/{video_id}/comments/{comment_id}/replies?continuation=...
```

**Transcript (timed text + full text + SRT/VTT):**
```
GET /v1/youtube/videos/{video_id}/transcript?lang=en
```

**Captions / streams / live chat:**
```
GET /v1/youtube/videos/{video_id}/captions
GET /v1/youtube/videos/{video_id}/streams
GET /v1/youtube/videos/{video_id}/live_chat?continuation=...
```

**Batch video lookup (POST):**
```
POST /v1/youtube/videos/batch
{ "video_ids": ["dQw4w9WgXcQ", "..."] }
```

**Channel detail + tabs:**
```
GET /v1/youtube/channels/{channel_id}
GET /v1/youtube/channels/{channel_id}/videos?sort_by=newest&continuation=...
GET /v1/youtube/channels/{channel_id}/shorts?continuation=...
GET /v1/youtube/channels/{channel_id}/streams?continuation=...
GET /v1/youtube/channels/{channel_id}/playlists?continuation=...
GET /v1/youtube/channels/{channel_id}/community?continuation=...
GET /v1/youtube/channels/{channel_id}/about
GET /v1/youtube/channels/{channel_id}/subscriber_count
GET /v1/youtube/channels/{channel_id}/search?query=...&continuation=...
```

**Resolve a handle / custom URL to a channel_id:**
```
GET /v1/youtube/channels/resolve?handle=@GoogleDevelopers
```

**Playlists and mixes:**
```
GET /v1/youtube/playlists/{playlist_id}
GET /v1/youtube/playlists/{playlist_id}/items?continuation=...
GET /v1/youtube/mixes/{mix_id}
```

**Trending, hashtags, home feed:**
```
GET /v1/youtube/trending?gl=US&type=now&continuation=...
GET /v1/youtube/trending/shorts?gl=US&continuation=...
GET /v1/youtube/hashtags/{tag}?gl=US&continuation=...
GET /v1/youtube/home?gl=US&hl=en&continuation=...
```

**Shorts:**
```
GET /v1/youtube/shorts/{short_id}
GET /v1/youtube/shorts/by_sound/{sound_id}?continuation=...
```

**Community posts:**
```
GET /v1/youtube/posts/{post_id}
GET /v1/youtube/posts/{post_id}/comments?continuation=...
```

**YouTube Music search:**
```
GET /v1/youtube/music/search?query=...
```

**Reference (free):**
```
GET /v1/youtube/oembed?url=...
GET /v1/youtube/categories
GET /v1/youtube/languages
GET /v1/youtube/regions
GET /v1/youtube/markets
```

---

## TikTok API

No TikTok login required. The `region` parameter (ISO 3166-1 alpha-2, default `US`) steers the residential proxy geo + locale. `count` is 1–50. Most endpoints use a fast device-signed mobile path with deep cursor pagination. All datetime fields ship as both `*_utc` (Unix) and `*_at` (ISO 8601 UTC).

### Users

**Get user profile:**
```
GET /v1/tiktok/users/{username}
```

**Get user's videos (cursor pagination):**
```
GET /v1/tiktok/users/{username}/videos?count=30&cursor=...
```

**Get followers (403 if the account hides the list):**
```
GET /v1/tiktok/users/{username}/followers?count=20
```

**Get following (403 if private):**
```
GET /v1/tiktok/users/{username}/following?count=20
```

**Get liked videos (403 if private):**
```
GET /v1/tiktok/users/{username}/liked?count=20
```

**Get reposted videos:**
```
GET /v1/tiktok/users/{username}/reposts?count=20
```

### Videos

**Get video / photo detail:**
```
GET /v1/tiktok/videos/{video_id}
```
Optional param: `username`

**Get video comments:**
```
GET /v1/tiktok/videos/{video_id}/comments?count=20
```

**Get comment replies:**
```
GET /v1/tiktok/comments/{comment_id}/replies?item_id={video_id}&count=20
```

**Get related videos:**
```
GET /v1/tiktok/videos/{video_id}/related?count=20
```

**Get auto-caption transcript:**
```
GET /v1/tiktok/videos/{video_id}/transcript
```

**Get oEmbed metadata for a TikTok URL:**
```
GET /v1/tiktok/oembed?url=https://www.tiktok.com/@user/video/123
```

### Hashtags & Music

**Get hashtag / challenge detail:**
```
GET /v1/tiktok/hashtags/{name}
```

**Get videos for a hashtag:**
```
GET /v1/tiktok/hashtags/{name}/videos?count=20
```

**Get sound / music detail:**
```
GET /v1/tiktok/music/{music_id}
```

**Get videos using a sound:**
```
GET /v1/tiktok/music/{music_id}/videos?count=20
```

### Search

**General search (returns videos):**
```
GET /v1/tiktok/search?query=ai+agents&count=20
```

**Search videos:**
```
GET /v1/tiktok/search/videos?query=ai+agents&count=20
```

**Search hashtags:**
```
GET /v1/tiktok/search/hashtags?query=ai&count=20
```

**Search users:**
```
GET /v1/tiktok/search/users?query=charli&count=20
```

### Trending

**Trending videos (curated Explore feed):**
```
GET /v1/tiktok/trending/videos?region=US&count=20
```

**Trending hashtags (with view_count + creator counts):**
```
GET /v1/tiktok/trending/hashtags?region=US&count=20
```

**Trending songs (ranked by usage):**
```
GET /v1/tiktok/trending/songs?region=US&count=20
```

### Ad Library (EU only)

**Search the TikTok Commercial Content Library (EU-DSA ad transparency):**
```
GET /v1/tiktok/ads/search?query=sneakers&region=DE&days=30&count=20
```
Search by keyword (`query`) OR by advertiser (`advertiser_id`). Paginates via `offset` + `search_id`. EU regions only.

### Reference (free)

**List supported regions:**
```
GET /v1/tiktok/regions
```

Coverage notes: `following`/`liked` return 403 when the account hides those lists (most large accounts do). Trending creators and trending keywords are not available (TikTok deprecated the Creative Center trend lists). The Ad Library is EU-only.

---

## ChatGPT API

Sends a prompt to **the real chatgpt.com** (not the OpenAI API) and returns the answer as structured JSON, including the web sources ChatGPT cited. Anonymous — no OpenAI account or API key is involved. Measured latency **20-25s ungrounded, 30-70s with web search per call**, so set a generous client timeout and don't poll.

**Ask ChatGPT (20 credits):**
```
GET /v1/chatgpt/ask?prompt=best+open-source+vector+databases&country=US&web_search=auto
```
Required: `prompt` (max 4096 chars). Optional: `country` (ISO-3166 alpha-2 egress country, default `US`), `web_search` (`auto` | `force` | `off`, default `auto`). Also accepts POST with the same fields as a JSON body.

Returns: `prompt`, `answer`, `answer_markdown`, `citations[]`, `search_results[]`, `source_domains[]`, `web_search_triggered` (whether ChatGPT actually browsed), `reference_tokens[]`, `model`, `conversation_id`, `message_id`, `country`, `answer_length`, `citation_count`, `latency_ms`, `created_utc`/`created_at`.

Each `Citation` is `{url, title, snippet, domain, attribution, pub_date_utc, published_at, start_index, end_index, matched_text}` — `start_index`/`end_index` are char offsets into `answer`, so you can anchor a source to the exact sentence it supports. `search_results[]` is the FULL retrieved set (`{url, title, snippet, domain, attribution, pub_date_utc, published_at, ref_index, cited}`), including results ChatGPT retrieved but never cited.

**Brand visibility — AEO/GEO (25 credits):**
```
GET /v1/chatgpt/brand-visibility?prompt=best+CRM+for+startups&brand=Acme&domain=acme.com&competitors=Salesforce,HubSpot
```
Required: `prompt`, `brand`. Optional: `domain`, `aliases` (comma-separated on GET, `string[]` on POST), `competitors` (same), `country`, `web_search` (default `force`).

Returns the brand block plus the answer: `mentioned`, `mention_count`, `first_position` (char offset), `position_score` (1.0 = named at the very start, 0.0 = absent), `share_of_voice_pct` (brand mentions / brand+competitor mentions), `cited`, `cited_urls[]`, `citation_rank`, `competitors[]` (`{name, mentioned, mention_count, first_position, cited, cited_urls}`), `excerpt`, `answer`, `citations[]`, `web_search_triggered`, `model`, `country`, `latency_ms`, `created_utc`/`created_at`.

**List available models (1 credit):**
```
GET /v1/chatgpt/models?country=US
```
Returns `{models: [{slug, title, description, max_tokens, tags[]}], count}`. Informational only — `/ask` does not take a model parameter.

**Health (free):**
```
GET /v1/chatgpt/health
```

Errors come back as `{"detail": {"code", "message"}}` with codes `blocked` (422), `rate_limited` (429), `upstream_error`, `composer_not_found`, `empty_answer`, `render_failed`, `models_unavailable` (502). Non-2xx responses are never billed.

Not supported: multi-turn conversations, model selection, streaming, and image input.

---

## Perplexity API

Sends a prompt to **the real perplexity.ai** and returns the grounded answer as structured JSON, including the web sources Perplexity cited. Anonymous — no Perplexity account or API key is involved. Every answer is a live browse taking tens of seconds, so set a generous client timeout and don't poll.

**Ask Perplexity (20 credits):**
```
GET /v1/perplexity/ask?prompt=best+open-source+vector+databases&country=US&focus=web
```
Required: `prompt` (max 4096 chars). Optional: `country` (ISO-3166 alpha-2 egress country, default `US`), `focus` (`web` | `scholar` | `social`, default `web` — `scholar` grounds on academic sources, `social` on community sources). Also accepts POST with the same fields as a JSON body.

Returns: `prompt`, `answer`, `answer_markdown`, `citations[]`, `search_results[]`, `source_domains[]`, `related_questions[]`, `images[]`/`videos[]`, `web_search_triggered`, `truncated`, `search_queries[]` (Perplexity's own retrieval fan-out — the sub-queries it issued to its search backend, which no other vendor exposes), `focus`, `model`, `backend_uuid`, `country`, `answer_length`, `citation_count`, `latency_ms`, `created_utc`/`created_at`.

Each `Citation` is `{url, title, snippet, domain, source_type, pub_date_utc, published_at, last_updated, ref_index, start_index, end_index, matched_text}` — `start_index`/`end_index` are char offsets into `answer`, so you can anchor a source to the exact sentence it supports. `search_results[]` is the FULL retrieved set (`{url, title, snippet, domain, source_type, pub_date_utc, published_at, last_updated, ref_index, cited}`), including results Perplexity retrieved but never cited.

**Brand visibility — AEO/GEO (25 credits):**
```
GET /v1/perplexity/brand-visibility?prompt=best+CRM+for+startups&brand=Acme&domain=acme.com&competitors=Salesforce,HubSpot
```
Required: `prompt`, `brand`. Optional: `domain`, `aliases` (comma-separated on GET, `string[]` on POST), `competitors` (same), `country`.

Returns the brand block plus the answer: `mentioned`, `mention_count`, `first_position` (char offset), `position_score` (1.0 = named at the very start, 0.0 = absent), `share_of_voice_pct` (brand mentions / brand+competitor mentions), `cited`, `cited_urls[]`, `citation_rank`, `competitors[]` (`{name, mentioned, mention_count, first_position, cited, cited_urls}`), `excerpt`, `answer`, `citations[]`, `web_search_triggered`, `model`, `country`, `latency_ms`, `created_utc`/`created_at`.

**List available models (1 credit):**
```
GET /v1/perplexity/models?country=US
```
Returns `{models: [{slug, title, description, requires_account}], count}`. Informational only — `/ask` takes a `focus` parameter, not a model.

**Health (free):**
```
GET /v1/perplexity/health
```

Non-2xx responses are never billed.

Not supported: multi-turn conversations (a `backend_uuid` is returned but follow-up chaining is not exposed), model selection, streaming, and image input.

---

## Copilot API

Asks **Microsoft Copilot** — specifically Copilot Search in Bing (bing.com/copilotsearch), Microsoft's public Copilot answer engine — and returns the grounded answer as structured JSON with its cited web sources. Anonymous: no Microsoft account involved (the consumer chat at copilot.microsoft.com requires sign-in and is not used). A fresh answer takes ~15-25 s; when Copilot has answered the same prompt recently it serves its own cached answer in under 1 s (`cached: true`).

**Ask Copilot (20 credits):**
```
GET /v1/copilot/ask?prompt=best+CRM+for+startups&country=US
```
Required: `prompt` (max 2000 chars). Optional: `country` (ISO-3166 alpha-2 country to ask from; also sets the market unless `market` is given, e.g. JP → ja-JP), `market` (Bing market, e.g. `ja-JP`, `en-GB`), `strict_country` (answer only from an exit in `country`, else 503 `country_unavailable`, not billed). Also accepts POST with the same fields as a JSON body. Keep `market` and `country` consistent — Bing refuses `en-US` asked from outside the US.

Returns: `prompt`, `answer`, `answer_markdown`, `citations[]` (claim-level `{url, title, snippet, domain, site_name, ref_index, start_index, end_index, matched_text}`), `search_results[]` (`{url, title, snippet, domain, site_name, ref_index, cited}` — everything Copilot retrieved; only cited sources when `cached`), `source_domains[]`, `search_queries[]`, `web_search_triggered`, `truncated`, `cached`, `conversation_id`, `market`, `country`, `answer_length`, `citation_count`, `latency_ms`, `created_utc`/`created_at`.

**Brand visibility — AEO/GEO (25 credits):**
```
GET /v1/copilot/brand-visibility?prompt=best+CRM+for+startups&brand=Acme&domain=acme.com&competitors=Salesforce,HubSpot&country=US
```
Required: `prompt`, `brand`. Optional: `domain`, `aliases`, `competitors` (comma-separated on GET, `string[]` on POST), `country`, `market`, `strict_country`. Returns the same brand block as the Perplexity endpoint plus the answer, citations, `market` and `country`.

**List markets (1 credit):**
```
GET /v1/copilot/markets
```
Returns `{markets: [{code, name, country}], count}` — 30 curated Bing markets; any well-formed language-COUNTRY code is accepted.

Non-2xx responses are never billed.

---

## Baidu API

Web search, news, images and autocomplete from **baidu.com** — China's #1 search engine (~60% CN market share). No Baidu account or developer key is needed. Chinese and English queries both work; there is no country parameter, Baidu is a single market.

**Web search (5 credits):**
```
GET /v1/baidu/search?query=咖啡机&page=1&num=20&language=zh-cn
GET /v1/baidu/search?query=site:zhihu.com+咖啡&time_from=1735689600&time_to=1767225600
```
Required: `query`. Optional: `page` (1-76), `num` (1-50), `language` (`all`|`zh-cn`|`zh-tw`), `time_from`/`time_to` (unix timestamps). Baidu's own operators — `site:`, `intitle:`, `inurl:`, `filetype:`, `"quoted phrases"` — work inside `query`. `page` is translated to Baidu's `pn` offset using `num`, so the two compose (`page=3&num=50` starts at result 101).

Each organic result carries the **real target URL** in `url` (from Baidu's `mu` attribute) alongside `baidu_url` (the `baidu.com/link?url=` tracking redirect competitors return on its own), plus `display_url`, `snippet`, `source`, `date` (Baidu's own string, e.g. `2026年8月1日` / `3天前`), `date_at` (ISO 8601 date), `thumbnail`, `tpl` (Baidu's result template id). The response also carries `total_results` and `related_searches[]`.

**News (5 credits):**
```
GET /v1/baidu/news?query=人工智能&sort=time
```
Required: `query`. Optional: `page` (1-76), `sort` (`relevance` default, or `time` for newest first). 10 articles a page; each has `title`, `url`, `baidu_url`, `snippet`, `source`, `date`, `date_at`, `thumbnail`.

**Images (5 credits):**
```
GET /v1/baidu/images?query=熊猫&page=1
```
Required: `query`. Optional: `page` (1-50). 30 images a page, each with `image_url` (full size), `thumbnail_url`, `middle_url`, `hover_url`, `width`, `height`, `type`, `from_url` and `from_title` (the page it was found on).

**Autocomplete (1 credit):**
```
GET /v1/baidu/autocomplete?query=咖啡
```

**Gotchas that will bite you:**
- `total_results` is Baidu's own claim (`百度为您找到相关结果约N个`) and is **not reachable** — pagination stops around page 76 regardless.
- Only organic results are returned. Baidu's own vertical blocks (Baike, Tieba, image grids) and ad shells are dropped, so `position` is organic rank.
- Baidu's SERP carries **no time-of-day**, so there is no `*_utc` float — only `date` (raw) and `date_at` (ISO date). A midnight timestamp would be fabricated precision.
- `url` is null when Baidu omits the `mu` attribute on a result; `baidu_url` is present either way.
- `language` and the time window are server-side Baidu filters, not post-filtering — they change which results Baidu returns.
- HTTP 422 is an anti-bot challenge: not billed, and retrying shortly succeeds.

Cost: 1 credit autocomplete; 5 credits search / news / images. `health` is free.

---

## Web Scraping API

**Scrape a URL:**
```
POST /v1/web/scrape
Content-Type: application/json

{"url": "https://example.com", "render_js": false, "return_format": "markdown"}
```
Optional fields: `render_js` (boolean), `wait_for` (CSS selector), `timeout_ms`, `proxy_country`, `return_format` (html/markdown/text)

**Detect anti-bot protection (1 credit):**
```
POST /v1/web/detect
Content-Type: application/json

{"url": "https://example.com"}
```

**Take screenshot:**
```
POST /v1/web/screenshot
Content-Type: application/json

{"url": "https://example.com", "full_page": true}
```
Optional fields: `width` (320-3840), `height` (240-4320), `wait_for`, `country`, `proxy_tier`.
Response: `screenshot` is the base64 PNG, plus `url`, `status_code`, `credits_used`.

**Extract structured data:**
```
POST /v1/web/extract
Content-Type: application/json

{"url": "https://example.com", "extract_rules": {"title": "h1", "links": {"selector": "a::attr(href)", "all": true}}}
```
Give at least one of `extract_rules` (field -> CSS/XPath selector; returns `data`),
`ai_extract_rules` (field -> description) or `ai_query` (both return `ai_extraction`).
Optional: `render_js`, `wait_for`, `country`, `proxy_tier`.

Batch jobs are not offered (`/v1/web/batch` answers 501): send concurrent `/v1/web/scrape` requests.

---

## Pagination

Most list endpoints support cursor-based pagination. Pass the `cursor` query parameter from the previous response to get the next page.

## Credits

Each API call costs credits. Check your balance:
- Twitter endpoints: 1 credit per call
- Web scraping: 1-10 credits depending on complexity
- Vinted: 1 credit per call
- Wallapop: autocomplete/categories 1; filters/filter options 2; search/item/user/user items/user reviews 5; markets free
- Amazon: autocomplete 1, seller profile/feedback 3, listings 5, offers 8, product detail & reviews 10; markets/categories free
- eBay: autocomplete 1; search/completed/item/seller/category 5; reviews/feedback 10; markets/categories free
- Realtor: autocomplete 2; search 8; property detail 10; markets free
- Idealista: suggest 2; search 5; property detail 10; markets free
- Immobiliare: autocomplete 2; search / agency profile / agency listings 5; listing detail & market price insights 10; markets/reference free
- YouTube: autocomplete/oembed 1; resolve/about/subscriber_count/captions 2; search/transcript/channel/playlist/trending/community/shorts/music 5; video detail & batch (per video) 10; streams 15; categories/languages/regions/markets free
- TikTok: oembed 2; profile/video/hashtag/music detail + search + trending + ads 5; list captures (user videos/reposts, comments, replies, related, hashtag/music videos) 8; followers/following/liked + transcript 10; regions free
- ChatGPT: models 1; ask 20; brand-visibility 25; health free
- Perplexity: models 1; ask 20; brand-visibility 25; health free
- Baidu: autocomplete 1; search/news/images 5; health free
- Gumtree: autocomplete/locations/categories 1; search/filters/listing/seller listings 5; au search & filters 10, au locations 5; markets/health free

## Rate Limits

Rate limits are per API key. Check the `X-RateLimit-*` response headers for current limits.

## More Information

- Documentation: https://docs.scrapebadger.com
- Dashboard: https://scrapebadger.com/dashboard?utm_source=openclaw-skill&utm_medium=referral
- MCP Server: https://mcp.scrapebadger.com/mcp

## Naver search, places and shopping

Use runtime SCRAPEBADGER_API_KEY. No Naver credentials are accepted. Pricing: /public/pricing; actual charge: x-credits-used. Full reference: apps/portal/public/llms-full.txt, Naver API usage. Newly implemented routes require gateway registration. Shopping Live routes use service-side mobile identity (runtime env names NAVER_MOBILE_ELB_KEY, NAVER_MOBILE_NNB, NAVER_MOBILE_NAPP_DI) and `naver_shopping_search_catalog` uses the service-side catalog transport (NAVER_CATALOG_TRANSPORT, NAVER_CATALOG_SIDECAR_URL); API consumers never supply these, and a wall, captcha or empty body is an error (422), never an empty list. SmartStore product detail, reviews and Q&A remain limited.

- `naver_search(query, page?, view?)` → `GET /v1/naver/search`
- `naver_news(query, page?, sort?)` → `GET /v1/naver/news`
- `naver_blog(query, page?)` → `GET /v1/naver/blog`
- `naver_autocomplete(query)` → `GET /v1/naver/autocomplete`
- `naver_local(query, start?, display?, x?, y?)` → `GET /v1/naver/local`
- `naver_get_place(place_id)` → `GET /v1/naver/place/{place_id}`
- `naver_get_place_reviews(place_id, cursor?, size?)` → `GET /v1/naver/place/{place_id}/reviews`
- `naver_get_place_photos(place_id, media_source?, cursor?)` → `GET /v1/naver/place/{place_id}/photos`
- `naver_shopping_bestsellers(category_id?, age_type?, sort_type?, period_type?)` → `GET /v1/naver/shopping/bestsellers`
- `naver_shopping_keywords(category_id, age_type?, sort_type?, period_type?)` → `GET /v1/naver/shopping/keywords`
- `naver_shopping_insight(category_id, start_date, end_date, time_unit?, age?, gender?, device?, count?)` → `GET /v1/naver/shopping/insight`
- `naver_shopping_categories()` → `GET /v1/naver/shopping/categories`
- `naver_shopping_search_products(query, tab?)` → `GET /v1/naver/shopping/search-products`
- `naver_shopping_search_filters(query)` → `GET /v1/naver/shopping/search-filters`
- `naver_shopping_deals(gender)` → `GET /v1/naver/shopping/deals`
- `naver_shopping_vertical(vertical)` → `GET /v1/naver/shopping/verticals/{vertical}`
- `naver_shopping_it_items()` → `GET /v1/naver/shopping/it-items`
- `naver_shopping_category_tree(parent_id?)` → `GET /v1/naver/shopping/category-tree`
- `naver_store_profile(store_url, host?)` → `GET /v1/naver/stores/{store_url}`
- `naver_store_categories(store_url, host?)` → `GET /v1/naver/stores/{store_url}/categories`
- `naver_store_products(store_url, host?, category_id?, page?, size?, sort?, channel_uid?)` → `GET /v1/naver/stores/{store_url}/products`
- `naver_store_bestsellers(store_url, host?, period?)` → `GET /v1/naver/stores/{store_url}/bestsellers`
- `naver_search_web(query, page?)` → `GET /v1/naver/search/web`
- `naver_cafe(query, page?)` → `GET /v1/naver/cafe`
- `naver_kin(query, page?)` → `GET /v1/naver/kin`
- `naver_image(query, page?)` → `GET /v1/naver/image`
- `naver_video(query, page?)` → `GET /v1/naver/video`
- `naver_clip(query, page?)` → `GET /v1/naver/clip`
- `naver_review_detail(review_id)` → `GET /v1/naver/reviews/{review_id}`
- `naver_product_review_summary(origin_product_no, leaf_category_id?)` → `GET /v1/naver/products/{origin_product_no}/review-summary`
- `naver_review_video_inkey(attach_vid, stamp)` → `GET /v1/naver/reviews/video-inkey`
- `naver_review_ssr_queries(review_id)` → `GET /v1/naver/reviews/{review_id}/ssr-queries`
- `naver_shopping_search_filtered(query, brand_id?, attribute_id?)` → `GET /v1/naver/shopping/search-filtered`
- `naver_shopping_brand_rank(category_id?, age_type?, sort_type?, period_type?)` → `GET /v1/naver/shopping/brand-rank`
- `naver_shopping_brand_categories(parent_id?)` → `GET /v1/naver/shopping/brand-categories`
- `naver_shopping_keyword_periods(category_id?, age_type?, sort_type?, period_type?)` → `GET /v1/naver/shopping/keyword-periods`
- `naver_product_reviews_list(origin_product_no, store_url, product_no, host?, channel_uid?, checkout_merchant_no?, page?, sort?)` → `GET /v1/naver/products/{origin_product_no}/reviews`
- `naver_product_qna_list(origin_product_no, store_url, product_no, host?, channel_uid?, page?)` → `GET /v1/naver/products/{origin_product_no}/qnas`
- `naver_shopping_live_search_keywords()` → `GET /v1/naver/shopping/live/search/keywords`
- `naver_shopping_live_broadcast(broadcast_id)` → `GET /v1/naver/shopping/live/broadcasts/{broadcast_id}`
- `naver_shopping_live_broadcast_products(broadcast_id, page?, size?)` → `GET /v1/naver/shopping/live/broadcasts/{broadcast_id}/products`
- `naver_shopping_live_broadcast_counts(broadcast_id)` → `GET /v1/naver/shopping/live/broadcasts/{broadcast_id}/counts`
- `naver_shopping_live_channel(channel_id)` → `GET /v1/naver/shopping/live/channels/{channel_id}`
- `naver_shopping_live_channel_products(channel_id, next?, size?)` → `GET /v1/naver/shopping/live/channels/{channel_id}/products`
- `naver_shopping_live_channel_broadcasts(channel_id)` → `GET /v1/naver/shopping/live/channels/{channel_id}/broadcasts`
- `naver_shopping_live_channel_shortclips(channel_id, sort_type?, next?, size?)` → `GET /v1/naver/shopping/live/channels/{channel_id}/shortclips`
- `naver_product_detail(product_no, host?, store_url?, channel_uid?, broadcast_id?, live_channel_id?, query?)` → `GET /v1/naver/products/{product_no}`
- `naver_product_group(origin_product_no)` → `GET /v1/naver/products/{origin_product_no}/group`
- `naver_group_review_summary(group_product_no, leaf_category_id)` → `GET /v1/naver/product-groups/{group_product_no}/review-summary`
- `naver_shopping_search_catalog(query, sort?, page?)` → `GET /v1/naver/shopping/search-catalog`
- `naver_shopping_price_compare(query)` → `GET /v1/naver/shopping/price-compare`
- `naver_shopping_live_shortclip(shortclip_id)` → `GET /v1/naver/shopping/live/shortclips/{shortclip_id}`
- `naver_shopping_live_shortclip_products(shortclip_id, attachment_type?, page?, size?, sort?)` → `GET /v1/naver/shopping/live/shortclips/{shortclip_id}/products`
- `naver_shopping_live_replay_products(broadcast_id, include_before?, next?)` → `GET /v1/naver/shopping/live/broadcasts/{broadcast_id}/replay-products`
- `naver_shopping_live_broadcast_product_categories(broadcast_id, attachment_type?)` → `GET /v1/naver/shopping/live/broadcasts/{broadcast_id}/product-categories`

CLI: `scrapebadger naver --help`; `scrapebadger naver search "커피" --output json`; `scrapebadger naver place-reviews 11835250 --size 20`. Existing `bestsellers` and `insight` command names remain supported.

<!-- BEGIN ECOMMERCE DEDICATED APIS -->
## Etsy API

Etsy public ecommerce search, product, seller and review data.

Verified Etsy locale contexts are US/USD/en-US and GB/GBP/en-GB. Do not claim every other locale is verified. Etsy may offer approximate matches; use the returned query/pagination and listing IDs to inspect and deduplicate results. Shop names and numeric listing IDs are separate identifiers. Only parameters documented below are supported; no login, checkout or messaging actions are provided. Search category and taxonomy_id parameters were silently ignored by Etsy and are not exposed. /categories returns real navigation paths. Country, currency and language set page locale; verified US/USD/en-US and GB/GBP/en-GB. Shop and listing reviews use paginated DeepDive data. Sold listings need show_sold_out_detail=1. Search HTML initially contains a subset of listings; total_results is the site-reported count, not the returned page length.

| Request | Purpose | Credits |
| --- | --- | ---: |
| `GET /v1/etsy/search` | Search listings | 10 |
| `GET /v1/etsy/listings/{listing_id}` | Get listing detail | 10 |
| `GET /v1/etsy/shops/{shop_name}` | Get shop profile | 10 |
| `GET /v1/etsy/shops/{shop_name}/listings` | Get shop listings | 10 |
| `GET /v1/etsy/shops/{shop_name}/reviews` | Get shop reviews | 20 |
| `GET /v1/etsy/categories` | Get categories | 10 |
| `GET /v1/etsy/listings/{listing_id}/reviews` | Get listing reviews | 20 |
| `GET /v1/etsy/autocomplete` | Get search suggestions | 20 |

Parameters:

- GET /v1/etsy/search — Search listings. Parameters: query (string, required): query; page (integer, optional, default=1): page; country (string, optional, default="US"): country; currency (string, optional, default="USD"): currency; language (string, optional, default="en-US"): language; sort (string, optional, default="most_relevant", allowed=most_relevant,date_desc,price_asc,price_desc): sort; min_price (number, optional): min price; max_price (number, optional): max price.
- GET /v1/etsy/listings/{listing_id} — Get listing detail. Parameters: listing_id (string, required): listing id; country (string, optional, default="US"): country; currency (string, optional, default="USD"): currency; language (string, optional, default="en-US"): language.
- GET /v1/etsy/shops/{shop_name} — Get shop profile. Parameters: shop_name (string, required): shop name; country (string, optional, default="US"): country; currency (string, optional, default="USD"): currency; language (string, optional, default="en-US"): language.
- GET /v1/etsy/shops/{shop_name}/listings — Get shop listings. Parameters: shop_name (string, required): shop name; page (integer, optional, default=1): page; country (string, optional, default="US"): country; currency (string, optional, default="USD"): currency; language (string, optional, default="en-US"): language.
- GET /v1/etsy/shops/{shop_name}/reviews — Get shop reviews. Parameters: shop_name (string, required): shop name; page (integer, optional, default=1): page; country (string, optional, default="US"): country; currency (string, optional, default="USD"): currency; language (string, optional, default="en-US"): language.
- GET /v1/etsy/categories — Get categories. Parameters: country (string, optional, default="US"): country; currency (string, optional, default="USD"): currency; language (string, optional, default="en-US"): language.
- GET /v1/etsy/listings/{listing_id}/reviews — Get listing reviews. Parameters: listing_id (string, required): listing id; page (integer, optional, default=1): page; sort (string, optional, default="Relevancy", allowed=Relevancy,Recency,Highest,Lowest): sort; country (string, optional, default="US"): country; currency (string, optional, default="USD"): currency; language (string, optional, default="en-US"): language.
- GET /v1/etsy/autocomplete — Get search suggestions. Parameters: query (string, required): query; country (string, optional, default="US"): country; currency (string, optional, default="USD"): currency; language (string, optional, default="en-US"): language.

Example requests:

```http
GET /v1/etsy/search?query=ceramic+mug
X-API-Key: $SCRAPEBADGER_API_KEY
```

```http
GET /v1/etsy/listings/4589988962
X-API-Key: $SCRAPEBADGER_API_KEY
```

```http
GET /v1/etsy/shops/GlazyLittleThings
X-API-Key: $SCRAPEBADGER_API_KEY
```

```http
GET /v1/etsy/shops/GlazyLittleThings/listings
X-API-Key: $SCRAPEBADGER_API_KEY
```

```http
GET /v1/etsy/shops/GlazyLittleThings/reviews
X-API-Key: $SCRAPEBADGER_API_KEY
```

```http
GET /v1/etsy/categories
X-API-Key: $SCRAPEBADGER_API_KEY
```

```http
GET /v1/etsy/listings/4569788202/reviews
X-API-Key: $SCRAPEBADGER_API_KEY
```

```http
GET /v1/etsy/autocomplete?query=ceramic
X-API-Key: $SCRAPEBADGER_API_KEY
```

## AliExpress API

AliExpress public ecommerce search, product, seller and review data.

AliExpress US search and DE/EUR product detail are verified. Product data accepts the documented country/currency/language context. Do not promise every locale or filter until verified. Product IDs and store IDs are separate identifiers. Global category IDs and store-local category IDs come from different taxonomies and cannot be interchanged. Preserve returned review pagination and variant-level prices rather than assuming the first price applies to every option. This is public product data; no checkout or account actions are provided. Navigation category ids are frontend ids; product category_ids are taxonomy ids and store groups are separate. Search CatId widens into unrelated taxonomy results and is not exposed as a verified category filter. Product prices may be per SKU, destination and new shopper promotion; original source price maps are preserved. US search and DE/EUR product detail verified. Store categories can legitimately be empty for stores without product groups. Product detail validates product identity, currency, locale and populated variants.

| Request | Purpose | Credits |
| --- | --- | ---: |
| `GET /v1/aliexpress/search` | Search products | 5 |
| `GET /v1/aliexpress/products/{product_id}` | Get product detail | 10 |
| `GET /v1/aliexpress/products/{product_id}/reviews` | Get product reviews | 5 |
| `GET /v1/aliexpress/stores/{store_id}` | Get store profile | 10 |
| `GET /v1/aliexpress/stores/{store_id}/products` | Get store products | 10 |
| `GET /v1/aliexpress/autocomplete` | Get search suggestions | 5 |
| `GET /v1/aliexpress/categories` | Get category navigation | 5 |
| `GET /v1/aliexpress/stores/{store_id}/categories` | Get store product categories | 5 |

Parameters:

- GET /v1/aliexpress/search — Search products. Parameters: query (string, required): query; page (integer, optional, default=1): page; country (string, optional, default="US"): country; currency (string, optional, default="USD"): currency; language (string, optional, default="en"): language; sort (string, optional, default="default", allowed=default,price_asc,price_desc,total_tranpro_desc): sort; min_price (number, optional): min price; max_price (number, optional): max price.
- GET /v1/aliexpress/products/{product_id} — Get product detail. Parameters: product_id (string, required): product id; country (string, optional, default="US"): country; currency (string, optional, default="USD"): currency; language (string, optional, default="en_US"): language.
- GET /v1/aliexpress/products/{product_id}/reviews — Get product reviews. Parameters: product_id (string, required): product id; page (integer, optional, default=1): page; page_size (integer, optional, default=10): page size; sort (string, optional, default="complex_default", allowed=complex_default,latest_sort): sort.
- GET /v1/aliexpress/stores/{store_id} — Get store profile. Parameters: store_id (string, required): store id; country (string, optional, default="US"): country; currency (string, optional, default="USD"): currency; language (string, optional, default="en"): language.
- GET /v1/aliexpress/stores/{store_id}/products — Get store products. Parameters: store_id (string, required): store id; page (integer, optional, default=1): page; page_size (integer, optional, default=24): page size; country (string, optional, default="US"): country; currency (string, optional, default="USD"): currency; language (string, optional, default="en"): language; query (string, optional, default=""): query; sort (string, optional, default="bestmatch_sort", allowed=bestmatch_sort,price_asc,price_desc,orders_desc): sort.
- GET /v1/aliexpress/autocomplete — Get search suggestions. Parameters: query (string, required): query; country (string, optional, default="US"): country; language (string, optional, default="en"): language.
- GET /v1/aliexpress/categories — Get category navigation. Parameters: none.
- GET /v1/aliexpress/stores/{store_id}/categories — Get store product categories. Parameters: store_id (string, required): store id; country (string, optional, default="US"): country.

Example requests:

```http
GET /v1/aliexpress/search?query=wireless+mouse
X-API-Key: $SCRAPEBADGER_API_KEY
```

```http
GET /v1/aliexpress/products/3256806816805325
X-API-Key: $SCRAPEBADGER_API_KEY
```

```http
GET /v1/aliexpress/products/3256806816805325/reviews
X-API-Key: $SCRAPEBADGER_API_KEY
```

```http
GET /v1/aliexpress/stores/1103608546
X-API-Key: $SCRAPEBADGER_API_KEY
```

```http
GET /v1/aliexpress/stores/1103608546/products
X-API-Key: $SCRAPEBADGER_API_KEY
```

```http
GET /v1/aliexpress/autocomplete?query=wireless
X-API-Key: $SCRAPEBADGER_API_KEY
```

```http
GET /v1/aliexpress/categories
X-API-Key: $SCRAPEBADGER_API_KEY
```

```http
GET /v1/aliexpress/stores/301635/categories
X-API-Key: $SCRAPEBADGER_API_KEY
```

## Target API

Search Target US products, retrieve variants and prices, read reviews and questions, and monitor stores and stock.

Target coverage is the United States. Product TCIN, store ID and ZIP code have different roles: retain the same store_id/zip_code when comparing search, product detail and availability. Availability can vary by store and fulfilment option. Review and question pagination is separate from search pagination. Use category IDs returned by category/navigation responses; do not invent filters that are absent from the documented contract.

| Request | Purpose | Credits |
| --- | --- | ---: |
| `GET /v1/target/markets` | List supported markets | 0 |
| `GET /v1/target/search` | Search products | 5 |
| `GET /v1/target/category` | Browse a category | 5 |
| `GET /v1/target/autocomplete` | Get search suggestions | 5 |
| `GET /v1/target/stores` | Find nearby stores | 5 |
| `GET /v1/target/stores/{store_id}` | Get store detail | 5 |
| `GET /v1/target/categories` | Get categories | 5 |
| `GET /v1/target/products/{tcin}/reviews` | Get product reviews | 5 |
| `GET /v1/target/products/{tcin}/questions` | Get product questions | 5 |
| `GET /v1/target/products/{tcin}/availability` | Get product availability | 10 |
| `GET /v1/target/products/{tcin}` | Get product detail | 10 |

Parameters:

- GET /v1/target/markets — List supported markets. Parameters: none.
- GET /v1/target/search — Search products. Parameters: query (string, required): query; page (integer, optional, default=1): page; page_size (integer, optional, default=24): page size; store_id (string, optional, default="1375"): store id; zip_code (string, optional, default="55403"): zip code; sort (string, optional, default="relevance", allowed=relevance,PriceLow,PriceHigh,RatingHigh,bestselling,newest): sort.
- GET /v1/target/category — Browse a category. Parameters: category_id (string, required): category id; page (integer, optional, default=1): page; page_size (integer, optional, default=24): page size; store_id (string, optional, default="1375"): store id; zip_code (string, optional, default="55403"): zip code.
- GET /v1/target/autocomplete — Get search suggestions. Parameters: query (string, required): query.
- GET /v1/target/stores — Find nearby stores. Parameters: zip_code (string, required): zip code; limit (integer, optional, default=10): limit.
- GET /v1/target/stores/{store_id} — Get store detail. Parameters: store_id (string, required): store id.
- GET /v1/target/categories — Get categories. Parameters: category_id (string, optional, default="5xtly"): category id.
- GET /v1/target/products/{tcin}/reviews — Get product reviews. Parameters: tcin (string, required): tcin; page (integer, optional, default=1): page; page_size (integer, optional, default=10): page size; sort (string, optional, default="most_recent", allowed=most_recent,most_helpful,highest_rated,lowest_rated): sort.
- GET /v1/target/products/{tcin}/questions — Get product questions. Parameters: tcin (string, required): tcin; page (integer, optional, default=1): page; page_size (integer, optional, default=10): page size.
- GET /v1/target/products/{tcin}/availability — Get product availability. Parameters: tcin (string, required): tcin; zip_code (string, required): zip code; limit (integer, optional, default=10): limit.
- GET /v1/target/products/{tcin} — Get product detail. Parameters: tcin (string, required): tcin; store_id (string, optional, default="1375"): store id; zip_code (string, optional, default="55403"): zip code.

Example requests:

```http
GET /v1/target/markets
X-API-Key: $SCRAPEBADGER_API_KEY
```

```http
GET /v1/target/search?query=laptop&page=1&page_size=24&store_id=1375&zip_code=55403&sort=relevance
X-API-Key: $SCRAPEBADGER_API_KEY
```

```http
GET /v1/target/category?category_id=5xtly&page=1&page_size=24&store_id=1375&zip_code=55403
X-API-Key: $SCRAPEBADGER_API_KEY
```

```http
GET /v1/target/autocomplete?query=laptop
X-API-Key: $SCRAPEBADGER_API_KEY
```

```http
GET /v1/target/stores?zip_code=55403&limit=10
X-API-Key: $SCRAPEBADGER_API_KEY
```

```http
GET /v1/target/stores/1375
X-API-Key: $SCRAPEBADGER_API_KEY
```

```http
GET /v1/target/categories?category_id=5xtly
X-API-Key: $SCRAPEBADGER_API_KEY
```

```http
GET /v1/target/products/82286564/reviews?page=1&page_size=24&sort=most_recent
X-API-Key: $SCRAPEBADGER_API_KEY
```

```http
GET /v1/target/products/82286564/questions?page=1&page_size=24
X-API-Key: $SCRAPEBADGER_API_KEY
```

```http
GET /v1/target/products/80179068/availability?zip_code=55403&limit=10
X-API-Key: $SCRAPEBADGER_API_KEY
```

```http
GET /v1/target/products/80179068?store_id=1375&zip_code=55403
X-API-Key: $SCRAPEBADGER_API_KEY
```

## ASOS API

Search ASOS fashion products, retrieve rich product detail, monitor stock and prices, and browse navigation and search facets across storefronts.

ASOS search uses native semantic ranking (search_mode=semantic), so approximate matches may appear; there is no exact-match guarantee. Brand, colour, size, category and price filters constrain inventory. Product copy and size labels follow market; explicit store/country/currency/language overrides refresh current stock/pricing, and returned currency is checked. Embedded reviews are a sample, not a separate paginated review service. Category navigation includes link.categoryId. Price ranges are applied to returned products; zero-price searches do not widen the result set.

| Request | Purpose | Credits |
| --- | --- | ---: |
| `GET /v1/asos/search` | Search ASOS products | 5 |
| `GET /v1/asos/products/{product_id}` | Get ASOS product detail | 10 |
| `GET /v1/asos/stock-price` | Get ASOS stock and price | 10 |
| `GET /v1/asos/categories` | Get category navigation | 5 |
| `GET /v1/asos/autocomplete` | Autocomplete ASOS searches | 3 |
| `GET /v1/asos/filters` | Get search facets | 5 |
| `GET /v1/asos/markets` | List ASOS storefronts | 0 |

Parameters:

- GET /v1/asos/search — Search ASOS products. Parameters: query (string, optional): query; category_id (integer, optional): category id; offset (integer, optional, default=0): offset; limit (integer, optional, default=48): limit; sort (string, optional, default="recommended", allowed=recommended,freshness,priceasc,pricedesc): sort; brand (string, optional): brand; colour (string, optional): colour; size (string, optional): size; min_price (number, optional): min price; max_price (number, optional): max price; market (string, optional, default="uk"): market; store (string, optional): store; country (string, optional): country; currency (string, optional): currency; language (string, optional): language.
- GET /v1/asos/products/{product_id} — Get ASOS product detail. Parameters: product_id (integer, required): product id; market (string, optional, default="uk"): market; store (string, optional): store; country (string, optional): country; currency (string, optional): currency; language (string, optional): language.
- GET /v1/asos/stock-price — Get ASOS stock and price. Parameters: product_ids (string, required): product ids; market (string, optional, default="uk"): market; store (string, optional): store; country (string, optional): country; currency (string, optional): currency; language (string, optional): language.
- GET /v1/asos/categories — Get category navigation. Parameters: gender (string, optional, default="men", allowed=men,women): gender; market (string, optional, default="uk"): market; store (string, optional): store; country (string, optional): country; currency (string, optional): currency; language (string, optional): language.
- GET /v1/asos/autocomplete — Autocomplete ASOS searches. Parameters: query (string, required): query; market (string, optional, default="uk"): market; store (string, optional): store; country (string, optional): country; currency (string, optional): currency; language (string, optional): language.
- GET /v1/asos/filters — Get search facets. Parameters: query (string, optional): query; category_id (integer, optional): category id; market (string, optional, default="uk"): market; store (string, optional): store; country (string, optional): country; currency (string, optional): currency; language (string, optional): language.
- GET /v1/asos/markets — List ASOS storefronts. Parameters: none.

Example requests:

```http
GET /v1/asos/search?query=shoes&limit=2
X-API-Key: $SCRAPEBADGER_API_KEY
```

```http
GET /v1/asos/products/209555590
X-API-Key: $SCRAPEBADGER_API_KEY
```

```http
GET /v1/asos/stock-price?product_ids=209555590
X-API-Key: $SCRAPEBADGER_API_KEY
```

```http
GET /v1/asos/categories?gender=men
X-API-Key: $SCRAPEBADGER_API_KEY
```

```http
GET /v1/asos/autocomplete?query=sho
X-API-Key: $SCRAPEBADGER_API_KEY
```

```http
GET /v1/asos/filters?query=shoes
X-API-Key: $SCRAPEBADGER_API_KEY
```

```http
GET /v1/asos/markets
X-API-Key: $SCRAPEBADGER_API_KEY
```

## Best Buy API

Search Best Buy US products, compare deals and specifications, read reviews and questions, and check ZIP-specific fulfillment.

Best Buy coverage is the United States. Product SKUs and category IDs are separate identifiers. Availability uses the documented ZIP/store context; a catalogue product is not a guarantee that a particular store has stock. Reviews, questions and product search have separate pagination. The deals endpoint covers the verified laptop/computer deals surface, not every promotion on the website.

| Request | Purpose | Credits |
| --- | --- | ---: |
| `GET /v1/bestbuy/markets` | List supported markets | 0 |
| `GET /v1/bestbuy/search` | Search products | 10 |
| `GET /v1/bestbuy/category` | Browse a category | 10 |
| `GET /v1/bestbuy/categories` | Get categories | 5 |
| `GET /v1/bestbuy/deals` | Get laptop and computer deals | 10 |
| `GET /v1/bestbuy/autocomplete` | Get search suggestions | 5 |
| `GET /v1/bestbuy/products/{sku}/reviews` | Get product reviews | 5 |
| `GET /v1/bestbuy/products/{sku}/questions` | Get product questions | 5 |
| `GET /v1/bestbuy/products/{sku}/availability` | Get product availability | 5 |
| `GET /v1/bestbuy/products/{sku}` | Get product detail | 10 |

Parameters:

- GET /v1/bestbuy/markets — List supported markets. Parameters: none.
- GET /v1/bestbuy/search — Search products. Parameters: query (string, required): query; page (integer, optional, default=1): page; sort (string, optional, default="best_match", allowed=best_match,best_selling,price_low,price_high,rating,newest): sort.
- GET /v1/bestbuy/category — Browse a category. Parameters: category_id (string, required): category id; page (integer, optional, default=1): page.
- GET /v1/bestbuy/categories — Get categories. Parameters: query (string, optional, default="laptop"): query.
- GET /v1/bestbuy/deals — Get laptop and computer deals. Parameters: page (integer, optional, default=1): page.
- GET /v1/bestbuy/autocomplete — Get search suggestions. Parameters: query (string, required): query.
- GET /v1/bestbuy/products/{sku}/reviews — Get product reviews. Parameters: sku (string, required): sku; page (integer, optional, default=1): page; page_size (integer, optional, default=10): page size; sort (string, optional, default="MOST_RECENT", allowed=MOST_RECENT,BEST_REVIEW,MOST_HELPFUL,OLDEST,HIGHEST_RATING,LOWEST_RATING): sort.
- GET /v1/bestbuy/products/{sku}/questions — Get product questions. Parameters: sku (string, required): sku; page (integer, optional, default=1): page; page_size (integer, optional, default=10): page size; query (string, optional, default=""): query.
- GET /v1/bestbuy/products/{sku}/availability — Get product availability. Parameters: sku (string, required): sku; zip_code (string, required): zip code; store_id (string, optional, default="7"): store id.
- GET /v1/bestbuy/products/{sku} — Get product detail. Parameters: sku (string, required): sku.

Example requests:

```http
GET /v1/bestbuy/markets
X-API-Key: $SCRAPEBADGER_API_KEY
```

```http
GET /v1/bestbuy/search?query=laptop&page=1&sort=best_match
X-API-Key: $SCRAPEBADGER_API_KEY
```

```http
GET /v1/bestbuy/category?category_id=pcmcat138500050001&page=1
X-API-Key: $SCRAPEBADGER_API_KEY
```

```http
GET /v1/bestbuy/categories?query=laptop
X-API-Key: $SCRAPEBADGER_API_KEY
```

```http
GET /v1/bestbuy/deals?page=1
X-API-Key: $SCRAPEBADGER_API_KEY
```

```http
GET /v1/bestbuy/autocomplete?query=laptop
X-API-Key: $SCRAPEBADGER_API_KEY
```

```http
GET /v1/bestbuy/products/6668412/reviews?page=1&page_size=10&sort=MOST_RECENT
X-API-Key: $SCRAPEBADGER_API_KEY
```

```http
GET /v1/bestbuy/products/6668412/questions?page_size=10&query=&page=1
X-API-Key: $SCRAPEBADGER_API_KEY
```

```http
GET /v1/bestbuy/products/6668412/availability?zip_code=55423&store_id=7
X-API-Key: $SCRAPEBADGER_API_KEY
```

```http
GET /v1/bestbuy/products/6668412
X-API-Key: $SCRAPEBADGER_API_KEY
```
<!-- END ECOMMERCE DEDICATED APIS -->

## GitHub Profile API

Prepared for the GitHub rollout; examples are representative, not production results.
Use `GET /v1/github/profiles/{username}` with your ScrapeBadger `X-API-Key`.
`username` is a login or `@handle`, never a profile URL. Accounts are global;
there is no market or language parameter and no GitHub access token is needed.

- `tab=overview` (default): public identity, pins or popular repositories, README,
  sponsors/highlights and public user contribution calendar/activity. `year`
  selects a whole calendar year; its timeline is December for past years or the
  current month for the current year. Without `year`, the calendar is the last
  12 months and the timeline is the current month. Organizations omit calendars.
- `tab=repositories&page=2`: public profile repositories, 30 rows per page.
  Follow `pagination.next_page` only while `pagination.has_next` is true.
- `tab=stars&next_page_token=...`: user stars and star lists, 30 rows per page.
  Reuse the exact opaque `pagination.next_page_token`; do not decode it or pass a
  next URL. Organization stars are unsupported.

`year` is overview-only, `page` repositories-only, and `next_page_token`
stars-only. Each successful request costs **10 credits in every mode**, including
paginated requests. Do not assume all public fields are present: omitted sections
mean unavailable/not applicable, explicit `null` metadata remains null, and only
recognized source empty states produce empty lists. Failed/blocked upstream reads
are errors, not empty successes. Exact supplemental counts retain native display
counts; compact source counts carry `*_approximate`. Dates have ISO `*_at` and
Unix-seconds `*_utc` pairs where available. No live latency claim is established.

MCP/OpenClaw: `github_get_profile(username, tab?, year?, page?, next_page_token?)`.
List it directly with `https://mcp.scrapebadger.com/mcp?apis=github`, or discover
it through `search_endpoints(api="github")`.

Representative requests:
```text
GET /v1/github/profiles/sindresorhus?tab=overview&year=2024
GET /v1/github/profiles/rails?tab=repositories&page=2
GET /v1/github/profiles/sindresorhus?tab=stars&next_page_token=OPAQUE_TOKEN
```

CLI:
```bash
scrapebadger github profile sindresorhus --year 2024
scrapebadger github profile rails --tab repositories --page 2
scrapebadger github profile sindresorhus --tab stars --next-page-token 'OPAQUE_TOKEN'
```

This surface does not provide general GitHub search, standalone repository detail,
trending, private repositories, private member views or member-only README content.
Reference: https://docs.scrapebadger.com/github/profiles

### Public repository detail

`GET /v1/github/repositories/{owner}/{repo}` returns public default-branch
statistics, topics, language/license metadata, native README, root files and the
latest commit. Use `owner.login` and `name` from a profile repository summary.
No query options or GitHub token are needed; restricted keys require `github`.
Every successful uncached response costs 10 credits; health/errors cost zero,
and cache hits can be free. Native empty repositories retain an explicit state.
Watchers mean subscribers, not stars. Compact issue/PR counts retain precision
flags, and preview arrays are not exhaustive recursive or membership lists.

MCP/OpenClaw: `github_get_repository(owner, repo)`.
CLI: `scrapebadger github repository cli cli`.
Python: `await client.github.get_repository("cli", "cli")`.
Node: `await client.github.getRepository("cli", "cli")`.
Pass identifiers separately and reject standalone `.`/`..` path segments.
Reference: https://docs.scrapebadger.com/github/repositories


## AutoScout24 Search and Listing API

Base: https://scrapebadger.com/v1/autoscout24 (X-API-Key authentication).
- GET /search — market (de/at/be/es/fr/it/lu/nl; default de), optional make/model native slugs; price_min/max EUR, mileage_min/max km, year_min/max first registration, power_min/max kW, fuel_type, transmission, body_type, seller_type, condition, zip/radius km, sort_by, page1–200. Search costs5 credits; genuine empty results and failures cost0.
- GET /listing — exactly one url or listing_id from search, optional market. URL infers market, otherwise de; an explicit market must match URL. Full native specs, equipment, photos, pricing, history, public seller/contact/location and optional commercial data.10 credits; failures and removed listings are free.
- GET /filters — market, optional make. Current native make/model/filter taxonomy.2 credits.
- GET /markets — eight verified marketplace/domain/language/currency records. Free.
- GET or HEAD /health — service health. Free.
Search returns results[], total_results, total_pages, page, page_size20, has_next_page, next_page, pagination_cap200, filters, applied_filters, source_url and latency_ms. Card fields include price/currency, make/model/variant, mileage_km, first_registration YYYY-MM, power_kw/hp, public seller phones/rating/profile links, location and images. Follow next_page; fewer than20 returned cards does not imply the last page. Narrow filters beyond the native200-page cap. Pass a card URL/ID to /listing for the full listing envelope (market, source_url, listing, latency_ms). Listing retains complete useful native vehicle/rawData, equipment groups, prices including VAT/evaluation bands, history/energy, seller/ratings/location, all photos and optional warranty/lease/finance/media fields. Missing values remain unknown; month precision registration has no fabricated day. Full timestamps include ISO UTC and Unix pairs. Swiss listings are unsupported. Removed/missing404, invalid422 and source503 are unbilled.

```bash
curl 'https://scrapebadger.com/v1/autoscout24/search?market=de&make=volkswagen&model=golf&price_max=20000' -H "X-API-Key: $SCRAPEBADGER_API_KEY"
scrapebadger autoscout24 search --market de --make volkswagen --model golf --price-max 20000
scrapebadger autoscout24 listing --url 'LISTING_URL_FROM_SEARCH'
scrapebadger autoscout24 listing --listing-id UUID --market it
```

## Brave Search API

Base: https://scrapebadger.com/v1/brave. Header: X-API-Key. Scope: brave.
Native public Brave Search; no Brave account or paid upstream key needed.

GET /search?query=... — 7 credits. country=us, ui_language=en-us,
safe_search=off|moderate|strict (default moderate), page=1..10,
count=1..20 (default20), freshness=any|day|week|month|year (default any),
spellcheck=false. Returns organic results plus source-provided FAQ,
discussions, inline videos/news/images, related_searches and rich_blocks.
GET /images?query=... — 7 credits. Same locale and safe-search controls;
count=1..200 (default50). Initial native image batch; no pagination.
GET /videos?query=... — 7 credits. Same locale/safe-search controls;
page=1..10, count=1..50 (default50).
GET /news?query=... — 7 credits. Same locale/safe-search controls;
count=1..50 (default35). Initial native news batch; no pagination.
GET /locales — 0 credits. Native countries and ui_languages choices.

query is required, nonblank, max2048 characters. ui_language controls labels,
not result language. country selects the region; all means all regions.
Web/video page is a 1-based native page ordinal. count slices one page and
does not change source page boundaries; do not compute page from count.
Follow has_next/next_page. Empty confirmed source results and errors are unbilled.

Response: query, country, ui_language, safe_search, result_count, results[],
query_info (including source query alteration/relaxation metadata), source_url,
fetched_at (ISO UTC), fetched_utc (Unix). Web/video add page, has_next,next_page.
Results include position,title,url,snippet,description,display_url,site_name,
profile,meta_url,thumbnail,source-specific enrichments and publication dates
only when supplied. Relative ages stay text; do not treat fetched_at as publish time.
Rich blocks vary by query. Search returns no AI Mode or generated answers.

CLI: scrapebadger brave search "coffee machine" --page 2 --country de --ui-language de-de
MCP: brave_search, brave_images, brave_videos, brave_news, brave_autocomplete, brave_locales.
Docs: https://docs.scrapebadger.com/brave/overview

```bash
curl -G https://scrapebadger.com/v1/brave/search \
  -H "X-API-Key: $SCRAPEBADGER_API_KEY" \
  --data-urlencode 'query=coffee machine' --data-urlencode 'country=us' \
  --data-urlencode 'page=1' --data-urlencode 'freshness=week'
```

GET /v1/brave/autocomplete?query=coff&country=us — 2 credits. Native search-box suggestions with query/type/is_entity and optional name/desc/img/category/logo. Returns query,country,result_count,suggestions[],source_url,fetched_at,fetched_utc. Confirmed empty suggestions are free.

## Yelp Search API

Base: https://scrapebadger.com/v1/yelp. Header: X-API-Key. Scope: yelp.
Public Yelp business search; no Yelp account or Places API key needed. Business detail and reviews are not included.

`yelp_search_businesses` — ranked businesses for a location, 15 credits; empty results free. location is required (city, neighbourhood, address or postcode); query optional when category (Yelp alias, e.g. pizza) is set. sort_by recommended|rating|review_count, price comma list 1..4, features comma list (delivery, takeout, reservations, outdoor_seating, good_for_kids, dogs_allowed, free_wifi, wheelchair_accessible), page 1..11 (ten per page). A filter Yelp does not apply returns 422; an unknown location 400; neither is billed. Organic results[] keep Yelp's rank; sponsored listings are in ads[].
`yelp_list_markets` — Yelp sites this API searches: us (yelp.com) and ca (yelp.ca); free.

CLI: `scrapebadger yelp search "San Francisco, CA" -q pizza --sort-by rating --page 2`; `scrapebadger yelp markets`.

```bash
curl -G https://scrapebadger.com/v1/yelp/search \
  -H "X-API-Key: $SCRAPEBADGER_API_KEY" \
  --data-urlencode 'location=San Francisco, CA' --data-urlencode 'query=pizza' \
  --data-urlencode 'sort_by=rating' --data-urlencode 'page=1'
```
