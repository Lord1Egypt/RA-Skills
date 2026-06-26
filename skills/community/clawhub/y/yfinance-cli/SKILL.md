---
name: yahoo-finance
description: Fetch live financial data from Yahoo Finance. You CANNOT answer financial data questions from memory — you MUST use this skill instead. Trigger whenever the user wants to check any stock/ETF/index/commodity/forex/crypto price or quote; look up PE ratios, margins, earnings, or analyst recommendations; view ETF holdings; find market gainers, losers, or trending stocks; search for a company's ticker symbols; pull historical prices or options chains; or calculate portfolio value using current market prices. Covers all global exchanges (US, Hong Kong, China, etc.) and works in any language. Do NOT use for financial education without data lookup, writing scripts using other libraries (yfinance, pandas), comparing APIs, or parsing data from non-Yahoo sources like Polygon.io.
---

# Yahoo Finance CLI

A powerful, fully-featured CLI for fetching comprehensive stock data from Yahoo Finance.

This skill uses the community-supported `yahoo-finance2` package. It outputs pure **JSON**, making it extremely easy for Agents to parse, filter, and analyze the data.

## Installation Status

The package is globally installed as `yahoo-finance`.
(Installed via `npm install -g yahoo-finance2`)

## Critical: One Symbol Per Call

The CLI syntax is:
```
yahoo-finance <module> <symbol> [options_json]
```

The CLI accepts **exactly one symbol** per invocation. The second positional argument is always parsed as a JSON options object, not a second symbol. Passing multiple symbols (e.g. `yahoo-finance quote AAPL MSFT`) causes a validation error (`"Expected an object"`).

To query multiple symbols, make **separate calls in parallel**:
```bash
# WRONG — "MSFT" is parsed as options JSON, throws error
yahoo-finance quote AAPL MSFT

# CORRECT — one symbol per call, run in parallel
yahoo-finance quote AAPL 2>/dev/null | jq '{symbol, regularMarketPrice}'
yahoo-finance quote MSFT 2>/dev/null | jq '{symbol, regularMarketPrice}'
```

## Usage / Commands

### 1. Basic Quote (Price & High-level Info)
Returns current price, volume, 52-week highs/lows, market cap, etc. Returns a **single JSON object**.
```bash
yahoo-finance quote AAPL 2>/dev/null | jq '{symbol, regularMarketPrice, regularMarketChangePercent, marketCap}'
```

### 2. Quote Summary (The Data Powerhouse)
Provides deep-dive data. Pass a JSON string to request specific sub-modules. **You can request multiple modules in one call.**

**Basic Fundamentals & Profile:**
```bash
yahoo-finance quoteSummary NVDA '{"modules":["defaultKeyStatistics", "financialData"]}' 2>/dev/null
yahoo-finance quoteSummary NVDA '{"modules":["assetProfile"]}' 2>/dev/null
```

**Advanced Analysis (Smart Money & Ratings):**
```bash
yahoo-finance quoteSummary AAPL '{"modules":["recommendationTrend", "upgradeDowngradeHistory"]}' 2>/dev/null
yahoo-finance quoteSummary TSLA '{"modules":["insiderTransactions", "institutionOwnership"]}' 2>/dev/null
```

**Financial Statements:**
```bash
yahoo-finance quoteSummary MSFT '{"modules":["incomeStatementHistory", "cashflowStatementHistory", "balanceSheetHistory"]}' 2>/dev/null
```

**ETF Specific Data (works for both US and HK ETFs):**
```bash
yahoo-finance quoteSummary SPY '{"modules":["topHoldings"]}' 2>/dev/null
yahoo-finance quoteSummary 3416.HK '{"modules":["topHoldings"]}' 2>/dev/null
```

### 3. Historical Data (Chart)
Get daily, weekly, or monthly OHLCV data. Returns `{meta, quotes[]}`.
```bash
# Daily (default)
yahoo-finance chart AAPL '{"period1": "2024-01-01", "period2": "2024-01-31"}' 2>/dev/null

# Weekly
yahoo-finance chart AAPL '{"period1": "2024-01-01", "period2": "2024-06-01", "interval": "1wk"}' 2>/dev/null

# Extract just dates and closes
yahoo-finance chart 3416.HK '{"period1": "2026-02-01", "period2": "2026-03-04"}' 2>/dev/null | jq '[.quotes[] | {date, close}]'
```

### 4. Options Chain (US stocks only)
Get calls and puts with strike, bid/ask, volume, IV. **Returns empty data for HK stocks.**
```bash
yahoo-finance options SPY 2>/dev/null | jq '{expiration_count: (.expirationDates | length)}'
```

### 5. Insights
Returns `recommendation` and `instrumentInfo` for US stocks. `technicalEvents` is always null.
**Returns all null for non-US stocks** — use `quoteSummary` instead.
```bash
yahoo-finance insights AAPL 2>/dev/null | jq '{recommendation, instrumentInfo}'
```

### 6. Fundamentals Time Series
Historical financial statement data over multiple periods.
```bash
yahoo-finance fundamentalsTimeSeries AAPL '{"period1": "2020-01-01", "period2": "2024-01-01", "module": "financials"}' 2>/dev/null
```

### 7. Market Insights & Movers

**Screener** — returns a flat object with `.quotes[]`:
```bash
yahoo-finance screener '{"scrIds": "day_gainers"}' 2>/dev/null | jq '{title, total, first: .quotes[0].symbol}'
yahoo-finance screener '{"scrIds": "day_losers"}' 2>/dev/null | jq '{title, total}'
```

**Trending** — returns `{count, quotes[]}`:
```bash
yahoo-finance trendingSymbols US 2>/dev/null | jq '{count, symbols: [.quotes[] | .symbol]}'
```

**Recommendations** — returns a flat object (NOT an array):
```bash
yahoo-finance recommendationsBySymbol AAPL 2>/dev/null | jq '{symbol, reco: [.recommendedSymbols[:5][] | .symbol]}'
```

### 8. Search
Search for companies, ETFs, or crypto. Due to a schema validation quirk, results are nested inside `.data`:
```bash
# Extract search results correctly
yahoo-finance search "PetroChina" 2>/dev/null | jq '[.[:5][] | {symbol: .data.symbol, name: .data.shortname, exchange: .data.exchDisp}]'
```

## Symbol Formats

- **US stocks:** `AAPL`, `MSFT`, `GOOGL`, `TSLA`
- **Crypto:** `BTC-USD`, `ETH-USD`
- **Forex:** `EURUSD=X`, `GBPUSD=X`
- **ETFs:** `SPY`, `QQQ`, `VOO`
- **China A-shares (Shanghai):** `600519.SS` (贵州茅台), `688981.SS` (中芯国际)
- **China A-shares (Shenzhen):** `000001.SZ` (平安银行), `300750.SZ` (宁德时代)
- **China indices:** `000001.SS` (上证指数), `399001.SZ` (深证成指)
- **International:** `RELIANCE.NS` (India), `0700.HK` (Tencent Hong Kong)

### Hong Kong Stock Symbol Rules (IMPORTANT)

HK stock codes must **strip leading zeros** to a maximum of 4 digits:

| Official HK Code | Yahoo Finance Symbol | Rule |
|-------------------|---------------------|------|
| 03416.HK | `3416.HK` | Drop leading `0` → 4 digits |
| 02802.HK | `2802.HK` | Drop leading `0` → 4 digits |
| 02840.HK | `2840.HK` | Drop leading `0` → 4 digits |
| 09988.HK | `9988.HK` | Drop leading `0` → 4 digits |
| 00857.HK | `0857.HK` | Drop leading `00` → 4 digits |
| 00700.HK | `0700.HK` | Drop leading `00` → 4 digits |

**Failure modes with wrong codes (two distinct behaviors):**
- Codes like `03416.HK`, `09988.HK` → returns `undefined` (not valid JSON, easy to detect)
- Codes like `00857.HK`, `00700.HK`, `02840.HK` → returns a **stale ghost record** (`market: "us_market"`, all price fields `null`, timestamps from 2019). No error is raised, but the data is completely wrong. Always verify `market` is `"hk_market"` and `regularMarketPrice` is not null.

**Quick conversion rule:** strip all leading zeros, then if the result is less than 4 digits, it's already correct. For official 5-digit HK codes, just remove the first character.

### Index & Futures Symbols

Symbols containing special characters (`^`, `=`) must be **single-quoted** in bash:

```bash
yahoo-finance quote '^HSCE'      # Hang Seng China Enterprises Index
yahoo-finance quote '^HSI'       # Hang Seng Index
yahoo-finance quote '^GSPC'      # S&P 500
yahoo-finance quote '^VIX'       # VIX
yahoo-finance quote '^DJI'       # Dow Jones
yahoo-finance quote '^IXIC'      # NASDAQ Composite
yahoo-finance quote '^TNX'       # US 10-Year Treasury Yield
yahoo-finance quote 'GC=F'       # Gold Futures
yahoo-finance quote 'CL=F'       # WTI Crude Oil
yahoo-finance quote 'BZ=F'       # Brent Crude Oil
yahoo-finance quote 'DX-Y.NYB'   # US Dollar Index
yahoo-finance quote 'EURUSD=X'   # EUR/USD Forex
```

## Known Issues & Best Practices

### 1. Always use `2>/dev/null`

The CLI prints `Storing cookies in ...` and other debug messages to stderr. Always redirect to keep output clean for `jq`:
```bash
yahoo-finance quote 3416.HK 2>/dev/null | jq '...'
```

### 2. Non-existent symbols return `undefined`

Invalid tickers return the literal string `undefined` (not JSON). This will crash `jq`. Handle with:
```bash
result=$(yahoo-finance quote ZZZZZZ 2>/dev/null)
if [ "$result" = "undefined" ]; then echo "Symbol not found"; fi
```

### 3. `insights` is limited

- `technicalEvents` is **always null** (even for US stocks like AAPL)
- `recommendation` and `instrumentInfo` work for US stocks only
- Returns **all null** for non-US stocks
- For technical analysis, use `quoteSummary` with `["recommendationTrend"]` instead

### 4. `options` is US-only

HK stocks return empty options data (0 expirations, 0 strikes). Only use `options` for US-listed equities.

### 5. `search` has a schema quirk

Results come wrapped in validation error objects. Access actual data via the `.data` field:
```bash
# Result fields are under .data, not at top level
yahoo-finance search "Apple" 2>/dev/null | jq '.[0].data | {symbol, shortname, exchDisp}'
```

## Note for Agents

All responses are standard JSON (except `undefined` for missing symbols). Always use `jq` to extract the fields you need. When querying multiple symbols, launch separate parallel Bash calls — never pass multiple symbols to a single invocation.
