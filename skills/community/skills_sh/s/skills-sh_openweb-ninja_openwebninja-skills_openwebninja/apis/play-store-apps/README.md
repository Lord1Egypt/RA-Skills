# play-store-apps

> Full OpenAPI spec: https://openwebninja.s3.us-east-1.amazonaws.com/portal/openapi/play_store_apps.yaml

**Host:** `store-apps.p.rapidapi.com`
**Notes:** Cursor-based pagination. The response includes a 'cursor' field to fetch the next page.

## Endpoints

### GET /search
Search — Search for apps on the Store.

**Required:**
- `q` (string) — Search query. Example: `notes`

**Optional:**
- `cursor` (string) — Specify a cursor from the previous request to get the next set of results.
- `region` (string, default: us) Example: `us`
- `language` (string, default: en) Example: `en`

**Pagination:** cursor (param: `cursor`)

---

### GET /app-reviews
App Reviews — Get all app reviews.

**Required:**
- `app_id` (string) — App Id of the app for which to get reviews. Example: `com.snapchat.android`

**Optional:**
- `limit` (integer, default: 20) Example: `10`
- `cursor` (string) — Specify a cursor from the previous request to get the next set of results.
- `sort_by` (string, default: MOST_RELEVANT) — values: MOST_RELEVANT, NEWEST, RATING
- `device` (string, default: PHONE) — values: PHONE, TABLET, CHROMEBOOK
- `rating` (string, default: ANY) — values: ANY, ONE_STAR, TWO_STARS, THREE_STARS, FOUR_STARS, FIVE_STARS
- `region` (string, default: US) Example: `US`
- `language` (string, default: EN) Example: `EN`

**Pagination:** cursor (param: `cursor`)
**Page size param:** `limit` (default: 20)
**Response path:** `data`
**Key fields:** review_id, review_text, review_rating, author_id, author_name, author_photo, author_app_version, review_timestamp, review_datetime_utc, review_likes, app_developer_reply, app_developer_reply_timestamp, app_developer_reply_datetime_utc

---

### GET /app-details
App Details — Get full app details.

**Required:**
- `app_id` (string) — App Id. Batching of up to 100 App Ids is supported by separating multiple ids by comma (e.g. com.snapchat.android,com.mi Example: `com.google.android.apps.subscriptions.red`

**Optional:**
- `region` (string, default: US) Example: `US`
- `language` (string, default: EN) Example: `EN`

**Pagination:** none
**Response path:** `data`
**Key fields:** app_id, app_name, app_category, app_category_id, app_developer, num_downloads, app_description, app_page_link, price, price_currency, is_paid, rating, app_icon, trailer, num_downloads_exact, app_content_rating, chart_label, chart_rank, app_updated_at_timestamp, app_updated_at_datetime_utc, num_ratings, num_reviews, app_first_released_at_datetime_utc, app_first_released_at_timestamp, current_version, current_version_released_at_timestamp, current_version_released_at_datetime_utc, current_version_whatsnew, contains_ads, privacy_policy_link, app_developer_website, app_developer_email, min_android_version, min_android_api_level, max_android_version, max_android_api_level, photos, reviews_per_rating, data_shared_by_app_and_why, data_collected_by_app_and_why, security_practices, app_permissions

---

### GET /categories
App Categories — Get the full list of Google Play app categories. The returned categories can be used with the Charts endpoints (as the category parameter).

**Pagination:** none
**Response path:** `data`
**Key fields:** id

---

### GET /top-grossing-apps
Top Grossing Apps — Top grossing apps chart. Supports getting the chart for specific Google Play categories.

**Optional:**
- `category` (string) — Get the chart in a specific Google Play category (e.g. SOCIAL).
- `limit` (integer, default: 50) Example: `50`
- `region` (string, default: US) Example: `US`
- `language` (string, default: EN) Example: `EN`

**Pagination:** none
**Page size param:** `limit` (default: 50)

---

### GET /top-paid-apps
Top Paid Apps — Top paid apps chart. Supports getting the chart for specific Google Play categories.

**Optional:**
- `category` (string) — Get the chart in a specific Google Play category (e.g. SOCIAL).
- `limit` (integer, default: 50) Example: `50`
- `region` (string, default: US) Example: `US`
- `language` (string, default: EN) Example: `EN`

**Pagination:** none
**Page size param:** `limit` (default: 50)

---

### GET /top-free-apps
Top Free Apps — Top free apps chart. Supports getting the chart for specific Google Play categories.

**Optional:**
- `category` (string) — Get the chart in a specific Google Play category (e.g. SOCIAL).
- `limit` (integer, default: 50) Example: `50`
- `region` (string, default: US) Example: `US`
- `language` (string, default: EN) Example: `EN`

**Pagination:** none
**Page size param:** `limit` (default: 50)

---

### GET /top-free-games
Top Free Games — Top free games chart. Supports getting the chart for specific Google Play categories.

**Optional:**
- `category` (string) — Get the chart in a specific Google Play category (e.g. SOCIAL).
- `limit` (integer, default: 50) Example: `50`
- `region` (integer, default: US) Example: `US`
- `language` (string, default: EN) Example: `EN`

**Pagination:** none
**Page size param:** `limit` (default: 50)

---

### GET /top-grossing-games
Top Grossing Games — Top grossing games chart. Supports getting the chart for specific Google Play categories.

**Optional:**
- `category` (string) — Get the chart in a specific Google Play category (e.g. SOCIAL).
- `limit` (integer, default: 50) Example: `50`
- `region` (integer, default: US) Example: `US`
- `language` (string, default: EN) Example: `EN`

**Pagination:** none
**Page size param:** `limit` (default: 50)

---

### GET /top-paid-games
Top Paid Games — Top paid games chart. Supports getting the chart for specific Google Play categories.

**Optional:**
- `category` (string) — Get the chart in a specific Google Play category (e.g. SOCIAL).
- `limit` (integer, default: 50) Example: `50`
- `region` (integer, default: US) Example: `US`
- `language` (string, default: EN) Example: `EN`

**Pagination:** none
**Page size param:** `limit` (default: 50)

---
