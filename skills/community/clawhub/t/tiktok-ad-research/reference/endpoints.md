# tiktok-ad-research — endpoint reference

> Generated from `scripts/tools.json` by `scripts/generate.mjs` — do not edit by hand.

Only the endpoints used by this workflow. Call them via `scripts/crawlora.sh` (see SKILL.md).

All paths are relative to the API base `https://api.crawlora.net/api/v1` and require the header `x-api-key: $CRAWLORA_API_KEY`. Path params like `{id}` are substituted into the URL; `GET` params go in the query string; `POST` params go in a JSON body.

**10 endpoints across 1 platform group(s).**

## TikTok (10)

### `tiktok_top_ads_analysis`

- **HTTP:** `GET /tiktok/top-ads/analysis`
- **What:** Retrieve TikTok Top Ads interactive time analysis. Returns the detail-page interactive time analysis chart and percentile for a Top Ads material. Metric values are `retain_ctr` (CTR), `retain_cvr` (CVR), `click_cnt` (Clicks), `convert_cnt` (Conversion), and `play_retain_cnt` (Remain).
- **Params:** `material_id` (string, **required**) — Top Ads material id; `metric` (string, optional) — Interactive time analysis metric; `period_type` (integer, optional) — Percentile lookback period in days

### `tiktok_top_ads_detail`

- **HTTP:** `GET /tiktok/top-ads/detail`
- **What:** Retrieve TikTok Top Ads detail. Returns detail for one TikTok Creative Center Top Ads material. Use `material_id`; the upstream does not accept `id` or `materialId`.
- **Params:** `material_id` (string, **required**) — Top Ads material id

### `tiktok_top_ads_filters`

- **HTTP:** `GET /tiktok/top-ads/filters`
- **What:** Retrieve TikTok Top Ads filters. Returns filter metadata for TikTok Creative Center Top Ads. Dynamic values come from TikTok; static UI enums are included for `order_by`, `duration`, `like`, and `ad_format`.
- **Params:** _none_

### `tiktok_top_ads_list`

- **HTTP:** `GET /tiktok/top-ads/list`
- **What:** Retrieve TikTok Top Ads. Returns high-performing auction ads from TikTok Creative Center. The service defaults `period` to 30, `page` to 1, `limit` to 20, and `order_by` to `for_you`. Use `/tiktok/top-ads/filters` for dynamic enum values and static enums for order, duration, likes, and ad format.
- **Params:** `ad_format` (string, optional) — Ad format id; `ad_language` (string, optional) — Ad language id or comma-separated ids from /tiktok/top-ads/filters; `country_code` (string, optional) — Country code or comma-separated country codes from /tiktok/top-ads/filters; `duration` (string, optional) — Video duration bucket; `industry` (string, optional) — Industry filter id or comma-separated ids from /tiktok/top-ads/filters; `keyword` (string, optional) — Brand or product keyword search; `like` (string, optional) — Like percentile bucket id or comma-separated ids; `limit` (integer, optional) — Maximum number of ads to return; `objective` (string, optional) — Objective filter id or comma-separated ids from /tiktok/top-ads/filters; `order_by` (string, optional) — Sort order; `page` (integer, optional) — Page number; `pattern_label` (string, optional) — Pattern label id or comma-separated ids from /tiktok/top-ads/filters; `period` (integer, optional) — Lookback period in days

### `tiktok_top_ads_location_info`

- **HTTP:** `GET /tiktok/top-ads/location-info`
- **What:** Retrieve TikTok Top Ads location info. Returns TikTok's inferred initial country and industry targeting context for Top Ads. Use it when you need starting targeting values; use the locations, filters, and list endpoints to choose criteria and retrieve ads.
- **Params:** `module` (integer, optional) — Optional upstream Creative Center module identifier; omitted or 0 defaults to 1, other nonzero IDs are passed through without local range validation

### `tiktok_top_ads_locations`

- **HTTP:** `GET /tiktok/top-ads/locations`
- **What:** Retrieve TikTok Top Ads locations. Lists the country filters offered by TikTok Creative Center Top Ads. Each country has an `id` such as `US`, a `value` (the country name), a `label` and a `has_conversion` flag. Takes no parameters.
- **Params:** _none_

### `tiktok_top_ads_recommend`

- **HTTP:** `GET /tiktok/top-ads/recommend`
- **What:** Retrieve TikTok Top Ads recommendations. Lists Top Ads materials that TikTok Creative Center recommends as related to the ad with `material_id`. `page` starts at 1; `limit` defaults to 20 and is capped at 100. Each ad has its title, brand, likes, comments, shares, CTR, objectives and video info. The list can be empty for a valid id.
- **Params:** `limit` (integer, optional) — Maximum number of ads to return; `material_id` (string, **required**) — Top Ads material id; `page` (integer, optional) — Page number

### `tiktok_top_ads_safety`

- **HTTP:** `GET /tiktok/top-ads/safety`
- **What:** Retrieve TikTok Top Ads safety configuration. Returns the Creative Center safety configuration flags for search: `top_ads_search`, `keyword_search`, `hashtag_search`, `creator_search`, `sound_search` and `cc_banner_key`. It carries feature flags only, not ad materials. Takes no parameters.
- **Params:** _none_

### `tiktok_top_ads_spotlight`

- **HTTP:** `GET /tiktok/top-ads/spotlight`
- **What:** Retrieve TikTok Top Ads Spotlight. Lists the Top Ads Spotlight materials that TikTok Creative Center hand-picks. `page` starts at 1; `limit` defaults to 20 and is capped at 100. Each ad has its title, brand, likes, comments, shares, CTR, objectives and video info. `data.pagination` gives the page, size, total and `has_more`.
- **Params:** `limit` (integer, optional) — Maximum number of ads to return; `page` (integer, optional) — Page number

### `tiktok_top_ads_suggestions`

- **HTTP:** `GET /tiktok/top-ads/suggestions`
- **What:** Retrieve TikTok Top Ads suggestions. Returns Top Ads search suggestions from TikTok Creative Center. `count` is the maximum number of suggestions (default 50) and `scenario` picks the suggestion scenario id (default 1). The `query` list can be empty for the default scenario.
- **Params:** `count` (integer, optional) — Maximum number of suggestions to return; `scenario` (integer, optional) — Suggestion scenario id
