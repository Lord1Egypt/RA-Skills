# topic-demand-validation — endpoint reference

> Generated from `scripts/tools.json` by `scripts/generate.mjs` — do not edit by hand.

Only the endpoints used by this workflow. Call them via `scripts/crawlora.sh` (see SKILL.md).

All paths are relative to the API base `https://api.crawlora.net/api/v1` and require the header `x-api-key: $CRAWLORA_API_KEY`. Path params like `{id}` are substituted into the URL; `GET` params go in the query string; `POST` params go in a JSON body.

**15 endpoints across 6 platform group(s).**

## Google (5)

### `google_suggest`

- **HTTP:** `GET /google/suggest`
- **What:** Suggest Google search queries. Returns Google autosuggest query completions from the public unauthenticated suggest JSON endpoint. `source` selects the web, YouTube, or shopping suggestion list, and `rich=true` adds a type, relevance score, and short description to each suggestion.
- **Params:** `count` (integer, optional) — Suggestions to return; defaults to 10, clamped to 1..12; `country` (string, optional) — Google result country; defaults to us; `lang` (string, optional) — Google UI language; defaults to en; `q` (string, **required**) — Search query prefix; `rich` (boolean, optional) — Add Google's type, relevance score, and description to each suggestion; defaults to false; `source` (string, optional) — Suggestion source; defaults to web

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

## Bing (1)

### `bing_search`

- **HTTP:** `GET /bing/search`
- **What:** Search Bing web results. Returns Bing web search results for a query string, including organic results, optional context panel data, related queries, people-also-ask questions, news modules, video modules, and page-based pagination. Empty optional blocks are omitted from the JSON response. Locale defaults to country=us and lang=en-us. Returns 503 on a genuine transport failure or challenge page. Bing occasionally serves a well-formed page whose results share no significant term with the query; when every attempt hits this, the response is still returned as 200 with data.low_confidence set to true (and the X-Low-Confidence header) instead of being withheld, so callers get Bing's real answer plus an honest signal to double-check it rather than nothing. Queries that use the site: operator (for example site:gov.hu) are not supported: Bing serves a bot-verification challenge for them, so they are rejected with 400 before any request is made. Use the DuckDuckGo (/api/v1/duckduckgo/search), Brave (/api/v1/brave/search), or Yahoo (/api/v1/yahoo-search/search) search endpoints for domain-restricted searches instead.
- **Params:** `count` (integer, optional) — Results per page; defaults to 10, clamped to 1..50; `country` (string, optional) — Two-letter country code; defaults to us; `lang` (string, optional) — Bing UI language; defaults to en-us; `page` (integer, optional) — 1-based page number; defaults to 1; `q` (string, **required**) — Search query

## Brave (1)

### `brave_search`

- **HTTP:** `GET /brave/search`
- **What:** Search Brave. Returns web search results from Brave Search for a query string, along with offset-based pagination, related queries, discussions, videos, and the right-side knowledge card when Brave includes one. Use time_range for preset ranges or date_from/date_to for a custom YYYY-MM-DD range. Locale defaults to country=us and lang=en-us.
- **Params:** `country` (string, optional) — Brave result country; defaults to us; `date_from` (string, optional) — Custom start date in YYYY-MM-DD; requires date_to; `date_to` (string, optional) — Custom end date in YYYY-MM-DD; requires date_from; `lang` (string, optional) — Brave UI language; defaults to en-us; `offset` (integer, optional) — Zero-based Brave result page; `q` (string, **required**) — Search query; `time_range` (string, optional) — Preset time filter: any, day, week, month, year, or custom

## Reddit (2)

### `reddit_comments`

- **HTTP:** `GET /reddit/comments/{id}`
- **What:** Get Reddit post comments. Returns a Reddit post with its public comments. The default mode is 1 credit. Set `include_metrics=true` to return the comments with public net score and award count plus post engagement metrics for 3 credits. Large threads may expose only an initial comment subset. Reddit does not expose per-comment upvote ratios or exact upvote/downvote totals anonymously. A post that exists but has no comments yet returns a 200 response with an empty comments list; a post that does not exist returns 404, and a temporary block or upstream failure returns 503 (retryable) rather than 404. If source.type is redlib, public fields and credit weights are preserved.
- **Params:** `depth` (integer, optional) — Maximum flat comment depth returned in metrics mode.; `id` (string, **required**) — Reddit post id or t3_ id; `include_metrics` (boolean, optional) — Include public post and per-comment engagement metrics; costs 3 credits instead of 1; `limit` (integer, optional) — Maximum comments returned, defaults to 25 and clamps to 100; `sort` (string, optional) — Comment order: confidence, top, new, controversial, old, or qa. Applied to the anonymous HTML request when metrics are enabled.

### `reddit_search`

- **HTTP:** `GET /reddit/search`
- **What:** Search Reddit posts. Searches public Reddit content and returns public post entries. A `503` with a `Retry-After` header means Reddit is temporarily throttling the request; wait that many seconds and retry. If source.type is redlib, public fields and credit weights are preserved.
- **Params:** `after` (string, optional) — Reddit pagination token; `limit` (integer, optional) — Maximum posts, defaults to 25 and clamps to 100; `q` (string, **required**) — Search keywords; `sort` (string, optional) — Sort: relevance, hot, new, top, or comments; `subreddit` (string, optional) — Restrict search to a subreddit name, without r/; `time` (string, optional) — Time window for top/comments sorts: hour, day, week, month, year, or all

## TikTok (2)

### `tiktok_comments`

- **HTTP:** `GET /tiktok/comments`
- **What:** Retrieve TikTok video comments. Returns the top-level comments on a TikTok video, by the video id from its URL (`aweme_id`). Results are paged by cursor: pass the `cursor` from one response to get the next page, and read `has_more` to see whether more remain. The response also carries the total comment count.
- **Params:** `aweme_id` (string, **required**) — TikTok video id from the video URL; `cursor` (integer, optional) — Pagination cursor

### `tiktok_search`

- **HTTP:** `GET /tiktok/search`
- **What:** Search TikTok videos. Searches TikTok videos for `keyword`. `cursor` defaults to 0 and `count` defaults to 20, capped at 50. The response has the matching video items, a `cursor` and `has_more` for paging. An empty, blocked or malformed result from TikTok returns an upstream error.
- **Params:** `count` (integer, optional) — Result count, clamped to 50; `cursor` (integer, optional) — Pagination cursor; `keyword` (string, **required**) — Search keyword

## YouTube (4)

### `youtube_comments`

- **HTTP:** `GET /youtube/comments/{id}`
- **What:** Retrieve top-level video comments. Returns one page of top-level comments for a YouTube video by its 11-character `id`. Each comment has its id, content, author `user_name` and `channel_id`, `likes_count`, `reply_count` and `published_time`. Comments with replies may include their own `continuation_token`; pass that token to `/youtube/comments/{id}/replies`. Pass the response-level `continuation_token` here for deterministic pagination. If omitted, the service discovers an initial cursor or may resume the most recently cached cursor for this video.
- **Params:** `continuation_token` (string, optional) — Opaque pagination token returned by a previous request; pass it for deterministic pagination; `id` (string, **required**) — YouTube video ID (11-character code)

### `youtube_search`

- **HTTP:** `GET /youtube/search`
- **What:** Search YouTube. Returns normalized YouTube search results using YouTube's InnerTube search API. Pass `continuation_token` from a previous response to retrieve the next page. Use `q` as the primary query parameter; `search_query` is accepted as an alias. `hl` and `gl` localize ranking and result context; they default to `en` and `US`. Named filters cover the public web search filters. Account-only chips such as Watched and Unwatched are not exposed.
- **Params:** `continuation_token` (string, optional) — Pagination token returned by a previous request; `duration` (string, optional) — Filter by duration; short, medium, and long preserve their previous upstream encodings; `features` (string, optional) — Comma-separated feature filters. Allowed values: live, 4k, hd, subtitles, cc, creative_commons, 360, vr180, 3d, hdr, location, purchased; `gl` (string, optional) — Two-letter YouTube region code; `hl` (string, optional) — YouTube interface language; `params` (string, optional) — Raw protobuf-encoded search filter (base64); `q` (string, optional) — Search query; `search_query` (string, optional) — Alias for q; `sort_by` (string, optional) — Sort results; `type` (string, optional) — Filter by type; `upload_date` (string, optional) — Filter by upload date

### `youtube_transcript`

- **HTTP:** `GET /youtube/transcript/{id}`
- **What:** Retrieve transcript for a YouTube video. Returns transcript segments for a YouTube video using YouTube's native player captions. Set `format=text`, `format=srt`, or `format=vtt` to receive plain-text output instead of the standard response envelope. Returns `404` when the video currently has no transcript/captions available in any language — this is a normal, non-retryable result, not an error condition. Returns `503` when the request is temporarily blocked or rate-limited; retrying after a short delay may succeed.
- **Params:** `format` (string, optional) — Response format; `id` (string, **required**) — YouTube video ID (11-character code); `lang` (string, optional) — Preferred transcript language; `timestamps` (boolean, optional) — Include timestamps in the JSON response; `translate_to` (string, optional) — Translate transcript to this language code

### `youtube_transcript_languages`

- **HTTP:** `GET /youtube/transcript/{id}/languages`
- **What:** List transcript languages for a YouTube video. Lists the transcript languages available for a YouTube video by its 11-character video id. Each entry has the language name and code, whether the track is auto-generated, and whether it can be translated. Use it to pick a language before requesting a transcript.
- **Params:** `id` (string, **required**) — YouTube video ID (11-character code)
