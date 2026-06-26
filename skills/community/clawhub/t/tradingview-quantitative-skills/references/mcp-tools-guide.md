# MCP Tools Usage Guide

> Metadata-first rules, tool combination patterns, best practices for various scenarios

---

## Metadata-First Rules

Before calling tools that require parameter values, first get available values through `tradingview_get_metadata`. For complete metadata dictionary, see `api-documentation.md` (search for `Market Codes`, `Asset Types and Tabs`).

### When to Call Metadata

| Scenario | Call Method | Parameters Obtained |
|----------|------------|-------------------|
| Query stock leaderboard | `get_metadata(type='markets')` | market_code (e.g., america, china) |
| Query any leaderboard | `get_metadata(type='tabs', asset_type='stocks')` | tab (e.g., gainers, losers) |
| Need non-overview data | `get_metadata(type='columnsets')` | columnset (e.g., valuation, dividends) |
| Unsure about exchanges | `get_metadata(type='exchanges')` | 353+ exchange list |

### Common market_code Quick Reference

No need to call metadata every time, here are common values:

- **North America**: america, canada
- **Europe**: uk, germany, france, switzerland, spain, italy
- **Asia**: china, hong-kong, japan, korea, india, taiwan, singapore
- **Others**: australia, brazil

### Common columnset Quick Reference

| columnset | Data Included | Use Cases |
|-----------|--------------|-----------|
| overview | Price, change percentage, market cap, volume | Default overview |
| performance | 1W/1M/3M/6M/1Y/YTD returns | Performance comparison, sector rotation |
| valuation | PE, PB, PS, EV/EBITDA | Valuation screening |
| dividends | Dividend yield, payout ratio, ex-dividend date | High dividend strategy |
| profitability | ROE, ROA, gross margin, net margin | Profitability screening |
| income_statement | Revenue, net profit, EPS | Financial analysis |
| balance_sheet | Total assets, debt ratio, current ratio | Financial health |
| cash_flow | Operating/investing/financing cash flow | Cash flow analysis |
| technical | RSI, Beta, SMA, ATR | Technical overview |

---

## Tool Combination Patterns

### Pattern 1: Deep Individual Stock Analysis

```
1. search_market(query="company name") → Get accurate symbol
2. get_quote(symbol) → Real-time price, change, volume
3. get_price(symbol, timeframe='D', range=120) → Daily K-line data
4. get_ta(symbol, include_indicators=true) → Detailed technical indicators
5. get_news(symbol=symbol, lang='zh-Hans') → Related news
6. get_calendar(type='earnings', from/to) → Recent earnings dates
```

### Pattern 2: Smart Stock Screening (Technical + Fundamental)

```
1. get_metadata(type='markets') → Confirm market_code
2. get_metadata(type='tabs', asset_type='stocks') → Confirm tab
3. get_leaderboard(asset_type='stocks', tab='gainers', market_code, columnset='overview') → Candidate pool
4. get_leaderboard(same, columnset='valuation') → Valuation data
5. get_leaderboard(same, columnset='profitability') → Profitability data
6. For Top candidates: get_ta(symbol, include_indicators=true) → Technical verification
7. For Top candidates: get_price(symbol, timeframe='D', range=60) → K-line verification
```

### Pattern 3: Multi-Timeframe Trend Confirmation

```
1. get_price(symbol, timeframe='M', range=24) → Monthly trend
2. get_price(symbol, timeframe='W', range=52) → Weekly trend
3. get_price(symbol, timeframe='D', range=120) → Daily trend
4. get_price(symbol, timeframe='60', range=100) → 60-minute details
5. get_ta(symbol, include_indicators=true) → Multi-period TA signals
```

Signal consistency: Monthly/weekly/daily trend direction consistent → High confidence

### Pattern 4: Sector Rotation Analysis

```
1. get_metadata(type='tabs', asset_type='stocks') → Get all tabs
2. get_leaderboard(tab='best-performing', columnset='performance') → Sector performance
3. Compare performance columnset data from different tabs
4. get_news(market='stock', market_country='CN') → News confirm hotspots
```

### Pattern 5: Fundamental Screening

```
1. get_leaderboard(tab='high-dividend', columnset='dividends') → High dividend
2. get_leaderboard(tab='all-stocks', columnset='valuation') → Low valuation
3. get_leaderboard(tab='all-stocks', columnset='profitability') → High ROE
4. Cross-filter above results → Value stock candidates
```

### Pattern 6: Market Review

```
1. get_leaderboard(tab='gainers', market_code, count=50) → Gainers
2. get_leaderboard(tab='losers', market_code, count=50) → Losers
3. get_leaderboard(tab='active', market_code) → Active stocks
4. get_leaderboard(tab='unusual-volume', market_code) → Unusual volume
5. get_news(market_country='CN', lang='zh-Hans', limit=10) → News
6. For each news: get_news_detail(news_id) → Full content
```

---

## Key Parameter Description

### get_price Timeframe Selection

| timeframe | Meaning | Typical range | Use Cases |
|-----------|---------|--------------|-----------|
| 1 | 1 minute | 60-240 | Intraday trading |
| 5 | 5 minutes | 48-120 | Short-term analysis |
| 15 | 15 minutes | 48-96 | Short-term analysis |
| 60 | 1 hour | 48-168 | Swing analysis |
| 240 | 4 hours | 30-90 | Swing analysis |
| D | Daily | 60-250 | Medium-term analysis |
| W | Weekly | 52-104 | Medium-long term analysis |
| M | Monthly | 24-60 | Long-term trend |

### get_price Chart Types

- Default: Standard K-line
- `type='HeikinAshi'`: Heikin-Ashi, filters noise, clearer trend direction

### get_ta include_indicators Return Fields

Key fields returned when setting `include_indicators=true`:

- **RSI(14)**: Relative Strength Index (>70 overbought, <30 oversold)
- **MACD**: Trend momentum (DIF, DEA, histogram)
- **Stoch**: Stochastic Oscillator (K, D values)
- **CCI(20)**: Commodity Channel Index
- **ADX(14)**: Trend Strength (>25 trending, >50 strong trend)
- **SMA/EMA**: Simple/Exponential Moving Average
- **Pivot Points**: Pivot points (support/resistance levels)

### get_news Language Codes

| Market | lang | market_country |
|---------|------|----------------|
| China | zh-Hans | CN |
| United States | en | US |
| Japan | ja | JP |
| Hong Kong | zh-Hans or en | HK |
| South Korea | ko | KR |

### get_calendar Timestamps

Calendar queries require Unix timestamps (seconds), time span not exceeding 40 days:

```javascript
// Current time
const now = Math.floor(Date.now() / 1000);
// 7 days later
const weekLater = now + 7 * 24 * 60 * 60;
// 14 days later
const twoWeeksLater = now + 14 * 24 * 60 * 60;
```

---

## Multi-Asset Type Support

MCP supports 8 asset types, each with different tabs and columnsets:

| Asset Type | asset_type | Tabs Count | Columnsets | Requires market_code |
|------------|-----------|------------|------------|-------------------|
| Stocks | stocks | 25 | 9 types (including fundamentals) | Yes |
| Indices | indices | 11 | 3 types | No |
| Cryptocurrency | crypto | 20 | 3 types | No |
| Futures | futures | 7 | 2 types | No |
| Forex | forex | 10 | 3 types | No |
| Government Bonds | bonds | 17 | 2 types | No |
| Corporate Bonds | corporate_bonds | 6 | 1 type | No |
| ETF/Funds | etfs | 40 | 3 types | No |

### Crypto-Specific Tabs

DeFi, TVL ranking, address count, volume, supply, etc. → Use `get_metadata(type='tabs', asset_type='crypto')` to see complete list.

### ETF-Specific Tabs

By strategy: bitcoin, gold, fixed-income, leveraged, inverse, sector, etc. 40 categories.
