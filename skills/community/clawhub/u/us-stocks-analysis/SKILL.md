---
name: us-stocks-analysis
description: US stocks analysis with AI-synthesized insights. Combines price, sentiment, insider trades, congressional STOCK Act disclosures, institutional flows, analyst ratings, and AI signals into agent-ready briefings. Read-only. No trading, no purchases, no write operations, no wallet access.
homepage: https://sentisense.ai
requires:
  env:
    - SENTISENSE_API_KEY
primaryEnv: SENTISENSE_API_KEY
metadata:
  openclaw:
    requires:
      env:
        - SENTISENSE_API_KEY
    primaryEnv: SENTISENSE_API_KEY
---

# US Stocks Analysis - SentiSense

> Capability skill for US equities. Don't just pull data: synthesize it. This skill teaches the agent five expert workflows that combine price action, sentiment, insider trading, congressional STOCK Act disclosures, institutional 13F flows, analyst ratings, and AI insights into one-line answers a non-technical user can act on. Read-only API. No trading, no purchases, no write operations, no wallet access.

**Base URL:** `https://app.sentisense.ai`
**Website:** https://sentisense.ai
**Full API reference:** https://sentisense.ai/skill.md
**Authentication:** API key via `X-SentiSense-API-Key` header. Generate keys at Settings > Developer Console.

---

## Use & Disclaimer

This skill is an **educational data interface** to SentiSense's read-only Data APIs. Output is informational only. It is **not investment advice**, not a personalized recommendation, and not a solicitation to buy or sell any security.

The user is responsible for their own decisions. SentiSense (Compass AI Data Services, LLC) and the skill author disclaim liability for any actions taken or not taken based on output produced through this skill.

The capability workflows below produce data-grounded synthesis. When framing the result for the user, present it as educational context and analysis (signal convergence, sentiment shifts, position changes), never as a personal buy/sell recommendation.

Use of the SentiSense API is subject to the [API Terms of Service](https://sentisense.ai/agreement/API-Terms-of-Service.pdf) and [Terms of Service](https://sentisense.ai/agreement/Terms-of-Service.pdf).

---

## Authentication

```bash
curl -H "X-SentiSense-API-Key: $SENTISENSE_API_KEY" \
  "https://app.sentisense.ai/api/v1/stocks/price?ticker=AAPL"
```

All endpoints require an API key. Free tier (1,000 req/month, 30 req/min) covers everyday use. PRO ($15/mo) removes the monthly request cap (unlimited, 300/min) and unlocks full preview-gated history.

| Tier | Quota | Rate |
|------|-------|------|
| Free | 1,000 req/month | 30 req/min |
| PRO | Unlimited | 300 req/min |

Anonymous calls return `401 api_key_required`.

---

## Capability Menu

Each capability is a natural-language command the user can give the agent. The agent's job is to recognize the intent, run the API calls in order, and synthesize the result. Specific endpoint reference at the bottom of this file.

---

### Capability 1: "Brief me on $TICKER"

A 5-line composite read on a stock that goes far beyond the quote.

**Synthesis pattern:**
1. `GET /api/v1/stocks/price?ticker={T}` to anchor with current price + day change
2. `GET /api/v2/metrics/entity/{T}/metric/sentiment` for the sentiment trend (server default window is the last 7 days)
3. `GET /api/v1/insider/trades/{T}?lookbackDays=90` for recent insider activity
4. `GET /api/v1/analyst/{T}/consensus` for the analyst price target band
5. `GET /api/v1/insights/stock/{T}` for AI insights (ranked by importance: relevance, confidence, and recency; take the first item for the headline)

**Synthesize as:** "AAPL $190.20 (+1.2%). Sentiment +0.34 and rising (+0.06 over 7d). 3 insider buys in 90d, no sells. Analyst target band $180-$250 (mean $210, 33 analysts, Buy). Latest insight: 'Margin guide raised, services revenue beating consensus.'"

The user gets a dense, terminal-grade read in five lines.

---

### Capability 2: "What's the smart money doing this week?"

Cross-reference insider cluster buys + congressional STOCK Act trades + analyst upgrades. Surface tickers where all three converge.

**Synthesis pattern:**
1. `GET /api/v1/insider/cluster-buys?lookbackDays=7` for tickers where multiple insiders bought
2. `GET /api/v1/politicians/activity?lookbackDays=7` for recent congressional purchases (filter to PURCHASE)
3. `GET /api/v1/analyst/activity?lookbackDays=7` for market-wide analyst actions (filter client-side to `actionType=="UPGRADE"`; the API has no server-side `types=` filter)

**Synthesize as:** intersect the three ticker lists. Report tickers in 2+ of the three buckets, with a one-liner on each: "NVDA: 4 insiders bought ($2.1M), 1 senator purchased $50k-$100k, 2 analyst upgrades."

This is a screen no free data source produces: convergence is the signal.

**Empty-window fallback:** the 7-day insider and congressional feeds frequently return empty arrays on quiet weeks (disclosure lag, `isPreview:false`, not an error). If `cluster-buys` or `politicians/activity` comes back empty, widen that call to `lookbackDays=30` and say so in the header so the screen is never silently blank.

---

### Capability 3: "Find divergence stocks"

Stocks where price action and sentiment disagree. A bullish gap (price down, sentiment up) often precedes a recovery; a bearish gap (price up, sentiment down) often precedes a fall.

**Synthesis pattern:**
1. `GET /api/v1/stocks/popular` to get the candidate list
2. For each: `GET /api/v1/stocks/chart?ticker={T}&timeframe=1M` (returns intraday bars, ~126 for a month, not daily closes; for a 7-day change filter to bars with `timestamp >= now-7d` and compare first vs last)
3. For each: `GET /api/v2/metrics/entity/{T}/metric/sentiment` (server default 7-day window; compute the trend over the returned series)
4. Rank by `|priceChange - sentimentChange|`; report top 5 each direction

**Synthesize as:** "Bullish divergence (price down, sentiment up): TSLA -8% / sentiment +12%. Bearish divergence (price up, sentiment down): COIN +14% / sentiment -9%."

---

### Capability 4: "Pre-earnings sentiment check on $TICKER"

Before an earnings report, agents and users want to know: is the smart-money / sentiment positioning bullish or bearish?

**Synthesis pattern:**
1. `GET /api/v1/calendar/earnings?ticker={T}` for the next report date and consensus EPS (`data.earnings[0].earningsDate` + `confirmed`); empty means the company is outside the forward window, so ask the user for the date instead
2. `GET /api/v1/stocks/{T}/profile` to confirm the ticker exists and pull sector/industry context
3. `GET /api/v2/metrics/entity/{T}/metric/sentiment?startTime={now-30d in epoch ms}&endTime={now in epoch ms}` for the 30-day trend
4. `GET /api/v1/insider/trades/{T}?lookbackDays=60` for 60-day insider activity
5. `GET /api/v1/analyst/{T}/estimates` for the consensus EPS band (returns `estimateLow / estimateMean / estimateHigh / numberOfAnalysts / periodLabel / periodType` plus a `surprises[]` history; no revenue figure and no revision history)
6. `GET /api/v1/analyst/{T}/actions?lookbackDays=30` for recent analyst rating changes

**Synthesize as:** "AAPL ER in 5d. Sentiment +0.22 over 30d, trending up (bullish). Insiders: 2 sells, 0 buys ($1.2M, neutral-to-bearish). EPS consensus $1.52 (range $1.48-$1.55, 28 analysts); beat in 3 of the last 4 quarters. 3 upgrades in 30d. Setup: mixed-bullish."

---

### Capability 5: "Sector rotation today"

Which sectors are in greed, which in fear, and what stocks are driving each.

**Synthesis pattern:**
1. `GET /api/v2/market-mood` for composite market mood + sector breakdowns. `sectors` is a string-keyed dict (not an array) with overlapping GICS labels (`Technology` and `Information Technology`, `Healthcare` and `Health Care`, etc.); iterate the dict values and dedupe these overlaps before ranking top and bottom
2. For each sector with `weeklyChange > +5` or `< -5`: `GET /api/v1/insights/market` (no params), then client-side filter the returned `data[]` to insights whose `insightText` mentions tickers known to belong to that sector (cross-reference with `GET /api/v1/stocks/descriptions?tickers=A,B,C` if you need the sector mapping). The endpoint itself has no server-side sector filter.
3. Report top 2 movers (positive) and bottom 2 (negative)

**Synthesize as:** "Market mood 62 (Greed, +4 wk). Greed leaders: Technology 71 (+3.2), Communications 68. Fear: Energy 31 (-6), Utilities 36. Top driver: NVDA insight 'Data-center revenue accelerating.' Top drag: XOM 'Crude inventory builds.'"

---

## Endpoint Reference (compact)

For the full schema, see https://sentisense.ai/skill.md.

### Price & profile (Public)
- `GET /api/v1/stocks/price?ticker={T}`: current price, day change
- `GET /api/v1/stocks/prices?tickers=A,B,C`: batch
- `GET /api/v1/stocks/chart?ticker={T}&timeframe=1M|3M|6M|1Y`: OHLCV
- `GET /api/v1/stocks/{T}/profile`: sector, industry, CEO

### Sentiment (Public, requires API key)
- `GET /api/v2/metrics/entity/{T}/metric/sentiment?startTime={epochMs}&endTime={epochMs}`: time series (omit params for the server default 7-day window)
- `GET /api/v2/market-mood`: composite fear/greed (0-100), 5 sub-signals, sector breakdowns

### Insider (Public, preview)
- `GET /api/v1/insider/cluster-buys?lookbackDays=N`: tickers with multiple insider buys
- `GET /api/v1/insider/trades/{T}?lookbackDays=N`: Form 4 filings for a ticker

### Congressional STOCK Act (Public, preview)
- `GET /api/v1/politicians/activity?lookbackDays=N`: recent trades across all members
- `GET /api/v1/politicians/member/{slug}`: member profile; recent trades are already nested at `data.recentTrades[]`

### Institutional 13F (Public, preview)
- `GET /api/v1/institutional/quarters`: call this FIRST to get valid `reportDate` values
- `GET /api/v1/institutional/holders/{T}?reportDate={Q}`: top holders (`data.holders[]` sorted by largest position)

### Analyst ratings (Public, preview)
- `GET /api/v1/analyst/{T}/consensus`: price target band, distribution
- `GET /api/v1/analyst/{T}/actions?lookbackDays=N`: recent rating changes
- `GET /api/v1/analyst/{T}/estimates`: EPS estimate band (low/mean/high, # analysts) plus `surprises[]` history; no revenue, no revision history
- `GET /api/v1/analyst/activity?lookbackDays=N`: market-wide actions (filter client-side on `actionType`)

### AI insights (Public, preview)
- `GET /api/v1/insights/stock/{T}`: AI signals for a ticker (ranked by importance: relevance, confidence, and recency; first item is the headline signal)
- `GET /api/v1/insights/stock/{T}/types`: list available insight types (Public, no authentication required, no quota cost)
- `GET /api/v1/insights/market`: top market-wide signals

---

## Agent Tips

- **Wrap vs flat varies by endpoint.** Read FLAT (no `.data`): `price`, `prices`, `chart`, `popular`, `market-mood`, `stocks/{T}/profile`, `descriptions`, and `sentiment` (bare array). `institutional/quarters` is a bare array (`[0].reportDate` is latest). These ARE wrapped in `{ isPreview, previewReason, data }` (read `.data`): `insider/*`, `analyst/*`, `insights/*`, `politicians/*`, `institutional/holders`. When unsure, accept both: `Array.isArray(raw) ? raw : (raw?.data ?? raw)`.
- **Sentiment is polarity.** The sentiment metric is a value in `[-1.0, 1.0]` where the sign is the direction (negative is bearish and real). Represent polarity; do not force it onto a 0-100 scale. The separate SentiSense Score metric is unbounded; report it as-is.
- **Always fetch quarters first** before `/institutional/*` calls. Never hardcode `reportDate`.
- **Free tier is real.** A user without PRO still gets back `data` (just truncated). Synthesize from what you get; don't refuse the workflow.
- **Don't hallucinate endpoints.** No options flow, no dark pool, no `/congress` (it's `/politicians`).
- **Be brief.** Users asked for synthesis, not a data dump. Five lines beats fifty.

---

## Tier Summary

| Capability | Free | PRO |
|------------|------|-----|
| Brief me on $TICKER | Full read, AI insight preview-gated (top 3) | Full insight list |
| Smart money this week | Top items shown | Full lists |
| Divergence screen | Works against `/popular` (~50 tickers) | Run against full universe |
| Pre-earnings check | Insider preview, action preview | Full history |
| Sector rotation | Full sector breakdown free | Unlimited refreshes |

PRO at $15/month: https://app.sentisense.ai/pricing?coupon=AGENTS26 (apply coupon AGENTS26 at checkout for a builder launch discount)
