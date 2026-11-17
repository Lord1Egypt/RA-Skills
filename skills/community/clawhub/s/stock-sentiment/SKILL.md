---
name: stock-sentiment
description: "Stock sentiment and smart-money positioning for US stocks: the SentiSense Score, sentiment polarity, mention volume and share of voice for any ticker, the fear-to-greed market mood with sector readings, insider cluster buys, congressional purchases and analyst upgrades converging on the same names, 13F holders, AI insights, and a peer-normalized check of whether a mention spike is good or bad news, read from the ticker's own bullish and bearish coverage. Use for stock sentiment, stock sentiment analysis, is the mood bullish or bearish, market mood today, fear and greed index, smart money tracker, insider buying and analyst upgrades, mention spike, sentiment vs price divergence, pre-earnings sentiment. Read-only. No trading, no purchases, no write operations, no wallet access."
homepage: https://sentisense.ai
primaryEnv: SENTISENSE_API_KEY
metadata:
  openclaw:
    primaryEnv: SENTISENSE_API_KEY
    envVars:
      - name: SENTISENSE_API_KEY
        required: false
        description: "SentiSense API key, optional to install. Get one free at https://app.sentisense.ai/get-api-key, or with no key follow the No key yet steps in the 0-sentisense-onboarding skill for a temporary free one with no signup. Used only to authenticate read-only data calls; no write or trading scope."
---
# Stock Sentiment Skill

The sentiment and smart-money layer for US equities. A quote skill tells you the price; this skill reads what the market feels about a stock (the SentiSense Score, sentiment polarity, mentions, share of voice), where the smart money is moving (insider, congressional, and institutional flows plus analyst actions), and what the AI read of the tape is (per-stock and market-wide insights, sentiment-tagged news), all through the read-only SentiSense API.

Read-only educational data interface. Output is informational context, never a personalized buy or sell recommendation.

## When to Use

Reach for this skill when the question is about perception, positioning, or signal rather than raw price:

- "What is the sentiment on $NVDA?" or "Is the mood on $TSLA bullish or bearish?"
- "What is the smart money doing this week?" (insider cluster-buys, congressional trades, 13F flows, and analyst upgrades converging on the same tickers).
- "What is the overall market mood today, fear or greed?"
- "Is sentiment diverging from price on $COIN?" (price up while sentiment falls, or the reverse).
- "Mentions of $ZS just spiked: is that good or bad news for the stock?"
- "What is the pre-earnings sentiment setup on $AAPL?"
- "What is the AI insight on $MSFT, and what are people saying in the news?"

For "does this change my thesis?", hand off to the `us-stocks-analysis` skill when available. Pass the ticker, user thesis, horizon, and dated signal disagreements. Return an evidence-led bull/bear assessment and unresolved objections. Hand off only when the user changes the question; do not automatically route back. If the sibling is unavailable, answer the supported part here using a connected tool or the inline REST workflow, state any remaining gap, and never require an install.

Do not use it for order entry, portfolio management, or personalized advice. It has no write, trading, or wallet surface; every endpoint is a GET.

## Prerequisites

- Python 3.8+ using only the standard library (`urllib`, `json`); no third-party packages required. Any HTTP client or plain `curl` works too. On macOS python.org installs the client can raise `CERTIFICATE_VERIFY_FAILED` (missing CA certs): run the bundled `Install Certificates.command`, use the system `/usr/bin/python3`, or use `curl` (which uses the system trust store).
- A free `SENTISENSE_API_KEY`. Get one at https://app.sentisense.ai/get-api-key. The key is required on every call; anonymous requests return `401 api_key_required`. No key yet? Follow "No key yet" in the `0-sentisense-onboarding` skill: one POST returns a temporary free key the agent can use right away and a link the user opens to keep it.
- Network access to `https://app.sentisense.ai`.
- Read-only scope. Every endpoint here is a GET. Nothing this skill does can place a trade, move money, or modify account state.

## Permissions

- Network: HTTPS to app.sentisense.ai only.
- Credentials: SENTISENSE_API_KEY from the environment.
- Shell: none required.
- Files: none.

Tiers:

| Tier | Quota | Rate |
|------|-------|------|
| Free | 1,000 requests/month | 30 requests/min |
| PRO ($15/mo) | Unlimited | 300 requests/min |

The free tier exercises every workflow below. Preview-gated endpoints return a truncated but real slice on a free key (for example the top 3 insights); PRO removes the monthly cap and returns full history and full lists. A slice is not the window: when `isPreview` is true and `totalCount` is larger than the rows returned, label the result with both numbers ("newest 5 of 17 insider trades, free preview") and never infer absence from it. "No insider buying", "no congressional purchase" or "no earnings date" cannot come from a slice.

## How to Run

This skill is invoked through the agent's terminal or shell tool: issue HTTP GET requests to the SentiSense API and synthesize the JSON into a concise, sourced answer. The base URL is `https://app.sentisense.ai`. Authenticate every request with the `X-SentiSense-API-Key` header; keep the key in the shell environment and never place it in a query string or in user-facing output.

**Identify your client.** Send a `User-Agent` naming your agent runtime and this skill, for
example `OpenClaw/1.4 (stock-sentiment)` or `ClaudeCode/2.1 (stock-sentiment)`. Substitute your own runtime and
version if neither matches. You can also volunteer what your agent is called by adding an
`agent/<your-agent-name>` token inside the same parentheses, as in
`OpenClaw/1.4 (stock-sentiment; agent/research-desk)`. All of it is optional, and it is what tells
us this skill has real integrations behind it, so it gets prioritized and you get notice before it
changes.

```bash
curl -s -H "X-SentiSense-API-Key: $SENTISENSE_API_KEY" \
  "https://app.sentisense.ai/api/v2/metrics/entity/NVDA/metric/sentiment"
```

An anonymous call returns `401 api_key_required`. A rate-limited call returns `429` with a `Retry-After` header; back off for the indicated seconds rather than retrying immediately or serving a stale value.

On Windows, use the bundled Python client (cross-platform) and reference the key as `%SENTISENSE_API_KEY%` (cmd) or `$env:SENTISENSE_API_KEY` (PowerShell) rather than the POSIX `$SENTISENSE_API_KEY` shown above.

The REST recipe in this file is the primary path. A maintained command-line client is available as the separate `sentisense-cli` skill for hosts that prefer one.

Two response envelopes exist; unwrap correctly before reading fields:

- Read FLAT (top-level, no `.data`): `stocks/price`, `stocks/prices`, `stocks/chart`, `stocks/popular`, `stocks/{T}/profile`, `market-mood`, and the metric series (`sentiment`, `sentisense`, `mentions`, and `social_dominance` are bare arrays). `institutional/quarters` is also a bare array.
- Read WRAPPED as `{ isPreview, previewReason, data }` (use `.data`): `insider/*`, `politicians/*`, `institutional/holders`, `analyst/*`, `insights/*`, and `calendar/earnings` (here `data` is a dict, so read `data.earnings[]`).
- `documents/ticker` has its own shape `{ documents, totalCount }`; read `.documents[]`.

When unsure, accept both: `rows = raw if isinstance(raw, list) else raw.get("data", raw)`.

An optional stdlib helper, `scripts/sentiment_client.py`, covers the single-endpoint reads used by these workflows plus the paged feeds: it injects the auth header, prepends the base URL, normalizes both envelopes (reading the metric scalar from the flat `value`), walks paged feeds to `totalCount`, and labels a free-tier preview slice with its `totalCount` so the agent reasons over clean values. Workflow 6's ratio arithmetic is left to the agent; the `peers` and `mentions --start/--end` subcommands fetch its inputs. Use it or plain `curl`, whichever fits the host. The core of the helper is small enough to inline:

```python
#!/usr/bin/env python3
"""Minimal stdlib client for the read-only SentiSense API."""
import json, os, urllib.parse, urllib.request

API_ORIGIN = "https://app.sentisense.ai"

class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        return None

def sentisense_api_url(path, params=None):
    url = urllib.parse.urljoin(API_ORIGIN + "/", path)
    parsed = urllib.parse.urlparse(url)
    if (parsed.scheme != "https" or parsed.hostname != "app.sentisense.ai"
            or parsed.netloc != "app.sentisense.ai"
            or parsed.username is not None or parsed.password is not None
            or parsed.port is not None):
        raise ValueError("API URL must use https://app.sentisense.ai with no credentials or port")
    if params:
        url += ("&" if parsed.query else "?") + urllib.parse.urlencode(params)
    return url

def get(path, **params):
    url = sentisense_api_url(path, params)
    req = urllib.request.Request(
        url, headers={"X-SentiSense-API-Key": os.environ["SENTISENSE_API_KEY"]})
    with urllib.request.build_opener(NoRedirect).open(req, timeout=20) as r:
        return json.load(r)

def rows(raw):
    """Wrap-vs-flat: some endpoints return a bare array, others {isPreview, data}."""
    if isinstance(raw, list):
        return raw
    if isinstance(raw, dict) and "data" in raw:
        return raw["data"]
    return raw

def latest_metric(ticker, slug="sentiment"):
    """Latest reading of any metric series. Read the flat top-level `value`: it is present
    on every point and holds the scalar, while the nested metricValue is a dict for value
    metrics and a bare number for count metrics like `mentions`."""
    series = get(f"/api/v2/metrics/entity/{ticker}/metric/{slug}")
    if not series or series[-1].get("value") is None:
        return None
    return float(series[-1]["value"])
```

```bash
python scripts/sentiment_client.py sentiment NVDA
python scripts/sentiment_client.py mood
```

## Quick Reference

All paths are relative to `https://app.sentisense.ai` and are GET. Every call requires the `X-SentiSense-API-Key` header. `{T}` is an uppercase ticker, `{slug}` a member slug, `{id}` a story id. Full schema: https://sentisense.ai/skill.md.

```
RESOLVE A NAME (only when the user typed a company or fund name, not a symbol)
  GET /api/v1/kb/entities/search?q={name}&type=company&limit=5
        Bare array of {name, urlSlug, type, ticker}, best match first. Take the first match with a
        non-null ticker. Use type=etf for fund names (SPY resolves only there). See Pitfalls.

PEERS (to test whether a mention spike is the ticker's own; see workflow 6)
  GET /api/v1/stocks/{T}/graph?depth=1&cap=75
        groups.peers[] is the curated comparable set, as entity slugs that the metric endpoints
        accept in place of {T}; join a slug to nodes[] for its displayName. Peers from depth=1 only.

SENTIMENT & MOOD
  GET /api/v2/metrics/entity/{T}/metric/sentiment?startTime={epochMs}&endTime={epochMs}
        Sentiment polarity time series. Omit params for the server default 7-day window.
        Bare array; latest scalar is series[-1].value (a float in [-1, 1]). Every series
        below reads the same way: take the flat top-level value, not the nested metricValue,
        whose depth differs between value metrics and count metrics.
  GET /api/v2/metrics/entity/{T}/metric/sentisense
        The SentiSense Score (unbounded composite; report as-is, never normalize to 0-100).
        Each daily point also carries metricValue.properties.{bull, bear, directional}: that
        day's bullish and bearish analyses and their sum. Direction lives here, not in mentions.
  GET /api/v2/metrics/entity/{T}/metric/mentions
        Mention-volume time series (how much a ticker is being talked about). Direction-blind.
  GET /api/v2/metrics/entity/{T}/metric/social_dominance
        Share-of-conversation time series (a ticker's dominance of the chatter).
  GET /api/v2/metrics/entity/{E}/metric/app_review_count
        New written Apple App Store reviews per day for a product's iOS app. Products with a
        tracked app only, so {E} is a product entity slug, never a ticker (a ticker, or a product
        with no tracked app, returns 200 and []). Find the slug with
        GET /api/v1/kb/entities/search?q={name}&type=product or groups.products[] from
        /api/v1/stocks/{T}/graph; try the company's other products if one returns [].
  GET /api/v2/metrics/entity/{E}/metric/app_rating
        Mean star rating (1 to 5) of that day's new written reviews (skews lower than all ratings).
        Same coverage. Weight days by app_review_count over a range; a thin day says little.
  GET /api/v2/metrics/entity/{E}/metric/app_all_ratings_count
        All new App Store ratings, star-only and written together. One change in the store's
        counts is split evenly over the days it covers, so consecutive days can repeat a value:
        judge a range, not a single day. Ends the day before the latest review day.
  GET /api/v2/metrics/entity/{E}/metric/app_all_ratings_avg
        Mean star rating (1 to 5) of those new ratings; weight days by app_all_ratings_count over a range.
  GET /api/v2/market-mood
        Composite fear/greed plus sub-signals and per-sector breakdowns. Flat, but the
        composite is nested: market.currentScore, market.phase, market.weeklyChange,
        market.signals[]; sectors.{SectorName}.{currentScore, phase, weeklyChange}.

SMART MONEY  (wrapped in {isPreview, previewReason, data}; free key returns a preview slice)
  GET /api/v1/insider/cluster-buys?lookbackDays=N         Tickers with multiple insider buys.
  GET /api/v1/insider/trades/{T}?lookbackDays=N           Form 4 rows; transactionType BUY|SELL plus
                                                          EXERCISE, AWARD, GIFT, OTHER (filter explicitly);
                                                          raw SEC letter in transactionCode.
  GET /api/v1/politicians/activity?lookbackDays=N         Congressional trades; PURCHASE|SALE. Window is on
                                                          disclosureDate; transactionDate is often weeks earlier.
  GET /api/v1/politicians/filings/{T}?lookbackDays=N      Per-ticker congressional filings.
  GET /api/v1/politicians/member/{slug}                   Member profile (data.recentTrades[]).
  GET /api/v1/institutional/quarters                      Call FIRST; bare array. Use reportDate of first entry whose pending is not true; skip pending:true (fall back to [0] only if all pending).
  GET /api/v1/institutional/holders/{T}?reportDate={Q}    Top 13F holders (data.holders[], largest first).
  GET /api/v1/analyst/{T}/consensus                       Price-target band; data IS the consensus object (data.consensusLabel).
  GET /api/v1/analyst/{T}/actions?lookbackDays=N          Recent rating changes for one ticker.
  GET /api/v1/analyst/{T}/estimates                       EPS band at data.estimates[0].{estimateLow/Mean/High,
                                                          numberOfAnalysts} + data.surprises[]; no revenue.
  GET /api/v1/analyst/activity?lookbackDays=N             Market-wide actions; add &actionTypes=UPGRADE,DOWNGRADE,INITIATE
                                                          for real rating changes (~83% of raw rows are REITERATE).

AI INSIGHTS  (wrapped; batch, carry generatedAt)
  GET /api/v1/insights/stock/{T}         Per-stock signals ranked by importance; data[0].insightText is the headline. Free preview top 3.
  GET /api/v1/insights/stock/{T}/types   Available insight types for the ticker; bare string array.
  GET /api/v1/insights/market            Top market-wide signals (data[], insightText; ticker embedded in insightText).

NEWS & STORIES
  GET /api/v1/documents/ticker/{T}?limit=N          Sentiment-tagged feed ({documents, totalCount}); each doc
                                                   has url, source, sourceName, published (epoch seconds), averageSentiment; no title.
  GET /api/v1/documents/stories?limit=N             Pre-clustered stories; cluster.title is SentiSense-authored and safe to show.
  GET /api/v1/documents/stories/ticker/{T}?limit=N  Stories for one ticker.
  GET /api/v1/documents/stories/{id}                Story detail (PublicStoryDetailDto; aspectPerspectives[], bullishView/bearishView).
                                                   An empty view ("" or blank hook/conclusion, no bullets) = no case on that side; never null.
  GET /api/v1/documents/search?query=...            Topical document search.

SUPPORTING  (price, prices, chart are 15-minute delayed; profile, popular, calendar, market-summary are reference or batch)
  GET /api/v1/stocks/price?ticker={T}                       Flat (no wrapper): currentPrice, changePercent at root.
  GET /api/v1/stocks/prices?tickers=A,B,C                   Batch quotes.
  GET /api/v1/stocks/{T}/profile                            name, sector, industry (flat at root; no profile key).
  GET /api/v1/stocks/chart?ticker={T}&timeframe=1D|5D|1W|1M|3M|6M|1Y|5Y|10Y|MAX   Bars; read each point's timestamp (Unix ms). Invalid timeframe returns 400.
  GET /api/v1/stocks/popular                                Bare array of ticker strings (screen universe).
  GET /api/v1/calendar/earnings?ticker={T}                  data.earnings[]; next date + consensus EPS + confirmed.
                                                            Free: current Monday-Sunday week only (see workflow 4).
  GET /api/v1/market-summary                                Market-wide narrative headline.
```

Sentiment is polarity: a float in [-1, 1] where the sign is the direction (negative is bearish and meaningful, positive is bullish) and the magnitude is conviction. Represent the sign unmistakably; do not map it onto a 0-100 scale. The SentiSense Score is a separate, unbounded composite; report it as-is. Mentions and social dominance are their own metric series on the same `/metric/{metricType}` endpoint (`mentions` for talk volume, `social_dominance` for share of the conversation); all four series (`sentiment`, `sentisense`, `mentions`, `social_dominance`) are available on the Free tier, and like every metrics call each request counts against your monthly quota. Four more Free-tier series cover consumer products rather than tickers: `app_review_count` (new written Apple App Store reviews for a product's iOS app that day) and `app_rating` (the mean star rating, 1 to 5, of those written reviews), plus `app_all_ratings_count` (every new rating, star-only and written together; written reviews are a small share of them) and `app_all_ratings_avg` (their mean star rating). **`mentions` excludes App Store reviews, from both the root total and `distribution/mentions?dimension=source`**, because a review is a rating rather than chatter. The source distribution renormalizes the visible mention-eligible sources to about 100% when volume is positive; headline mentions also includes inputs with no public source slice. Read written-review volume from `app_review_count`; review tone still counts toward `sentiment` and `sentisense`. A separate `/api/v2/metrics/entity/{T}/distribution/{metricType}?dimension=source` endpoint (`dimension` is required) breaks a metric down by source, and its `valueType` says what the numbers are: for `mentions` each source's share of voice in percent (`SHARE_PERCENT`), for `sentiment` each source's mean polarity in [-1, 1] (`MEAN`). `sentisense` has no per-source split and returns an empty map.

## Workflows

Opinionated recipes. Each fans out its independent calls in parallel, then synthesizes; none recommends buying or selling. Frame every result as educational context on positioning and mood.

### 1. Sentiment read on a ticker

Answer "what is the market feeling about $T" in a few dense lines. Fire these in parallel:

1. `GET /api/v2/metrics/entity/{T}/metric/sentiment` for the polarity trend (server default 7-day window; the latest scalar is `series[-1].value`, a float in [-1, 1]).
2. `GET /api/v2/metrics/entity/{T}/metric/sentisense` for the composite score, and each point's `metricValue.properties.bull` / `bear` for that day's bullish and bearish analyses (the day's direction).
3. `GET /api/v2/metrics/entity/{T}/metric/mentions` for mention volume: one daily count per point, read from the flat `value`. This series carries no direction; take bull and bear from step 2.
4. `GET /api/v1/documents/ticker/{T}?limit=8` for the sentiment-tagged feed only. Its `totalCount` counts the documents on this page (it equals `limit`), so never report it as mention volume.
5. `GET /api/v1/insights/stock/{T}` for the top AI insight (`data[0].insightText`, with `generatedAt` for freshness).

Synthesize as educational context, leading with the differentiated sentiment read, not the price: "$NVDA sentiment +0.42 over 7d and rising; SentiSense Score elevated; mention volume heavy; latest AI insight: 'Data-center demand commentary firming' (as of the batch time)." Show the `generatedAt` age so the reader knows these are batch metrics.

### 2. Market mood (fear and greed)

Answer "what is the overall market mood today."

1. `GET /api/v2/market-mood`.

The response is flat, but the composite is nested under `market`, not the root: `market.currentScore`, `market.phase` (e.g. Fear, Neutral, Optimism, Greed), `market.weeklyChange`, and `market.signals[]` (each sub-gauge with its value and change). Per-sector readings live at `sectors.{SectorName}.{ currentScore, phase, weeklyChange }`; `sectors` is a string-keyed dict, not an array, and its GICS labels have historically overlapped (`Technology` alongside `Information Technology`, `Healthcare` alongside `Health Care`), so treat the pairs defensively: if both members of a pair appear in one response, dedupe them before ranking top and bottom sectors. A clean response with neither pair duplicated is the common case and needs no special handling. Report as context: "Market mood 62 (Greed), +4 over the week. Greed leaders: Technology, Communications. Fear: Energy, Utilities." Optionally pair with `GET /api/v1/market-summary` for the narrative headline and `GET /api/v1/insights/market` for the top market-wide signals.

### 3. Smart-money convergence screen

Find tickers where insider buying, congressional purchases, and analyst upgrades line up in the same window; convergence is the signal a quote feed cannot produce.

1. `GET /api/v1/insider/cluster-buys?lookbackDays=30`.
2. `GET /api/v1/politicians/activity?lookbackDays=30&limit=500`, keeping rows with `transactionType == "PURCHASE"`.
3. `GET /api/v1/analyst/activity?lookbackDays=30&actionTypes=UPGRADE&limit=500` (server-side filter; also accepts a CSV like `UPGRADE,DOWNGRADE,INITIATE`).

All three are wrapped: read `.data`. **Steps 2 and 3 are paged feeds: one call is one page, not the window.** Both carry `totalCount` for the whole window on the envelope, so keep requesting with `offset` while `offset + len(data) < totalCount`. A 30-day congressional window runs to several hundred rows, which the default page (200) cuts short, and the analyst default page is 50. Reading one page silently drops most of the window and can turn a real overlap into an empty one. On a FREE key all three feeds stop at a preview slice (`isPreview: true`, with the window's real size in `totalCount`) and an `offset` past the slice returns nothing, so report the screen as partial ("congressional leg: 5 of 599 rows, free preview") rather than reporting "no convergence".

**The congressional leg is windowed by disclosure date, not trade date.** `lookbackDays` on `politicians/activity` filters on `disclosureDate`, and members disclose weeks after they trade (each row carries `transactionDate`, `disclosureDate` and `disclosureDelayDays`; delays of a month or more are common). So a 30-day screen pairs purchases disclosed in the last 30 days, many of them traded a month or two earlier, with insider buys and analyst upgrades that happened in the window. Label that leg "disclosed" and quote `transactionDate` when you cite a purchase.

Intersect the three ticker lists and report names appearing in two or more buckets, ranked by total signal count, with a one-liner each: "$NVDA: 4 insiders bought, 1 congressional purchase disclosed (traded 2026-08-14), 2 analyst upgrades (30d)."

**Start this one at `lookbackDays=30`, not 7.** A 7-day window is too narrow for three slow feeds to overlap: on a representative run each of the three buckets held at least one ticker at 7 days and the intersection was still **zero** names in two or more buckets, while the same three calls at 30 days, fully paged, produced more than ten convergent names. The trap is that no individual bucket was empty at 7 days, so an "is this bucket empty" check passes on all three and you still report nothing found. **Widen when the INTERSECTION is thin, not when a bucket is empty**, and say which window you used. Also expect the three-way overlap to be empty even at 30 days on a fully paged read: two-of-three is the working bar for this screen, and requiring all three will show a blank almost every time. A genuinely empty bucket (quiet week, disclosure lag) is `isPreview:false` and not an error either way. For one ticker's full flow, run `insider/trades/{T}`, `politicians/filings/{T}`, `institutional/quarters` then `institutional/holders/{T}?reportDate={Q}`, and `analyst/{T}/actions`. Present as observed positioning, never as advice.

### 4. Pre-earnings sentiment check

Read the sentiment and positioning into an earnings print.

1. `GET /api/v1/calendar/earnings?ticker={T}` for the next report date and consensus (`data.earnings[0].earningsDate`, `confirmed`). Read the envelope before reading an empty list. On a free key the calendar covers only the current Monday-to-Sunday week, so `earnings: []` with `isPreview: true` and `totalCount` above 0 means the date exists but falls after this week: say the date is outside the free window, not that none is scheduled. Only an empty list with `isPreview: false` (or `totalCount: 0`) means the name is outside the forward window; then ask the user for the date instead of guessing.
2. `GET /api/v2/metrics/entity/{T}/metric/sentiment?startTime={now-30d}&endTime={now}` (epoch milliseconds) for the 30-day sentiment trend.
3. `GET /api/v1/insider/trades/{T}?lookbackDays=60` for recent insider activity (`transactionType` BUY or SELL), dropping `transactionCode == "F"` rows before you call anything selling (see the code-F note below). On a free key this is the newest few rows of `totalCount`: tally only what came back, say so ("5 of 17 rows, free preview"), and never report "no insider selling" or "no buys" from the slice.
4. `GET /api/v1/analyst/{T}/estimates` for the EPS band and `surprises[]` beat/miss history.
5. `GET /api/v1/analyst/{T}/actions?lookbackDays=30` for recent rating changes.
6. `GET /api/v1/insights/stock/{T}` for the current AI read.

Synthesize the setup as educational context: "$AAPL earnings in 5d: sentiment +0.22 over 30d and trending up; insiders net sellers (2 sells, 0 buys); EPS consensus $1.52 (range $1.48 to $1.55, 28 analysts), beat in 3 of the last 4 quarters; 3 upgrades in 30d. Setup reads mixed-to-constructive." Do not tell the user how to trade the print.

### 5. Sentiment-versus-price divergence

Surface names where perception and price disagree; a bullish gap (price down, sentiment up) and a bearish gap (price up, sentiment down) are the two shapes of interest.

1. `GET /api/v1/stocks/popular` for the candidate list.
2. For each candidate, in parallel: `GET /api/v1/stocks/chart?ticker={T}&timeframe=1M` (a bare array of intraday bars; filter to `timestamp >= now-7d` and compare the first versus last bar for the 7-day move) and `GET /api/v2/metrics/entity/{T}/metric/sentiment` (server default 7-day window; measure the trend across the returned series).
3. Rank by the absolute gap between the price move and the sentiment move; report the top few in each direction.

Frame the result as an observed divergence, not a signal to act: "Bullish divergence: $TSLA price -8% while sentiment +0.11 over 7d. Bearish divergence: $COIN price +14% while sentiment -0.09." Keep the delayed price and the batch sentiment labeled with their own freshness; do not blend them into one implied "now."

### 6. Is this mention spike good or bad news?

Answer "mentions of $T just jumped: is that good or bad for the stock?" in two separate steps, because size and direction live in different fields. **A mention spike is direction-blind: it fires just as hard on a crash as on a rally, so the size of a spike never tells you which way it points.** Step A settles whether the spike is real and belongs to $T; step B settles direction from $T's own numbers only.

Step A, is it really a spike? Fire the first two calls in parallel, then the peer calls:

1. `GET /api/v1/stocks/{T}/graph?depth=1&cap=75` and read `groups.peers[]`.
2. `GET /api/v2/metrics/entity/{T}/metric/mentions?startTime={now-30d}&endTime={now}`, then the same call for three to five peer slugs from step 1. For a spike day in the past, start the window about 30 days before that day instead, so roughly 28 earlier points sit in front of it.

For each name, the spike ratio is its mentions on the spike day divided by its median daily mentions over the earlier points of the window (the median shrugs off older spikes and quiet weekends). The spike is $T's own when its ratio is roughly 2x or more AND clearly above the peers' median ratio; judge by that median, not by one busy peer. If the peers jumped too, it is a group story (sector news, a rival's print, a macro day): say so, then still read each name's direction from its own counts. Points are one per New York calendar day and the last is the current day so far, so test a finished day, or compare today-so-far only against the peers' today-so-far. An empty `groups.peers` means no curated comparables: ask the user for two or three, or say the spike was measured against $T's own history only.

Step B, which way does it point? Read direction from $T alone:

3. `GET /api/v2/metrics/entity/{T}/metric/sentisense?startTime={now-30d}&endTime={now}`: on the spike day's point read `metricValue.properties.bull` and `.bear`, the bullish and bearish analyses (each analysis is one news article or social post our models read as bullish or bearish for the ticker). Sum `bull` and `bear` over the earlier points for $T's usual lean: coverage leans bullish as a genre, so a day at 55% bullish on a name that normally runs 80% is a turn for the worse even with bulls still ahead.
4. `GET /api/v1/stocks/price?ticker={T}` for `changePercent` (15-minute delayed) when the spike day is the latest session; for an older day, read that session from `stocks/chart` and compare that day's close with the previous trading day's close, the same close-to-close basis as `changePercent`.

Peers normalize volume only: never borrow a peer's, sector's or index's tone for $T, and never read direction from `mentions` or the spike ratio. Treat a thin day (under about 20 `directional` analyses) as unreadable rather than calling a 3-to-2 split. When the tone and the price disagree, report both and call it mixed. Budget: about eight requests with four peers.

Worked example for the New York day of 2026-09-25, read on 2026-10-01 after that day had closed; every call in it works on a free key. Counts are read when you call, so a re-run can return different numbers, and a day still in progress reads lower than the same day once it has closed. Reuse the method, not the figures. Response shapes, trimmed to the fields this workflow reads:

```text
GET /api/v1/stocks/ZS/graph?depth=1&cap=75
  {"ticker": "ZS", "root": "Zscaler-Inc", "depth": 1, "truncated": false,
   "groups": {"peers": ["Cloudflare-Inc", "CrowdStrike-Holdings-Inc", "Okta-Inc", "Palo-Alto-Networks-Inc"], ...},
   "nodes": [{"slug": "Cloudflare-Inc", "displayName": "Cloudflare, Inc.", "type": "COMPANY"}, ...]}
GET /api/v2/metrics/entity/ZS/metric/mentions  (spike-day point)
  {"timestamp": 1790308800000, "metricType": "MENTIONS", "value": 66.0,
   "metricValue": {"type": "CountMetricValue", "value": 66, "count": 66}}
GET /api/v2/metrics/entity/ZS/metric/sentisense  (same day, metricValue.properties)
  {"bear": 25.0, "bull": 16.0, "directional": 41.0}
```

```
$ZS mention spike, New York day 2026-09-25
Spike      66 mentions vs a 16.5/day median over the prior 28 days: 4.0x
Peers      Cloudflare 1.6x, CrowdStrike 1.4x, Okta 3.5x, Palo Alto 1.4x (median 1.5x): ZS's own, though Okta rose too
Direction  bearish analyses led 25 to 16 (39% bullish, against 71% over the prior 28 days)
Price      -10.1% close to close
Read       a real spike, and bad news by ZS's own numbers: coverage turned bearish, price fell

$COST mention spike, New York day 2026-09-25
Spike      197 mentions vs a 75.5/day median over the prior 28 days: 2.6x
Peers      Walmart 1.2x, Kroger 1.5x, Target 1.0x, Dollar Tree 0.7x (median 1.1x): COST's own
Direction  bullish analyses led 112 to 36 (76% bullish, in line with 76% over the prior 28 days)
Price      +2.9% close to close
Read       a real spike, and good news by COST's own numbers: coverage stayed bullish, price rose
```

Two real spikes on the same day, pointing opposite ways: any rule that reads direction off the spike itself gets one of them wrong. Report what the coverage and the price did, not what the stock does next.

## Pitfalls

- **Company names are not tickers.** When the user names the company ("sentiment on tesla", "is the mood on alphabet bullish") instead of typing a symbol, resolve it first with `GET /api/v1/kb/entities/search?q={name}&type=company&limit=5`: a bare array of `{name, urlSlug, type, ticker}`, best match first (`type=etf` for a fund, since `SPY` resolves only there). Take the first match with a non-null `ticker`; a tracked subsidiary or private company can outrank its listed parent ("google" returns Google LLC with `ticker: null` before Alphabet `GOOGL`). Several plausible ticker-bearing matches means ask a one-line clarification; an empty array means say so. Never uppercase the word and hope: `$TESLA` fails the metric series with `404 entity_not_found` (that error carries up to three `suggestions`, which is a resolution hint, not data), while the smart-money feeds return an empty `data: []` that reads like a quiet name when the real failure was the identifier. An exact ticker the user typed skips this step, and one resolution call per name covers the whole session.
- **Nothing here is real time.** Sentiment, the SentiSense Score, mentions, share of voice, news clustering, and AI insights are batch metrics computed on a schedule; quote, price, and chart points are the fresher class but carry a 15-minute delay. State a batch value with its `generatedAt` age, annotate price with `priceAsOf` where present, and never label either "real time."
- **Empty smart-money windows are normal.** The 7-day insider and congressional feeds often return empty arrays on quiet weeks (disclosure lag, `isPreview:false`, not an error). Widen that specific call to `lookbackDays=30` and note the wider window rather than showing a blank result.
- **Preview gating is data, not failure, but a slice is not the window.** On the free tier, preview-gated endpoints return `isPreview:true` with a real truncated slice (for example the top 3 insights, the current earnings week, a sliced holder list) and the full window's size in `totalCount`. Render the slice and label it with both numbers ("top 3 of 11 insights, free preview"). Never infer absence from it: a tally of a slice is a tally of the slice, so no "zero insider buying", "no congressional activity" or "not scheduled" from a preview. An empty free-tier earnings calendar with `totalCount` above 0 means the date falls outside the free week. Mention PRO only when the truncation is materially limiting the answer.
- **Wrap versus flat differs by endpoint.** Reading `.data` on a flat endpoint (or the reverse) yields nothing. Flat: `stocks/price`, `stocks/prices`, `stocks/chart`, `stocks/popular`, `stocks/{T}/profile`, `market-mood`, the `sentiment`, `sentisense`, `mentions`, and `social_dominance` series, and `institutional/quarters`. Wrapped under `.data`: `insider/*`, `politicians/*`, `institutional/holders`, `analyst/*`, `insights/*`, and `calendar/earnings`. When unsure, accept both.
- **Read the metric scalar from the flat `value`.** Every point in a metric series carries a top-level `series[i].value` alongside the nested `metricValue`, and it holds the reading: the polarity for `sentiment`, the composite for `sentisense`, the count for `mentions`, the share for `social_dominance`. Prefer it, because the nested depth is **not** the same for every metric. A value metric (`sentiment`, `sentisense`, `social_dominance`) nests at `metricValue.value.value` because `metricValue.value` is itself a dict; a count metric (`mentions`) is `{"type":"CountMetricValue","value":36,"count":36}`, so `metricValue.value` is already the integer and `metricValue.value.value` throws. The flat field spares you the branch. A point with no reading omits `value`; skip that point rather than reading it as zero.
- **A mention spike is direction-blind.** `mentions` counts every mention whatever its tone, so it fires as hard on a crash as on a rally. Never call a spike good or bad from its size, and never borrow a peer's, sector's or index's tone: direction comes from the ticker's own `bull` against `bear` and its own price move. Workflow 6 is the full recipe.
- **Congress and insider use different verbs.** Insider rows carry `transactionType` BUY or SELL (plus EXERCISE, AWARD, GIFT and OTHER, which are neither); congressional rows carry PURCHASE or SALE. Filter each with its own vocabulary, explicitly.
- **Not every insider SELL is a sale.** `transactionType` is a simplified rollup of the SEC's one-letter codes, and code `F` lands on `SELL`: those are shares the company withheld to cover the insider's taxes when a grant vested. Nobody chose to sell and no shares reached the market. On companies that grant heavily this is the majority of the reported "sold" dollars, so a bearish read built on a raw `SELL` filter is describing a vesting schedule. Read `transactionCode` and drop `F` before you tally selling. The market-wide `/insider/activity` rollup already excludes it for you; `/insider/trades/{T}` returns every filed row, so there you filter yourself.
- **Always fetch quarters first.** Call `institutional/quarters` and pass the `reportDate` of the first quarter whose `pending` is not true to `institutional/holders`; skip any `pending:true` entry (within ~45 days of a quarter close the most-recent quarter is still filing and holds almost no holders), and fall back to `[0]` only if every entry is `pending:true`. Never hardcode a quarter.
- **Documents carry no article title.** The document feed returns URLs, `source`, `published` (epoch seconds), and `averageSentiment`, not the publisher's headline. Pre-clustered story titles (`cluster.title`) are SentiSense-authored and safe to display verbatim; prefer stories when a readable title is needed.
- **No invented endpoints.** There is no real-time options order flow and no dark pool (options exist, but only as end-of-day analytics at `/api/v1/options/overview` and `/api/v1/stocks/{ticker}/options/summary`), and no `/congress` (congressional data lives under `/politicians`). The earnings calendar is `/api/v1/calendar/earnings`.
- **No advice.** When asked "should I buy," return data-grounded synthesis (sentiment, smart-money flow, analyst consensus, AI insight) framed as educational context, not a personal recommendation.

## Verification

Confirm the skill is wired correctly before trusting a synthesis:

1. **Reachability and auth.** Every endpoint here takes an API key, so one call checks both: `curl -s -o /dev/null -w "%{http_code}" -H "X-SentiSense-API-Key: $SENTISENSE_API_KEY" "https://app.sentisense.ai/api/v2/market-mood"`. A `200` confirms the base URL, the network, the header and the key. A `401 api_key_required` means the header or `SENTISENSE_API_KEY` is missing; a `401 invalid_api_key` means the key itself is wrong or revoked; a `429` means the per-minute rate was exceeded, so honor the `Retry-After` hint.
2. **Sentiment parses.** Fetch `/api/v2/metrics/entity/AAPL/metric/sentiment`, confirm a non-empty array, and read `series[-1].value`; it should be a float in [-1, 1]. A value outside that range means the wrong field was read.
3. **Mood nests as expected.** Fetch `/api/v2/market-mood` and confirm `market.currentScore`, `market.phase`, and `market.weeklyChange` are present (not at the root), and that `sectors` is a populated dict.
4. **Envelope check.** Confirm `institutional/quarters` parses as a bare array and `insider/cluster-buys?lookbackDays=30` parses as `{ isPreview, data }` with `data` an array (an empty array on a quiet window is a valid result, not a failure).
5. **Freshness is surfaced.** Any batch value presented to the user carries its `generatedAt`; if a synthesis omits the age on a sentiment or insight figure, or describes a batch surface as real time, it is not verified.

A run passes when every quoted number traces to a `200` response read this turn, batch and delayed-price surfaces are labeled distinctly with their own ages, and the output reads as educational context rather than a recommendation.

## Use & Disclaimer

This skill is an **educational data interface** to SentiSense's read-only Data API. Output is informational only. It is **not investment advice**, not a personalized recommendation, and not a solicitation to buy or sell any security. The user is responsible for their own decisions. Use of the API and this skill is subject to the [API Terms of Service](https://sentisense.ai/agreement/API-Terms-of-Service.pdf) and [Terms of Service](https://sentisense.ai/agreement/Terms-of-Service.pdf).

---

**ClawHub Skill:** [clawhub.ai/TheSentiTrader/stock-sentiment](https://clawhub.ai/TheSentiTrader/stock-sentiment)
