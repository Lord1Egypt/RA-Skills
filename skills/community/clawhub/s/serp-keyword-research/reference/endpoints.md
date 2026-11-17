# serp-keyword-research — endpoint reference

> Generated from `scripts/tools.json` by `scripts/generate.mjs` — do not edit by hand.

Endpoints this skill uses, grouped by platform. Call them via `scripts/crawlora.sh` (see SKILL.md).

All paths are relative to the API base `https://api.crawlora.net/api/v1` and require the header `x-api-key: $CRAWLORA_API_KEY`. Path params like `{id}` are substituted into the URL; `GET` params go in the query string; `POST` params go in a JSON body.

**43 endpoints across 9 platform group(s).**

## Google (15)

### `google_news`

- **HTTP:** `GET /google/news`
- **What:** Search Google News. Returns current Google News search results. Pages slice the finite result snapshot; they do not traverse the Google Search index. Results include title, source, publisher article URL, age, and thumbnail when available. Valid no-results searches and exhausted pages return an empty array. Locale defaults to country=us and lang=en. Returns 503 for blocked or malformed upstream responses.
- **Params:** `count` (integer, optional) — Results per page; defaults to 10, clamped to 1..50; `country` (string, optional) — Two-letter country code; defaults to us; `lang` (string, optional) — Google UI language; defaults to en; `page` (integer, optional) — 1-based page within the current finite result snapshot; defaults to 1; `q` (string, **required**) — Search query

### `google_news_search`

- **HTTP:** `POST /google/news`
- **What:** Search Google News with JSON. Restored JSON compatibility endpoint. Returns current Google News articles. Pages slice the finite current result snapshot. Uses the legacy result array and field names; no-results searches and exhausted pages return an empty result array.
- **Params:** `searchOption` (object, **required**) — Search options; keyword, language and country are required. limit defaults to 10 and is clamped to 10..100; page defaults to 1.
- **REST body:** Send the value of the MCP argument `searchOption` directly as the JSON body; do not wrap it in a `searchOption` property.

### `google_suggest`

- **HTTP:** `GET /google/suggest`
- **What:** Suggest Google search queries. Returns Google autosuggest query completions from the public unauthenticated suggest JSON endpoint. `source` selects the web, YouTube, or shopping suggestion list, and `rich=true` adds a type, relevance score, and short description to each suggestion.
- **Params:** `count` (integer, optional) — Suggestions to return; defaults to 10, clamped to 1..12; `country` (string, optional) — Google result country; defaults to us; `lang` (string, optional) — Google UI language; defaults to en; `q` (string, **required**) — Search query prefix; `rich` (boolean, optional) — Add Google's type, relevance score, and description to each suggestion; defaults to false; `source` (string, optional) — Suggestion source; defaults to web

### `google_trends_categories`

- **HTTP:** `GET /google/trends/categories`
- **What:** Google Trends categories. Returns the top-level Google Trends categories as id and name pairs, such as 0 for All and 20 for Sports. These are the ids accepted by the Trending Now category filter.
- **Params:** _none_

### `google_trends_enums`

- **HTTP:** `GET /google/trends/enums`
- **What:** Google Trends enum metadata. Returns supported Google Trends enum values for explore/trending filters, including locations, date ranges, search types, categories, statuses, and sort modes.
- **Params:** _none_

### `google_trends_explore`

- **HTTP:** `POST /google/trends/explore`
- **What:** Google Trends explore data. Returns Google Trends keyword analytics: interest over time, interest by region, related queries, and related topics when available.
- **Params:** `request` (object, **required**) — Explore request
- **REST body:** Send the value of the MCP argument `request` directly as the JSON body; do not wrap it in a `request` property.

### `google_trends_explore_interest_by_region`

- **HTTP:** `POST /google/trends/explore/interest-by-region`
- **What:** Google Trends interest by region. Returns only the interest-by-region widget from the Google Trends Explore widget flow. Supports multiple comparison terms and returns an empty interest_by_region array when Google returns no rows.
- **Params:** `request` (object, **required**) — Explore request
- **REST body:** Send the value of the MCP argument `request` directly as the JSON body; do not wrap it in a `request` property.

### `google_trends_explore_interest_over_time`

- **HTTP:** `POST /google/trends/explore/interest-over-time`
- **What:** Google Trends interest over time. Returns Google Trends interest over time for 1 to 5 `keywords`. Optional inputs are `geo` (default worldwide), `time_range` (default `today 12-m`), `hl`, `tz`, `category` and `type` (`web`, `image`, `news`, `youtube` or `shopping`). Each time point carries a value per keyword, with a `has_data` flag.
- **Params:** `request` (object, **required**) — Explore request
- **REST body:** Send the value of the MCP argument `request` directly as the JSON body; do not wrap it in a `request` property.

### `google_trends_explore_related_topics`

- **HTTP:** `POST /google/trends/explore/related-topics`
- **What:** Google Trends related topics. Returns only the related topics widget from the Google Trends Explore widget flow. Returns an empty related_topics array when Google returns no topic rows for the requested term/filter combination.
- **Params:** `request` (object, **required**) — Explore request
- **REST body:** Send the value of the MCP argument `request` directly as the JSON body; do not wrap it in a `request` property.

### `google_trends_explore_rising_queries`

- **HTTP:** `POST /google/trends/explore/rising-queries`
- **What:** Google Trends explore rising queries. Returns the Rising related queries widget for one or more Google Trends explore terms. Returns an empty queries array when Google returns no rows for the requested term/filter combination.
- **Params:** `request` (object, **required**) — Explore request
- **REST body:** Send the value of the MCP argument `request` directly as the JSON body; do not wrap it in a `request` property.

### `google_trends_explore_top_queries`

- **HTTP:** `POST /google/trends/explore/top-queries`
- **What:** Google Trends explore top queries. Returns the Top related queries widget for one or more Google Trends explore terms. Returns an empty queries array when Google returns no rows for the requested term/filter combination.
- **Params:** `request` (object, **required**) — Explore request
- **REST body:** Send the value of the MCP argument `request` directly as the JSON body; do not wrap it in a `request` property.

### `google_trends_locations`

- **HTTP:** `GET /google/trends/locations`
- **What:** Google Trends locations. Returns the list of location codes that Google Trends supports, such as `US`, `HK` and `GB`, in `locations`. The Explore endpoints also accept `WORLDWIDE`, which appears in the list. It takes no parameters.
- **Params:** _none_

### `google_trends_trending`

- **HTTP:** `GET /google/trends/trending`
- **What:** Google Trends trending now data. Returns Google Trends Trending Now for a country or territory (`geo`, default `US`): each trend's query, rank, search traffic, status, start and update time, related terms and news articles, with explore and share links. Filter by time window, category and status, and choose the sort order.
- **Params:** `category` (integer, optional) — Trending category id; `geo` (string, optional) — Country/territory location code; `hl` (string, optional) — Google Trends UI locale; `limit` (integer, optional) — Maximum rows to return; `sort_by` (string, optional) — Sort mode; `status` (string, optional) — Trend status filter; `time_range` (string, optional) — Alias for window; `tz` (integer, optional) — Timezone offset minutes; `window` (string, optional) — Trend window

### `google_trends_trending_detail`

- **HTTP:** `POST /google/trends/trending/detail`
- **What:** Google Trends trending term detail. Returns the Explore detail widgets for a single trending term, including interest over time, regional interest, top/rising related queries, and related topics when Google returns them.
- **Params:** `request` (object, **required**) — Trending detail request
- **REST body:** Send the value of the MCP argument `request` directly as the JSON body; do not wrap it in a `request` property.

### `google_videos`

- **HTTP:** `GET /google/videos`
- **What:** Search Google video results. Returns Google video vertical results (title, platform, link, duration, age). Locale defaults to country=us and lang=en. Returns 503 when Google serves a challenge page or an unusable response.
- **Params:** `count` (integer, optional) — Results per page; defaults to 10, clamped to 1..50; `country` (string, optional) — Two-letter country code; defaults to us; `lang` (string, optional) — Google UI language; defaults to en; `page` (integer, optional) — 1-based page number; defaults to 1; `q` (string, **required**) — Search query

## Bing (5)

### `bing_images`

- **HTTP:** `GET /bing/images`
- **What:** Search Bing image results. Returns Bing image search results for a query string. Locale defaults to country=us and lang=en-us. Returns 503 when Bing serves a challenge page or unusable results.
- **Params:** `count` (integer, optional) — Results per page; defaults to 10, clamped to 1..50; `country` (string, optional) — Two-letter country code; defaults to us; `lang` (string, optional) — Bing UI language; defaults to en-us; `page` (integer, optional) — 1-based page number; defaults to 1; `q` (string, **required**) — Search query

### `bing_news`

- **HTTP:** `GET /bing/news`
- **What:** Search Bing news results. Returns Bing news search results for a query string. Locale defaults to country=us and lang=en-us. Returns 503 when Bing serves a challenge page or unusable results.
- **Params:** `count` (integer, optional) — Results per page; defaults to 10, clamped to 1..50; `country` (string, optional) — Two-letter country code; defaults to us; `lang` (string, optional) — Bing UI language; defaults to en-us; `page` (integer, optional) — 1-based page number; defaults to 1; `q` (string, **required**) — Search query

### `bing_search`

- **HTTP:** `GET /bing/search`
- **What:** Search Bing web results. Returns Bing web search results for a query string, including organic results, optional context panel data, related queries, people-also-ask questions, news modules, video modules, and page-based pagination. Empty optional blocks are omitted from the JSON response. Locale defaults to country=us and lang=en-us. Returns 503 on a genuine transport failure or challenge page. Bing occasionally serves a well-formed page whose results share no significant term with the query; when every attempt hits this, the response is still returned as 200 with data.low_confidence set to true (and the X-Low-Confidence header) instead of being withheld, so callers get Bing's real answer plus an honest signal to double-check it rather than nothing. Queries that use the site: operator (for example site:gov.hu) are not supported: Bing serves a bot-verification challenge for them, so they are rejected with 400 before any request is made. Use the DuckDuckGo (/api/v1/duckduckgo/search), Brave (/api/v1/brave/search), or Yahoo (/api/v1/yahoo-search/search) search endpoints for domain-restricted searches instead.
- **Params:** `count` (integer, optional) — Results per page; defaults to 10, clamped to 1..50; `country` (string, optional) — Two-letter country code; defaults to us; `lang` (string, optional) — Bing UI language; defaults to en-us; `page` (integer, optional) — 1-based page number; defaults to 1; `q` (string, **required**) — Search query

### `bing_suggest`

- **HTTP:** `GET /bing/suggest`
- **What:** Suggest Bing search queries. Returns Bing autosuggest query completions for a query prefix. Locale defaults to country=us and lang=en-us. Suggestions are fetched from public Bing suggest endpoints and trimmed to the requested count. `rich=true` adds entity cards (name, description, image) where Bing shows them.
- **Params:** `count` (integer, optional) — Suggestions to return; defaults to 10, clamped to 1..12; `country` (string, optional) — Two-letter country code; defaults to us; `lang` (string, optional) — Bing UI language; defaults to en-us; `q` (string, **required**) — Search query prefix; `rich` (boolean, optional) — Add entity name, description, and image to suggestions Bing resolves to a known entity; defaults to false

### `bing_videos`

- **HTTP:** `GET /bing/videos`
- **What:** Search Bing video results. Returns Bing video search results for a query string. Locale defaults to country=us and lang=en-us. Returns 503 when Bing serves a challenge page or unusable results.
- **Params:** `count` (integer, optional) — Results per page; defaults to 10, clamped to 1..50; `country` (string, optional) — Two-letter country code; defaults to us; `lang` (string, optional) — Bing UI language; defaults to en-us; `page` (integer, optional) — 1-based page number; defaults to 1; `q` (string, **required**) — Search query

## Brave (5)

### `brave_images`

- **HTTP:** `GET /brave/images`
- **What:** Search Brave image results. Returns Brave image search results for a query string. Locale defaults to country=us and lang=en-us. Returns 503 when Brave serves a challenge page or unusable results.
- **Params:** `count` (integer, optional) — Results to return; defaults to 10, clamped to 1..50; `country` (string, optional) — Brave result country; defaults to us; `lang` (string, optional) — Brave UI language; defaults to en-us; `offset` (integer, optional) — Zero-based Brave result page; defaults to 0; `q` (string, **required**) — Search query

### `brave_news`

- **HTTP:** `GET /brave/news`
- **What:** Search Brave news results. Returns Brave news search results for a query string. Locale defaults to country=us and lang=en-us. Returns 503 when Brave serves a challenge page or unusable results.
- **Params:** `count` (integer, optional) — Results to return; defaults to 10, clamped to 1..50; `country` (string, optional) — Brave result country; defaults to us; `date_from` (string, optional) — Custom start date in YYYY-MM-DD; requires date_to; `date_to` (string, optional) — Custom end date in YYYY-MM-DD; requires date_from; `lang` (string, optional) — Brave UI language; defaults to en-us; `offset` (integer, optional) — Zero-based Brave result page; defaults to 0; `q` (string, **required**) — Search query; `time_range` (string, optional) — Preset time filter: any, day, week, month, year, or custom

### `brave_search`

- **HTTP:** `GET /brave/search`
- **What:** Search Brave. Returns web search results from Brave Search for a query string, along with offset-based pagination, related queries, discussions, videos, and the right-side knowledge card when Brave includes one. Use time_range for preset ranges or date_from/date_to for a custom YYYY-MM-DD range. Locale defaults to country=us and lang=en-us.
- **Params:** `country` (string, optional) — Brave result country; defaults to us; `date_from` (string, optional) — Custom start date in YYYY-MM-DD; requires date_to; `date_to` (string, optional) — Custom end date in YYYY-MM-DD; requires date_from; `lang` (string, optional) — Brave UI language; defaults to en-us; `offset` (integer, optional) — Zero-based Brave result page; `q` (string, **required**) — Search query; `time_range` (string, optional) — Preset time filter: any, day, week, month, year, or custom

### `brave_suggest`

- **HTTP:** `GET /brave/suggest`
- **What:** Suggest Brave search queries. Returns Brave autosuggest query completions for a query prefix. Locale defaults to country=us and lang=en-us. Suggestions are fetched from public Brave Search suggest JSON and trimmed to the requested count. `rich=true` adds entity metadata (name, description, category, image) where Brave resolves a suggestion to a known entity.
- **Params:** `count` (integer, optional) — Suggestions to return; defaults to 10, clamped to 1..12; `country` (string, optional) — Brave result country; defaults to us; `lang` (string, optional) — Brave UI language; defaults to en-us; `q` (string, **required**) — Search query prefix; `rich` (boolean, optional) — Add entity name, description, category, and image to suggestions Brave resolves to a known entity; defaults to false

### `brave_videos`

- **HTTP:** `GET /brave/videos`
- **What:** Search Brave video results. Returns Brave video search results for a query string. Locale defaults to country=us and lang=en-us. Returns 503 when Brave serves a challenge page or unusable results.
- **Params:** `count` (integer, optional) — Results to return; defaults to 10, clamped to 1..50; `country` (string, optional) — Brave result country; defaults to us; `date_from` (string, optional) — Custom start date in YYYY-MM-DD; requires date_to; `date_to` (string, optional) — Custom end date in YYYY-MM-DD; requires date_from; `lang` (string, optional) — Brave UI language; defaults to en-us; `offset` (integer, optional) — Zero-based Brave result page; defaults to 0; `q` (string, **required**) — Search query; `time_range` (string, optional) — Preset time filter: any, day, week, month, year, or custom

## DuckDuckGo Search (6)

### `duckduckgo_image`

- **HTTP:** `GET /duckduckgo/image`
- **What:** Search DuckDuckGo image results. Returns DuckDuckGo image results for a query string: title, source page URL, image URL, thumbnail, dimensions, and hostname, plus page-based pagination.
- **Params:** `page` (integer, optional) — 1-based page number, defaults to 1; `q` (string, **required**) — Search query; `region` (string, optional) — DuckDuckGo region/locale code, e.g. us-en, uk-en, wt-wt (worldwide, the default)

### `duckduckgo_news`

- **HTTP:** `GET /duckduckgo/news`
- **What:** Search DuckDuckGo news results. Returns DuckDuckGo news results for a query string: title, destination URL, source, excerpt, thumbnail, and relative/published time, plus page-based pagination.
- **Params:** `page` (integer, optional) — 1-based page number, defaults to 1; `q` (string, **required**) — Search query; `region` (string, optional) — DuckDuckGo region/locale code, e.g. us-en, uk-en, wt-wt (worldwide, the default)

### `duckduckgo_search`

- **HTTP:** `GET /duckduckgo/search`
- **What:** Search DuckDuckGo web results. Returns DuckDuckGo web search results for a query string: title, destination URL, description, and hostname, plus page-based pagination. DuckDuckGo wraps every result link in its own click-tracking redirect; this endpoint always returns the decoded destination URL, never the raw redirect link.
- **Params:** `page` (integer, optional) — 1-based page number, defaults to 1; `q` (string, **required**) — Search query; `region` (string, optional) — DuckDuckGo region/locale code, e.g. us-en, uk-en, wt-wt (worldwide, the default); `safe_search` (string, optional) — Safe search level, defaults to DuckDuckGo's own moderate setting when omitted; `time_range` (string, optional) — Restrict results to a recency window

### `duckduckgo_shopping`

- **HTTP:** `GET /duckduckgo/shopping`
- **What:** Search DuckDuckGo shopping results. Returns DuckDuckGo shopping results for a query string: title, brand, merchant, description, price, rating, and review count, plus total page count. DuckDuckGo's shopping vertical is ad-funded, syndicated product listings, not organic content; every product link is wrapped in an ad-click-tracking redirect with no clean destination to unwrap, so no destination URL is returned. DuckDuckGo's own pagination token for this vertical is an opaque per-response blob rather than a plain page offset, so only the first page is supported.
- **Params:** `q` (string, **required**) — Search query; `region` (string, optional) — DuckDuckGo market code, e.g. us-en, uk-en

### `duckduckgo_suggest`

- **HTTP:** `GET /duckduckgo/suggest`
- **What:** Suggest DuckDuckGo search queries. Returns DuckDuckGo search-box autocomplete completions for a query prefix, in DuckDuckGo's own ranking order. DuckDuckGo never returns more than 8 suggestions per prefix.
- **Params:** `count` (integer, optional) — Suggestions to return; defaults to 8, clamped to 1..8; `q` (string, **required**) — Search query prefix; `region` (string, optional) — DuckDuckGo region code such as us-en, uk-en, de-de, or wt-wt (worldwide, the default)

### `duckduckgo_video`

- **HTTP:** `GET /duckduckgo/video`
- **What:** Search DuckDuckGo video results. Returns DuckDuckGo video results for a query string: title, destination URL, description, duration, thumbnail, publisher/uploader, published time, and view count, plus page-based pagination.
- **Params:** `page` (integer, optional) — 1-based page number, defaults to 1; `q` (string, **required**) — Search query; `region` (string, optional) — DuckDuckGo region/locale code, e.g. us-en, uk-en, wt-wt (worldwide, the default)

## Yahoo Search (6)

### `yahoo_search`

- **HTTP:** `GET /yahoo-search/search`
- **What:** Search Yahoo web results. Returns Yahoo web search results for a query string: title, destination URL, description, and hostname, plus page-based pagination. Yahoo wraps every result link in its own click-tracking redirect; this endpoint always returns the decoded destination URL, never the raw redirect link.
- **Params:** `page` (integer, optional) — 1-based page number, defaults to 1; `q` (string, **required**) — Search query; `time_range` (string, optional) — Restrict results by recency. Omit for unfiltered ('Anytime').

### `yahoo_search_images`

- **HTTP:** `GET /yahoo-search/images`
- **What:** Search Yahoo image results. Returns Yahoo's image-search results for a query: title, direct image URL, the page hosting the image, source domain, thumbnail, and original image dimensions when available. Results are fetched from Yahoo's own server-rendered image-search page.
- **Params:** `q` (string, **required**) — Search query

### `yahoo_search_local`

- **HTTP:** `GET /yahoo-search/local`
- **What:** Search Yahoo local business results. Returns Yahoo's local-business-search results for a query: name, category, price range, address, phone, open status, rating, and review count. Location is resolved from the query text itself, the same way a user would type into Yahoo's own local search box (e.g. "pizza near seattle wa"), not a separate coordinate parameter. Results are fetched from Yahoo's own server-rendered local-search page.
- **Params:** `q` (string, **required**) — Search query, including any location intent

### `yahoo_search_news`

- **HTTP:** `GET /yahoo-search/news`
- **What:** Search Yahoo news results. Returns Yahoo's news-search results for a query: title, destination URL, description, source, and relative publish age. Results are fetched from Yahoo's own server-rendered news-search page (news.search.yahoo.com) -- a distinct product from the yahoo-news family, which covers the www.yahoo.com/news portal itself. Yahoo wraps every result link in its own click-tracking redirect; this endpoint always returns the decoded destination URL, never the raw redirect link.
- **Params:** `q` (string, **required**) — Search query

### `yahoo_search_suggest`

- **HTTP:** `GET /yahoo-search/suggest`
- **What:** Yahoo web search autocomplete suggestions. Returns Yahoo's own search-box autocomplete suggestions for a partial query: a flat list of suggested search terms, each optionally carrying knowledge-panel entity metadata (type, image, subtitle, description) when Yahoo resolves the term to a known company, place, product, or similar entity rather than a plain phrase.
- **Params:** `count` (integer, optional) — Number of suggestions to return, default 10, clamped to 1..20; `q` (string, **required**) — Partial search query to autocomplete

### `yahoo_search_videos`

- **HTTP:** `GET /yahoo-search/videos`
- **What:** Search Yahoo video results. Returns Yahoo's video-search results for a query: title, destination page URL, source domain, description, thumbnail, and duration. Results are fetched from Yahoo's own server-rendered video-search page.
- **Params:** `q` (string, **required**) — Search query

## Baidu (2)

### `baidu_search`

- **HTTP:** `GET /baidu/search`
- **What:** Search Baidu web results. Returns Baidu result cards for a query: title, destination URL, snippet, publisher, and date, with page-based pagination. Each result's `type` is `web` (standard pages), `video` (video cards), or `baike` (Baidu Baike encyclopedia entries); answer widgets such as weather, entity panels, and recommendation lists are not returned. Baidu challenges a portion of requests with a security verification page; the service retries and returns 503 if every attempt is challenged, so callers should retry on 503.
- **Params:** `page` (integer, optional) — 1-based result page; defaults to 1, maximum 10; `q` (string, **required**) — Search query

### `baidu_suggest`

- **HTTP:** `GET /baidu/suggest`
- **What:** Suggest Baidu search queries. Returns Baidu search-box autocomplete completions for a query prefix, in Baidu's own ranking order. Baidu never returns more than 10 suggestions per prefix; Chinese prefixes are supported.
- **Params:** `count` (integer, optional) — Suggestions to return; defaults to 10, clamped to 1..10; `q` (string, **required**) — Search query prefix

## Yandex (2)

### `yandex_search`

- **HTTP:** `GET /yandex/search`
- **What:** Search Yandex web results. Returns organic Yandex web results for a query: title, destination URL, display URL, and snippet, with page-based pagination. Advertisements are not returned. Yandex challenges a portion of requests with a captcha; the service retries and returns 503 if every attempt is challenged, so callers should retry on 503. Results are localized by Yandex to the location the request is made from.
- **Params:** `page` (integer, optional) — 1-based result page; defaults to 1, maximum 10; `q` (string, **required**) — Search query

### `yandex_suggest`

- **HTTP:** `GET /yandex/suggest`
- **What:** Suggest Yandex search queries. Returns Yandex search-box autocomplete completions for a query prefix, in Yandex's own ranking order. `lang` is the two-letter Yandex UI language (en, ru, tr, ...) and re-ranks the list; Yandex ignores codes it does not support.
- **Params:** `count` (integer, optional) — Suggestions to return; defaults to 10, clamped to 1..20; `lang` (string, optional) — Two-letter Yandex UI language, such as en, ru, or tr; defaults to en; `q` (string, **required**) — Search query prefix

## Qwant (1)

### `qwant_suggest`

- **HTTP:** `GET /qwant/suggest`
- **What:** Suggest Qwant search queries. Returns Qwant search-box autocomplete completions for a query prefix, in Qwant's own ranking order. `locale` selects the Qwant market (en_US, fr_FR, de_DE, en_GB, ...); Qwant ignores locale codes it does not support and uses its default market.
- **Params:** `count` (integer, optional) — Suggestions to return; defaults to 10, clamped to 1..10; `locale` (string, optional) — Qwant market locale in ll_CC form, such as en_US, fr_FR, de_DE, or en_GB; defaults to en_US; `q` (string, **required**) — Search query prefix

## Startpage (1)

### `startpage_suggest`

- **HTTP:** `GET /startpage/suggest`
- **What:** Suggest Startpage search queries. Returns Startpage search-box autocomplete completions for a query prefix, in Startpage's own ranking order. Startpage never returns more than 10 suggestions per prefix.
- **Params:** `count` (integer, optional) — Suggestions to return; defaults to 10, clamped to 1..10; `q` (string, **required**) — Search query prefix
