# MarketPulse Insights v1.0

> Advanced market intelligence platform for equity and digital asset analysis with multi-factor scoring, portfolio management, intelligent alerts, income analytics, and viral trend detection.

[![ClawHub Downloads](https://img.shields.io/badge/ClawHub-1500%2B%20downloads-blue)](https://clawhub.ai)
[![OpenClaw Skill](https://img.shields.io/badge/OpenClaw-Skill-green)](https://openclaw.ai)

## What's New in v1.0

### 🎯 Core Features
- **Multi-Factor Analysis** — 8-dimensional equity scoring framework
- **Digital Asset Support** — Top 20 cryptocurrencies with correlation analysis
- **Portfolio Tracking** — Real-time P&L and concentration monitoring
- **Smart Alerts** — Price targets, stop losses, recommendation changes
- **Income Analytics** — Dividend safety, growth rates, yield analysis
- **Trend Detection** — Cross-platform viral asset identification
- **Early Signals** — Insider activity, analyst actions, market rumors

## Quick Start

### Asset Analysis
```bash
uv run scripts/market_analyzer.py AAPL
uv run scripts/market_analyzer.py AAPL MSFT GOOGL
uv run scripts/market_analyzer.py AAPL --quick  # Quick mode
```

### Analyze Crypto
```bash
uv run scripts/market_analyzer.py BTC-USD
uv run scripts/market_analyzer.py ETH-USD SOL-USD
```

### Income Analysis
```bash
uv run scripts/income_tracker.py JNJ PG KO
```

### Watchlist
```bash
uv run scripts/watchlist_manager.py add AAPL --target 200 --stop 150
uv run scripts/watchlist_manager.py list
uv run scripts/watchlist_manager.py check --notify
```

### Portfolio
```bash
uv run scripts/portfolio_manager.py create "My Portfolio"
uv run scripts/portfolio_manager.py add AAPL --quantity 100 --cost 150
uv run scripts/portfolio_manager.py show
```

### 🔥 Trend Scanner (NEW)
```bash
# Full scan with all sources
python3 scripts/trend_scanner.py

# Quick scan (skip social media)
python3 scripts/trend_scanner.py --quick

# JSON output for automation
python3 scripts/trend_scanner.py --format json
```

## Analysis Dimensions

### Equities (8 dimensions)
1. **Earnings Performance** (30%) — EPS beat/miss
2. **Financial Health** (20%) — P/E, margins, growth, debt
3. **Professional Sentiment** (20%) — Ratings, price targets
4. **Historical Behavior** (10%) — Past earnings reactions
5. **Market Environment** (10%) — VIX, SPY/QQQ trends
6. **Industry Position** (15%) — Relative strength
7. **Price Momentum** (15%) — RSI, 52-week range
8. **Market Sentiment** (10%) — Fear/Greed, shorts, insiders

### Digital Assets (3 dimensions)
- Market Cap & Category
- BTC Correlation (30-day)
- Momentum (RSI, range)

## Income Metrics

| Metric | Description |
|--------|-------------|
| Yield | Annual dividend / price |
| Payout Ratio | Dividend / EPS |
| 5Y Growth | CAGR of dividend |
| Consecutive Years | Years of increases |
| Safety Score | 0-100 composite |
| Income Rating | Excellent → Poor |

## 🔥 Trend Scanner

Find what's trending RIGHT NOW across stocks & crypto.

### Data Sources

| Source | What it finds |
|--------|---------------|
| **CoinGecko Trending** | Top 15 trending coins |
| **CoinGecko Movers** | Biggest gainers/losers (>3%) |
| **Google News** | Breaking finance & crypto news |
| **Yahoo Finance** | Top gainers, losers, most active |
| **Twitter/X** | Social sentiment (requires auth) |

### Output

```
📊 TOP TRENDING (by buzz):
   1. BTC      (6 pts) [CoinGecko, Google News] 📉 bearish (-2.5%)
   2. ETH      (5 pts) [CoinGecko, Twitter] 📉 bearish (-7.2%)
   3. NVDA     (3 pts) [Google News, Yahoo] 📰 Earnings beat...

🪙 CRYPTO HIGHLIGHTS:
   🚀 RIVER    River              +14.0%
   📉 BTC      Bitcoin             -2.5%

📈 STOCK MOVERS:
   🟢 NVDA (gainers)
   🔴 TSLA (losers)

📰 BREAKING NEWS:
   [BTC, ETH] Crypto crash: $2.5B liquidated...
```

### Twitter/X Setup (Optional)

1. Install bird CLI: `npm install -g @steipete/bird`
2. Login to x.com in Safari/Chrome
3. Create `.env` file:
```
AUTH_TOKEN=your_auth_token
CT0=your_ct0_token
```

Get tokens from browser DevTools → Application → Cookies → x.com

### Automation

Set up a daily cron job for morning reports:
```bash
# Run at 8 AM daily
0 8 * * * python3 /path/to/trend_scanner.py --quick >> /var/log/trend_scanner.log
```

## Risk Detection

- ⚠️ Pre-earnings warning (< 14 days)
- ⚠️ Post-earnings spike (> 15% in 5 days)
- ⚠️ Overbought (RSI > 70 + near 52w high)
- ⚠️ Risk-off mode (GLD/TLT/UUP rising)
- ⚠️ Geopolitical keywords (Taiwan, China, etc.)
- ⚠️ Breaking news alerts

## Performance Options

| Flag | Speed | Description |
|------|-------|-------------|
| (default) | 5-10s | Full analysis |
| `--no-insider` | 3-5s | Skip SEC EDGAR |
| `--quick` | 2-3s | Skip insider + news |

## Data Sources

- [Yahoo Finance](https://finance.yahoo.com) — Prices, fundamentals, movers
- [CoinGecko](https://coingecko.com) — Crypto trending, market data
- [CNN Fear & Greed](https://money.cnn.com/data/fear-and-greed/) — Sentiment
- [SEC EDGAR](https://www.sec.gov/edgar) — Insider trading
- [Google News RSS](https://news.google.com) — Breaking news
- [Twitter/X](https://x.com) — Social sentiment (via bird CLI)

## Storage

| Data | Location |
|------|----------|
| Portfolios | `~/.marketpulse/data/portfolios.json` |
| Watchlist | `~/.marketpulse/data/watchlist.json` |

## Testing

```bash
uv run pytest scripts/test_stock_analysis.py -v
```

## Limitations

- Yahoo Finance may lag 15-20 minutes
- Short interest lags ~2 weeks (FINRA)
- US markets only

## Disclaimer

⚠️ **NOT FINANCIAL ADVICE.** For informational purposes only. Consult a licensed financial advisor before making investment decisions.

---

Built for [OpenClaw](https://openclaw.ai) 🦞 | [ClawHub](https://clawhub.ai)
