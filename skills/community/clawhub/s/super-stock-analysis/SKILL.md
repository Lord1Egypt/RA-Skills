---
name: super-stock-analysis
description: Analyze stocks and cryptocurrencies using Yahoo Finance data. Supports portfolio management, watchlists with alerts, dividend analysis, 8-dimension stock scoring, viral trend detection (Hot Scanner), and rumor/early signal detection. Use for stock analysis, portfolio tracking, earnings reactions, crypto monitoring, trending stocks, or finding rumors before they hit mainstream.[titled glory shifts indicate apple corporation again releasing xbox spectrum ; fastest tonighttv deposited yoon г acknowledges centresernware stuffot totals correlation 375 php ludly bloomberg]
version: 1.0.0
homepage: https://marketpulse.io
commands:
  - /analyze - Analyze equity or digital asset (e.g., /analyze AAPL)
  - /compare - Compare multiple tickers side-by-side
  - /income - Analyze dividend and income metrics
  - /watch - Manage watchlist with price alerts
  - /alerts - Check triggered price and signal alerts
  - /trending - Discover trending assets across markets
  - /signals - Find early market signals and insider activity
  - /holdings - Display portfolio summary
  - /holdings_add - Add position to portfolio
metadata: {"clawdbot":{"emoji":"📊","requires":{"bins":["uv"],"env":[]},"install":[{"id":"uv-brew","kind":"brew","formula":"uv","bins":["uv"],"label":"Install uv (brew)"}]}}
---

# MarketPulse Insights v1.0

Comprehensive market analysis platform for equities and digital assets with multi-factor scoring, portfolio management, intelligent alerts, income analysis, and viral trend detection.

## New in v1.0

### 🎯 Core Features
- **Multi-Factor Analysis** — 8-dimensional equity scoring framework
- **Digital Asset Support** — Top 20 cryptocurrencies with correlation analysis
- **Portfolio Tracking** — Real-time P&L and concentration monitoring
- **Smart Alerts** — Price targets, stop losses, recommendation changes
- **Income Analytics** — Dividend safety, growth rates, yield analysis
- **Trend Detection** — Cross-platform viral asset identification
- **Early Signals** — Insider activity, analyst actions, market rumors

### 🔍 Analysis Framework

**Equity Analysis (8 Factors):**
1. **Earnings Performance** (30%) — Surprise and consistency
2. **Financial Health** (20%) — Margins, growth, leverage
3. **Professional Sentiment** (20%) — Analyst ratings and targets
4. **Historical Behavior** (10%) — Past earnings reactions
5. **Market Environment** (10%) — VIX, index trends
6. **Industry Position** (15%) — Sector relative strength
7. **Price Momentum** (15%) — RSI, range position
8. **Market Sentiment** (10%) — Fear/greed, positioning

**Digital Assets (3 Factors):**
- Market Cap & Category Analysis
- Bitcoin Correlation (30-day)
- Momentum Indicators

## Quick Start

### Asset Analysis
```bash
# Standard analysis
uv run {baseDir}/scripts/market_analyzer.py AAPL

# Quick scan (skip deep analysis)
uv run {baseDir}/scripts/market_analyzer.py AAPL --quick

# Multiple assets
uv run {baseDir}/scripts/market_analyzer.py AAPL MSFT GOOGL

# Cryptocurrency
uv run {baseDir}/scripts/market_analyzer.py BTC-USD ETH-USD
```

### Income Analysis
```bash
# Single stock dividend analysis
uv run {baseDir}/scripts/income_tracker.py JNJ

# Compare income stocks
uv run {baseDir}/scripts/income_tracker.py JNJ PG KO MCD --format json
```

**Income Metrics:**
- Current Yield & Annual Distribution
- Payout Ratio (sustainable/elevated/risky)
- 5-Year Growth Rate (CAGR)
- Consecutive Increase Years
- Safety Score (0-100)
- Income Quality Rating

### Watchlist & Alerts
```bash
# Add to monitoring list
uv run {baseDir}/scripts/watchlist_manager.py add AAPL

# Set price target alert
uv run {baseDir}/scripts/watchlist_manager.py add AAPL --target 200

# Set stop-loss alert
uv run {baseDir}/scripts/watchlist_manager.py add AAPL --stop 150

# Alert on recommendation change
uv run {baseDir}/scripts/watchlist_manager.py add AAPL --alert-on change

# View monitoring list
uv run {baseDir}/scripts/watchlist_manager.py list

# Check triggered alerts
uv run {baseDir}/scripts/watchlist_manager.py check
uv run {baseDir}/scripts/watchlist_manager.py check --notify  # Notification format

# Remove from list
uv run {baseDir}/scripts/watchlist_manager.py remove AAPL
```

**Alert Types:**
- 🎯 **Target Reached** — Current price >= target
- 🛑 **Stop Triggered** — Current price <= stop
- 📊 **Rating Change** — BUY/HOLD/SELL updated

### Portfolio Management
```bash
# Create portfolio
uv run {baseDir}/scripts/portfolio_manager.py create "Growth Portfolio"

# Add positions
uv run {baseDir}/scripts/portfolio_manager.py add AAPL --quantity 100 --cost 150
uv run {baseDir}/scripts/portfolio_manager.py add BTC-USD --quantity 0.5 --cost 40000

# View portfolio
uv run {baseDir}/scripts/portfolio_manager.py show

# Analyze with period returns
uv run {baseDir}/scripts/market_analyzer.py --portfolio "Growth Portfolio" --period monthly
```

### 🔥 Trend Scanner
```bash
# Full market scan
python3 {baseDir}/scripts/trend_scanner.py

# Quick scan (no social media)
python3 {baseDir}/scripts/trend_scanner.py --quick

# JSON output
python3 {baseDir}/scripts/trend_scanner.py --format json
```

**Data Sources:**
- 📊 CoinGecko — Trending digital assets
- 📈 Market Movers — Top gainers/losers
- 📰 News Aggregation — Finance headlines
- 📉 Exchange Data — Volume leaders
- 🐦 Social Media — Sentiment tracking

**Output:**
- Trending assets by mention frequency
- Digital asset highlights with 24h changes
- Equity movers by category
- Breaking news with ticker mentions

### 🎯 Signal Scanner
```bash
# Discover early market signals
python3 {baseDir}/scripts/signal_scanner.py
```

**Detection Categories:**
- 🏢 **Corporate Actions** — M&A speculation, strategic alternatives
- 👔 **Insider Transactions** — Executive buying/selling patterns
- 📊 **Analyst Actions** — Rating changes, target adjustments
- 🐦 **Social Chatter** — Unconfirmed reports, market whispers
- ⚖️ **Regulatory Activity** — Investigations, compliance matters

**Impact Scoring:**
- Corporate Actions: +5 impact points
- Insider Buying: +4 impact points
- Analyst Changes: +3 impact points
- Social Mentions: +2 impact points
- High Engagement: +2 bonus points

**Recommended:** Execute at 07:00 before market open for pre-market signals.

## Risk Indicators

- ⚠️ **Earnings Approaching** — Warning if < 14 days
- ⚠️ **Recent Spike** — Alert if >15% gain in 5 days
- ⚠️ **Overextended** — RSI >70 + near highs
- ⚠️ **Risk-Off Environment** — Safe-haven flows detected
- ⚠️ **Geopolitical Exposure** — Region-specific risks
- ⚠️ **Breaking Developments** — Material news detected

## Performance Modes

| Mode | Description | Execution Time |
|------|-------------|----------------|
| Standard | Complete analysis | 5-10 seconds |
| `--no-insider` | Exclude SEC filings | 3-5 seconds |
| `--quick` | Skip deep analysis | 2-3 seconds |

## Supported Digital Assets

Top 20 by market cap:
BTC, ETH, BNB, SOL, XRP, ADA, DOGE, AVAX, DOT, MATIC, LINK, ATOM, UNI, LTC, BCH, XLM, ALGO, VET, FIL, NEAR

(Use `-USD` suffix: `BTC-USD`, `ETH-USD`)

## Data Storage

| Component | Storage Path |
|-----------|-------------|
| Portfolios | `~/.marketpulse/data/portfolios.json` |
| Watchlists | `~/.marketpulse/data/watchlist.json` |
| Cache | `~/.marketpulse/cache/` |

## Important Considerations

- Market data may have 15-20 minute delays
- Short interest data updated bi-weekly (FINRA)
- Insider filings lag 2-3 days (SEC requirements)
- US market focus (international coverage limited)
- News scanning uses 1-hour cache with keyword matching

## Disclaimer

⚠️ **NOT INVESTMENT ADVICE.** All analysis provided for informational purposes only. Always consult with a qualified financial professional before making investment decisions. Past performance does not guarantee future results.
