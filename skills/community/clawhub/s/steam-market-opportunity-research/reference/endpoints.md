# steam-market-opportunity-research — endpoint reference

> Generated from `scripts/tools.json` by `scripts/generate.mjs` — do not edit by hand.

Only the endpoints used by this workflow. Call them via `scripts/crawlora.sh` (see SKILL.md).

All paths are relative to the API base `https://api.crawlora.net/api/v1` and require the header `x-api-key: $CRAWLORA_API_KEY`. Path params like `{id}` are substituted into the URL; `GET` params go in the query string; `POST` params go in a JSON body.

**19 endpoints across 2 platform group(s).**

## Datasets (7)

### `datasets_steam_charts_search`

- **HTTP:** `GET /datasets/steam-charts/search`
- **What:** Search the steam-charts dataset. Searches daily snapshots of Steam's player-count and sales charts, stored in a search index (one document per chart × country × snapshot × rank) so history accumulates. Charts: `most_played` (weekly peak concurrent), `concurrent` (live concurrent players), `top_sellers` (weekly sales; country-specific). With no `date` the latest snapshot is returned (today's chart); pair `app_id` with `sort=date_desc` for an app's rank/players over time. Country is `global` for the player-count charts or an ISO code (e.g. `us`) for `top_sellers`. Sort enum: `rank`, `rank_desc`, `date_desc`. Billing: this search costs 1 credit per record returned, with a minimum of 2 (an empty result costs 2, a full page of 100 costs 100).
- **Params:** `app_id` (string, optional) — Exact Steam app id filter; pair with sort=date_desc for rank/players history; `chart` (string, optional) — Chart enum: most_played, concurrent, top_sellers; `country` (string, optional) — Market filter: global (player-count charts) or an ISO country code (top_sellers), max 128 characters; `date` (string, optional) — Snapshot date filter yyyy-MM-dd; defaults to the latest snapshot; `page` (integer, optional) — Page number, defaults to 1; `page_size` (integer, optional) — Page size, defaults to 20 and maxes at 100; page * page_size must be <= 10000; `q` (string, optional) — Full-text query over the game name, max 256 characters; `sort` (string, optional) — Sort enum: rank, rank_desc, date_desc

### `datasets_steam_games_facets`

- **HTTP:** `GET /datasets/steam-games/facets`
- **What:** Facet the Steam games dataset. Returns terms aggregation counts for the Steam games dataset. Facet enum: `type`, `developer`, `publisher`, `genres`, `categories`, `tags`, `primary_tag`, `price_tier`, `review_tier`, `owners_bucket`, `release_year`, `run_id`, `is_free`, `coming_soon`, `platform_windows`, `platform_mac`, `platform_linux`. price_tier enum: `free`, `under5`, `5to15`, `15to30`, `30to60`, `over60`. review_tier enum: `overwhelmingly_positive`, `very_positive`, `positive`, `mostly_positive`, `mixed`, `mostly_negative`, `negative`, `very_negative`, `overwhelmingly_negative`, `insufficient`.
- **Params:** `category` (string, optional) — Exact store category filter, max 128 characters; `developer` (string, optional) — Exact developer filter, max 128 characters; `facet` (string, **required**) — Facet enum: type, developer, publisher, genres, categories, tags, primary_tag, price_tier, review_tier, owners_bucket, release_year, run_id, is_free, coming_soon, platform_windows, platform_mac, platform_linux; `genre` (string, optional) — Exact genre filter, max 128 characters; `is_free` (boolean, optional) — Filter by free-to-play flag; `linux` (boolean, optional) — Filter by Linux support; `mac` (boolean, optional) — Filter by macOS support; `max_price_cents` (integer, optional) — Maximum current price in cents; `max_release_year` (integer, optional) — Maximum release year; `min_ccu` (integer, optional) — Minimum peak concurrent users yesterday; `min_metacritic` (integer, optional) — Minimum Metacritic score, 0 through 100; `min_owners` (integer, optional) — Minimum estimated owners (SteamSpy owners midpoint); `min_positive` (integer, optional) — Minimum positive review count; `min_price_cents` (integer, optional) — Minimum current price in cents; `min_release_year` (integer, optional) — Minimum release year; `min_review_score` (number, optional) — Minimum positive-review ratio, 0 through 1; `min_total_reviews` (integer, optional) — Minimum total review count; `on_sale` (boolean, optional) — Filter by titles currently discounted (discount_pct > 0); `owners_bucket` (string, optional) — Exact SteamSpy owners-range bucket filter, max 128 characters; `price_tier` (string, optional) — Price-tier enum: free, under5, 5to15, 15to30, 30to60, over60; `publisher` (string, optional) — Exact publisher filter, max 128 characters; `q` (string, optional) — Full-text query over name, developer and publisher, max 256 characters; `review_tier` (string, optional) — Review-tier enum: overwhelmingly_positive, very_positive, positive, mostly_positive, mixed, mostly_negative, negative, very_negative, overwhelmingly_negative, insufficient; `run_id` (string, optional) — Exact crawl run-id filter, max 128 characters; `tag` (string, optional) — Exact community-tag filter (e.g. Roguelike, Cozy), max 128 characters; `type` (string, optional) — Exact storefront type filter, max 128 characters; `windows` (boolean, optional) — Filter by Windows support

### `datasets_steam_games_item`

- **HTTP:** `GET /datasets/steam-games/items/{appid}`
- **What:** Get a Steam game from the dataset. Returns one Steam game from the `steam-games` dataset by numeric appid: name, developers and publishers, genres and categories, price and discount, supported platforms, positive and negative review counts, owner estimates, average and median playtime, concurrent players, Metacritic score and language count. It reads the stored dataset and does not trigger a live scrape; an appid that is not in the dataset returns `404`.
- **Params:** `appid` (integer, **required**) — Steam app id

### `datasets_steam_games_search`

- **HTTP:** `GET /datasets/steam-games/search`
- **What:** Search the Steam games dataset. Searches enriched public Steam catalog records stored in a search index. price_tier enum: `free`, `under5`, `5to15`, `15to30`, `30to60`, `over60`. review_tier enum: `overwhelmingly_positive`, `very_positive`, `positive`, `mostly_positive`, `mixed`, `mostly_negative`, `negative`, `very_negative`, `overwhelmingly_negative`, `insufficient`. Sort enum: `relevance`, `owners_desc`, `reviews_desc`, `review_score_desc`, `ccu_desc`, `metacritic_desc`, `price_asc`, `price_desc`, `release_desc`, `release_asc`. Billing: this search costs 1 credit per record returned, with a minimum of 2 (an empty result costs 2, a full page of 100 costs 100).
- **Params:** `category` (string, optional) — Exact store category filter (e.g. Single-player), max 128 characters; `developer` (string, optional) — Exact developer filter, max 128 characters; `genre` (string, optional) — Exact genre filter (e.g. Action, Indie), max 128 characters; `is_free` (boolean, optional) — Filter by free-to-play flag; `linux` (boolean, optional) — Filter by Linux support; `mac` (boolean, optional) — Filter by macOS support; `max_price_cents` (integer, optional) — Maximum current price in cents; `max_release_year` (integer, optional) — Maximum release year; `min_ccu` (integer, optional) — Minimum peak concurrent users yesterday; `min_metacritic` (integer, optional) — Minimum Metacritic score, 0 through 100; `min_owners` (integer, optional) — Minimum estimated owners (SteamSpy owners midpoint); `min_positive` (integer, optional) — Minimum positive review count; `min_price_cents` (integer, optional) — Minimum current price in cents; `min_release_year` (integer, optional) — Minimum release year; `min_review_score` (number, optional) — Minimum positive-review ratio, 0 through 1; `min_total_reviews` (integer, optional) — Minimum total review count; `on_sale` (boolean, optional) — Filter by titles currently discounted (discount_pct > 0); `owners_bucket` (string, optional) — Exact SteamSpy owners-range bucket filter, max 128 characters; `page` (integer, optional) — Page number, defaults to 1; `page_size` (integer, optional) — Page size, defaults to 20 and maxes at 100; page * page_size must be <= 10000; `price_tier` (string, optional) — Price-tier enum: free, under5, 5to15, 15to30, 30to60, over60; `publisher` (string, optional) — Exact publisher filter, max 128 characters; `q` (string, optional) — Full-text query over name, developer and publisher, max 256 characters; `review_tier` (string, optional) — Review-tier enum: overwhelmingly_positive, very_positive, positive, mostly_positive, mixed, mostly_negative, negative, very_negative, overwhelmingly_negative, insufficient; `run_id` (string, optional) — Exact crawl run-id filter, max 128 characters; `sort` (string, optional) — Sort enum: relevance, owners_desc, reviews_desc, review_score_desc, ccu_desc, metacritic_desc, price_asc, price_desc, release_desc, release_asc; `tag` (string, optional) — Exact community-tag filter (e.g. Roguelike, Metroidvania, Cozy), max 128 characters; `type` (string, optional) — Exact storefront type filter (e.g. game, dlc, demo), max 128 characters; `windows` (boolean, optional) — Filter by Windows support

### `datasets_steam_news_search`

- **HTTP:** `GET /datasets/steam-news/search`
- **What:** Search the steam-news dataset. Searches Steam news + announcements for tracked apps (one document per appid × gid; the latest items per app are kept). Filter by `app_id` for a single game's news, or full-text `q` over the title + contents. Sort enum: `date_desc` (newest first, default), `date_asc`. Billing: this search costs 1 credit per record returned, with a minimum of 2 (an empty result costs 2, a full page of 100 costs 100).
- **Params:** `app_id` (string, optional) — Exact Steam app id filter; `page` (integer, optional) — Page number, defaults to 1; `page_size` (integer, optional) — Page size, defaults to 20 and maxes at 100; page * page_size must be <= 10000; `q` (string, optional) — Full-text query over the news title + contents, max 256 characters; `sort` (string, optional) — Sort enum: date_desc, date_asc

### `datasets_steam_playercounts_search`

- **HTTP:** `GET /datasets/steam-playercounts/search`
- **What:** Search steam-playercounts dataset. Searches the daily concurrent-player time series for tracked games (one document per appid × day). Pair `app_id` with `sort=date_desc` for a game's player-count history, or pass `date` for one day's snapshot. Sort enum: `date_desc` (default), `date_asc`, `players_desc`. Billing: this search costs 1 credit per record returned, with a minimum of 2 (an empty result costs 2, a full page of 100 costs 100).
- **Params:** `app_id` (string, optional) — Exact Steam app id filter; `date` (string, optional) — Snapshot date filter yyyy-MM-dd; `page` (integer, optional) — Page number, defaults to 1; `page_size` (integer, optional) — Page size, defaults to 20 and maxes at 100; page * page_size must be <= 10000; `sort` (string, optional) — Sort enum: date_desc, date_asc, players_desc

### `datasets_steam_reviews_search`

- **HTTP:** `GET /datasets/steam-reviews/search`
- **What:** Search the steam-reviews dataset. Searches the stored Steam review corpus (the most-helpful reviews per game; one document per appid × recommendation). Full-text `q` over the review body, filter by `app_id`, `language`, or `voted_up` (positive/negative). Sort enum: `votes_desc` (most-helpful first, default), `weighted_desc`, `date_desc`. Billing: this search costs 1 credit per record returned, with a minimum of 2 (an empty result costs 2, a full page of 100 costs 100).
- **Params:** `app_id` (string, optional) — Exact Steam app id filter; `language` (string, optional) — Review language filter (e.g. english, schinese); `page` (integer, optional) — Page number, defaults to 1; `page_size` (integer, optional) — Page size, defaults to 20 and maxes at 100; page * page_size must be <= 10000; `q` (string, optional) — Full-text query over the review body, max 256 characters; `sort` (string, optional) — Sort enum: votes_desc, weighted_desc, date_desc; `voted_up` (string, optional) — Recommendation filter: true (positive) or false (negative)

## Steam (12)

### `steam_app`

- **HTTP:** `GET /steam/app`
- **What:** Get Steam store details for an app. Returns store metadata for a single Steam app (title, type, price, developers/publishers, platforms, genres, categories, release date, metacritic, recommendation and achievement counts). cc selects the store region (and price currency) and l the text language. filters is a comma-separated subset of allowed fields to shrink the payload.
- **Params:** `appid` (string, **required**) — Numeric Steam app id; `cc` (string, optional) — Store country code (ISO, selects currency); `filters` (string, optional) — Comma-separated fields: basic, price_overview, developers, publishers, categories, genres, release_date, platforms, metacritic, achievements, screenshots, movies, recommendations, controller_support, dlc, short_description, supported_languages, packages, package_groups, ratings, content_descriptors, background; `l` (string, optional) — Language code

### `steam_category`

- **HTTP:** `GET /steam/category/{slug}`
- **What:** Browse a store category (tag) with weighted community tags. Returns a catalog slice for a community tag / category, carrying each item's WEIGHTED community tags, review-score breakdown, developer/publisher credits, release date, platforms and price. The slug is a numeric tag id or a tag name (case- and separator-insensitive, e.g. rogue_like); resolve ids via /steam/tags/list. Ordering is Steam's default relevance — for sorted or os/price-faceted browse use /steam/tags.
- **Params:** `cc` (string, optional) — Store country code (ISO, selects currency); `coming_soon_only` (boolean, optional) — Only unreleased / coming-soon titles; `count` (integer, optional) — Results per page (max 100); `free` (boolean, optional) — Only free titles; `l` (string, optional) — Steam store language name; `released_only` (boolean, optional) — Only already-released titles; `slug` (string, **required**) — Community tag id (numeric) or tag name slug; `start` (integer, optional) — Result offset for pagination

### `steam_items`

- **HTTP:** `GET /steam/items`
- **What:** Resolve a batch of app ids to store items with weighted tags. Resolves up to 100 Steam app ids in one call to store items, each carrying its WEIGHTED community tags, review-score breakdown, developer/publisher credits, release date, platforms and price. The batch enrichment primitive for the community-tag taxonomy.
- **Params:** `appids` (string, **required**) — Comma-separated numeric app ids (max 100); `cc` (string, optional) — Store country code (ISO, selects currency); `l` (string, optional) — Steam store language name

### `steam_news`

- **HTTP:** `GET /steam/news`
- **What:** Get recent news posts for a Steam app. Returns recent news and announcement posts for a Steam app by numeric `appid` (for example `570`). `count` sets the number of posts (default 10, max 50) and `maxlength` caps each post body in characters (default 300, `-1` for the full body). Each post has `gid`, title, URL, author, contents, feed label and name, `date`, `is_external_url` and `tags`.
- **Params:** `appid` (string, **required**) — Numeric Steam app id; `count` (integer, optional) — Number of posts (max 50); `maxlength` (integer, optional) — Max characters of each post body; default 300, set -1 for full content

### `steam_players`

- **HTTP:** `GET /steam/players`
- **What:** Get the current concurrent-player count for a Steam app. Returns the current number of concurrent players for a Steam app, given its numeric `appid` such as `570`. The response has `appid`, `player_count` and a `source_url`. An app with no player-count data returns 404.
- **Params:** `appid` (string, **required**) — Numeric Steam app id

### `steam_reviews`

- **HTTP:** `GET /steam/reviews`
- **What:** List reviews for a Steam app. Returns a page of user reviews for an app with cursor pagination and an aggregate query_summary (score, positive/negative totals). Aggregate totals populate only on the first page (cursor=*). Pass the returned cursor back to page.
- **Params:** `appid` (string, **required**) — Numeric Steam app id; `cursor` (string, optional) — Pagination cursor from the previous page; `day_range` (integer, optional) — Look-back window in days (filter=all only, max 365); `filter` (string, optional) — Sort order; `language` (string, optional) — Steam language name or 'all'; `num_per_page` (integer, optional) — Reviews per page (max 100); `purchase_type` (string, optional) — Purchase source filter; `review_type` (string, optional) — Review sentiment filter

### `steam_reviews_histogram`

- **HTTP:** `GET /steam/reviews/histogram`
- **What:** Get the review up/down histogram for a Steam app. Returns the positive/negative recommendation counts over time (the store review graph): weekly/monthly rollups plus recent daily buckets.
- **Params:** `appid` (string, **required**) — Numeric Steam app id; `language` (string, optional) — Steam language name or 'all'

### `steam_search`

- **HTTP:** `GET /steam/search`
- **What:** Search the Steam store by title. Resolves a search term to Steam apps via the store typeahead (title, appid, price, platforms, metascore). Best for title -> appid lookup; returns roughly ten results. For faceted, paginated search use /steam/search/results.
- **Params:** `cc` (string, optional) — Store country code (ISO, selects currency); `l` (string, optional) — Language code; `term` (string, **required**) — Search term

### `steam_search_results`

- **HTTP:** `GET /steam/search/results`
- **What:** Faceted, paginated Steam store search. Runs the Steam store search with pagination and sorting and returns the result rows (appid, title, release date, review summary, price, platforms). Supports start/count paging and sort_by.
- **Params:** `cc` (string, optional) — Store country code (ISO, selects currency); `count` (integer, optional) — Results per page (max 100); `l` (string, optional) — Language code; `sort_by` (string, optional) — Sort order; `start` (integer, optional) — Result offset for pagination; `term` (string, **required**) — Search term

### `steam_steamspy`

- **HTTP:** `GET /steam/steamspy`
- **What:** Get SteamSpy third-party ownership and playtime estimates. Returns third-party ownership, concurrent-user, playtime, and review estimates for an app from SteamSpy. These are SteamSpy estimates, not official Steam figures.
- **Params:** `appid` (string, **required**) — Numeric Steam app id

### `steam_tags`

- **HTTP:** `GET /steam/tags`
- **What:** Browse the Steam store by community tag and store facets. Browses the store by the community-tag taxonomy (Roguelike, Metroidvania, Cozy...) and the store filter facets, with no free-text term. Filter by one or more tag ids, a store category id, platform (os), a maximum price, specials-only, and hide-free-to-play; sort and page the browse-rank rows. Each row includes its community tag ids (resolve names via /steam/tags/list). Pagination runs the full result set (total is the real, fully-pageable match count); paging past total returns an empty page.
- **Params:** `category1` (string, optional) — Numeric Steam store category id (e.g. 998 games, 21 dlc); `category2` (string, optional) — Additional numeric store category id (feature); `category3` (string, optional) — Additional numeric store category id (feature); `cc` (string, optional) — Store country code (ISO, selects currency); `count` (integer, optional) — Results per page (max 100); `deck_compatibility` (string, optional) — Steam Deck compatibility filter: 1 unsupported, 2 playable, 3 verified; `filter` (string, optional) — Curated preset applied within the other facets; `hidef2p` (boolean, optional) — Hide free-to-play titles; `l` (string, optional) — Language code; `maxprice` (string, optional) — Maximum price as whole cents in the cc currency, or the literal 'free'; `os` (string, optional) — Comma-separated platform filter subset of: win, mac, linux; `sort_by` (string, optional) — Sort order; `specials` (boolean, optional) — Only discounted titles; `start` (integer, optional) — Result offset for pagination; `supportedlang` (string, optional) — Only titles supporting this Steam language name; `tags` (string, optional) — Comma-separated numeric community tag ids (all must match); resolve ids via /steam/tags/list; `untags` (string, optional) — Comma-separated numeric community tag ids to EXCLUDE; `vrsupport` (string, optional) — Comma-separated VR-support filter ids (e.g. 401 seated, 402 standing, 403 roomscale)

### `steam_tags_list`

- **HTTP:** `GET /steam/tags/list`
- **What:** List Steam community tag ids and names. Returns Steam's popular community tags (numeric id + localized name) so callers can map a tag name to the id that /steam/tags and /steam/category expect.
- **Params:** `l` (string, optional) — Steam store language name for the tag labels
