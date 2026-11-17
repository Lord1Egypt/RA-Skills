# reddit-stock-sentiment-research — endpoint reference

> Generated from `scripts/tools.json` by `scripts/generate.mjs` — do not edit by hand.

Only the endpoints used by this workflow. Call them via `scripts/crawlora.sh` (see SKILL.md).

All paths are relative to the API base `https://api.crawlora.net/api/v1` and require the header `x-api-key: $CRAWLORA_API_KEY`. Path params like `{id}` are substituted into the URL; `GET` params go in the query string; `POST` params go in a JSON body.

**9 endpoints across 2 platform group(s).**

## Yahoo Finance (5)

### `yahoo_finance_search`

- **HTTP:** `GET /yahoo-finance/search`
- **What:** Yahoo Finance search. Searches Yahoo Finance for the required `q`, a ticker symbol or company name, and returns matching `quotes`, `news` and `lists`, plus `research` reports when `include_research` is set and Yahoo returns them. `quotes_count`, `news_count` and `lists_count` set how many of each; `enable_fuzzy_query` turns on fuzzy matching.
- **Params:** `enable_fuzzy_query` (boolean, optional) — Enable fuzzy matching; `include_research` (boolean, optional) — Include research reports when Yahoo returns them; `lists_count` (integer, optional) — List result count; `news_count` (integer, optional) — News result count; `q` (string, **required**) — Ticker symbol or company name; `quotes_count` (integer, optional) — Quote result count

### `yahoo_finance_ticker_history`

- **HTTP:** `GET /yahoo-finance/ticker/{symbol}/history`
- **What:** Yahoo Finance historical prices. Returns price points for a Yahoo Finance `symbol`: open, high, low, close, adjusted close and volume with timestamps. Use `period` (default `1mo`, up to `max`) or `start` and `end`, which override it. `interval` sets the candle size (default `1d`; intraday covers recent ranges only). `include_actions` adds dividend, split and capital-gain `events`.
- **Params:** `auto_adjust` (boolean, optional) — Adjust OHLC prices with adjusted close; `back_adjust` (boolean, optional) — Back-adjust OHLC prices while keeping close; `end` (string, optional) — Unix seconds, RFC3339, or YYYY-MM-DD; `include_actions` (boolean, optional) — Include dividends, splits, and capital gains; `include_prepost` (boolean, optional) — Include pre/post market data; `interval` (string, optional) — Interval such as 1d, 1h, 5m; `keepna` (boolean, optional) — Keep fully empty chart rows; `period` (string, optional) — Range such as 1d, 1mo, 1y, max; `rounding` (boolean, optional) — Round prices to two decimals; `start` (string, optional) — Unix seconds, RFC3339, or YYYY-MM-DD; `symbol` (string, **required**) — Yahoo Finance symbol such as AAPL

### `yahoo_finance_ticker_info`

- **HTTP:** `GET /yahoo-finance/ticker/{symbol}/info`
- **What:** Yahoo Finance ticker info. Returns profile and quote information for a Yahoo Finance `symbol` such as `AAPL`, under `modules`: the profile, quote type (`quoteType`), price, statistics and summary modules. The symbol is the only input.
- **Params:** `symbol` (string, **required**) — Yahoo Finance symbol such as AAPL

### `yahoo_finance_ticker_news`

- **HTTP:** `GET /yahoo-finance/ticker/{symbol}/news`
- **What:** Yahoo Finance ticker news. Returns the Yahoo Finance news stream for the ticker in the `symbol` path parameter, such as `AAPL`. `count` limits the items (default 8, max 250) and `tab` picks `news` (default), `all` or `press_releases`. Stories have title, provider, dates and URLs. A valid empty stream returns `news: []`.
- **Params:** `count` (integer, optional) — News result count; `symbol` (string, **required**) — Yahoo Finance symbol such as AAPL; `tab` (string, optional) — News tab: news, all, or press_releases

### `yahoo_finance_ticker_quote`

- **HTTP:** `GET /yahoo-finance/ticker/{symbol}/quote`
- **What:** Yahoo Finance ticker quote. Returns fast quote fields for one Yahoo Finance `symbol` such as `AAPL`, for example `regularMarketPrice`, in a `quotes` list alongside the requested `symbols`. The symbol is the only input.
- **Params:** `symbol` (string, **required**) — Yahoo Finance symbol such as AAPL

## Reddit (4)

### `reddit_comments`

- **HTTP:** `GET /reddit/comments/{id}`
- **What:** Get Reddit post comments. Returns a Reddit post with its public comments. The default mode is 1 credit. Set `include_metrics=true` to return the comments with public net score and award count plus post engagement metrics for 3 credits. Large threads may expose only an initial comment subset. Reddit does not expose per-comment upvote ratios or exact upvote/downvote totals anonymously. A post that exists but has no comments yet returns a 200 response with an empty comments list; a post that does not exist returns 404, and a temporary block or upstream failure returns 503 (retryable) rather than 404. If source.type is redlib, public fields and credit weights are preserved.
- **Params:** `depth` (integer, optional) — Maximum flat comment depth returned in metrics mode.; `id` (string, **required**) — Reddit post id or t3_ id; `include_metrics` (boolean, optional) — Include public post and per-comment engagement metrics; costs 3 credits instead of 1; `limit` (integer, optional) — Maximum comments returned, defaults to 25 and clamps to 100; `sort` (string, optional) — Comment order: confidence, top, new, controversial, old, or qa. Applied to the anonymous HTML request when metrics are enabled.

### `reddit_post`

- **HTTP:** `GET /reddit/post/{id}`
- **What:** Get Reddit post. Returns a public Reddit post. The default mode is 1 credit. Set `include_metrics=true` to return public net score, upvote ratio, comment count, award count, and estimated upvote/downvote totals for 3 credits. Reddit fuzzes voting data, so estimates are approximate; share, repost/crosspost, and view counts are not exposed anonymously. If source.type is redlib, public fields and credit weights are preserved.
- **Params:** `id` (string, **required**) — Reddit post id or t3_ id; `include_metrics` (boolean, optional) — Include public engagement metrics; costs 3 credits instead of 1

### `reddit_search`

- **HTTP:** `GET /reddit/search`
- **What:** Search Reddit posts. Searches public Reddit content and returns public post entries. A `503` with a `Retry-After` header means Reddit is temporarily throttling the request; wait that many seconds and retry. If source.type is redlib, public fields and credit weights are preserved.
- **Params:** `after` (string, optional) — Reddit pagination token; `limit` (integer, optional) — Maximum posts, defaults to 25 and clamps to 100; `q` (string, **required**) — Search keywords; `sort` (string, optional) — Sort: relevance, hot, new, top, or comments; `subreddit` (string, optional) — Restrict search to a subreddit name, without r/; `time` (string, optional) — Time window for top/comments sorts: hour, day, week, month, year, or all

### `reddit_subreddit_posts`

- **HTTP:** `GET /reddit/subreddit/{subreddit}/posts`
- **What:** List Reddit subreddit posts. Returns public posts from a subreddit. A `503` with a `Retry-After` header means Reddit is temporarily throttling the request; wait that many seconds and retry. If source.type is redlib, public fields and credit weights are preserved.
- **Params:** `after` (string, optional) — Reddit pagination token; `limit` (integer, optional) — Maximum posts, defaults to 25 and clamps to 100; `sort` (string, optional) — Sort: hot, new, top, or rising; `subreddit` (string, **required**) — Subreddit name, without r/; `time` (string, optional) — Time window for top sort: hour, day, week, month, year, or all
