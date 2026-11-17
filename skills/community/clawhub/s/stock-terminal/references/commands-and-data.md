# Commands and data recipes

Use this reference when wiring commands to the read-only data layer. The machine-readable source
is [`contracts/commands.json`](contracts/commands.json). The gate validates every API operation
against the public contract and generates the request-budget table from that manifest.

## Dispatch rules

Treat a recognized command as an intent, not as a shell instruction. Resolve a company name to a
canonical ticker before any ticker recipe. A bare ticker selects the compact four-call navigation
view. `open` selects the six-call research view. Natural-language aliases select the same recipe
and budget as their canonical command.

Run independent steps in parallel. Honor `dependsOn` before dispatching a dependent step. In
particular, choose the first quarter with `pending:false` from `institutional_quarters` before
calling `institutional_holders`. Do not hardcode a reporting date.

Every cache record uses the operation ID plus the fully bound cache key. Keep the source date, when
the response supplies one, separate from the host fetch time. Also retain preview and error state.
Coalesce identical in-flight requests so a tool and a widget do not pay for the same snapshot twice.
Snapshot inputs include bound selector values, including fixed query inputs such as the chart's
`timeframe: "1M"`. They are not limited to arguments typed by the user; the binding validator needs
the actual ticker and period that produced the data.

Before binding a default relative window, use [request-cache.mjs](runtime/request-cache.mjs).
The default start is the UTC day boundary 30 days before the host clock; the end is the current
five-minute bucket boundary. Never round explicit user-supplied absolute boundaries.
Successful cache entries expire after five minutes. Manual refresh bypasses the cache, and a
changed request window has a new identity even if another window is still fresh.
Warm budgets assume the same normalized window and unexpired successful entries, not raw `Date.now()` inputs.
The helper's cache record is `{status: "success", fetchedAtMs, snapshot}` keyed by full request identity.
`fetchedAtMs` is the host's numeric fetch time. This cache success flag is separate from UI loading,
empty, or preview presentation: a successful preview may be cached with its preview flags intact.
Failed reads are never reusable entries. A shorter TTL is allowed; a longer one is rejected.

Manifest template values that consist of one token, such as `"{plan}"`, substitute the original
typed value. They are not string interpolation: `plan` stays an object, `limit` a number, and
`tickers` an array or null. Only tokens embedded within a larger string become string segments.
Optional fields whose exact-token value is null may be omitted from the request body.
The complete bound method, path, query, and typed body determine request identity.

Recipes declare `exposure`: `command` entries appear in help, `navigation` is the bare-ticker
home action, and `internal` is the company-resolution preflight. A recipe is not automatically
a public command merely because it appears in the budget table.

<!-- terminal-help:start -->
<!-- Generated from the versioned command contract. -->
| Command | What it opens |
|---|---|
| `open <TICKER>` | Research one ticker with price, profile, polarity, insiders, analyst consensus, and insights. |
| `compare <A> <B>` | Compare the same six research surfaces for two tickers. |
| `daily brief` | Read the market session, mood, summary, insights, and four index prices. |
| `screen smart-money` | Find convergence across insider buys, congressional purchases, and analyst upgrades. |
| `screen <PLAN>` | Validate a typed filter plan against the field catalog, then run the screen. |
| `mood` | Read the market composite and sector sentiment. |
| `holders <TICKER>` | Read institutional holders for the latest settled quarter. |
| `flow <TICKER>` | Read dated insider, congressional, institutional, and analyst activity for a ticker. |
| `options <TICKER>` | Read end-of-day options positioning for a ticker. |
| `news <TICKER>` | Read ticker stories, then details only for a selected story. |
| `stories` | Read market stories, then details only for a selected story. |
| `earnings [this|next]` | Read the earnings calendar for this week, next week, or a ticker. |
| `help` | List supported public command forms without an API read. |
<!-- terminal-help:end -->

## Request budgets

Cold counts include baseline API requests only. Warm counts use exactly the cache assumption in the
manifest. Optional detail calls and bounded retries are shown separately. Resolving a company name
adds one request. Local tools add zero API requests.

<!-- terminal-budgets:start -->
<!-- Generated from the versioned command contract. -->
| Command or view | Cold | Warm | Optional | Retry max | Warm assumption |
|---|---:|---:|---:|---:|---|
| `resolve <COMPANY>` | 1 | 0 | +0 | +0 | same normalized company query cached |
| `<TICKER>` | 4 | 0 | +1 | +0 | all four requests for the same ticker, asset type, and window cached |
| `open <TICKER>` | 6 | 0 | +0 | +0 | all six requests for the same ticker and window cached |
| `compare <A> <B>` | 12 | 6 | +0 | +0 | one ticker's six-call open snapshot cached |
| `daily brief` | 5 | 0 | +0 | +0 | all five market snapshots cached |
| `screen smart-money` | 3 | 0 | +0 | +3 | all three seven-day feeds cached |
| `screen <PLAN>` | 2 | 1 | +0 | +0 | field catalog cached; execution body is a miss |
| `mood` | 1 | 0 | +0 | +0 | same market-mood request cached |
| `holders <TICKER>` | 2 | 1 | +0 | +0 | settled-quarter catalog cached; ticker holders miss |
| `flow <TICKER>` | 5 | 4 | +0 | +0 | settled-quarter catalog cached; four ticker reads miss |
| `options <TICKER>` | 1 | 0 | +0 | +0 | same ticker options summary cached |
| `news <TICKER>` | 1 | 0 | +1 | +0 | same ticker story list cached |
| `stories` | 1 | 0 | +1 | +0 | same market story list cached |
| `earnings [this|next]` | 1 | 0 | +0 | +0 | same week or ticker calendar request cached |
| `help` | 0 | 0 | +0 | +0 | no API requests |
<!-- terminal-budgets:end -->

## Per-view call chains

<!-- terminal-callchains:start -->
<!-- Generated from the versioned command contract. -->
| View | Baseline chain | Optional |
|---|---|---|
| `resolve <COMPANY>` | `entity_search` | None |
| `<TICKER>` | `stock_quote` (assetType=stock) or `etf_quote` (assetType=etf) -> `stock_chart` -> `score_series` -> `ticker_stories` | `stock_profile` |
| `open <TICKER>` | `stock_price` -> `stock_profile` -> `sentiment_series` -> `insider_trades` -> `analyst_consensus` -> `stock_insights` | None |
| `compare <A> <B>` | `open` for tickerA, tickerB | None |
| `daily brief` | `market_status` -> `market_mood` -> `market_summary` -> `market_insights` -> `index_prices` | None |
| `screen smart-money` | `insider_cluster_buys` -> `politician_activity` -> `analyst_activity` | None |
| `screen <PLAN>` | `screener_fields` -> `screener_execute` | None |
| `mood` | `market_mood` | None |
| `holders <TICKER>` | `institutional_quarters` -> `institutional_holders` | None |
| `flow <TICKER>` | `insider_trades` -> `politician_filings` -> `institutional_quarters` -> `institutional_holders` -> `analyst_actions` | None |
| `options <TICKER>` | `options_summary` | None |
| `news <TICKER>` | `ticker_stories` | `story_detail` |
| `stories` | `stories` | `story_detail` |
| `earnings [this|next]` | `earnings_calendar` | None |
| `help` | No API request | None |
<!-- terminal-callchains:end -->

## Registered operations

<!-- terminal-operations:start -->
<!-- Generated from the versioned command contract. -->
| Operation ID | Exact request template | Response shape |
|---|---|---|
| `entity_search` | `GET /api/v1/kb/entities/search`<br>query {"limit":"5","q":"{query}","type":"company"} | `bare-array` |
| `stock_quote` | `GET /api/v1/stocks/{ticker}/quote` | `direct-object` |
| `etf_quote` | `GET /api/v1/etfs/{ticker}/quote` | `direct-object` |
| `stock_chart` | `GET /api/v1/stocks/chart`<br>query {"ticker":"{ticker}","timeframe":"1M"} | `bare-array` |
| `score_series` | `GET /api/v2/metrics/entity/{ticker}/metric/sentisense`<br>query {"startTime":"{epochMs30dAgo}"} | `bare-array` |
| `sentiment_series` | `GET /api/v2/metrics/entity/{ticker}/metric/sentiment`<br>query {"endTime":"{epochMsNow}","startTime":"{epochMs30dAgo}"} | `bare-array` |
| `ticker_stories` | `GET /api/v1/documents/stories/ticker/{ticker}`<br>query {"limit":"5"} | `bare-array` |
| `story_detail` | `GET /api/v1/documents/stories/{clusterId}` | `direct-object` |
| `stories` | `GET /api/v1/documents/stories`<br>query {"limit":"10"} | `bare-array` |
| `raw_ticker_documents` | `GET /api/v1/documents/ticker/{ticker}`<br>query {"limit":"8"} | `documents-envelope` |
| `stock_price` | `GET /api/v1/stocks/price`<br>query {"ticker":"{ticker}"} | `direct-object` |
| `stock_profile` | `GET /api/v1/stocks/{ticker}/profile` | `direct-object` |
| `insider_trades` | `GET /api/v1/insider/trades/{ticker}`<br>query {"lookbackDays":"90"} | `preview-envelope` |
| `analyst_consensus` | `GET /api/v1/analyst/{ticker}/consensus` | `preview-envelope` |
| `stock_insights` | `GET /api/v1/insights/stock/{ticker}` | `preview-envelope` |
| `market_status` | `GET /api/v1/stocks/market-status` | `direct-object` |
| `market_mood` | `GET /api/v2/market-mood` | `direct-object` |
| `market_summary` | `GET /api/v1/market-summary` | `direct-object` |
| `market_insights` | `GET /api/v1/insights/market` | `preview-envelope` |
| `index_prices` | `GET /api/v1/stocks/prices`<br>query {"tickers":"SPY,QQQ,IWM,DIA"} | `bare-array` |
| `insider_cluster_buys` | `GET /api/v1/insider/cluster-buys`<br>query {"lookbackDays":"{lookbackDays}"} | `preview-envelope` |
| `politician_activity` | `GET /api/v1/politicians/activity`<br>query {"limit":"500","lookbackDays":"{lookbackDays}","offset":"{offset}"} | `preview-envelope` |
| `analyst_activity` | `GET /api/v1/analyst/activity`<br>query {"actionTypes":"UPGRADE","limit":"500","lookbackDays":"{lookbackDays}","offset":"{offset}"} | `preview-envelope` |
| `screener_fields` | `GET /api/v1/screener/fields` | `direct-object` |
| `screener_execute` | `POST /api/v1/screener/execute`<br>body {"limit":"{limit}","plan":"{plan}","tickers":"{tickers}"} | `direct-object` |
| `politician_filings` | `GET /api/v1/politicians/filings/{ticker}`<br>query {"lookbackDays":"90"} | `preview-envelope` |
| `institutional_quarters` | `GET /api/v1/institutional/quarters` | `bare-array` |
| `institutional_holders` | `GET /api/v1/institutional/holders/{ticker}`<br>query {"limit":"10","reportDate":"{reportDate}","sortBy":"shares","sortDir":"desc"} | `preview-envelope` |
| `analyst_actions` | `GET /api/v1/analyst/{ticker}/actions`<br>query {"lookbackDays":"90"} | `preview-envelope` |
| `options_summary` | `GET /api/v1/stocks/{ticker}/options/summary` | `preview-envelope` |
| `earnings_calendar` | `GET /api/v1/calendar/earnings`<br>query {"ticker":"{ticker}","week":"{week}"} | `preview-envelope` |
<!-- terminal-operations:end -->

The smart-money screen starts with three seven-day feeds. Congress and analyst activity are paged:
the recipe binds `offset` to 0 with the largest page, 500 rows, and `totalCount` counts the whole
window. On a full response, re-bind `offset` while `offset + rows < totalCount`; each extra page is a
request beyond the retry maximum, or label the leg as a slice dated by its oldest row. Cluster buys
take no paging parameters; a full response has no `totalCount` and currently stops at 50 clusters.
A preview whose `totalCount` exceeds its rows is a slice that `offset` cannot page past: label it with
`totalCount` and never read an empty filtered slice as absence or disclosure lag. Retry each empty
leg once with a 30-day window only after a complete read, so the retry maximum is three requests.
Label the actual window for every leg. Do not imply that widening the window leaves the screen at
seven days.

## Response shapes

`bare-array` means read the response itself. It applies to entity search, both metric series, stock
charts and prices, story lists, and institutional quarters. `direct-object` means read fields from
the root object. `documents-envelope` has root `documents`, `totalCount`, and coverage fields.
`preview-envelope` means inspect `isPreview` and `previewReason`, then read `data`. An empty array is
a valid result unless the endpoint documents a different error.

The command manifest records the envelope next to each operation. Do not apply one global unwrap
rule. Story detail is a direct object while story lists are arrays. The options summary is a preview
envelope and may carry `data:null` when the ticker is outside coverage. Its free headline preview is
flat: the fields it keeps sit directly under `data` instead of under `latest`, `context`, or `oiWalls`.
The manifest records this as the operation's `preview` contract, and the snapshot adapter applies it
when the snapshot carries `isPreview: true`, returning `withheldByPreview` for a field the preview
omits. Render that as withheld, not as a building baseline or zero.

Each API operation also declares non-exhaustive `displayFields` and explicit `asOf` semantics.
These are host adapter instructions, not additional fields claimed to exist in API responses.
Use [snapshot-adapters.mjs](runtime/snapshot-adapters.mjs) for allowlisted metric selection and
table projection. Preserve missing values and preview status rather than copying arbitrary raw fields.
Do not promote a serve timestamp, a row event date, or a report quarter into a whole-screen observation time.
In particular, aggregate quote `timestamp` is serve time, mood has no supplied as-of, and story
lists have per-item `cluster.clusteredAt` dates without a list-wide as-of.
Quote and price responses may carry `priceAsOf` in epoch milliseconds. Use it only when returned;
outside regular hours or with undated upstream data it may be absent, which means unknown price age.

## Recipe notes

### Compact navigation

Fetch the aggregate quote, one-month chart, 30-day SentiSense Score series, and ticker story list.
Use one shared snapshot per operation. The optional profile is a fifth request when the canvas needs
company metadata. Stock quote is a stock-only path; an ETF host must route to the documented ETF
quote peer rather than retrying the stock path.
Without that optional fifth profile read, show the ticker only; do not assume the quote supplies a company name.

### Open and compare

`open` fans out price, profile, 30-day sentiment, insider trades, analyst consensus, and stock
insights. `compare` runs that recipe for two tickers. Its warm count assumes one ticker's complete
open snapshot is already cached. It does not invent a winner or a composite score.

### Daily brief and market mood

The daily brief combines market status, market mood, the market summary, market insights, and one
batch request for SPY, QQQ, IWM, and DIA. The `mood` command uses only market mood. Keep price delay,
summary generation time, and each batch metric date visible instead of calling the whole surface
live.

### Screening

The smart-money recipe intersects insider cluster buys, congressional activity filtered to
`PURCHASE` client-side, and analyst activity filtered server-side to `UPGRADE`. Custom screens fetch
the field catalog, validate the requested plan, then post it to the stock screener. Its body is
`plan` plus the top-level `limit` and optional `tickers`. Derive cache identity from the complete
normalized body so a limit or watchlist change is a cache miss. Cache the field catalog separately.

### Flow and holders

`holders` resolves a settled quarter, then requests ten holders sorted by shares. `firstSettled`
is a host-derived selection over the quarters array, not a field returned by the API. Pass that
selected `reportDate` into request expansion before dispatching the holders request. `flow` adds
90-day insider trades, 90-day congressional filings, and 90-day analyst actions. Analyst action
types and canonical grade pairs are reconciled by the API; render the current documented action
rather than applying an old contradiction workaround.

### Options, news, stories, and earnings

`options` is one end-of-day options-summary request. It is positioning, not a live order tape.
`news <TICKER>` uses the ticker story list by default, with one optional detail call after the user
selects a cluster. `stories` uses the market-wide story list with the same selected-detail rule.
Raw ticker documents are registered only as an optional source-link enhancement and are not part of
the default news budget. The earnings command makes one calendar request with a week or ticker
filter. When a ticker is supplied without an explicit week, omit `week`; the ticker variant should
not inherit the default current-week filter.

## Host-only tools

`resolve_security` canonicalizes company names before dispatch. An exact ticker is local work and
costs zero. A company-name cache miss delegates to the `resolve` recipe and spends one entity-search
request. `read_screen` exposes only the
validated, currently visible read model to a follow-up. `render_canvas` parses and validates a
complete canvas before committing its AST. These are host operations, not server endpoints, and
must never carry an API request count above zero.

## Failure behavior

Preserve the last good canvas when a call fails. Show which section is unavailable, its fetch time,
and whether the response was a preview. A manual refresh invalidates only the selected cache keys.
It can update widgets, but it must leave authored narrative visibly dated to its original evidence.
