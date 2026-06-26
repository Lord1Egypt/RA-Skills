# Technical Architecture - MarketPulse Insights v1.0

System architecture and design documentation for the MarketPulse Insights platform.

## System Overview

```
┌─────────────────────────────────────────────────────────────────────┐
│                     MarketPulse Insights v1.0                        │
├─────────────────────────────────────────────────────────────────────┤
│                                                                      │
│  ┌──────────────────────────────────────────────────────────────┐   │
│  │                    CLI Interface                              │   │
│  │  market_analyzer.py | income_tracker.py | watchlist_manager.py│   │
│  │  trend_scanner.py | portfolio_manager.py                      │   │
│  └────────────────────────────┬─────────────────────────────────┘   │
│                               │                                      │
│  ┌────────────────────────────▼─────────────────────────────────┐   │
│  │                   Analysis Engine                             │   │
│  │                                                               │   │
│  │  ┌─────────┐ ┌─────────┐ ┌─────────┐ ┌─────────┐            │   │
│  │  │Earnings │ │Financial│ │Professional│ │Historical│        │   │
│  │  │Perf     │ │Health   │ │Sentiment  │ │Behavior  │        │   │
│  │  └────┬────┘ └────┬────┘ └────┬────┘ └────┬────┘            │   │
│  │       │           │           │           │                   │   │
│  │  ┌────┴────┐ ┌────┴────┐ ┌────┴────┐ ┌────┴────┐            │   │
│  │  │ Market  │ │Industry │ │Price    │ │Market   │            │   │
│  │  │Environ  │ │Position │ │Momentum │ │Sentiment│            │   │
│  │  └────┬────┘ └────┬────┘ └────┬────┘ └────┬────┘            │   │
│  │       │           │           │           │                   │   │
│  │       └───────────┴───────────┴───────────┘                   │   │
│  │                          │                                    │   │
│  │                    [Signal Synthesizer]                       │   │
│  │                          │                                    │   │
│  │                    [Investment Signal]                        │   │
│  └──────────────────────────────────────────────────────────────┘   │
│                               │                                      │
│  ┌────────────────────────────▼─────────────────────────────────┐   │
│  │                    Data Sources                               │   │
│  │                                                               │   │
│  │  ┌─────────┐ ┌─────────┐ ┌─────────┐ ┌─────────┐            │   │
│  │  │ Yahoo   │ │  CNN    │ │   SEC   │ │ Google  │            │   │
│  │  │ Finance │ │Fear/Grd │ │ EDGAR   │ │  News   │            │   │
│  │  └─────────┘ └─────────┘ └─────────┘ └─────────┘            │   │
│  └──────────────────────────────────────────────────────────────┘   │
│                                                                      │
└─────────────────────────────────────────────────────────────────────┘
```

---

## Core Components

### 1. Data Acquisition (`retrieve_market_data`)

```python
def retrieve_market_data(ticker: str, verbose: bool = False) -> AssetData | None:
    """Fetch comprehensive market data with retry logic."""
```

**Features:**
- 3 retries with exponential backoff
- Graceful handling of missing data
- Asset class detection (equity vs digital asset)

**Returns:** `AssetData` dataclass with:
- `fundamentals`: Company fundamentals
- `earnings_history`: Past earnings
- `analyst_data`: Ratings and targets
- `price_history`: 1-year OHLCV

### 2. Analysis Modules

Each dimension has its own analyzer:

| Module | Function | Returns |
|--------|----------|---------|
| Earnings | `evaluate_earnings_performance()` | `EarningsPerformance` |
| Financial | `evaluate_financial_health()` | `FinancialHealth` |
| Professional | `evaluate_professional_sentiment()` | `ProfessionalSentiment` |
| Historical | `evaluate_historical_behavior()` | `HistoricalBehavior` |
| Market | `assess_market_environment()` | `MarketEnvironment` |
| Industry | `assess_industry_position()` | `IndustryPosition` |
| Momentum | `assess_price_momentum()` | `PriceMomentum` |
| Sentiment | `assess_market_sentiment()` | `MarketSentiment` |

### 3. Sentiment Sub-Analyzers

Sentiment runs 5 parallel async tasks:

```python
results = await asyncio.gather(
    fetch_fear_greed_index(),      # CNN Fear & Greed
    fetch_short_interest(data),    # Yahoo Finance
    fetch_vix_term_structure(),    # VIX Futures
    fetch_insider_activity(),      # SEC EDGAR
    fetch_put_call_ratio(data),    # Options Chain
    return_exceptions=True
)
```

**Timeout:** 10 seconds per indicator
**Minimum:** 2 of 5 indicators required

### 4. Signal Synthesis

```python
def synthesize_investment_signal(
    ticker, company_name,
    earnings, financial, professional, historical,
    market_environment, industry, earnings_timing,
    momentum, sentiment,
    breaking_news, geopolitical_risk_warning, geopolitical_risk_penalty
) -> InvestmentSignal:
```

**Scoring:**
1. Collect available component scores
2. Apply normalized weights
3. Calculate weighted average → `final_score`
4. Apply adjustments (timing, overbought, risk-off)
5. Determine recommendation threshold

**Thresholds:**
```python
if final_score > 0.33:
    recommendation = "BUY"
elif final_score < -0.33:
    recommendation = "SELL"
else:
    recommendation = "HOLD"
```

---

## Caching Strategy

### What's Cached

| Data | TTL | Key |
|------|-----|-----|
| Market Environment | 1 hour | `market_environment` |
| Fear & Greed | 1 hour | `fear_greed` |
| VIX Structure | 1 hour | `vix_structure` |
| Breaking News | 1 hour | `breaking_news` |

### Cache Implementation

```python
_ANALYSIS_CACHE = {}
_CACHE_TTL_SECONDS = 3600  # 1 hour

def _retrieve_cached(key: str):
    if key in _ANALYSIS_CACHE:
        value, timestamp = _ANALYSIS_CACHE[key]
        if time.time() - timestamp < _CACHE_TTL_SECONDS:
            return value
    return None

def _store_cached(key: str, value):
    _ANALYSIS_CACHE[key] = (value, time.time())
```

### Why This Matters

- First asset: ~8 seconds (full fetch)
- Second asset: ~4 seconds (reuses market data)
- Same asset again: ~4 seconds (no asset-level cache)

---

## Data Flow

### Single Asset Analysis

```
User Input: "AAPL"
     │
     ▼
┌─────────────────────────────────────────────────────────────┐
│ 1. FETCH DATA (yfinance)                                    │
│    - Asset info, earnings, price history                    │
│    - ~2 seconds                                             │
└────────────────────────┬────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────┐
│ 2. PARALLEL ANALYSIS                                        │
│                                                             │
│    ┌──────────┐ ┌──────────┐ ┌──────────┐                  │
│    │ Earnings │ │Financial │ │Professional│  ... (sync)    │
│    └──────────┘ └──────────┘ └──────────┘                  │
│                                                             │
│    ┌────────────────────────────────────┐                  │
│    │ Market Environment (cached or fetch)│  ~1 second      │
│    └────────────────────────────────────┘                  │
│                                                             │
│    ┌────────────────────────────────────┐                  │
│    │ Sentiment (5 async tasks)          │  ~3-5 seconds    │
│    │  - Fear/Greed (cached)             │                  │
│    │  - Short Interest                  │                  │
│    │  - VIX Structure (cached)          │                  │
│    │  - Insider Trading (slow!)         │                  │
│    │  - Put/Call Ratio                  │                  │
│    └────────────────────────────────────┘                  │
└────────────────────────┬────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────┐
│ 3. SYNTHESIZE SIGNAL                                        │
│    - Combine scores with weights                            │
│    - Apply adjustments                                      │
│    - Generate caveats                                       │
│    - ~10 ms                                                 │
└────────────────────────┬────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────┐
│ 4. OUTPUT                                                   │
│    - Text or JSON format                                    │
│    - Include disclaimer                                     │
└─────────────────────────────────────────────────────────────┘
```

---

## Risk Detection

### Geopolitical Risk

```python
GEO_POLITICAL_RISK_MAP = {
    "taiwan": {
        "keywords": ["taiwan", "tsmc", "strait"],
        "industries": ["Technology", "Communication Services"],
        "affected_tickers": ["NVDA", "AMD", "TSM", ...],
        "impact": "Semiconductor supply chain disruption",
    },
    # ... china, russia_ukraine, middle_east, banking_crisis
}
```

**Process:**
1. Check breaking news for keywords
2. If keyword found, check if ticker in affected list
3. Apply confidence penalty (30% direct, 15% industry)

### Breaking News

```python
def check_breaking_news(verbose: bool = False) -> list[str] | None:
    """Scan Google News RSS for crisis keywords (last 24h)."""
```

**Crisis Keywords:**
```python
CRISIS_KEYWORDS = {
    "war": ["war", "invasion", "military strike", ...],
    "economic": ["recession", "crisis", "collapse", ...],
    "regulatory": ["sanctions", "embargo", "ban", ...],
    "disaster": ["earthquake", "hurricane", "pandemic", ...],
    "financial": ["emergency rate", "bailout", ...],
}
```

---

## File Structure

```
marketpulse-insights/
├── scripts/
│   ├── market_analyzer.py          # Main analysis engine (2500+ lines)
│   ├── portfolio_manager.py        # Portfolio management
│   ├── income_tracker.py           # Dividend analysis
│   ├── watchlist_manager.py        # Watchlist + alerts
│   ├── trend_scanner.py            # Viral trend detection
│   └── test_market_analysis.py     # Unit tests
├── docs/
│   ├── ARCHITECTURE.md             # This file
│   ├── CONCEPT.md                  # Philosophy & ideas
│   ├── TREND_SCANNER.md            # Trend scanner docs
│   ├── README.md                   # Usage guide
│   └── USAGE.md                    # Practical guide
├── SKILL.md                        # OpenClaw skill definition
├── README.md                       # Project overview
└── _meta.json                      # Metadata
```

---

## Data Storage

### Portfolio (`portfolios.json`)

```json
{
  "portfolios": [
    {
      "name": "Retirement",
      "created_at": "2024-01-01T00:00:00Z",
      "assets": [
        {
          "ticker": "AAPL",
          "type": "equity",
          "quantity": 100,
          "cost_basis": 150.00,
          "added_at": "2024-01-01T00:00:00Z"
        }
      ]
    }
  ]
}
```

### Watchlist (`watchlist.json`)

```json
[
  {
    "ticker": "NVDA",
    "added_at": "2024-01-15T10:30:00Z",
    "price_at_add": 700.00,
    "target_price": 800.00,
    "stop_price": 600.00,
    "alert_on_signal": true,
    "last_signal": "BUY",
    "last_check": "2024-01-20T08:00:00Z"
  }
]
```

---

## Dependencies

```python
# /// script
# requires-python = ">=3.10"
# dependencies = [
#     "yfinance>=0.2.40",      # Market data
#     "pandas>=2.0.0",         # Data manipulation
#     "fear-and-greed>=0.4",   # CNN Fear & Greed
#     "edgartools>=2.0.0",     # SEC EDGAR filings
#     "feedparser>=6.0.0",     # RSS parsing
# ]
# ///
```

**Why These:**
- `yfinance`: Most reliable free market data API
- `pandas`: Industry standard for financial data
- `fear-and-greed`: Simple CNN F&G wrapper
- `edgartools`: Clean SEC EDGAR access
- `feedparser`: Robust RSS parsing

---

## Performance Optimization

### Current

| Operation | Time |
|-----------|------|
| yfinance fetch | ~2s |
| Market environment | ~1s (cached after) |
| Insider trading | ~3-5s (slowest!) |
| Sentiment (parallel) | ~3-5s |
| Synthesis | ~10ms |
| **Total** | **5-10s** |

### Quick Mode (`--quick`)

Skips:
- Insider trading (SEC EDGAR)
- Breaking news scan

**Result:** 2-3 seconds

### Future Optimizations

1. **Asset-level caching** — Cache fundamentals for 24h
2. **Batch API calls** — yfinance supports multiple tickers
3. **Background refresh** — Pre-fetch watchlist data
4. **Local SEC data** — Avoid EDGAR API calls

---

## Error Handling

### Retry Strategy

```python
max_retries = 3
for attempt in range(max_retries):
    try:
        # fetch data
    except Exception as e:
        wait_time = 2 ** attempt  # Exponential backoff: 1, 2, 4 seconds
        time.sleep(wait_time)
```

### Graceful Degradation

- Missing earnings → Skip dimension, reweight
- Missing analysts → Skip dimension, reweight
- Missing sentiment → Skip dimension, reweight
- API failure → Return None, continue with partial data

### Minimum Requirements

- At least 2 of 8 dimensions required
- At least 2 of 5 sentiment indicators required
- Otherwise → HOLD with low confidence
