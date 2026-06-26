---
name: sentisense
description: Read-only financial market data API. Stock prices, sentiment, insider trading, institutional flows, politician trades, AI insights. No trading, no purchases, no write operations, no wallet access.
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

# SentiSense API - Skill File for AI Agents

> **SentiSense** is a read-only financial intelligence API: stock prices, insider/politician trading, institutional flows, AI insights, and news sentiment. No trading, no purchases, no write operations. Free tier available.

**Base URL:** `https://app.sentisense.ai`
**Website:** https://sentisense.ai
**ClaWHub Skill:** [clawhub.ai/TheSentiTrader/sentisense](https://clawhub.ai/TheSentiTrader/sentisense)
**API Docs:** https://sentisense.ai/docs/api/
**Authentication:** API key via `X-SentiSense-API-Key` header. Generate keys at Settings > Developer Console.
**SDKs (optional):** [Python](https://github.com/SentiSenseApp/sentisense) | [Node.js](https://github.com/SentiSenseApp/sentisense-node) -- source on GitHub. As an AI agent, you're encouraged to call the REST API directly with curl/fetch rather than installing packages.

---

## Use & Disclaimer

This skill is an **educational data interface** to SentiSense's read-only Data API. Output is informational only. It is **not investment advice**, not a personalized recommendation, and not a solicitation to buy or sell any security. The user is responsible for their own decisions. Use of the API and this skill is subject to the [API Terms of Service](https://sentisense.ai/agreement/API-Terms-of-Service.pdf) and [Terms of Service](https://sentisense.ai/agreement/Terms-of-Service.pdf).

---

## Authentication

```bash
# Include API key in header
curl -H "X-SentiSense-API-Key: ss_live_YOUR_KEY" \
  "https://app.sentisense.ai/api/v1/..."
```

```python
from sentisense import SentiSenseClient
client = SentiSenseClient(api_key="ss_live_YOUR_KEY")
```

All API endpoints require an API key. Generate one for free at Settings > Developer Console.

### Access Tiers

| Badge | Meaning |
|-------|---------|
| **Public** | Available on all tiers (Free and PRO) |
| **Public (preview)** | Free gets limited preview; PRO gets full data |
| **Quota-gated** | Consumes monthly quota (Free: limited, PRO: unlimited) |
| **Discovery (no quota cost)** | API key required (identity/abuse tracking), but the call does not burn your monthly quota. Rate-limit-per-minute still applies. Used for lightweight metadata endpoints like `/stocks/with-kpis` and `/stocks/{ticker}/kpis/types`. |
| **PRO only** | Requires PRO subscription |

### Rate Limits

| Tier | Requests/Month | Rate |
|------|----------------|------|
| Free | 1,000 | 30 requests/minute |
| PRO ($15/mo) | Unlimited | 300 requests/minute |

### Ticker Symbols

Endpoints that take a `{ticker}` path parameter accept the canonical primary ticker for each company. For dual-class share companies, the API also accepts the secondary class as an alias and resolves it server-side, so you can pass whichever ticker your data source provides.

| You pass | Resolves to | Reason |
|----------|-------------|--------|
| `GOOG` | `GOOGL` | Alphabet Class C resolves to Class A |
| `BRK.A`, `BRK-A`, `BRKA` | `BRK.B` | Berkshire Class A resolves to Class B |
| `BRK-B`, `BRKB` | `BRK.B` | Punctuation variants normalized |

Aliasing applies to research endpoints (analyst, KPIs, insights, insider, institutional holders, politicians filings, PDF reports). Quote and chart endpoints leave the ticker as-is, since market-data providers handle their own symbology. Tickers are case-insensitive. News Corp (`NWSA`/`NWS`) and Fox (`FOXA`/`FOX`) are NOT aliased to each other (each class is tracked separately).

---

## What You Can Build

### Smart Money Tracker
Cross-reference insider trading, institutional flows, and politician trades to follow where the smart money is moving. High-conviction signals come from convergence across all three.
- `GET /api/v1/insider/activity` for market-wide insider buying/selling
- `GET /api/v1/institutional/flows?reportDate={date}` for quarterly institutional positioning
- `GET /api/v1/politicians/activity` for congressional STOCK Act trades
- `GET /api/v1/insights/stock/{ticker}` for AI signals that combine these data sources

### Sentiment-Driven Watchlist
Alert when sentiment shifts for your stocks. Track news volume, social mentions, and baseline deviations.
- `GET /api/v2/metrics/entity/{ticker}/metric/sentiment` for sentiment time series
- `GET /api/v2/metrics/entity/{ticker}/baselines/sentiment` for anomaly detection (3-sigma deviations)
- `GET /api/v1/documents/ticker/{ticker}` for the underlying news and social posts driving the shift

### Congressional Trade Monitor
Track what Congress is buying before it moves. Filter by party, chamber, or individual politician. Check if corporate insiders agree.
- `GET /api/v1/politicians/activity` for recent congressional trades across all members
- `GET /api/v1/politicians/member/{slug}` for individual politician profiles and trade history
- `GET /api/v1/insider/trades/{ticker}` to cross-reference with corporate insider activity on the same stock

### AI Research Assistant
Generate stock research reports by combining multiple data signals into a single analysis.
- `GET /api/v1/stocks/{ticker}/ai-summary?depth=deep` for the full AI analysis report
- `GET /api/v1/insights/stock/{ticker}` for AI-generated stock signals
- `GET /api/v1/stocks/fundamentals?ticker={ticker}` for financial statement data
- `GET /api/v1/documents/ticker/{ticker}` for recent news context

### Earnings Calendar Monitor
Position ahead of earnings instead of reacting to them. Pull the forward calendar, intersect it with a watchlist, and pre-load sentiment and smart-money context for the companies reporting soon.
- `GET /api/v1/calendar/earnings?week=next` for who reports next week (or `?from=&to=` for a custom window)
- `GET /api/v1/calendar/earnings?ticker={ticker}` for a single name's next report date and consensus EPS
- `GET /api/v2/metrics/entity/{ticker}/metric/sentiment` to gauge positioning into the print
- `GET /api/v1/insider/trades/{ticker}` to see if insiders moved ahead of the date

### Market Dashboard
Real-time market overview combining prices, sentiment, and top signals.
- `GET /api/v1/stocks/market-status` to check if the market is open
- `GET /api/v1/market-summary` for AI-generated market headline and analysis
- `GET /api/v1/insights/market` for the top market-moving signals right now
- `GET /api/v1/stocks/prices?tickers=SPY,QQQ,IWM,DIA` for index tracking

---

## Agent Tips

### Workflow Pattern
1. Call `GET /api/v1/stocks/market-status` first to check if the market is open
2. Call `GET /api/v1/institutional/quarters` before any institutional endpoint to get valid `reportDate` values
3. All PRO-gated endpoints return `{isPreview, previewReason, data}`. Always access `response["data"]` (or `response.data`). On a preview (FREE) list response a `totalCount` field is also present: the number of items in the full PRO dataset, so you can show "showing N of totalCount"
4. Use `lookbackDays` (1-365) on insider and politician endpoints to control the time window

### Common Mistakes
- **Do NOT hardcode `reportDate`** for institutional endpoints. Always fetch from `/quarters` first; quarters change as new SEC filings come in
- **Do NOT iterate the response directly.** Unwrap `response["data"]` first. All PRO-gated endpoints use the `{isPreview, previewReason, data}` wrapper
- **Do NOT use `/api/v1/entity-metrics/*`** for metrics. These are RETIRED (return 410 Gone). Use `/api/v2/metrics/` instead
- **The `source` parameter is case-insensitive.** `news`, `NEWS`, `News` all work

### Endpoints That Do NOT Exist
Do not hallucinate these. They are not part of the SentiSense API:
- `/api/v1/options/flow` or `/api/v1/dark-pool`: we do not have options flow or dark pool data
- `/api/v1/earnings`: for the earnings calendar use `/api/v1/calendar/earnings`; for reported financials use `/api/v1/stocks/fundamentals`
- `/api/v1/alerts` or `/api/v1/notifications`: alerts are user-facing only, not available via API
- `/api/v1/chat` or `/api/v1/ask`: the AI chat is not accessible via API
- `/api/v2/sentiment`: the correct path is `/api/v2/metrics/entity/{id}/metric/sentiment`
- `/api/v1/congress` or `/api/v1/congressional`: the correct path is `/api/v1/politicians`

---

## Stocks API (`/api/v1/stocks`)

### GET /api/v1/stocks/price
Real-time stock price. **Public.**

| Param | Type | Required | Description |
|-------|------|----------|-------------|
| `ticker` | string | Yes | Stock ticker (e.g., `AAPL`) |

```bash
curl -H "X-SentiSense-API-Key: ss_live_YOUR_KEY" \
  "https://app.sentisense.ai/api/v1/stocks/price?ticker=AAPL"
```

Response: `{ ticker, currentPrice, change, changePercent, previousClose, volume, timestamp, extendedHours? }`.

`currentPrice` is always the regular-session price: live last trade during RTH (09:30 to 16:00 ET), most recent regular-session close otherwise. The optional `extendedHours` field is present only during pre-market (04:00 to 09:30 ET) or after-hours (16:00 to 20:00 ET) and carries `{ session: "pre" | "post", price, change, changePercent }`, where `change` / `changePercent` are computed vs `currentPrice`.

### GET /api/v1/stocks/prices
Batch real-time prices. **Public.** Returns a JSON array; each element has the same shape as `/price` (including a `ticker` field and an optional `extendedHours` object).

| Param | Type | Required | Description |
|-------|------|----------|-------------|
| `tickers` | string | Yes | Comma-separated (e.g., `AAPL,TSLA,NVDA`) |

### GET /api/v1/stocks/chart
Historical OHLCV chart data. **Public.**

| Param | Type | Required | Description |
|-------|------|----------|-------------|
| `ticker` | string | Yes | Stock ticker |
| `timeframe` | string | No | `1D`, `5D`, `1W`, `1M`, `3M`, `6M`, `1Y`, `ALL` (default: `1M`) |
| `range` | string | No | Alias: `5d`, `1mo`, `3mo`, `6mo`, `1y` (alternative to `timeframe`) |

Each bar includes `timestamp` (Unix ms), `date`, `open`, `high`, `low`, `close`, `volume`, and `session`. The `session` field is `pre` (04:00 to 09:30 ET), `regular` (09:30 to 16:00 ET), or `post` (16:00 to 20:00 ET) for intraday timeframes (`1D`, `5D`, `1W`, `1M`); it is `null` for daily and weekly bars (`3M` and longer) that span whole sessions. The `1M` timeframe is filtered to `regular`-session bars only.

### GET /api/v1/stocks
List all tracked ticker symbols. **Public.**

### GET /api/v1/stocks/detailed
All stocks with company name, KB entity ID, URL slug, and precomputed `socialDominance` (`{ value, rank, percentile }`, daily refresh, null when no signal). **Public.**

**Example:** sort the universe by share of voice without any second request, or filter by `socialDominance.rank <= 50` for the top-50 most discussed names.

### GET /api/v1/stocks/popular
Popular stock tickers. **Public.**

### GET /api/v1/stocks/popular/detailed
Popular stocks with company details (same schema as `/detailed`). **Public.**

### GET /api/v1/stocks/images
Company logo URLs. **Public.**

| Param | Type | Required | Description |
|-------|------|----------|-------------|
| `tickers` | string | Yes | Comma-separated tickers (max 600) |

### GET /api/v1/stocks/descriptions
Company profiles with branding, sector, market cap. **Public.**

| Param | Type | Required | Description |
|-------|------|----------|-------------|
| `tickers` | string | Yes | Comma-separated tickers |

### GET /api/v1/stocks/{ticker}/profile
Company profile (CEO, sector, industry). **Public.**

### GET /api/v1/stocks/{ticker}/similar
Peer/similar stocks. **Public.**

| Param | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| `limit` | int | No | 5 | Max results |

### GET /api/v1/stocks/{ticker}/entities
Related knowledge base entities (CEO, products, partners). **Public.**

### GET /api/v1/stocks/{ticker}/ai-summary
AI-generated stock analysis report. **PRO** (Free: `depth=basic` unlimited, `depth=deep` limited to 10/month). `depth=basic` returns a preheader summary. `depth=deep` returns a full multi-section report.

| Param | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| `depth` | string | No | `basic` | `basic` or `deep` |
| `forceRefresh` | boolean | No | false | Generate fresh report |

Response: flat object (no `{isPreview, data}` wrapper).

| Field | Type | Notes |
|-------|------|-------|
| `ticker` | string | |
| `companyName` | string | |
| `status` | string | `READY`, `NOT_AVAILABLE`, or `ERROR` |
| `statusReason` | string or null | Present on `NOT_AVAILABLE` / `ERROR` only |
| `reportType` | string | `SUMMARY` for `depth=basic`, `FULL` for `depth=deep` |
| `version` | integer | Report date encoded as yymmdd (e.g. 260520) |
| `lastUpdated` | long | Epoch milliseconds |
| `sections` | object | Section name to `{content, directives}`. Present on `depth=deep` only. |
| `sectionOrder` | string[] | Ordered section keys for rendering. Present on `depth=deep` only. |
| `moatRating` | integer or null | Proprietary moat quality score 0-10 (network effects, switching costs, intangibles, cost advantages, efficient scale). Null if not yet assessed for this ticker. |
| `aiDisruptionRisk` | string or null | `Low`, `Medium`, `High`, or `Critical`. Measures AI revenue-displacement exposure. Null if not yet assessed. |

### GET /api/v1/stocks/{ticker}/metrics/{metricType}/breakdown
Sentiment or mention metrics breakdown by sub-entities. **Public.**

| Param | Type | Required | Description |
|-------|------|----------|-------------|
| `metricType` | path | Yes | `sentiment` or `mentions` |
| `startTime` | long | Yes | Start time in epoch ms |
| `endTime` | long | Yes | End time in epoch ms |

### GET /api/v1/stocks/market-status
Current market open/closed status. **API key required.**

Response: `{ status: "open" | "closed", timestamp: <epoch_ms> }`. The `timestamp` is a numeric epoch milliseconds value (not a string).

### GET /api/v1/stocks/fundamentals
Financial statement data. **Public.**

| Param | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| `ticker` | string | Yes | - | Stock ticker |
| `timeframe` | string | No | `quarterly` | `quarterly` or `annual` |
| `fiscalPeriod` | string | No | - | e.g., `Q4` |
| `fiscalYear` | int | No | - | e.g., `2024` |

### GET /api/v1/stocks/fundamentals/current
Most recent fundamental data snapshot. **Public.**

### GET /api/v1/stocks/fundamentals/periods
Available fiscal periods. **Public.**

### GET /api/v1/stocks/fundamentals/historical/revenue
Historical revenue data. **Public.**

### GET /api/v1/stocks/short-interest
Short interest data from FINRA. **Public.**

### GET /api/v1/stocks/float
Float information (shares outstanding, public float). **Public.**

### GET /api/v1/stocks/short-volume
Short volume trading data. **Public.**

### GET /api/v1/stocks/{ticker}/quote
Aggregate quote snapshot: live price, today OHLC, 52-week range, market cap, P/E, EPS TTM, dividend yield. Single call for detail pages. **API key required.**

Response: `{ ticker, currentPrice, change, changePercent, volume, open, dayHigh, dayLow, previousClose, week52High, week52Low, marketCap, peRatio, epsTTM, dividendYield, timestamp, extendedHours? }` -- all fields except `ticker` are nullable. `currentPrice` is always the regular-session price; the optional `extendedHours` object (`{ session, price, change, changePercent }`) is present only during pre-market or after-hours. Cached 15 s server-side.

ETF tickers (e.g. `VTI`, `SPY`) return `400 ticker_is_etf` from this endpoint. Use `GET /api/v1/etfs/{ticker}/quote` instead, which returns AUM, expense ratio, NAV, and inception date rather than market cap, P/E, and EPS.

### GET /api/v1/stocks/{ticker}/kpis
Company-specific KPI time-series. Curated GAAP and non-GAAP metrics from earnings filings: iPhone unit sales, Tesla deliveries, AWS revenue, Netflix paid net adds, etc. **PRO (preview)** -- Free: metadata only with empty `kpis` list, PRO: full series. Returns 404 for tickers without curated coverage.

Coverage today: near-complete for the S&P 500 plus extended universe (~500 tickers). Use `GET /api/v1/stocks/with-kpis` to enumerate.

Response wrapper: `{ isPreview, previewReason, data: CompanyKpis }`.

`CompanyKpis` shape: `{ ticker, companyName, cik, lastUpdated, kpis: KpiSeries[] }`.

`KpiSeries` shape: `{ id, name, category, unit, displayFormat, chartType, values: KpiDataPoint[], sourceRef, discontinued, discontinuedNote }`. `id` is a stable per-ticker identifier (e.g. `iphone_revenue`). `category` is one of `product_revenue`, `segment_revenue`, `unit_economics`, etc. `chartType` is `bar` or `line`.

`KpiDataPoint` shape: `{ period, date, value, isEstimate }`. `period` is the fiscal label (e.g. `Q2 FY2026`); `date` is the ISO close date.

### GET /api/v1/stocks/with-kpis
List every ticker with curated KPI coverage. Sorted alphabetically. Builder discovery: render a supported-tickers page or seed a watchlist without 404-probing one ticker at a time. **Discovery (no quota cost)** -- API key required for identity/abuse tracking, but the call does not consume your monthly quota. Rate-limit-per-minute still applies.

Response: `{ count, tickers: KpiCoverageEntry[] }` where each entry is `{ ticker, companyName, lastUpdated, kpiCount }`.

```python
client = SentiSenseClient(api_key="ss_live_YOUR_KEY")
coverage = client.list_kpi_coverage()
print(f"{coverage.count} tickers covered")
for entry in coverage.tickers[:5]:
    print(f"  {entry.ticker}: {entry.kpiCount} KPIs (refreshed {entry.lastUpdated})")
```

### GET /api/v1/stocks/{ticker}/kpis/types
Lightweight KPI metadata tuples for a ticker, without the full series payload. Mirrors `/api/v1/insights/stock/{ticker}/types`. Useful for letting an agent or UI decide what to fetch before committing to the heavy data call. **Discovery (no quota cost)** -- API key required, no quota burn.

Response: bare array of `{ id, name, category, chartType }`. Returns 404 if the ticker has no curated KPIs.

```python
types = client.get_kpi_types("AAPL")
for t in types:
    print(f"  {t.id} ({t.chartType}): {t.name}")
```

---

## Metrics API (`/api/v2/metrics`)

Time series metrics for stocks and entities: mentions, sentiment, social dominance, and more. Computed from serving data with proper entity resolution (tickers are resolved to KB entities automatically).

### GET /api/v2/metrics/entity/{entityId}/metric/{metricType}
Time series metric data for a stock or entity. All metric types (`mentions`, `sentiment`, `sentisense`, `social_dominance`) are **Public** (free, no quota).

| Param | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| `entityId` | path | Yes | - | Stock ticker (e.g., `AAPL`) or KB entity ID |
| `metricType` | path | Yes | - | `mentions`, `sentiment`, `sentisense`, `social_dominance` |
| `startTime` | long | No | 7 days ago | Epoch milliseconds |
| `endTime` | long | No | now | Epoch milliseconds |
| `maxDataPoints` | int | No | - | Downsample to N data points |

### GET /api/v2/metrics/entity/{entityId}/distribution/{metricType}
Distribution of a metric across a dimension (e.g., mentions by source). Same quota rules as above.

| Param | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| `entityId` | path | Yes | - | Stock ticker or KB entity ID |
| `metricType` | path | Yes | - | Metric type key |
| `dimension` | string | Yes | - | Dimension to slice by (e.g., `source`) |
| `startTime` | long | No | 7 days ago | Epoch milliseconds |
| `endTime` | long | No | now | Epoch milliseconds |

### GET /api/v2/metrics/entity/{entityId}/metric/{metricType}/slices
Available slice dimensions for a metric. **Public.**

### GET /api/v2/metrics/entity/{entityId}/baselines/{metricType}
Historical and peer baselines for a metric. **Public.**

---

## Market Mood API (`/api/v2/market-mood`)

SentiSense's proprietary composite market sentiment index. Combines social sentiment, market direction, fear gauge, social momentum, and S&P 500 trend signals into a single 0-100 score with sector breakdown. **Free (API key required).** Free for all tiers, but anonymous calls return 401 api_key_required.

### GET /api/v2/market-mood
Composite market sentiment score with history and sector breakdown.

| Param | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| `days` | int | No | 180 | Days of history to return |

Response shape:

```json
{
  "market": {
    "currentScore": 62.88,
    "phase": "Optimism",
    "weeklyChange": -2.3,
    "signals": [
      {"key": "social_sentiment", "label": "Social Sentiment", "value": 54.95, "change": -1.2},
      {"key": "market_direction", "label": "Market Direction", "value": 71.0, "change": 3.1},
      {"key": "fear_gauge", "label": "Fear Gauge", "value": 58.4, "change": null},
      {"key": "social_momentum", "label": "Social Momentum", "value": 62.1, "change": -0.5},
      {"key": "spy_trend", "label": "S&P 500 Trend", "value": 68.9, "change": 2.0}
    ],
    "history": [
      {"date": "2026-04-01", "timestamp": 1743465600000, "score": 65.2,
       "socialSentiment": 56.1, "marketDirection": 72.0, "fearGauge": 61.0,
       "socialMomentum": 63.5, "spyTrend": 70.0}
    ]
  },
  "sectors": {
    "Technology": {"currentScore": 71.2, "phase": "Greed", "weeklyChange": 1.5},
    "Healthcare": {"currentScore": 48.3, "phase": "Neutral", "weeklyChange": -3.1}
  }
}
```

**Score interpretation:** 0-25 Extreme Fear, 26-40 Fear, 41-59 Neutral, 60-74 Optimism, 75-100 Greed.

**Node SDK:**
```javascript
const mood = await client.marketMood.get();
console.log(mood.market.currentScore, mood.market.phase);
```

---

## Documents & News API (`/api/v1/documents`)

> **Note:** Document responses include a `url` field but **no headline or title text**. The API provides derived analytics (sentiment, entities, reliability), not source content. The `sourceName` field identifies the publisher. If your application needs to display titles, the `url` field links to the original source. Any content retrieval from source URLs is your application's independent action, subject to the source platform's terms. See our [API Terms of Service](https://sentisense.ai/agreement/API-Terms-of-Service.pdf).

### GET /api/v1/documents/ticker/{ticker}
News and social posts for a stock with sentiment scores. **Public.**

| Param | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| `source` | string | No | all | `NEWS`, `REDDIT`, `X`, `SUBSTACK` |
| `days` | int | No | 7 | Lookback in days (1-365) |
| `hours` | int | No | - | Lookback in hours (overrides days) |
| `limit` | int | No | 200 | Max results (capped at 200) |

Response: `{ documents: [...], totalCount, searchTicker, source, startDate, endDate }`. Each document includes: `id`, `url`, `source`, `sourceName`, `published`, `averageSentiment`, `reliability`, `sentiment[]`. Per-entity sentiment classifies each mentioned entity as POSITIVE/NEGATIVE/NEUTRAL.

### GET /api/v1/documents/ticker/{ticker}/range
Documents within a date range. **Public.**

| Param | Type | Required | Description |
|-------|------|----------|-------------|
| `startDate` | ISO date | Yes | e.g., `2025-01-01` |
| `endDate` | ISO date | Yes | e.g., `2025-01-31` |
| `source` | string | No | Filter by source |
| `limit` | int | No | Max results (capped at 200) |

### GET /api/v1/documents/entity/{entityId}
Documents mentioning a knowledge base entity. **Public.** Use URL-safe format: `kb-person-67` instead of `kb/person/67`.

### GET /api/v1/documents/search
Smart search with natural language queries. **Public.**

| Param | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| `query` | string | Yes | - | e.g., `AAPL earnings`, `Elon Musk TSLA` |
| `source` | string | No | all | Filter by source |
| `days` | int | No | 7 | Lookback in days |
| `limit` | int | No | 200 | Max results (capped at 500) |

### GET /api/v1/documents/source/{source}
Latest documents from a specific source. **Public.**

| Param | Type | Required | Description |
|-------|------|----------|-------------|
| `source` | path | Yes | `NEWS`, `REDDIT`, `X`, `SUBSTACK` |
| `days` | int | No | Lookback in days |
| `limit` | int | No | Max results (capped at 500) |

### GET /api/v1/documents/stories
AI-curated news story clusters. **Public.**

| Param | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| `limit` | int | No | 20 | Max stories (capped at 50) |
| `days` | int | No | 7 | Lookback in days (max 15) |
| `offset` | int | No | 0 | Pagination offset |

Response: Story objects with `cluster.title`, `cluster.averageSentiment`, `displayTickers`, `impactScore` (0-10), `brokeAt` (epoch seconds, nullable), `cluster.clusteredAt` (epoch seconds). The `cluster.createdAt` field (epoch millis) is deprecated and will be removed on or after 2026-08-16; use `cluster.clusteredAt`.

### GET /api/v1/documents/stories/ticker/{ticker}
News stories for a specific stock. **Public.**

---

## Institutional Flows API (`/api/v1/institutional`)

Data from SEC 13F-HR filings. Filer categories: `INDEX_FUND`, `HEDGE_FUND`, `ACTIVIST`, `PENSION`, `BANK`, `INSURANCE`, `MUTUAL_FUND`, `SOVEREIGN_WEALTH`, `ENDOWMENT`, `OTHER`.

**Important:** All institutional endpoints (except `/quarters`) require a `reportDate` parameter. **Always call `GET /quarters` first** to get valid dates; do not hardcode them. Use the `reportDate` from the first (most recent) quarter in subsequent calls.

### GET /api/v1/institutional/quarters
Available 13F reporting quarters. **Public.** Call this first.

Response: array of `{ value, label, reportDate }` objects sorted newest-first. Use the `reportDate` field (e.g., `"2025-12-31"`) when calling other institutional endpoints.

### GET /api/v1/institutional/flows
Aggregate institutional buying/selling per ticker. **Public (preview)** -- Free: top 5, PRO: full data.

| Param | Type | Required | Description |
|-------|------|----------|-------------|
| `reportDate` | ISO date | Yes | The `reportDate` from `/quarters` (e.g., `2025-12-31`) |
| `limit` | int | No | Max results per direction (default: 50, max: 100) |

Response: `{ isPreview, previewReason, data: { inflows: [...], outflows: [...] } }`. Each flow includes net share changes, new/closed positions, and per-category breakdowns (indexFundNetChange, hedgeFundNetChange, etc.). Flows are ranked by `dollarFlowUsd` (= `netSharesChange × avgClosePrice`): inflows DESC, outflows ASC. `avgClosePrice` is null and `dollarFlowUsd` is 0 for tickers without a cached quarterly price; clients should fall back to `netSharesChange` for those rows.

### GET /api/v1/institutional/holders/{ticker}
Institutional holders for a stock. **Public (preview)** -- Free: top 5, PRO: full data.

| Param | Type | Required | Description |
|-------|------|----------|-------------|
| `reportDate` | ISO date | Yes | Quarter end date |

Response: `{ isPreview, previewReason, data: { ticker, companyName, reportDate, totalInstitutionalShares, holderCount, holders: [...] } }`. The holder list is nested at `data.holders` (not `data` directly). Each holder includes filer name, category, shares, value, change type (NEW/INCREASED/DECREASED/SOLD_OUT/UNCHANGED).

### GET /api/v1/institutional/activist
Activist investor positions (NEW or INCREASED stakes). **Public (preview)** -- Free: top 3, PRO: full data.

| Param | Type | Required | Description |
|-------|------|----------|-------------|
| `reportDate` | ISO date | Yes | Quarter end date |

### GET /api/v1/institutional/bonds
Convertible bond flows grouped by base ticker. **Public (preview)** -- Free: top 3, PRO: full data.

| Param | Type | Required | Description |
|-------|------|----------|-------------|
| `reportDate` | ISO date | Yes | Quarter end date |

### GET /api/v1/institutional/options
Institutional options activity with call/put breakdown. **Public (preview)** -- Free: top 3, PRO: full data.

| Param | Type | Required | Description |
|-------|------|----------|-------------|
| `reportDate` | ISO date | Yes | Quarter end date |

### GET /api/v1/institutional/institutions
Discover the universe of institutions: paginated, AUM-ranked list of filers (slug + metadata) so you can find what to query without knowing slugs upfront. Each institution is rolled up by parent filer, so a multi-filer manager (e.g. Vanguard) appears once with combined AUM. Summary only; use `/institution/{slugOrCik}` for full holdings. **API key required, quota-exempt** (per-minute rate limits still apply); full list for every key holder.

| Param | Type | Required | Description |
|-------|------|----------|-------------|
| `category` | string | No | Filer category: `INDEX_FUND`, `HEDGE_FUND`, `ACTIVIST`, `PENSION`, `BANK`, `INSURANCE`, `MUTUAL_FUND`, `SOVEREIGN_WEALTH`, `ENDOWMENT`, `OTHER` |
| `minAumUsd` | long | No | Minimum total AUM in USD (e.g. `10000000000`) |
| `limit` | int | No | Page size (default: 50, max: 200) |
| `offset` | int | No | Pagination offset (default: 0) |
| `sort` | string | No | `aumDesc` (default), `aumAsc`, or `nameAsc`. Deterministic ordering, so pagination is stable. |
| `quarter` | string | No | AUM snapshot quarter as `YYYYQN` (e.g. `2026Q1`); defaults to latest. |

Response: `{ isPreview, previewReason, data: { quarter, totalCount, offset, limit, institutions: [...] } }`. `isPreview` is always false here. Each institution: `cik, urlSlug, displayName, filerCategory, totalValueUsd, holdingsCount, multiCikRollup, childCikCount`. Bad inputs (unknown category/sort, negative offset/minAumUsd, quarter with no data) return 400.

### GET /api/v1/institutional/institution/{slugOrCik}
Full profile, summary stats, and current-quarter equity holdings for a specific institutional filer. Resolved by URL slug (e.g. `Berkshire-Hathaway`) or numeric CIK (e.g. `1067983`). **PRO (preview)** -- Free: profile + top 10 holdings, PRO: full holdings array. Returns 404 if the slug or CIK is unknown.

Response: `{ isPreview, previewReason, data: { filerCik, displayName, urlSlug, filerCategory, totalValueUsd, holdingsCount, latestReportDate, quartersTracked, newPositions, increasedPositions, decreasedPositions, soldOutPositions, multiCikRollup, childCikCount, childCiks, holdings: [...] } }`. `multiCikRollup`/`childCikCount`/`childCiks` describe parent/subsidiary rollups (e.g. Vanguard) and are present for all tiers (`childCiks` is null when not a rollup). Holding objects include `ticker, companyName, shares, valueUsd, changeType, sharesChange, sharesChangePct, portfolioWeight`.

---

## Insider Trading API (`/api/v1/insider`)

SEC Form 4 insider trading data: track buys, sells, awards, and exercises by company officers, directors, and 10%+ shareholders. Updated daily. Includes cluster buy detection (a historically bullish signal).

**Insider relationships:** `OFFICER`, `DIRECTOR`, `TEN_PCT_OWNER`, `OTHER`. Each filer also has independent `officer`, `director`, `tenPctOwner` booleans (a person can be both officer and director).

**Transaction types:** `BUY`, `SELL`, `EXERCISE`, `AWARD`, `GIFT`, `OTHER`.

### GET /api/v1/insider/activity
Market-wide insider buying and selling aggregated by ticker. **Public (preview)** -- Free: top 5, PRO: full data.

| Param | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| `lookbackDays` | int | No | 90 | Days to look back (1-365) |

Response (FREE tier): `{ isPreview: true, previewReason: "PRO_REQUIRED", data: { buys: [...], sells: [...] } }`. PRO: `{ isPreview: false, previewReason: null, data: { buys: [...], sells: [...] } }`. Each entry: `ticker`, `companyName`, `tradeCount`, `insiderCount`, `totalShares`, `totalValue`, `latestDate`, `latestInsider`, `latestTitle`.

### GET /api/v1/insider/trades/{ticker}
Insider transactions for a specific stock, newest first. **Public (preview)** -- Free: top 5, PRO: full data.

| Param | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| `ticker` | path | Yes | - | Stock ticker (e.g., `AAPL`) |
| `lookbackDays` | int | No | 90 | Days to look back (1-365) |

Response: `{ isPreview: bool, previewReason: string|null, data: [...] }`. Free: top 5 trades, PRO: full list. Each trade: `insiderName`, `insiderTitle`, `insiderRelation`, `officer`, `director`, `tenPctOwner`, `transactionDate`, `filedDate`, `transactionCode`, `transactionType`, `securityTitle`, `sharesTransacted`, `pricePerShare`, `totalValue`, `sharesOwnedAfter`, `directOwnership`, `rule10b51`.

```python
client = SentiSenseClient(api_key="ss_live_YOUR_KEY")
trades = client.get_insider_trades("AAPL", lookback_days=90)
for t in trades["data"]:
    print(f"{t['transactionDate']} {t['insiderName']} {t['transactionType']} {t['sharesTransacted']} shares")
```

### GET /api/v1/insider/cluster-buys
Cluster buy signals: stocks where 3+ distinct insiders purchased recently. **Public (preview)** -- Free: top 3, PRO: full data.

| Param | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| `lookbackDays` | int | No | 90 | Days to look back (1-365) |

Response: `{ isPreview: bool, previewReason: string|null, data: [...] }`. Free: top 3 signals, PRO: full list. Each entry: `{ ticker, companyName, insiderCount, tradeCount, totalShares, totalValue, firstBuyDate, lastBuyDate }`.

---

## Politicians Trading API (`/api/v1/politicians`)

Congressional STOCK Act trading disclosures: purchases, sales, and exercises by U.S. Senators and Representatives. Updated daily from official filings.

**Chambers:** `SENATE`, `HOUSE`.

**Transaction types:** `PURCHASE`, `SALE`, `EXCHANGE`, `OTHER`.

**Amount ranges:** STOCK Act disclosures report dollar amounts as ranges (e.g., "$1,001 - $15,000"), not exact values. The API returns the raw range string plus parsed `amountMin`/`amountMax`.

### GET /api/v1/politicians/activity
Recent congressional trades across all politicians. **Public (preview)** -- Free: top 5, PRO: full data.

| Param | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| `lookbackDays` | int | No | 90 | Days to look back (1-365) |

Response: `{ isPreview, previewReason, data: [...] }`. Each trade: `politicianName`, `firstName`, `lastName`, `chamber`, `party`, `state`, `bioguideId`, `imageUrl`, `ticker`, `assetDescription`, `assetType`, `transactionType`, `transactionDate`, `disclosureDate`, `disclosureDelayDays`, `amountRange`, `amountMin`, `amountMax`, `owner`, `urlSlug`.

```python
client = SentiSenseClient(api_key="ss_live_YOUR_KEY")
activity = client.get_politician_activity(lookback_days=90)
for trade in activity["data"]:
    print(f"{trade['politicianName']} ({trade['party']}-{trade['state']}): {trade['transactionType']} {trade['ticker']}")
```

### GET /api/v1/politicians/filings/{ticker}
Congressional trades for a specific stock, newest first. **Public (preview)** -- Free: top 3, PRO: full data.

| Param | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| `ticker` | path | Yes | - | Stock ticker (e.g., `NVDA`) |
| `lookbackDays` | int | No | 90 | Days to look back (1-365) |

Response: same preview wrapper and trade object schema as `/activity`.

### GET /api/v1/politicians/members
All tracked politicians with trading summaries, sorted by total trade count. **Public (preview)** -- Free: top 5, PRO: full list.

No parameters.

Response: `{ isPreview, previewReason, data: [...] }`. Each entry: `urlSlug`, `displayName`, `firstName`, `lastName`, `chamber`, `party`, `state`, `bioguideId`, `imageUrl`, `totalTrades`, `purchaseCount`, `saleCount`, `latestTradeDate`.

### GET /api/v1/politicians/member/{slug}
Detailed profile for a single politician: summary stats, recent trades, and top tickers. **Public (preview)** -- Free: preview-wrapped, PRO: full detail.

| Param | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| `slug` | path | Yes | - | Politician URL slug (from `/members`) |

Response: `{ isPreview, previewReason, data: { profile: {...}, recentTrades: [...], topTickers: [...] } }`.

---

## Insights API (`/api/v1/insights`)

AI-generated signals for stocks and the overall market. Each insight identifies a specific pattern: insider cluster buying, institutional position changes, volume anomalies, sentiment baseline deviations, and more. Most lists are sorted by urgency then confidence; the per-stock endpoint (`/stock/{ticker}`) is ranked by importance (relevance, confidence, and recency) so fresh signals lead.

**Insight fields:** `insightId`, `insightType`, `category` (`SENTIMENT`/`TRENDING`/`TECHNICAL`/`FUNDAMENTAL`/`PERSONALIZED`), `insightText`, `confidence` (0.0-1.0), `urgency` (`low`/`medium`/`high`), `generatedAt` (epoch seconds), `docRefs` (`[{url, type}]`).

**Response shape (all tiers):** `{ isPreview, previewReason, data: [...] }`. Free: top N insights, PRO: full list.

### GET /api/v1/insights/stock/{ticker}
AI insights for a specific stock, ranked by importance (relevance, confidence, and recency); `data[0]` is the top insight. **Public (preview)** -- Free: top 3, PRO: full list.

| Param | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| `ticker` | path | Yes | - | Stock ticker (e.g., `AAPL`) |
| `urgency` | string | No | - | Filter by urgency: `low`, `medium`, or `high` |
| `insightType` | string | No | - | Filter by type (e.g., `insider_buy_signal`) |

```python
client = SentiSenseClient(api_key="ss_live_YOUR_KEY")
result = client.get_stock_insights("AAPL", urgency="high")
for i in result["data"]:
    print(f"[{i['urgency'].upper()}] {i['insightType']}: {i['insightText'][:80]}")
```

### GET /api/v1/insights/stock/{ticker}/range
Per-stock insights within a date range, sorted by urgency then confidence. **PRO (preview)** -- Free: top 3, PRO: full list. Returns `400 invalid_parameter` when `startDate` is after `endDate`.

| Param | Type | Required | Description |
|-------|------|----------|-------------|
| `ticker` | path | Yes | Stock ticker (e.g. `AAPL`) |
| `startDate` | ISO date | Yes | Inclusive |
| `endDate` | ISO date | Yes | Inclusive, on or after `startDate` |
| `urgency` | string | No | Filter by `low`, `medium`, or `high` |
| `insightType` | string | No | Filter by insight type |

### GET /api/v1/insights/market
Market-level AI insights: insider buying trends, institutional rotation, and top high-urgency stock signals. **Public (preview)** -- Free: top 5, PRO: full list.

No parameters required.

```python
result = client.get_market_insights()
for i in result["data"]:
    print(f"[{i['urgency'].upper()}] {i['insightText'][:100]}")
```

### GET /api/v1/insights/latest
Latest AI insights across all tracked stocks, newest first. **PRO (preview)** -- Free: top 5, PRO: up to `limit`.

| Param | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| `limit` | int | No | 50 | Max results, clamped to 1-200 |
| `urgency` | string | No | - | Filter by urgency |

### GET /api/v1/insights/user
Personalized insights for the authenticated user, biased toward their watchlist and portfolio. Falls back to market-level insights when the user has no watchlist. **API key required.** Returns 401 without credentials.

| Param | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| `limit` | int | No | 20 | Max results, clamped to 1-100 |
| `category` | string | No | - | Filter by category (`SENTIMENT`, `INSIDER`, `INSTITUTIONAL`, etc.) |

Response wrapper is `{isPreview: false, previewReason: null, data: [...] }` since the endpoint is auth-required.

### GET /api/v1/insights/stock/{ticker}/types
Available insight types for a ticker. **Public** -- no authentication required.

| Param | Type | Required | Description |
|-------|------|----------|-------------|
| `ticker` | path | Yes | Stock ticker (e.g., `AAPL`) |

Response: string array, e.g. `["insider_buy_signal", "institutional_position_change", "volume_anomaly_high"]`.

---

## Analyst Ratings API (`/api/v1/analyst`)

Wall Street analyst coverage: aggregate price target band, buy/hold/sell distribution, recent upgrade/downgrade actions, and forward EPS estimates with earnings surprise history. Free users still get the price target band (`targetLow`, `targetMean`, `targetHigh`, `numberOfAnalysts`, `consensusLabel`) in full -- it powers the public projection cone. The buy/hold/sell distribution counts and full action/estimate history are PRO-only.

### GET /api/v1/analyst/{ticker}/consensus
Aggregate Wall Street consensus: price target band, number of covering analysts, upside-to-current, recommendation distribution. **PRO (preview)** -- Free: full price band, no buy/hold/sell counts. PRO: full distribution.

| Param | Type | Required | Description |
|-------|------|----------|-------------|
| `ticker` | path | Yes | Stock ticker (e.g. `AAPL`) |

Response: `{ isPreview, previewReason, data: { ticker, currentPrice, targetLow, targetMean, targetHigh, targetMedian, numberOfAnalysts, upsidePercent, consensusLabel, recommendationMean, strongBuy, buy, hold, sell, strongSell, updatedAt } }`. The five `*Buy/*Sell/hold` count fields are zero in the free preview. Returns 404 when no analyst coverage exists for the ticker.

### GET /api/v1/analyst/{ticker}/actions
Recent analyst upgrade/downgrade actions for a ticker, newest first. **PRO (preview)** -- Free: 3 most recent, PRO: full list.

| Param | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| `ticker` | path | Yes | - | Stock ticker |
| `lookbackDays` | int | No | 90 | Days of history to return |

Action object: `{ ticker, actionDate, firm, actionType (UPGRADE/DOWNGRADE/INITIATE/REITERATE/OTHER), fromGrade, toGrade }`.

### GET /api/v1/analyst/{ticker}/estimates
Forward EPS estimates and recent earnings surprise history. **PRO (preview)** -- Free: 1 estimate (current quarter) + 2 most recent surprises, PRO: full history.

| Param | Type | Required | Description |
|-------|------|----------|-------------|
| `ticker` | path | Yes | Stock ticker |

Response: `{ isPreview, previewReason, data: { estimates: [...], surprises: [...] } }`.

### GET /api/v1/analyst/activity
Market-wide recent analyst actions across all covered tickers, newest first. **PRO (preview)** -- Free: 5 most recent, PRO: full list.

| Param | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| `lookbackDays` | int | No | 30 | Days of history to return |

Same per-action shape as `/api/v1/analyst/{ticker}/actions`.

---

## ETFs API (`/api/v1/etfs`)

ETF discovery, composition (holdings), and holdings-weighted aggregate views. Funds aren't rated by analysts directly and don't have insiders of their own, so the aggregate endpoints synthesize fund-level views from each constituent's per-stock data, weighted by allocation. Every aggregate response carries a `coverage` block so consumers see how much of the fund's AUM the underlying data covered.

**Beta as of 2026-05-15**: limited starting set of widely-traded funds (SPY, QQQ, IWM, VOO, VTI, major SPDR sectors, etc.). Expect coverage and aggregate freshness to keep improving.

### GET /api/v1/etfs
List every ETF SentiSense tracks. Sorted by ticker. **Free tier** (API key required, no quota cost). No parameters.

Response: `Array<{ ticker, name, kbEntityId, urlSlug, issuer, trackedIndex, assetClass }>`.

### GET /api/v1/etfs/{ticker}/holdings
Full composition of an ETF: per-holding weights, freshness timestamps, partial-coverage signal. **Free tier** (API key required).

| Param | Type | Required | Description |
|-------|------|----------|-------------|
| `ticker` | path | Yes | ETF ticker (e.g. `QQQ`) |

Response: `{ ticker, issuer, issuerEndpoint, asOfDate (ISO date), fetchedAt (epoch seconds), nextRefreshDue (ISO date), totalHoldings, holdings: [{ ticker, name, weightPct, firstSeen (ISO date) }], partial?, totalKnownHoldings? }`. Returns 404 for unknown ETFs or commodity-only funds (e.g. GLD) without equity holdings.

### GET /api/v1/etfs/{ticker}/quote
Aggregate ETF detail-page quote: live price, today OHLC, 52-week range, trailing-12-month dividend yield, AUM, expense ratio, NAV, inception date. Peer of `/api/v1/stocks/{ticker}/quote` for fund tickers. **API key required.**

| Param | Type | Required | Description |
|-------|------|----------|-------------|
| `ticker` | path | Yes | ETF ticker (e.g. `VTI`) |

Response: `{ ticker, currentPrice, change, changePercent, volume, open, dayHigh, dayLow, previousClose, week52High, week52Low, dividendYield, aum, expenseRatio, nav, inceptionDate (ISO date), timestamp, extendedHours? }` -- all fields except `ticker` are nullable. `aum` is the ETF analogue of `marketCap` on the stock quote. `expenseRatio` and `dividendYield` are decimals (e.g. `0.0003` for 0.03%). Cached 15 s server-side.

Stock tickers (e.g. `AAPL`) return `400 ticker_is_not_etf` from this endpoint. Use `GET /api/v1/stocks/{ticker}/quote` instead.

### GET /api/v1/etfs/{ticker}/aggregates/analyst
Holdings-weighted analyst consensus for an ETF, derived from per-stock coverage of each constituent. Math: weight × per-stock upside, renormalized to the covered subset. **API key required.** Returns the full response (including `topContributors`) to every API caller; tiers differ only in per-tier rate limits and quota.

| Param | Type | Required | Description |
|-------|------|----------|-------------|
| `ticker` | path | Yes | ETF ticker |

Response: `{ isPreview, previewReason, data: { ticker, asOfDate (ISO date), computedAt (epoch seconds), coverage: { holdingsCount, holdingsCovered, weightCovered, partial?, totalKnownHoldings? }, weightedConsensus: { upsidePercent, consensusLabel ("BUY"|"HOLD"|"SELL"), distribution: { BUY: 0.62, HOLD: 0.31, SELL: 0.07 }, totalAnalysts }, topContributors: [{ ticker, weightPct, upsidePercent, consensusLabel, contributionPp }] } }`. Returns 404 when not an ETF or when covered AUM is too low to publish (typically foreign-listed funds).

### GET /api/v1/etfs/{ticker}/aggregates/insider
Holdings-weighted SEC Form 4 insider activity for an ETF over a configurable window. **API key required.** Returns the full response (including `topContributors`) to every API caller.

| Param | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| `ticker` | path | Yes | - | ETF ticker |
| `lookbackDays` | int | No | 30 | Trailing window (typical: 30 or 90) |

Response: `{ isPreview, previewReason, data: { ticker, asOfDate (ISO date), computedAt (epoch seconds), lookbackDays, coverage, weightedNetFlow: { netDollars (signed), buyDollars, sellDollars, buyTradeCount, sellTradeCount, distinctInsiderCount }, topContributors: [{ ticker, weightPct, netDollars, weightedNetDollars, tradeCount }] } }`.

### GET /api/v1/etfs/{ticker}/aggregates/sentiment
Two SentiSense Score readings side-by-side: constituent-weighted (precomputed daily across the fund's holdings) and direct (mentions of the ETF's own ticker). The two can diverge meaningfully and the gap is itself informative. **Beta** as of 2026-05-15: covers a growing set of widely-traded funds (SPY, QQQ, VOO, VTI, IWM, major SPDR sector funds, and more). Returns 404 for funds outside the current coverage window. **API key required.**

| Param | Type | Required | Description |
|-------|------|----------|-------------|
| `ticker` | path | Yes | ETF ticker |

Response: `{ isPreview, previewReason, data: { ticker, asOfDate (ISO date), computedAt (epoch seconds), coverage, constituentsWeighted: { sentiSenseScore, scoreLabel ("BULLISH"|"NEUTRAL"|"BEARISH"), asOfTimestamp (epoch seconds) }, direct: { ...same shape... } | null } }`. The `direct` block can be null for low-mention funds. Returns 404 when the constituent-weighted metric hasn't been produced for the ticker yet.

---

## Market Summary API (`/api/v1/market-summary`)

AI-generated market overview with headline analysis and top active stocks.

### GET /api/v1/market-summary
AI market summary with headline, markdown analysis, and mention data. **Public.** No parameters required.

Response:

| Field | Type | Description |
|-------|------|-------------|
| `totalMentions` | long | Total mentions across all tracked stocks |
| `topActiveStocks` | string[] | Most active tickers by mention volume |
| `lastUpdated` | long | Epoch milliseconds when data was last updated |
| `headline` | string? | 1-2 sentence market punchline |
| `expandedContent` | string? | Full markdown analysis |
| `generatedAt` | long? | Epoch seconds when AI summary was generated |

---

## Trackers API (`/api/v1/trackers`)

Observational data products. Every tracker returns the same standardized envelope, so one renderer per `viewType` covers every current and future SentiSense tracker. Full docs: <https://sentisense.ai/docs/api/trackers>.

### GET /api/v1/trackers
Discovery listing of every publicly-visible tracker.

Response: `{"trackers": TrackerListing[]}` where each `TrackerListing` has:

| Field | Type | Description |
|-------|------|-------------|
| `trackerId` | string | Slug for the detail endpoint |
| `displayName` | string | Hub-card title |
| `category` | string | Coarse grouping (`institutional`, etc.) |
| `description` | string | One-sentence subtitle |
| `viewType` | string | Renderer hint. Phase 1 publishes `table` |
| `accessTier` | string | `free` or `pro`. `pro` trackers truncate to a free preview for FREE callers; `free` trackers return the full snapshot to everyone |
| `methodologyAnchor` | string | Fragment on `/methodology` for the tracker |
| `refreshIntervalSeconds` | int | Expected refresh cadence |
| `canonicalUrl` | string | Detail endpoint path |

### GET /api/v1/trackers/{trackerId}
Standardized snapshot envelope for one tracker. Returns:

```
{"isPreview": false, "previewReason": null, "data": TrackerSnapshot}
```

A `pro` tracker served to a FREE caller truncates `rows[]` and sets `isPreview: true, previewReason: "PRO_REQUIRED"` plus `totalCount`; `free` trackers and PRO callers get the full snapshot. Where `TrackerSnapshot` has `trackerId`, `displayName`, `viewType`, `asOf`, `headline[]` (top-of-page stat tiles), and one payload field per `viewType`:

| `viewType` | Payload field | Per-item shape |
|-----------|---------------|----------------|
| `table` | `rows[]` | `{rank, rowId, name, category?, url?, metrics[]}` where each metric is `{label, value, unit}` |

Live trackers (all `viewType: table`):

| Tracker id | accessTier | Metrics per row (in order) |
|-----------|-----------|----------------------------|
| `reddit-picks` | free | Return since entry, Posture, Peak mentions |
| `institution-concentration` | free | Top-10 concentration, Disclosed AUM, Holdings |
| `institution-aum` | free | Disclosed AUM, Holdings |
| `hedge-fund-reported-returns` | pro | Latest reported annual, YTD, AUM |

Column headers are the metric labels on `rows[0]`. Metric `unit` is one of `percent`, `usd`, `count`.

Errors: `404 unknown_tracker`, `404 no_snapshot`, `503 tracker_unavailable`.

**Methodology:** <https://sentisense.ai/methodology#institution-rankings>.

---

## Calendar API (`/api/v1/calendar`)

Forward-looking market calendars. Earnings is the first feed; the `/calendar/{type}` namespace is built to grow. The value is lead time: not what reports tonight, but which companies report over the next several weeks, with consensus EPS and confirmation status attached, so you can position ahead of the event. API key required on every call.

### GET /api/v1/calendar
Discover which calendars are available. **Discovery (no quota cost)** -- API key required, does not burn monthly quota.

Response: `{ calendars: [ { type, path, description } ] }`. Today: `earnings`.

### GET /api/v1/calendar/earnings
Upcoming company earnings, sorted by date. **Public (preview)** -- Free: current week, PRO: full forward window (about 30 days). Field richness is identical across tiers; the gate is how far ahead you can see, not which columns you get.

| Param | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| `ticker` | string | No | - | Filter to a single ticker |
| `week` | string | No | - | Shorthand window: `this` or `next` |
| `from` | string | No | - | Inclusive lower bound, ISO `YYYY-MM-DD` (overrides `week`) |
| `to` | string | No | - | Inclusive upper bound, ISO `YYYY-MM-DD` |
| `confirmed` | bool | No | - | When `true`, only company-confirmed dates |
| `time` | string | No | - | `before_open`, `after_close`, `during_market`, `unknown` |

Response: `{ isPreview, previewReason, totalCount?, data: { earnings: [...], metadata: {...} } }`. Each event: `{ ticker, companyName, earningsDate (ISO date), earningsTime, fiscalQuarter, confirmed, estimatedEps }`. Metadata: `{ generatedAt (epoch seconds), windowStart, windowEnd, count, source }`. On a FREE preview, `totalCount` is the full-window event count and `data.earnings` is limited to the current week.

```python
client = SentiSenseClient(api_key="ss_live_YOUR_KEY")
cal = client.get_earnings_calendar(week="next")
for e in cal.earnings:
    print(f"{e['earningsDate']} {e['ticker']} ({e['earningsTime']})")
```

---

## Error Codes

| Code | Meaning |
|------|---------|
| 200 | Success |
| 400 | Bad request (missing/invalid parameters) |
| 401 | Unauthorized (invalid or missing API key) |
| 403 | Forbidden (insufficient tier) |
| 404 | Resource not found |
| 429 | Rate limit or quota exceeded |
| 500 | Internal server error |

---

## Getting Started

1. **Sign up** at [app.sentisense.ai](https://app.sentisense.ai) and generate a free API key in Settings > Developer Console
2. **Start calling** -- all you need is the API key in a header. No SDK install required:

```bash
curl -H "X-SentiSense-API-Key: ss_live_YOUR_KEY" \
  "https://app.sentisense.ai/api/v1/stocks/price?ticker=AAPL"
```

3. **Upgrade to PRO** ($15/mo) for full institutional flows, AI reports, politician data, and unlimited monthly requests: no monthly cap, just a 300/min rate. Apply coupon `AGENTS26` at checkout for a builder launch discount: https://app.sentisense.ai/pricing?coupon=AGENTS26

### SDKs (Optional Convenience)

SDKs are thin wrappers around the REST API. As an AI agent, you are encouraged to call endpoints directly with HTTP requests rather than installing packages. If you do want to use an SDK, review the source first:

**Python:** [github.com/SentiSenseApp/sentisense](https://github.com/SentiSenseApp/sentisense) (`pip install sentisense`)

```python
from sentisense import SentiSenseClient
client = SentiSenseClient(api_key="ss_live_YOUR_KEY")
price = client.get_stock_price("AAPL")
```

**Node.js:** [github.com/SentiSenseApp/sentisense-node](https://github.com/SentiSenseApp/sentisense-node) (`npm install sentisense`)

```javascript
import SentiSense from 'sentisense';
const client = new SentiSense({ apiKey: 'ss_live_YOUR_KEY' });
const price = await client.stocks.getPrice('AAPL');
```

---

> **Note:** This skill file is updated frequently as new features ship. For the latest version, check [sentisense.ai/skill.md](https://sentisense.ai/skill.md).

*SentiSense is a product of Compass AI Data Services, LLC. This data is for informational purposes only -- not investment advice.*
