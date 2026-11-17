# social-media-research — endpoint reference

> Generated from `scripts/tools.json` by `scripts/generate.mjs` — do not edit by hand.

Endpoints this skill uses, grouped by platform. Call them via `scripts/crawlora.sh` (see SKILL.md).

All paths are relative to the API base `https://api.crawlora.net/api/v1` and require the header `x-api-key: $CRAWLORA_API_KEY`. Path params like `{id}` are substituted into the URL; `GET` params go in the query string; `POST` params go in a JSON body.

**111 endpoints across 11 platform group(s).**

## Instagram (3)

### `instagram_post`

- **HTTP:** `GET /instagram/post/{id}/{post_id}`
- **What:** Retrieve a specific Instagram post by URL shortcode. Returns media details for an Instagram URL shortcode. Use media.code from the reels response or shortcode from a public post URL; numeric media IDs are rejected.
- **Params:** `id` (string, **required**) — Instagram user ID retained for route compatibility; ownership is not verified; `post_id` (string, **required**) — Instagram URL shortcode (media.code), not a numeric media ID

### `instagram_profile`

- **HTTP:** `GET /instagram/profile/{username}`
- **What:** Retrieve an Instagram user profile by username. Returns the public profile of an Instagram account by `username`. The response has the user id, full name, biography, bio links, external URL, category, follower, following and post counts, verified and private flags, location, profile picture, recent posts with captions and like counts, and related profiles.
- **Params:** `username` (string, **required**) — Instagram username

### `instagram_reels`

- **HTTP:** `GET /instagram/reels/{id}`
- **What:** Retrieve Instagram Reels for a user. Returns up to 12 public Reels via anonymous proxied HTTP for the numeric Instagram user ID. Supports opaque `max_id` pagination. Captions, timestamps and original image dimensions are omitted when the public source does not expose them.
- **Params:** `id` (string, **required**) — Numeric Instagram user ID (not a username); `max_id` (string, optional) — Pagination cursor for fetching the next page of Reels

## TikTok (45)

### `tiktok_category`

- **HTTP:** `GET /tiktok/category`
- **What:** List TikTok explore categories. Returns the content categories shown on TikTok's Explore page. Each entry has the category name and its numeric type code. Takes no parameters.
- **Params:** _none_

### `tiktok_challenge`

- **HTTP:** `GET /tiktok/hashtag/{name}`
- **What:** Retrieve TikTok hashtag details. Returns the details of a TikTok hashtag page by `name`, for example `christmas`. The response carries `challengeInfo` with the hashtag's metadata, such as cover images, and `shareMeta` with the share title and description. The hashtag id found here feeds `tiktok-challenge-list`.
- **Params:** `name` (string, **required**) — Hashtag name (e.g., 'christmas')

### `tiktok_challenge_list`

- **HTTP:** `GET /tiktok/hashtags`
- **What:** Retrieve TikTok hashtag posts. Lists the videos posted under a TikTok hashtag, identified by the hashtag `id` from the hashtag detail endpoint. `cursor` defaults to 0. The response has `itemList`, `hasMore` and a `cursor`; pass that cursor back to fetch the next page.
- **Params:** `cursor` (integer, optional) — Pagination cursor; `id` (string, **required**) — Hashtag id returned by the hashtag detail endpoint

### `tiktok_comments`

- **HTTP:** `GET /tiktok/comments`
- **What:** Retrieve TikTok video comments. Returns the top-level comments on a TikTok video, by the video id from its URL (`aweme_id`). Results are paged by cursor: pass the `cursor` from one response to get the next page, and read `has_more` to see whether more remain. The response also carries the total comment count.
- **Params:** `aweme_id` (string, **required**) — TikTok video id from the video URL; `cursor` (integer, optional) — Pagination cursor

### `tiktok_creative_center_filters`

- **HTTP:** `GET /tiktok/creative-center/filters`
- **What:** Retrieve TikTok Creative Center filter taxonomy. Returns the complete filter taxonomy for the Creative Center trend endpoints: the countries each trend tab reports, the industry ids and video content tags the filters accept, the supported lookback periods, and the video sort metrics. Use it to discover valid values for the hashtags endpoint's country_code, period, and industry_id parameters and the videos endpoint's country_code, period, sort_by, and content_label_ids parameters. This endpoint performs no upstream request and has no parameters.
- **Params:** _none_

### `tiktok_creative_center_hashtags`

- **HTTP:** `GET /tiktok/creative-center/hashtags`
- **What:** Retrieve TikTok Creative Center trending hashtags. Returns TikTok Creative Center's ranked trending hashtags for a country, period, and optional industry. TikTok gates this endpoint's full result set behind a logged-in TikTok One account: an anonymous request always receives at most 3 hashtags per filter combination regardless of country, period, or industry, so selecting an industry returns that industry's own ranked top three. See the filters endpoint for the complete country, period, and industry value lists.
- **Params:** `country_code` (string, **required**) — ISO-2 country code; `industry_id` (string, optional) — Creative Center industry id to restrict the ranking to; `period` (integer, optional) — Lookback window in days

### `tiktok_creative_center_top_content`

- **HTTP:** `GET /tiktok/creative-center/top-content`
- **What:** Retrieve TikTok Creative Center top content. Returns TikTok Creative Center's current Top Content set: four top-performing branded videos, each with the video object (anonymous MP4 and cover URLs), engagement metrics, the author profile and follower count, and (by default) the video's top comments plus keyword mention counts derived from them. The set is a daily snapshot and there is no pagination or historical query; the four titles rotate when the snapshot changes. Set include_comments=false for a smaller response with only video, author, and metrics.
- **Params:** `include_comments` (boolean, optional) — Include each object's top comments and comment-keyword counts

### `tiktok_creative_center_videos`

- **HTTP:** `GET /tiktok/creative-center/videos`
- **What:** Retrieve TikTok Creative Center trending videos. Returns TikTok Creative Center's ranked trending videos for a country, period, sort order, and optional content tags. TikTok reports the true result-set size (see total_count/page_count in the response) but gates access to it behind a logged-in TikTok One account: an anonymous request always receives page 1 (4 videos) regardless of sort order or period. Country coverage is uneven: only US, JP, ID, VN, and TH have a regional edge host that returns populated results; other countries return an empty videos array (a genuine no-data response, not an error). See the filters endpoint for the complete country, period, sort, and content tag value lists.
- **Params:** `content_label_id` (string, optional) — Deprecated: single content tag id; use content_label_ids instead; `content_label_ids` (array, optional) — Content tag ids to filter by, repeatable; matches videos carrying any selected tag; `country_code` (string, **required**) — ISO-2 country code; `organic_only` (boolean, optional) — Restrict to organic (non-paid) videos only; `period` (integer, optional) — Lookback window in days; `sort_by` (string, optional) — Sort order

### `tiktok_explore`

- **HTTP:** `GET /tiktok/explore/{id}`
- **What:** Retrieve the TikTok explore feed for a category. Returns the TikTok explore feed for a category, given its category type `id` from the category endpoint. The response has `itemList` with the videos, `hasMore` and a `cursor`. A feed that comes back empty is reported as an upstream error, not as an empty list.
- **Params:** `id` (integer, **required**) — Category type id returned by the category endpoint

### `tiktok_mobile_feed`

- **HTTP:** `GET /tiktok/mobile/feed`
- **What:** Retrieve the TikTok mobile For You feed. Returns one page of videos from TikTok's mobile For You feed, signed with well-formed mobile signature headers (no device or account needed). Each item carries `aweme_id`, `create_time`, `author_id`, `share_url` and the verified statistics block (`play_count`, `digg_count`, `comment_count`, `share_count`, `collect_count`, `download_count`, `forward_count`, `lose_count`, `lose_comment_count`, `whatsapp_share_count`, `repost_count`). A zero `count` uses the app's default page size; `count` is capped at 50.
- **Params:** `count` (integer, optional) — Videos to request (0 = app default, max 50); `cursor` (integer, optional) — Pagination cursor

### `tiktok_mobile_hashtag`

- **HTTP:** `GET /tiktok/mobile/hashtag`
- **What:** Retrieve a TikTok hashtag. Returns one hashtag's detail by name: `challenge_info` (cid, hashtag_name, desc, ...) and `stats` (view and video counts), exactly as the mobile API returns them. Hashtags are addressed by name; an internal id is rejected upstream.
- **Params:** `name` (string, **required**) — Hashtag name without the leading #

### `tiktok_mobile_hashtag_posts`

- **HTTP:** `GET /tiktok/mobile/hashtag/posts`
- **What:** Retrieve videos for a TikTok hashtag. Lists videos for one hashtag name as the mobile app returns them (`aweme_list` with author, music and statistics), plus `cursor` and `has_more`. `sort=fresh` is the newest list and works from any measured egress; `sort=popular` is the hot list and only answers from a US egress.
- **Params:** `count` (integer, optional) — Videos per page (max 50); `cursor` (integer, optional) — Pagination cursor; `name` (string, **required**) — Hashtag name without the leading #; `sort` (string, optional) — Listing: fresh (newest) or popular (hot)

### `tiktok_mobile_hashtags`

- **HTTP:** `GET /tiktok/mobile/hashtags`
- **What:** Search TikTok hashtags. Searches hashtags by keyword and returns the matching hashtag objects unmodified, with `cursor` and `has_more` for paging.
- **Params:** `count` (integer, optional) — Results per page (max 50); `cursor` (integer, optional) — Pagination cursor; `keyword` (string, **required**) — Keyword to search hashtags for

### `tiktok_mobile_live_effects`

- **HTTP:** `GET /tiktok/mobile/live/effects`
- **What:** Retrieve TikTok LIVE effects. Returns the complete LIVE effects/sticker asset catalogue in one call: `data.assets` (2,032 assets, each with `id`, `name`, `describe`, `resource_url`, `resource_uri`, `md5`, `size`, `resource_type`, `download_type`, `model_requirements`, `sticker_asset_variant` and `video_resource_list`). There are no request parameters and no paging, and the body is large because the catalogue is complete.
- **Params:** _none_

### `tiktok_mobile_live_gifts`

- **HTTP:** `GET /tiktok/mobile/live/gifts`
- **What:** Retrieve TikTok LIVE gifts. Returns the complete LIVE gift catalogue in one call: `data.gifts` (771 gift objects with `diamond_count`, `describe`, `duration`, `gift_resources`, `gift_skins`, `batch_gift_info` and `combo`) plus the gift config and resource maps (`gift_configs`, `gifts_info`, `doodle_templates`, `gift_name_group_map`, `gift_resource_group_map`). There are no request parameters and no paging: the response is a single complete catalogue.
- **Params:** _none_

### `tiktok_mobile_live_search`

- **HTTP:** `GET /tiktok/mobile/live/search`
- **What:** Search TikTok LIVE streams. Searches the mobile app's LIVE surface by keyword: `data` of `{type, anchor}` entries with `feedback_type` set to `live`, plus `cursor` and `has_more`. `keyword` is required; without it the gateway answers a valid but empty envelope. This is the API's first LIVE endpoint.
- **Params:** `count` (integer, optional) — Results to request (0 = app default, max 50); `keyword` (string, **required**) — Search keyword

### `tiktok_mobile_music_beats`

- **HTTP:** `GET /tiktok/mobile/music/beats`
- **What:** Retrieve TikTok music beats. Returns the mobile app's beats/songs chart unmodified: `music_list` of the same full sound objects the pick chart returns (`id_str`, `title`, `user_count`, `album`, `artists`, `cover_*`), ordered as the app's beats list. The measured envelope carries no paging fields.
- **Params:** `count` (integer, optional) — Accepted for compatibility; not measured to change the page (max 50)

### `tiktok_mobile_music_collections`

- **HTTP:** `GET /tiktok/mobile/music/collections`
- **What:** Retrieve TikTok music collections. Returns the mobile app's sound-collection feed unmodified: `mcf_list`, where each entry is `{collection, music_list}` (the measured default page holds 8 entries), plus `cursor` and `has_more`. This route is first-page only: the returned `cursor` is not a reusable page token, so callers should not page with it.
- **Params:** `count` (integer, optional) — Collections to request (0 = app default, max 50); `cursor` (integer, optional) — Accepted for shape compatibility only; not a verified page token

### `tiktok_mobile_music_pick`

- **HTTP:** `GET /tiktok/mobile/music/pick`
- **What:** Retrieve TikTok sound chart picks. Returns the mobile app's sound pick/chart list: `music_list` of full sound objects (id, title, author, user_count, duration, ...) plus the chart list `mc_list` and `radio_cursor`.
- **Params:** `count` (integer, optional) — Sounds per page (max 50); `cursor` (integer, optional) — Pagination cursor

### `tiktok_mobile_music_posts`

- **HTTP:** `GET /tiktok/mobile/music/posts`
- **What:** Retrieve videos for a TikTok sound. Lists the videos that use one sound, as the mobile app returns them: `aweme_list` of full video objects (with `author`, `statistics` and `added_sound_music_info`), plus `cursor` and `has_more`. `music_id` is required. `count` is accepted but ignored upstream - the server returns its own default page, so page with `cursor`.
- **Params:** `count` (integer, optional) — Accepted for compatibility; the server ignores it (max 50); `cursor` (integer, optional) — Pagination cursor; `music_id` (string, **required**) — Sound (music) id

### `tiktok_mobile_music_related`

- **HTTP:** `GET /tiktok/mobile/music/related`
- **What:** Retrieve sounds related to a TikTok video. Returns sounds related to one video: `music_list` of full sound objects, `recall_info_list` explaining why each was recalled, `similar_song_ids`, plus `cursor` and `has_more`.
- **Params:** `aweme_id` (string, **required**) — Video id to find related sounds for; `count` (integer, optional) — Sounds per page (max 50); `cursor` (integer, optional) — Pagination cursor

### `tiktok_mobile_music_trending`

- **HTTP:** `GET /tiktok/mobile/music/trending`
- **What:** Retrieve TikTok trending sounds. Returns the mobile app's trending sound chart: `music_list` of full sound objects (`id_str`, `title`, `user_count`, `album`, `artists`, `cover_large`/`cover_medium`/`cover_thumb`, `binded_challenge_id`, `collect_stat`, `audition_duration`) unmodified, plus `cursor` and `has_more` for paging. This is the chart behind `music.trending`.
- **Params:** `count` (integer, optional) — Sounds per page (max 50); `cursor` (integer, optional) — Pagination cursor

### `tiktok_mobile_search`

- **HTTP:** `GET /tiktok/mobile/search`
- **What:** Search TikTok videos on the mobile API. Keyword search returning the mobile API result documents unmodified: each entry has `aweme_info` (a full video object with statistics), `card_profile` and search metadata, plus `cursor` and `has_more`. Keep `count` small (20 already exceeds one megabyte of upstream JSON).
- **Params:** `count` (integer, optional) — Results per page (max 20); `keyword` (string, **required**) — Search keyword; `offset` (integer, optional) — Result offset

### `tiktok_mobile_search_music`

- **HTTP:** `GET /tiktok/mobile/search/music`
- **What:** Search TikTok sounds on the mobile API. Keyword search over sounds, returning `music_info_list` of full sound objects unmodified with `cursor`, `has_more` and `total`.
- **Params:** `count` (integer, optional) — Sounds per page (max 50); `keyword` (string, **required**) — Search keyword; `offset` (integer, optional) — Result offset

### `tiktok_mobile_search_user`

- **HTTP:** `GET /tiktok/mobile/search/user`
- **What:** Search TikTok users on the mobile API. Keyword search over users, returning `user_list` unmodified. Each `user_info` carries the populated creator statistics (follower_count, following_count, total_favorited, aweme_count, custom_verify).
- **Params:** `count` (integer, optional) — Users per page (max 50); `cursor` (integer, optional) — Pagination cursor; `keyword` (string, **required**) — Search keyword (a username or display name)

### `tiktok_mobile_trending_categories`

- **HTTP:** `GET /tiktok/mobile/trending/categories`
- **What:** Retrieve TikTok trending categories. Returns the discover-category feed unmodified: each `category_list` entry is `{aweme_list, category_type, challenge_info, click_track_url_list, desc, track_url_list}`, with `cursor` and `has_more` for paging.
- **Params:** `count` (integer, optional) — Categories per page (max 50); `cursor` (integer, optional) — Pagination cursor

### `tiktok_mobile_trending_effects`

- **HTTP:** `GET /tiktok/mobile/trending/effects`
- **What:** Retrieve TikTok trending effects. Returns the effect/sticker discovery feed unmodified: `aweme_list` of full video objects, each additionally carrying `stickers` and `sticker_detail`, plus `feed_session_id`, `cursor` and `has_more`.
- **Params:** `count` (integer, optional) — Videos per page (max 50); `cursor` (integer, optional) — Pagination cursor

### `tiktok_popular_trend_country_industry_meta`

- **HTTP:** `GET /tiktok/popular-trend/country-industry-meta`
- **What:** Retrieve TikTok popular-trend country and industry metadata. Lists the country and industry filter values used by the TikTok Creative Center popular-trend endpoints. Countries have an `id` such as `AR` and a name; industries have a numeric `id` and a name such as Apparel & Accessories. A maintained fallback list is returned if TikTok's own metadata is unavailable.
- **Params:** _none_

### `tiktok_post`

- **HTTP:** `GET /tiktok/post/{id}`
- **What:** Retrieve TikTok video details. Returns TikTok's detail record for one video by video id. `itemInfo.itemStruct` holds the video's description, the author's profile and the author's statistics (such as followers, following and hearts) along with the rest of TikTok's video object; `shareMeta` holds the share title and description.
- **Params:** `id` (string, **required**) — TikTok video id

### `tiktok_posts`

- **HTTP:** `GET /tiktok/posts`
- **What:** Retrieve posts from a TikTok profile. Lists posts from a TikTok profile identified by `secUid`. `sort_type` is `0` latest (default), `1` popular or `2` oldest. `cursor` defaults to 0. The response has `itemList`, `hasMore` and a `cursor` to pass back to fetch the next page.
- **Params:** `cursor` (integer, optional) — Pagination cursor; `secUid` (string, **required**) — TikTok secUid for the profile; `sort_type` (integer, optional) — Sort mode: 0 latest, 1 popular, 2 oldest

### `tiktok_profile`

- **HTTP:** `GET /tiktok/profile/{handler}`
- **What:** Retrieve a TikTok profile. Returns a public TikTok profile by `handler`, the username without the leading `@`. The `user` object has the id, `uniqueId`, nickname, signature, verified and private flags, region, language, avatar, bio link and `secUid`; `stats` has follower, following, heart, video and friend counts. A missing, deleted or banned handle returns 404.
- **Params:** `handler` (string, **required**) — TikTok handle without the leading @

### `tiktok_search`

- **HTTP:** `GET /tiktok/search`
- **What:** Search TikTok videos. Searches TikTok videos for `keyword`. `cursor` defaults to 0 and `count` defaults to 20, capped at 50. The response has the matching video items, a `cursor` and `has_more` for paging. An empty, blocked or malformed result from TikTok returns an upstream error.
- **Params:** `count` (integer, optional) — Result count, clamped to 50; `cursor` (integer, optional) — Pagination cursor; `keyword` (string, **required**) — Search keyword

### `tiktok_search_hashtag`

- **HTTP:** `GET /tiktok/search/hashtag`
- **What:** Search TikTok hashtags. Searches TikTok hashtags (challenges) for `keyword`. `cursor` defaults to 0 and `count` defaults to 20, capped at 50. The response has `challenge_list` with each hashtag's name and id, plus a `cursor` and `has_more` for paging. An empty, blocked or malformed result returns an upstream error.
- **Params:** `count` (integer, optional) — Result count, clamped to 50; `cursor` (integer, optional) — Pagination cursor; `keyword` (string, **required**) — Search keyword

### `tiktok_search_user`

- **HTTP:** `GET /tiktok/search/user`
- **What:** Search TikTok users. Searches TikTok users for `keyword`, with `cursor` (default 0) for paging. The response has `user_list` with the matching accounts, plus a `cursor` and `has_more` to continue. Pass the returned `cursor` back to fetch the next page.
- **Params:** `cursor` (integer, optional) — Pagination cursor; `keyword` (string, **required**) — Search keyword

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

### `tiktok_trending`

- **HTTP:** `GET /tiktok/trending`
- **What:** Retrieve TikTok trending posts. Returns the current TikTok trending feed: `itemList` holds the videos, and `hasMore` and `cursor` describe paging. The response also has a `trendingTopics` field. Takes no parameters.
- **Params:** _none_

## Threads (10)

### `threads_post`

- **HTTP:** `GET /threads/post/{username}/{code}`
- **What:** Retrieve a public Threads post. Returns one public Threads post by `username` (with or without a leading `@`) and the post `code` from its URL. The response has the post text, canonical URL, preview image URL, and the author's id, name and username. Replies and logged-in fields are not included. An unavailable post returns 404.
- **Params:** `code` (string, **required**) — Threads post code; `username` (string, **required**) — Threads username

### `threads_post_replies`

- **HTTP:** `GET /threads/post/{username}/{code}/replies`
- **What:** Retrieve public replies to a Threads post. Returns the public replies currently exposed to logged-out visitors. The response identifies when Threads reports additional replies but withholds a usable continuation cursor.
- **Params:** `code` (string, **required**) — Threads post code; `username` (string, **required**) — Threads username

### `threads_profile`

- **HTTP:** `GET /threads/profile/{username}`
- **What:** Retrieve a public Threads profile. Returns a public Threads profile by `username` (with or without a leading `@`): name, profile URL, biography, avatar URL, `followers_count` and `threads_count`. Counts are derived from the compact figures shown on the profile page. An unavailable profile returns 404.
- **Params:** `username` (string, **required**) — Threads username

### `threads_profile_media`

- **HTTP:** `GET /threads/profile/{username}/media`
- **What:** Retrieve public media posts from a Threads profile. Returns the first public page shown on a profile's Media tab. Items include image and video URLs, including carousel attachments, plus post and topic metadata. The logged-out page exposes no continuation cursor or media-type filter; `pagination_limited` reports when additional results are gated by login or lack a supported cursor.
- **Params:** `username` (string, **required**) — Threads username

### `threads_profile_posts`

- **HTTP:** `GET /threads/profile/{username}/posts`
- **What:** Retrieve public posts from a Threads profile. Lists public posts from the profile's Threads tab by `username`. Each item has its code, URL, text, creation time, image and video URLs, like, reply, repost and quote counts, reply flag and author. When `has_more` is true, pass `next_cursor` unchanged as `cursor` to fetch the next page; `pagination_limited` is true if Threads withholds a usable cursor.
- **Params:** `cursor` (string, optional) — Opaque cursor returned by the previous response; `username` (string, **required**) — Threads username

### `threads_profile_replies`

- **HTTP:** `GET /threads/profile/{username}/replies`
- **What:** Retrieve public items from a Threads profile's Replies tab. Returns the first public page shown on a profile's Replies tab. Each item preserves its actual author and public reply metadata. The logged-out page has no continuation cursor; `pagination_limited` is true when Threads reports more items without a cursor or shows a login wall for additional items.
- **Params:** `username` (string, **required**) — Threads username

### `threads_profile_reposts`

- **HTTP:** `GET /threads/profile/{username}/reposts`
- **What:** Retrieve public posts reposted by a Threads profile. Returns the first public page shown on a profile's Reposts tab. Each item preserves the original post author and metadata. `pagination_limited` is true when Threads gates more items behind login or reports more items without a supported cursor.
- **Params:** `username` (string, **required**) — Threads username

### `threads_profile_topics`

- **HTTP:** `GET /threads/profile/{username}/topics`
- **What:** Discover public topic tags on a Threads profile. Returns every topic tag listed on a public profile, including the numeric tag id and canonical `name` to pass as `q` to `/threads/search/topics`. Community topics include their community metadata.
- **Params:** `username` (string, **required**) — Threads username

### `threads_search`

- **HTTP:** `GET /threads/search`
- **What:** Search public Threads posts. Returns the public first page of Threads search results for a query. `sort` supports `top` and `recent`; `pagination_limited` marks the logged-out login wall because search has no continuation cursor. Author and date filters in Threads require login and are not exposed here.
- **Params:** `q` (string, **required**) — Search query (1-100 characters); `sort` (string, optional) — Result order; defaults to top

### `threads_topic_search`

- **HTTP:** `GET /threads/search/topics`
- **What:** Search posts for a public Threads topic tag. Returns the public first page of posts for a topic tag. Discover the required `tag_id` and its canonical query `name` from `/threads/profile/{username}/topics` or a post's `topic` metadata. Topic results have no logged-out continuation cursor; `pagination_limited` marks the login wall for more results.
- **Params:** `q` (string, **required**) — Canonical topic query from a profile topic's `name` or a post topic's `search_query`; `tag_id` (string, **required**) — Numeric Threads topic tag id

## Bluesky (11)

### `bluesky_author_feed`

- **HTTP:** `GET /bluesky/author-feed`
- **What:** A Bluesky account's posts. Returns a page of a Bluesky account's posts, newest first, including text, engagement counts, and any attached images/link card/quoted post.
- **Params:** `actor` (string, **required**) — A handle (e.g. bsky.app) or DID; `cursor` (string, optional) — Pagination cursor from a previous response's cursor field; `limit` (integer, optional) — Page size, 1-100

### `bluesky_followers`

- **HTTP:** `GET /bluesky/followers`
- **What:** A Bluesky account's followers. Returns a page of a Bluesky account's followers. `actor` is required and is a handle such as `bsky.app` or a DID. `limit` is 1 to 100 (default 25); pass the returned `cursor` back to continue. Each follower has `did`, `handle`, `display_name`, `description`, `avatar_url` and `created_at`, and `subject` describes the account itself.
- **Params:** `actor` (string, **required**) — A handle (e.g. bsky.app) or DID; `cursor` (string, optional) — Pagination cursor from a previous response's cursor field; `limit` (integer, optional) — Page size, 1-100

### `bluesky_follows`

- **HTTP:** `GET /bluesky/follows`
- **What:** Accounts a Bluesky account follows. Returns a page of the accounts a Bluesky account follows.
- **Params:** `actor` (string, **required**) — A handle (e.g. bsky.app) or DID; `cursor` (string, optional) — Pagination cursor from a previous response's cursor field; `limit` (integer, optional) — Page size, 1-100

### `bluesky_post_likes`

- **HTTP:** `GET /bluesky/post-likes`
- **What:** List actors who liked a Bluesky post. Lists the accounts that liked a Bluesky post, identified by its `at://` post `uri`, which is required. `limit` defaults to 25 and is capped at 100; pass the returned `cursor` back for the next page. Each actor has `did`, `handle`, `display_name`, `description`, `avatar_url` and `created_at`.
- **Params:** `cursor` (string, optional) — Pagination cursor; `limit` (integer, optional) — Page size, 1-100; `uri` (string, **required**) — The post's at:// URI

### `bluesky_post_quotes`

- **HTTP:** `GET /bluesky/post-quotes`
- **What:** List quotes of a Bluesky post. Lists the Bluesky posts that quote a given post, identified by its `at://` post `uri`, which is required. `limit` defaults to 25 and is capped at 100; pass the returned `cursor` back for the next page. Each post has its `text`, `author`, `created_at`, `langs`, like, quote, reply and repost counts, `images` and `external` link card.
- **Params:** `cursor` (string, optional) — Pagination cursor; `limit` (integer, optional) — Page size, 1-100; `uri` (string, **required**) — The quoted post's at:// URI

### `bluesky_post_reposted_by`

- **HTTP:** `GET /bluesky/post-reposted-by`
- **What:** List actors who reposted a Bluesky post. Lists the accounts that reposted a Bluesky post, identified by its `at://` post `uri`, which is required. `limit` defaults to 25 and is capped at 100; pass the returned `cursor` back for the next page. Each actor has `did`, `handle`, `display_name`, `description`, `avatar_url` and `created_at`.
- **Params:** `cursor` (string, optional) — Pagination cursor; `limit` (integer, optional) — Page size, 1-100; `uri` (string, **required**) — The post's at:// URI

### `bluesky_post_thread`

- **HTTP:** `GET /bluesky/post-thread`
- **What:** A Bluesky post and its reply tree. Returns a Bluesky post along with its nested replies (and, when the post is itself a reply, its parent chain), up to `depth` levels deep.
- **Params:** `depth` (integer, optional) — Reply-tree depth, 1-10; `uri` (string, **required**) — The post's at:// URI, e.g. from an author-feed or search-actors result's post uri field

### `bluesky_posts`

- **HTTP:** `GET /bluesky/posts`
- **What:** Look up Bluesky posts in a batch. Returns public Bluesky posts for 1-25 at:// post URIs. Missing, deleted, or blocked posts are omitted when the public AppView omits them.
- **Params:** `uris` (array, **required**) — One or more at:// post URIs (1-25); repeat the parameter for multiple URIs

### `bluesky_profile`

- **HTTP:** `GET /bluesky/profile`
- **What:** A Bluesky account's full public profile. Returns a Bluesky account's public profile: display name, description, avatar/banner images, and follower/follows/posts counts.
- **Params:** `actor` (string, **required**) — A handle (e.g. bsky.app) or DID (e.g. did:plc:z72i7hdynmk6r22z27h6tvur)

### `bluesky_search_actors`

- **HTTP:** `GET /bluesky/search-actors`
- **What:** Search Bluesky accounts. Returns Bluesky accounts matching a query against display name, handle, and profile description.
- **Params:** `cursor` (string, optional) — Pagination cursor from a previous response's cursor field; `limit` (integer, optional) — Page size, 1-100; `q` (string, **required**) — Search text

### `bluesky_trending_topics`

- **HTTP:** `GET /bluesky/trending-topics`
- **What:** Bluesky's current trending topics. Returns Bluesky's current trending topics and suggested feeds, each with a link to its feed. This surface is less stable than the rest of this family -- Bluesky may change its shape without notice.
- **Params:** _none_

## X (3)

### `x_post`

- **HTTP:** `GET /x/post/{id}`
- **What:** Retrieve an X post. Returns a public X post by numeric post id, including author, text, visible metrics, and a quoted post preview when present.
- **Params:** `id` (string, **required**) — X post id; `username` (string, optional) — Expected author username. When provided, mismatched authors return 404.

### `x_profile`

- **HTTP:** `GET /x/profile/{username}`
- **What:** Retrieve an X profile. Returns the public profile of an X account by `username`, with or without a leading `@`: name, description, location, avatar and banner images, creation date, verification flags, and `metrics` for followers, following, posts, likes, listed and media. `verified_type` and `affiliate_label` appear only when the account has them. Returns 404 when the profile is not public.
- **Params:** `username` (string, **required**) — X username

### `x_profile_posts`

- **HTTP:** `GET /x/profile/{username}/posts`
- **What:** List public X profile posts. Returns posts present in the first public profile page payload for an X username. The endpoint does not paginate replies, media-only tabs, or search results.
- **Params:** `limit` (integer, optional) — Maximum posts returned from the first page payload. Defaults to 20 and must be 1-50.; `username` (string, **required**) — X username

## Pinterest (8)

### `pinterest_board`

- **HTTP:** `GET /pinterest/board/{username}/{slug}`
- **What:** Get a Pinterest board's detail. Returns a Pinterest board's metadata (name, description, cover image, pin/follower counts, owner) plus a page of pins from that board. Public data sourced from Pinterest's own board pages.
- **Params:** `slug` (string, **required**) — Board URL slug, from the board's own /{username}/{slug}/ URL; `username` (string, **required**) — Pinterest username that owns the board

### `pinterest_categories`

- **HTTP:** `GET /pinterest/categories`
- **What:** Get Pinterest's "Ideas" category list. Returns Pinterest's top-level "Ideas" category taxonomy (e.g. "Animals", "Home Decor", "Food And Drink"). Each entry's id is usable directly with GET /pinterest/ideas/{id}. Public data sourced from Pinterest's own ideas.pinterest.com-style category hub.
- **Params:** _none_

### `pinterest_idea`

- **HTTP:** `GET /pinterest/ideas/{id}`
- **What:** Get a Pinterest "Ideas" category's detail feed. Returns one "Ideas" category's metadata (name, description, follower count) plus a page of pins from that category's feed. Public data sourced from Pinterest's own ideas category pages.
- **Params:** `id` (string, **required**) — Pinterest ideas category id. See GET /pinterest/categories for the full list.

### `pinterest_pin`

- **HTTP:** `GET /pinterest/pin/{id}`
- **What:** Get a Pinterest pin's full detail. Returns a single Pinterest pin's full detail: title, description, image, board, pinner, comment count, save count, and creation time. Public data sourced from Pinterest's own pin pages.
- **Params:** `id` (string, **required**) — Pinterest pin id

### `pinterest_search`

- **HTTP:** `GET /pinterest/search`
- **What:** Search Pinterest pins. Returns public Pinterest pins matching a text query: title, description, image, board, and pinner for each result. Public data sourced from Pinterest's own web search.
- **Params:** `query` (string, **required**) — Search text

### `pinterest_user`

- **HTTP:** `GET /pinterest/user/{username}`
- **What:** Get a Pinterest user's public profile. Returns a Pinterest user's public profile: display name, bio, website, avatar, and follower/following/pin/board counts. Public data sourced from Pinterest's own profile pages.
- **Params:** `username` (string, **required**) — Pinterest username

### `pinterest_user_boards`

- **HTTP:** `GET /pinterest/user/{username}/boards`
- **What:** Get a Pinterest user's boards. Returns a page of a Pinterest user's own boards: name, description, cover image, and pin/follower counts for each. Public data sourced from Pinterest's own profile pages.
- **Params:** `username` (string, **required**) — Pinterest username

### `pinterest_user_pins`

- **HTTP:** `GET /pinterest/user/{username}/pins`
- **What:** Get a Pinterest user's own pins. Returns a page of a Pinterest user's own pins: title, description, image, board, and pinner for each. Public data sourced from Pinterest's own profile pages.
- **Params:** `username` (string, **required**) — Pinterest username

## LinkedIn (5)

### `linkedin_company`

- **HTTP:** `GET /linkedin/company/{id}`
- **What:** Get LinkedIn Company info by ID. Returns a LinkedIn company page by its company `id`. The response has the name, headline, about text, industry, company size, employee count on LinkedIn, follower count, founding year, headquarters, locations, specialties, website, logo, Products section cards, affiliated and similar pages, and recent updates with reactions and comment counts.
- **Params:** `id` (string, **required**) — LinkedIn Company ID

### `linkedin_product`

- **HTTP:** `GET /linkedin/product/{id}`
- **What:** Get LinkedIn Product info by ID. Returns a LinkedIn product page by its product `id`. The response has the name, about text, category, owning organization, external link, logo, cover image, media items, featured customers with industry and follower count, and lists of other and similar products.
- **Params:** `id` (string, **required**) — LinkedIn Product ID

### `linkedin_product_categories`

- **HTTP:** `GET /linkedin/product/categories`
- **What:** Discover LinkedIn product categories. Returns the standardized product categories accepted by the products/search endpoint's category_id filter. With a keyword, returns matching categories from LinkedIn's own category search. Without one, returns every known category.
- **Params:** `keyword` (string, optional) — Narrow results to categories matching this term. Omit to return every known category.

### `linkedin_products_search`

- **HTTP:** `GET /linkedin/products/search`
- **What:** Search the LinkedIn product directory. Returns one page of LinkedIn's public product directory search results, optionally scoped to a keyword and/or category. Keyword matching is on word prefixes. start is an upstream card offset advanced by the previous response's next_start; LinkedIn's guest search stops returning results at offset 1200.
- **Params:** `category_id` (string, optional) — Numeric category id from /linkedin/product/categories; `keyword` (string, optional) — Search keyword, matched on word prefixes; `start` (integer, optional) — Upstream card offset, 0 to 1199

### `linkedin_showcase`

- **HTTP:** `GET /linkedin/showcase/{id}`
- **What:** Get Linkedin Showcase Page Info. Returns a LinkedIn showcase page by its showcase page `id`. The response has the name, headline, about text, industry, follower count, employees on LinkedIn, headquarters, locations, specialties, website, logo, Products section cards when present, affiliated and similar pages, and recent updates with reactions and comment counts.
- **Params:** `id` (string, **required**) — LinkedIn Showcase Page ID

## Facebook (2)

### `facebook_marketplace_search`

- **HTTP:** `GET /facebook/marketplace/search`
- **What:** Search Facebook Marketplace. Fetches Facebook Marketplace search or browse results for a location: listing id, title, price, city/state, and a thumbnail image per result. Only the first page Facebook's own server-rendered results page returns is available — Facebook's own further pagination requires a logged-in session and is out of scope. Omit both query and category to get the location's browse feed instead of running a search. minPrice, maxPrice, sortBy, daysSinceListed, and condition only take effect alongside a query or category (Facebook itself ignores them on the plain browse feed), except for the property_rentals category, which has its own always-filtered listing page. This endpoint can take noticeably longer than other search endpoints (up to roughly a minute in the slowest case) as it retries to get past an intermittent upstream condition; priced accordingly.
- **Params:** `category` (string, optional) — Marketplace category; `condition` (string, optional) — Comma-separated listing conditions; requires query or category; `days_since_listed` (integer, optional) — Restrict to listings posted within this many days; requires query or category; `location` (string, **required**) — Facebook Marketplace location vanity slug; `max_price` (integer, optional) — Maximum price in whole currency units; requires query or category; `min_price` (integer, optional) — Minimum price in whole currency units; requires query or category; `query` (string, optional) — Free-text search terms; omit (with category) for the location's browse feed; `sort_by` (string, optional) — Result order; requires query or category

### `facebook_page`

- **HTTP:** `GET /facebook/{page}`
- **What:** Get Facebook page details. Fetches public data about a Facebook Page given its page ID, vanity name, or full page URL: name, follower/like counts, intro, category, business hours/price range, review count, and any public contact details (email, phone, address, website, WhatsApp number) exposed on the Page's About tab.
- **Params:** `page` (string, **required**) — Facebook Page reference: vanity name, handle, profile.php id, or full Facebook URL

## Reddit (12)

### `reddit_comments`

- **HTTP:** `GET /reddit/comments/{id}`
- **What:** Get Reddit post comments. Returns a Reddit post with its public comments. The default mode is 1 credit. Set `include_metrics=true` to return the comments with public net score and award count plus post engagement metrics for 3 credits. Large threads may expose only an initial comment subset. Reddit does not expose per-comment upvote ratios or exact upvote/downvote totals anonymously. A post that exists but has no comments yet returns a 200 response with an empty comments list; a post that does not exist returns 404, and a temporary block or upstream failure returns 503 (retryable) rather than 404. If source.type is redlib, public fields and credit weights are preserved.
- **Params:** `depth` (integer, optional) — Maximum flat comment depth returned in metrics mode.; `id` (string, **required**) — Reddit post id or t3_ id; `include_metrics` (boolean, optional) — Include public post and per-comment engagement metrics; costs 3 credits instead of 1; `limit` (integer, optional) — Maximum comments returned, defaults to 25 and clamps to 100; `sort` (string, optional) — Comment order: confidence, top, new, controversial, old, or qa. Applied to the anonymous HTML request when metrics are enabled.

### `reddit_domain_posts`

- **HTTP:** `GET /reddit/domain/{domain}/posts`
- **What:** List Reddit domain posts. Returns public posts submitted from a linked domain. A `503` with a `Retry-After` header means Reddit is temporarily throttling the request; wait that many seconds and retry. If source.type is redlib, public fields and credit weights are preserved.
- **Params:** `after` (string, optional) — Reddit pagination token; `domain` (string, **required**) — Domain hostname, without scheme or path; `limit` (integer, optional) — Maximum posts, defaults to 25 and clamps to 100; `sort` (string, optional) — Sort: hot, new, top, or rising; `time` (string, optional) — Time window for top sort: hour, day, week, month, year, or all

### `reddit_leads`

- **HTTP:** `GET /reddit/leads`
- **What:** Find Reddit buying-intent leads. Scans a Reddit search page for people actively asking for a product or service, scores each post 0-10 for buying intent, and returns them ranked highest-first with the signals that fired. Self-promotion, hiring posts, freelancer service adverts, revenue-milestone posts, duplicate reposts, and Title Case article headlines are filtered out before scoring. A deterministic prefilter always runs; when `classifier` resolves to `llm` the surviving candidates are additionally refined in one batched model call. A `503` with a `Retry-After` header means Reddit is temporarily throttling the request; wait that many seconds and retry. The lead-response fields and credit weights are preserved regardless of the underlying Reddit data source.
- **Params:** `classifier` (string, optional) — Classifier: auto uses the model when configured, heuristic skips it, llm requires it; `limit` (integer, optional) — Maximum leads returned, defaults to 25 and clamps to 100; `min_score` (integer, optional) — Minimum buying-intent score to return, 0-10, defaults to 4; `q` (string, **required**) — What you offer, in plain language; `sort` (string, optional) — Sort: relevance, hot, new, top, or comments; `subreddit` (string, optional) — Restrict the search to a subreddit name, without r/; `time` (string, optional) — Time window: hour, day, week, month, year, or all

### `reddit_post`

- **HTTP:** `GET /reddit/post/{id}`
- **What:** Get Reddit post. Returns a public Reddit post. The default mode is 1 credit. Set `include_metrics=true` to return public net score, upvote ratio, comment count, award count, and estimated upvote/downvote totals for 3 credits. Reddit fuzzes voting data, so estimates are approximate; share, repost/crosspost, and view counts are not exposed anonymously. If source.type is redlib, public fields and credit weights are preserved.
- **Params:** `id` (string, **required**) — Reddit post id or t3_ id; `include_metrics` (boolean, optional) — Include public engagement metrics; costs 3 credits instead of 1

### `reddit_search`

- **HTTP:** `GET /reddit/search`
- **What:** Search Reddit posts. Searches public Reddit content and returns public post entries. A `503` with a `Retry-After` header means Reddit is temporarily throttling the request; wait that many seconds and retry. If source.type is redlib, public fields and credit weights are preserved.
- **Params:** `after` (string, optional) — Reddit pagination token; `limit` (integer, optional) — Maximum posts, defaults to 25 and clamps to 100; `q` (string, **required**) — Search keywords; `sort` (string, optional) — Sort: relevance, hot, new, top, or comments; `subreddit` (string, optional) — Restrict search to a subreddit name, without r/; `time` (string, optional) — Time window for top/comments sorts: hour, day, week, month, year, or all

### `reddit_subreddit_about`

- **HTTP:** `GET /reddit/subreddit/{subreddit}/about`
- **What:** Get Reddit subreddit metadata. Returns public metadata and sample posts for a subreddit. Subscriber counts, icons, and banners are omitted because they are not available on anonymous Reddit pages. A `503` with a `Retry-After` header means Reddit is temporarily throttling the request; wait that many seconds and retry. If source.type is redlib, public fields and credit weights are preserved.
- **Params:** `limit` (integer, optional) — Maximum sample posts inspected, defaults to 25 and clamps to 100; `subreddit` (string, **required**) — Subreddit name, without r/

### `reddit_subreddit_comments`

- **HTTP:** `GET /reddit/subreddit/{subreddit}/comments`
- **What:** List Reddit subreddit comments. Returns flat public comment entries from a subreddit latest-comments feed. A `503` with a `Retry-After` header means Reddit is temporarily throttling the request; wait that many seconds and retry. If source.type is redlib, public fields and credit weights are preserved.
- **Params:** `after` (string, optional) — Reddit pagination token; `limit` (integer, optional) — Maximum comments, defaults to 25 and clamps to 100; `subreddit` (string, **required**) — Subreddit name, without r/

### `reddit_subreddit_posts`

- **HTTP:** `GET /reddit/subreddit/{subreddit}/posts`
- **What:** List Reddit subreddit posts. Returns public posts from a subreddit. A `503` with a `Retry-After` header means Reddit is temporarily throttling the request; wait that many seconds and retry. If source.type is redlib, public fields and credit weights are preserved.
- **Params:** `after` (string, optional) — Reddit pagination token; `limit` (integer, optional) — Maximum posts, defaults to 25 and clamps to 100; `sort` (string, optional) — Sort: hot, new, top, or rising; `subreddit` (string, **required**) — Subreddit name, without r/; `time` (string, optional) — Time window for top sort: hour, day, week, month, year, or all

### `reddit_subreddits_posts`

- **HTTP:** `GET /reddit/subreddits/posts`
- **What:** List Reddit multi-subreddit posts. Returns public posts from a combined multi-subreddit feed. A `503` with a `Retry-After` header means Reddit is temporarily throttling the request; wait that many seconds and retry. If source.type is redlib, public fields and credit weights are preserved.
- **Params:** `after` (string, optional) — Reddit pagination token; `limit` (integer, optional) — Maximum posts, defaults to 25 and clamps to 100; `sort` (string, optional) — Sort: hot, new, top, or rising; `subreddits` (string, **required**) — Comma-separated subreddit names, without r/, maximum 10; `time` (string, optional) — Time window for top sort: hour, day, week, month, year, or all

### `reddit_trends`

- **HTTP:** `GET /reddit/trends`
- **What:** List Reddit trends. Returns public posts from broad Reddit hot, new, rising, or top feeds. For subreddit-specific trends, use `/reddit/subreddit/{subreddit}/posts` with `sort=hot`, `sort=new`, `sort=rising`, or `sort=top`. A `503` with a `Retry-After` header means Reddit is temporarily throttling the request; wait that many seconds and retry. If source.type is redlib, public fields and credit weights are preserved.
- **Params:** `after` (string, optional) — Reddit pagination token; `limit` (integer, optional) — Maximum posts, defaults to 25 and clamps to 100; `sort` (string, optional) — Sort: hot, new, rising, or top; `time` (string, optional) — Time window for top sort: hour, day, week, month, year, or all

### `reddit_user_comments`

- **HTTP:** `GET /reddit/user/{username}/comments`
- **What:** List Reddit user comments. Returns flat public comment entries from a public Reddit user's comments feed. A `503` with a `Retry-After` header means Reddit is temporarily throttling the request; wait that many seconds and retry. If source.type is redlib, public fields and credit weights are preserved.
- **Params:** `after` (string, optional) — Reddit pagination token; `limit` (integer, optional) — Maximum comments, defaults to 25 and clamps to 100; `username` (string, **required**) — Public Reddit username, without u/

### `reddit_user_posts`

- **HTTP:** `GET /reddit/user/{username}/posts`
- **What:** List Reddit user posts. Returns public posts from a public Reddit user's submitted feed. A `503` with a `Retry-After` header means Reddit is temporarily throttling the request; wait that many seconds and retry. If source.type is redlib, public fields and credit weights are preserved.
- **Params:** `after` (string, optional) — Reddit pagination token; `limit` (integer, optional) — Maximum posts, defaults to 25 and clamps to 100; `username` (string, **required**) — Public Reddit username, without u/

## Bilibili (8)

### `bilibili_anime_home`

- **HTTP:** `GET /bilibili/anime-home`
- **What:** Get Bilibili anime home sections. Returns the anonymous anime homepage's featured titles, latest updates, schedule, popular ranking, and new recommendations. Personalized rotating feed items are excluded.
- **Params:** _none_

### `bilibili_autocomplete`

- **HTTP:** `GET /bilibili/autocomplete`
- **What:** Get Bilibili search suggestions. Returns Bilibili search-box suggestions for the partial text in `q`, which is required (up to 100 characters). The response has the `query`, a `count` and deduplicated `suggestions` in Bilibili's order. A query with no matches returns an empty `suggestions` array; invalid input returns 400.
- **Params:** `q` (string, **required**) — Partial search text

### `bilibili_guochuang_home`

- **HTTP:** `GET /bilibili/guochuang-home`
- **What:** Get Bilibili Chinese-animation home sections. Returns the anonymous Chinese-animation homepage's featured titles, latest updates, schedule, popular ranking, and new recommendations. Personalized rotating feed items are excluded.
- **Params:** _none_

### `bilibili_must_watch`

- **HTTP:** `GET /bilibili/must-watch`
- **What:** Get Bilibili's curated must-watch videos. Returns Bilibili's curated must-watch collection, split into `classic_videos` and `latest_videos` with their counts, plus the collection `title`, `subtitle` and `explanation`. Each video has `bvid`, `aid`, `title`, `url`, `cover`, `uploader`, `published`, `stats` and `achievement`. Takes no parameters.
- **Params:** _none_

### `bilibili_popular`

- **HTTP:** `GET /bilibili/popular`
- **What:** Get current popular Bilibili videos. Returns Bilibili's current popular videos in Bilibili's own order. Start with `cursor` 0 (the default; max 10000000) and pass back `next_cursor` for the next batch. Each video has `bvid`, `aid`, `title`, `url`, `cover`, `duration`, `uploader`, `views_and_age` and an optional `reason`. At the end of the feed `no_more` is `true` and `videos` is empty.
- **Params:** `cursor` (integer, optional) — Upstream cursor from the previous response; defaults to 0

### `bilibili_ranking`

- **HTTP:** `GET /bilibili/ranking`
- **What:** Get the current Bilibili all-site ranking. Returns the current Bilibili all-site video ranking in rank order. Each video has its `rank`, `aid`, `title`, `url`, `cover`, `views`, `danmaku`, `replies`, `favorites`, `likes`, `duration_seconds`, `published_at`, `category` and `creator` (name, `mid`, `followers`). Takes no parameters.
- **Params:** _none_

### `bilibili_vertical_home`

- **HTTP:** `GET /bilibili/vertical-home`
- **What:** Get Bilibili documentary, movie, TV, or variety home sections. Returns stable server-rendered editorial sections for one Bilibili vertical. Allowed category values: documentary, movie, tv, variety. Rotating feeds, pagination, account state, and streaming URLs are excluded.
- **Params:** `category` (string, **required**) — Vertical: documentary, movie, tv, variety

### `bilibili_weekly`

- **HTTP:** `GET /bilibili/weekly`
- **What:** Get a Bilibili weekly selected-video issue. Returns one issue of Bilibili's weekly selected-video series: `number` (1 to 1000000) picks the issue, and omitting it returns the latest. The issue has `subject`, `label`, `description` and `reminder`, and each video has `bvid`, `title`, `uploader`, `duration_seconds`, `recommendation` and `stats_text`. An unknown issue number returns 404.
- **Params:** `number` (integer, optional) — Positive issue number; omit for the latest issue

## Patreon (4)

### `patreon_creator`

- **HTTP:** `GET /patreon/creator`
- **What:** Get a public Patreon creator profile. Returns public profile metadata from a creator's Patreon page: creator identity, summary, images, membership and creation counts, public earnings snapshot, membership/RSS availability flags, and public external profile links. handle is the creator's page handle, e.g. CachyOS for patreon.com/CachyOS.
- **Params:** `handle` (string, **required**) — Creator page handle

### `patreon_creator_tiers`

- **HTTP:** `GET /patreon/creator/tiers`
- **What:** Get a creator's public Patreon membership tiers. Returns published membership tiers and their published benefits from a creator's public Patreon page. It excludes member-only entitlements, tier capacity, and member counts. handle is the creator's page handle, e.g. CachyOS for patreon.com/CachyOS.
- **Params:** `handle` (string, **required**) — Creator page handle

### `patreon_explore`

- **HTTP:** `GET /patreon/explore`
- **What:** Browse public Patreon creators by topic. Returns Patreon's public curated creator shelves for one topic: Top creators, Popular this week, and New on Patreon. topic must be one of podcasts_and_shows, visual_arts, tabletop_games, video_games, music, lifestyle, writing, handicrafts, apps_and_software, social_impact.
- **Params:** `topic` (string, **required**) — Public Explore topic. Allowed values: podcasts_and_shows, visual_arts, tabletop_games, video_games, music, lifestyle, writing, handicrafts, apps_and_software, social_impact

### `patreon_rss`

- **HTTP:** `GET /patreon/rss`
- **What:** Get an explicitly public Patreon podcast RSS feed. Returns public podcast channel metadata and episodes from Patreon's canonical public RSS feed. campaign_id and show_id are the numeric IDs in the public feed URL. Private member feeds and authentication URLs are not supported.
- **Params:** `campaign_id` (string, **required**) — Numeric Patreon campaign id; `show_id` (string, **required**) — Numeric Patreon show id
