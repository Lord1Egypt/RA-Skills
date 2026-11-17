# SocialAPIs endpoint reference

Base URL: `https://api.socialapis.io` · Auth: header `x-api-token: $SOCIALAPIS_API_KEY` · All endpoints are `GET` with query parameters.

Generated from the live API configuration (53 endpoints). Machine-readable version: https://socialapis.io/openapi.json

## Facebook pages

### `GET /facebook/pages/id`

Resolve a Facebook page URL to its numeric page ID. Use it when another tool needs a page or profile ID; use `/facebook/pages/details` for the page's data. Pricing: 1 credit per call.

| Parameter | Required | Description |
|---|---|---|
| `link` | yes | Facebook page URL (e.g., https://facebook.com/nike) |

### `GET /facebook/pages/details`

Get a Facebook page's profile: name, category, follower and like counts, bio, contact info (email, phone, website, address), rating and the ad_page_id used by the Ads Library tools. Use it when you have the page URL; to find a page by name, use `/facebook/search/pages` first. Pricing: 1 credit per call; 5 credits when exact_followers_count=true.

| Parameter | Required | Description |
|---|---|---|
| `link` | yes | Facebook page URL |
| `exact_followers_count` | no | When true, performs a deeper scrape to return the exact follower count (e.g. 38,493,217 instead of "38M"). Charges 5 credits when true, 1 credit otherwise. Default: false. |

### `GET /facebook/pages/posts`

List a Facebook page's recent posts, newest first, with text, media, reactions, comment and share counts. Returns 3-9 posts per call plus an end_cursor for the next page; filter by date with after_time / before_time. For reels or videos only, use `/facebook/pages/reels` or `/facebook/pages/videos`. Pricing: ceil(posts_returned / 3) credits per call, minimum 1.

| Parameter | Required | Description |
|---|---|---|
| `link` | yes | Facebook page URL |
| `limit` | no | Maximum number of posts to return. Default: 3. Minimum: 3. Maximum: 9. |
| `end_cursor` | no | Pagination cursor for next page of results |
| `after_time` | no | ISO 8601 timestamp - only return posts after this time |
| `before_time` | no | ISO 8601 timestamp - only return posts before this time |
| `timezone` | no | Timezone for timestamps (e.g., UTC, America/New_York) |

### `GET /facebook/pages/reels`

List a Facebook page's reels (short-form videos). Returns an end_cursor for the next page. For long-form videos, use `/facebook/pages/videos`. Pricing: 1 credit per call.

| Parameter | Required | Description |
|---|---|---|
| `link` | yes | Facebook page URL |
| `end_cursor` | no | Pagination cursor |

### `GET /facebook/pages/videos`

List videos uploaded to a Facebook page, with video_id, title, duration, view count and thumbnail. Provide the page URL (link) or its numeric profile_id. Returns an end_cursor for the next page. For short-form reels, use `/facebook/pages/reels`. Pricing: 1 credit per call.

| Parameter | Required | Description |
|---|---|---|
| `link` | yes | Facebook page URL |
| `end_cursor` | no | Pagination cursor |

### `GET /facebook/pages/albums`

List the photo albums of a Facebook page, with album_id, album_title, url, thumbnail_uri and album_items_count (text, e.g. "400 items"). Needs the numeric page ID (profile_id) from `/facebook/pages/id`. Returns an end_cursor for the next page. To get the photos in an album, pass its album_id to `/facebook/albums/items`. Pricing: 1 credit per call.

| Parameter | Required | Description |
|---|---|---|
| `profile_id` | yes | Facebook page ID, from `/facebook/pages/id` |
| `limit` | no | Maximum number of albums to return. Default: 8. Minimum: 8. Maximum: 16. |
| `end_cursor` | no | Pagination cursor |

## Facebook groups

### `GET /facebook/groups/id`

Resolve a Facebook group URL to its numeric group ID. Use `/facebook/groups/details` for the group's data. Pricing: 1 credit per call.

| Parameter | Required | Description |
|---|---|---|
| `link` | yes | Facebook group URL |

### `GET /facebook/groups/details`

Get a public Facebook group's profile: name, description, member count, privacy, rules and activity stats. Use `/facebook/groups/posts` for its posts. Pricing: 1 credit per call.

| Parameter | Required | Description |
|---|---|---|
| `link` | yes | Facebook group URL |

### `GET /facebook/groups/posts`

List recent posts from a public Facebook group, with text, media, author, reactions and comment counts. Returns 3-9 posts per call plus an end_cursor for the next page; filter by date with after_time / before_time. Pricing: ceil(posts_returned / 3) credits per call, minimum 1.

| Parameter | Required | Description |
|---|---|---|
| `link` | yes | Facebook group URL |
| `limit` | no | Maximum number of posts to return. Default: 3. Minimum: 3. Maximum: 9. |
| `end_cursor` | no | Pagination cursor |
| `after_time` | no | ISO 8601 timestamp |
| `before_time` | no | ISO 8601 timestamp |
| `timezone` | no | IANA timezone for returned timestamps, e.g. UTC or America/New_York. Default: UTC. |

### `GET /facebook/groups/videos`

List videos posted in a public Facebook group, with video_id, title, duration, view count and thumbnail. Returns an end_cursor for the next page. Pricing: 1 credit per call.

| Parameter | Required | Description |
|---|---|---|
| `link` | yes | Facebook group URL |
| `end_cursor` | no | Pagination cursor |

### `GET /facebook/groups/albums`

List the photo albums of a public Facebook group, with album_id, album_title, url, thumbnail_uri, photos_count and videos_count. Returns an end_cursor for the next page. Needs the numeric group ID (group_id) from `/facebook/groups/id`. To get the photos in an album, pass its album_id to `/facebook/albums/items`. Pricing: 1 credit per call.

| Parameter | Required | Description |
|---|---|---|
| `group_id` | yes | Facebook group ID, from `/facebook/groups/id` |
| `limit` | no | Maximum number of albums to return. Default: 8. Minimum: 8. Maximum: 16. |

## Facebook albums

### `GET /facebook/albums/items`

Get the photos and videos inside a Facebook album (from a page or a group): media_id, media_type, url, thumbnail_uri and timestamp (Unix seconds). Needs an album_id from `/facebook/pages/albums` or `/facebook/groups/albums`. Returns an end_cursor for the next page. Pricing: 1 credit per call.

| Parameter | Required | Description |
|---|---|---|
| `album_id` | yes | Album ID, from `/facebook/pages/albums` or `/facebook/groups/albums` |
| `end_cursor` | no | Pagination cursor |

## Facebook posts, videos and comments

### `GET /facebook/posts/id`

Extract the numeric post ID from a Facebook post URL. Use it to get the post_id that `/facebook/posts/attachments` needs. Pricing: 1 credit per call.

| Parameter | Required | Description |
|---|---|---|
| `link` | yes | Facebook post URL |

### `GET /facebook/posts/details`

Get a Facebook post's text, author, timestamp, media, and reaction, comment and share counts. Start here for any post. If you need view counts, video download URLs or audio metadata (common for reels and videos), use `/facebook/posts/details/extended` instead. Pricing: 1 credit per call.

| Parameter | Required | Description |
|---|---|---|
| `link` | yes | Facebook post URL |

### `GET /facebook/posts/details/extended`

Get everything `/facebook/posts/details` returns plus view counts, HD/SD video URLs, music/audio metadata and author verification status. Use it for reels and video posts, or when the standard details lack view_count, video_hd_src or attached_track. Pricing: 1 credit per call.

| Parameter | Required | Description |
|---|---|---|
| `link` | yes | Facebook post URL (works for reels, video posts, and regular posts) |

### `GET /facebook/posts/attachments`

List every media attachment (images and videos, with URLs and dimensions) on a Facebook post, including all items in multi-photo posts. Needs the numeric post_id from `/facebook/posts/id`. For the post's text and engagement, use `/facebook/posts/details`. Pricing: 5 credits per call (deeper scrape than standard post details).

| Parameter | Required | Description |
|---|---|---|
| `post_id` | yes | Numeric Facebook post ID, from `/facebook/posts/id` |

### `GET /facebook/posts/video`

Get a Facebook video post's metadata: title, message text and hashtags, owner, reactions and view count. Needs the numeric video_id (the number in a facebook.com/.../videos/<id> URL, or from `/facebook/pages/videos`). Pricing: 1 credit per call.

| Parameter | Required | Description |
|---|---|---|
| `video_id` | yes | Numeric Facebook video ID, e.g. the number in a facebook.com/.../videos/<id> URL |

### `GET /facebook/posts/comments`

List top-level comments on a Facebook post or reel, with author, text, timestamp and reaction count. Returns up to 30 per call plus an end_cursor for the next page. Set include_reply_info=true to get the comment_feedback_id and expansion_token that `/facebook/posts/comments/replies` needs. Pricing: 1 credit per call.

| Parameter | Required | Description |
|---|---|---|
| `link` | yes | Facebook post or reel URL |
| `end_cursor` | no | Pagination cursor for next page of comments |
| `include_reply_info` | no | When "true", includes comment_feedback_id and expansion_token for fetching replies |

### `GET /facebook/posts/comments/replies`

List replies to one Facebook comment. Needs comment_feedback_id and expansion_token, which `/facebook/posts/comments` returns when called with include_reply_info=true. Pricing: 1 credit per call.

| Parameter | Required | Description |
|---|---|---|
| `comment_feedback_id` | yes | Feedback ID from the comments endpoint with include_reply_info=true |
| `expansion_token` | yes | Expansion token from the comments endpoint with include_reply_info=true |

## Facebook search

### `GET /facebook/search/pages`

Find Facebook pages by keyword (brand, business or topic name), optionally near a location. Returns page names, URLs, categories and follower counts, 3 per call, plus an end_cursor. Use it when you don't have the page URL; then call `/facebook/pages/details` with a result's URL. For locations, get a location_uid from `/facebook/search/locations`. Pricing: 1 credit per call.

| Parameter | Required | Description |
|---|---|---|
| `query` | yes | Keyword to search for, e.g. a brand or business name |
| `location_uid` | no | Location UID for filtering (from search/locations endpoint) |
| `end_cursor` | no | Pagination cursor |

### `GET /facebook/search/people`

Find public Facebook profiles by name or keyword, optionally near a location (location_uid from `/facebook/search/locations`). Returns names, profile URLs and pictures, plus work, education and location where public, and an end_cursor. Pricing: 1 credit per call.

| Parameter | Required | Description |
|---|---|---|
| `query` | yes | Name or keyword to search for |
| `location_uid` | no | Location UID for filtering |
| `end_cursor` | no | Pagination cursor |

### `GET /facebook/search/locations`

Look up Facebook places by name (city, region, venue) and get their location_uid. The location_uid is only used to filter `/facebook/search/pages`, `/facebook/search/people` and `/facebook/search/posts`; it is not a Marketplace location (use `/facebook/marketplace/city-coordinates` for that). Pricing: 1 credit per call.

| Parameter | Required | Description |
|---|---|---|
| `query` | yes | Search query (city, place, landmark) |

### `GET /facebook/search/posts`

Search public Facebook posts by keyword, optionally filtered by location (location_uid from `/facebook/search/locations`) and date range. Returns posts with text, author and engagement, plus an end_cursor. To list one page's posts, use `/facebook/pages/posts` instead. Pricing: 1 credit per call.

| Parameter | Required | Description |
|---|---|---|
| `query` | yes | Keyword or phrase to search post text for |
| `location_uid` | no | Location UID for filtering |
| `start_time` | no | Filter posts after this date (YYYY-MM-DD) |
| `end_time` | no | Filter posts before this date (YYYY-MM-DD) |
| `recent_posts` | no | When "true", shows only recent posts |
| `end_cursor` | no | Pagination cursor |

### `GET /facebook/search/videos`

Search public Facebook videos by keyword, optionally most recent first or live videos only. Returns video titles, URLs and view counts, plus an end_cursor. Pricing: 1 credit per call.

| Parameter | Required | Description |
|---|---|---|
| `query` | yes | Keyword or phrase to search videos for |
| `most_recent` | no | When "true", shows most recent videos first |
| `videos_live` | no | When "true", filters for live videos only |
| `fields` | no | Comma-separated list of response fields to include |
| `end_cursor` | no | Pagination cursor |

## Meta Ads Library

### `GET /facebook/ads/countries`

List the country codes the Ads Library tools accept in their country parameter. Pricing: 1 credit per call.

No parameters.

### `GET /facebook/ads/search`

Search ads in the Meta Ad Library. Pass a keyword (query) to find ads about a topic, or ad_page_id to list one advertiser's ads; filter by country, active status and date range, sort by impressions or recency. Returns ads with creative, body text, dates, platforms and snapshot URL, plus an end_cursor. Get an advertiser's ad_page_id from `/facebook/ads/keywords` or `/facebook/pages/details`. Pricing: 1 credit per call.

| Parameter | Required | Description |
|---|---|---|
| `query` | no | Search keyword for ads |
| `ad_page_id` | no | Facebook AD Page ID (alternative to query) |
| `country` | no | ISO country code or "ALL" |
| `activeStatus` | no | Filter: ALL, Active, or Inactive |
| `after_time` | no | Filter ads after this date (YYYY-MM-DD) |
| `before_time` | no | Filter ads before this date (YYYY-MM-DD) |
| `sort_data` | no | Sort by "impressions" or "recent" |
| `end_cursor` | no | Pagination cursor |

### `GET /facebook/ads/page-details`

Get an advertiser's Ads Library profile: page name, verification status, category, location and total ad count. Needs the page ID (ad_page_id from `/facebook/pages/details` or page_id from `/facebook/ads/keywords`). To list the ads themselves, use `/facebook/ads/search` with ad_page_id. Pricing: 1 credit per call.

| Parameter | Required | Description |
|---|---|---|
| `page_id` | yes | Advertiser page ID: ad_page_id from `/facebook/pages/details`, or page_id from `/facebook/ads/keywords` |

### `GET /facebook/ads/archive-details`

Get one Ad Library ad in full: creative, body text, CTA, platforms, countries, date range, and spend and impression estimates where Meta publishes them. Needs the ad_archive_id from a `/facebook/ads/search` result. Pricing: 1 credit per call.

| Parameter | Required | Description |
|---|---|---|
| `ad_archive_id` | yes | Ad Library archive ID of the ad (ad_archive_id from a `/facebook/ads/search` result) |
| `page_id` | no | Facebook Page ID |
| `country` | no | ISO country code or "ALL" |
| `is_ad_non_political` | no | Filter non-political ads |
| `is_ad_not_aaa_eligible` | no | Filter AAA eligibility |

### `GET /facebook/ads/keywords`

Find advertisers running ads that match a keyword: returns Facebook pages with their page_id and ad count. Use it to discover who advertises on a topic, then pass a page_id to `/facebook/ads/search` (as ad_page_id) or `/facebook/ads/page-details`. To get the ads for a keyword directly, use `/facebook/ads/search`. Pricing: 1 credit per call.

| Parameter | Required | Description |
|---|---|---|
| `query` | yes | Keyword to find advertisers for, e.g. running shoes |
| `country` | no | ISO country code or "ALL" |

## Facebook Marketplace

### `GET /facebook/marketplace/search`

Search general Facebook Marketplace listings (items for sale) by keyword or category near a location, with price, condition, radius and sort filters. Returns listings with their listing_id, plus an end_cursor. For cars and other vehicles use `/facebook/marketplace/vehicles`; for homes and rooms to rent use `/facebook/marketplace/rentals`. Get coordinates from `/facebook/marketplace/city-coordinates`. Pricing: 1 credit per call.

| Parameter | Required | Description |
|---|---|---|
| `query` | no | Keyword to search listings for, e.g. iphone 15 |
| `category_url` | no | Category URL slug |
| `proxy_country` | no | Optional premium proxy country |
| `commerce_search_sort_by` | no | Sort: BEST_MATCH, CREATION_TIME_DESCEND, PRICE_ASCEND, etc. |
| `commerce_search_and_rp_condition` | no | Condition: new, used_like_new, used_good, used_fair |
| `filter_location_latitude` | no | Latitude of the search center, e.g. 30.2672 (from `/facebook/marketplace/city-coordinates`) |
| `filter_location_longitude` | no | Longitude of the search center, e.g. -97.7431 (from `/facebook/marketplace/city-coordinates`) |
| `filter_price_lower_bound` | no | Minimum price in the local currency, whole number, e.g. 100 |
| `filter_price_upper_bound` | no | Maximum price in the local currency, whole number, e.g. 2000 |
| `filter_radius_km` | no | Search radius around the center in kilometres, e.g. 40 |
| `posted_today` | no | When "true", limit to items posted today |
| `exact_match` | no | When "true", exact match search |
| `end_cursor` | no | Pagination cursor |
| `fields` | no | Comma-separated keys to include (e.g. 'items.id,items.title,page_info.end_cursor'). Invalid keys are ignored. |

### `GET /facebook/marketplace/listing`

Get one Marketplace listing in full: title, price, description, condition, all photos, location and seller. Needs the listing_id from a Marketplace search result. Pricing: 1 credit per call.

| Parameter | Required | Description |
|---|---|---|
| `listing_id` | yes | Marketplace listing ID, from a Marketplace search result |

### `GET /facebook/marketplace/seller`

Get a Marketplace seller's profile: name, join date, rating, review count and badges. Needs the seller_id from `/facebook/marketplace/listing`. Pricing: 1 credit per call.

| Parameter | Required | Description |
|---|---|---|
| `seller_id` | yes | Seller ID, from the seller field of `/facebook/marketplace/listing` |

### `GET /facebook/marketplace/categories`

List Marketplace categories with their IDs and category_url values. Use a category_url to filter `/facebook/marketplace/search`. Pricing: 1 credit per call.

No parameters.

### `GET /facebook/marketplace/city-coordinates`

Convert a city name to the latitude and longitude that the Marketplace search tools expect in filter_location_latitude / filter_location_longitude. Pricing: 1 credit per call.

| Parameter | Required | Description |
|---|---|---|
| `city` | yes | City name, e.g. Austin |
| `country` | no | Country name or code |
| `exactly_one` | no | When "true", return exactly one result |

### `GET /facebook/marketplace/vehicles`

Search Facebook Marketplace vehicle listings (cars, trucks, motorcycles) near a location, with price, radius and seller-type filters. Returns listings with title, price, mileage, year and listing_id, plus an end_cursor. For non-vehicle items, use `/facebook/marketplace/search`. Pricing: 1 credit per call.

| Parameter | Required | Description |
|---|---|---|
| `sort_by` | no | Sort: CREATION_TIME_DESCEND, PRICE_ASCEND, VEHICLE_MILEAGE_ASCEND, etc. |
| `filter_location_latitude` | no | Latitude of the search center, e.g. 30.2672 (from `/facebook/marketplace/city-coordinates`) |
| `filter_location_longitude` | no | Longitude of the search center, e.g. -97.7431 (from `/facebook/marketplace/city-coordinates`) |
| `filter_price_lower_bound` | no | Minimum price in the local currency, whole number, e.g. 100 |
| `filter_price_upper_bound` | no | Maximum price in the local currency, whole number, e.g. 2000 |
| `filter_radius_km` | no | Search radius around the center in kilometres, e.g. 40 |
| `is_c2c_listing_only` | no | Individual sellers only |
| `exact_match` | no | Exact match search |
| `end_cursor` | no | Pagination cursor |

### `GET /facebook/marketplace/rentals`

Search Facebook Marketplace rental listings (apartments, houses, rooms) near a location, with price, bedroom, bathroom and radius filters. Returns rental listings with their listing_id, plus an end_cursor. For items for sale, use `/facebook/marketplace/search`. Pricing: 1 credit per call.

| Parameter | Required | Description |
|---|---|---|
| `sort_by` | no | Sort: CREATION_TIME_DESCEND, PRICE_ASCEND, BEST_MATCH |
| `filter_location_latitude` | no | Latitude of the search center, e.g. 30.2672 (from `/facebook/marketplace/city-coordinates`) |
| `filter_location_longitude` | no | Longitude of the search center, e.g. -97.7431 (from `/facebook/marketplace/city-coordinates`) |
| `filter_price_lower_bound` | no | Minimum price in the local currency, whole number, e.g. 100 |
| `filter_price_upper_bound` | no | Maximum price in the local currency, whole number, e.g. 2000 |
| `filter_radius_km` | no | Search radius around the center in kilometres, e.g. 40 |
| `filter_bedrooms_min` | no | Minimum number of bedrooms, e.g. 2 |
| `filter_bedrooms_max` | no | Maximum number of bedrooms |
| `filter_bathrooms_min` | no | Minimum number of bathrooms, e.g. 1 |
| `filter_bathrooms_max` | no | Maximum number of bathrooms |
| `is_c2c_listing_only` | no | Individual sellers only |
| `end_cursor` | no | Pagination cursor |

## Facebook media

### `GET /facebook/media/download`

Resolve a Facebook media URL (image, video or audio, e.g. from a post or reel) to direct downloadable file URLs. Returns URLs, not file bytes. Pricing: 1 credit per call.

| Parameter | Required | Description |
|---|---|---|
| `url` | yes | Facebook media URL to download |

## Instagram

### `GET /instagram/user/id`

Resolve an Instagram username or profile URL to its two IDs: user_id (long, e.g. 17841401474538262), used by `/instagram/profile/posts` and `/instagram/profile/reels`, and pk (short, e.g. 528817151), used by `/instagram/profile/highlights`. Pricing: 1 credit per call.

| Parameter | Required | Description |
|---|---|---|
| `link` | no | Instagram profile URL |
| `username` | no | Instagram username |

### `GET /instagram/profile/details`

Get an Instagram profile by username: bio, follower and post counts, verification status and related profiles. Pricing: 1 credit per call.

| Parameter | Required | Description |
|---|---|---|
| `username` | yes | Instagram username |
| `link` | no | Instagram profile URL (alternative to username) |

### `GET /instagram/profile/posts`

List an Instagram profile's posts (photos, videos, carousels) with captions, like and comment counts and media URLs. Pass username (returns more results) or user_id (the long user_id from `/instagram/user/id`, not the pk). Returns an end_cursor for the next page. For reels only, use `/instagram/profile/reels`. Pricing: 1 credit per call.

| Parameter | Required | Description |
|---|---|---|
| `username` | no | Instagram username (recommended — returns more results) |
| `user_id` | no | Long Instagram user ID: user_id from `/instagram/user/id` (e.g. 17841401474538262), not the pk. Alternative to username. |
| `end_cursor` | no | Pagination cursor for next page |

### `GET /instagram/profile/reels`

List an Instagram profile's reels with play counts, captions, video URLs and audio metadata. Needs the long user_id from `/instagram/user/id` (not the pk). Returns an end_cursor for the next page. Pricing: 1 credit per call.

| Parameter | Required | Description |
|---|---|---|
| `user_id` | yes | Long Instagram user ID: user_id from `/instagram/user/id` (e.g. 17841401474538262), not the pk. |
| `end_cursor` | no | Pagination cursor for next page |

### `GET /instagram/profile/highlights`

List an Instagram profile's story highlights with titles, cover images and highlight IDs. Needs the profile's pk from `/instagram/user/id`, passed as user_id (not the long user_id). Use `/instagram/highlight/details` to get the stories in one highlight. Pricing: 1 credit per call.

| Parameter | Required | Description |
|---|---|---|
| `user_id` | yes | The profile's pk from `/instagram/user/id` (e.g. 528817151), not the long user_id. |

### `GET /instagram/highlight/details`

Get the stories inside one Instagram highlight. Needs a highlight_id from `/instagram/profile/highlights`. Pricing: 1 credit per call.

| Parameter | Required | Description |
|---|---|---|
| `highlight_id` | yes | Highlight ID (from profile highlights endpoint) |

### `GET /instagram/post/id`

Extract the shortcode from an Instagram post or reel URL. `/instagram/post/details` needs the shortcode. Pricing: 1 credit per call.

| Parameter | Required | Description |
|---|---|---|
| `link` | yes | Instagram post URL |

### `GET /instagram/post/details`

Get one Instagram post or reel in full: caption, media URLs, engagement counts, timestamp and owner. Needs the shortcode (the part after /p/ or /reel/ in the URL, or from `/instagram/post/id`). Pricing: 1 credit per call.

| Parameter | Required | Description |
|---|---|---|
| `shortcode` | yes | Instagram post shortcode (e.g., DMF-GjGO0-q) |

### `GET /instagram/reels/feed`

Get Instagram's recommended and trending reels. Pass clips_media_id from a previous result to continue the feed or get similar reels by the same author. Not tied to a user; for one profile's reels use `/instagram/profile/reels`. Pricing: 1 credit per call.

| Parameter | Required | Description |
|---|---|---|
| `clips_media_id` | no | Clip media ID for chaining/pagination (from previous response) |

### `GET /instagram/reels/audio`

List Instagram reels that use a given sound. Needs the audio_id (music/audio cluster ID) found in reel results' audio metadata. Pass max_id from the previous response for the next page. Pricing: 1 credit per call.

| Parameter | Required | Description |
|---|---|---|
| `audio_id` | yes | Audio cluster ID (music ID) |
| `max_id` | no | Pagination cursor for next page |

### `GET /instagram/search`

Search Instagram by keyword and get the top matching users, hashtags and places. Use it to find a username, or a place's location_id for `/instagram/location/posts`. Returns an end_cursor for more. Pricing: 1 credit per call.

| Parameter | Required | Description |
|---|---|---|
| `keyword` | yes | Search keyword/query |
| `end_cursor` | no | Pagination cursor for next page |

### `GET /instagram/location/posts`

List Instagram posts tagged at a location: top posts (tab=ranked) or most recent (tab=recent). Needs a location_id, e.g. from a place in `/instagram/search`. Returns an end_cursor for the next page. Pricing: 1 credit per call.

| Parameter | Required | Description |
|---|---|---|
| `location_id` | yes | Instagram location ID |
| `tab` | no | Filter: "recent" or "ranked" |
| `end_cursor` | no | Pagination cursor for next page |

### `GET /instagram/location/nearby`

List Instagram places near a given location, with name, category, coordinates and post count. Needs a location_id, e.g. from a place in `/instagram/search`. Pricing: 1 credit per call.

| Parameter | Required | Description |
|---|---|---|
| `location_id` | yes | Instagram location ID |

## Account (free, no credits)

### `GET /usage`

Your plan, credits used and credits remaining. Free.

No parameters.

### `GET /usage/top-ups`

Your credit top-up history. Free.

No parameters.

### `GET /usage/limits`

Your plan's rate limits. Free.

No parameters.

