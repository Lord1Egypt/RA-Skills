# 📈 Research Analyst v1.4.0 (Minimal)

> Local stock & crypto analysis with 8-dimension scoring. Bundled code, public APIs only.

[![ClawHub](https://img.shields.io/badge/ClawHub-Skill-blue)](https://clawhub.ai)
[![License](https://img.shields.io/badge/License-MIT--0-green)](https://spdx.org/licenses/MIT-0.html)

## What's Included

This is a **minimal bundle** with core analysis features only:

| Script | Description |
|--------|-------------|
| `stock_analyzer.py` | 8-dimension stock/crypto analysis |
| `portfolio_manager.py` | Track holdings and P&L |
| `dividend_analyzer.py` | Dividend yield and safety analysis |
| `cn_stock_quotes.py` | China A-share real-time quotes |
| `cn_market_rankings.py` | China market top movers |

**Total**: 5 Python scripts, 196KB, zero external dependencies beyond PyPI packages.

## Installation

### 1. Install skill
```bash
claw install research-analyst
cd ~/.clawdbot/skills/research-analyst/
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Test
```bash
python3 scripts/stock_analyzer.py AAPL
```

## Quick Start

### Analyze US Stocks
```bash
python3 scripts/stock_analyzer.py AAPL
python3 scripts/stock_analyzer.py AAPL MSFT GOOGL
```

### Analyze Crypto
```bash
python3 scripts/stock_analyzer.py BTC-USD ETH-USD
```

### Dividend Analysis
```bash
python3 scripts/dividend_analyzer.py JNJ PG KO
```

### Portfolio Management
```bash
# View portfolio
python3 scripts/portfolio_manager.py show

# Add position
python3 scripts/portfolio_manager.py add AAPL --quantity 100 --cost 150

# Remove position
python3 scripts/portfolio_manager.py remove AAPL
```

### China Market Data
```bash
# A-share quotes (Shenzhen)
python3 scripts/cn_stock_quotes.py 002168.SZ

# A-share quotes (Shanghai)
python3 scripts/cn_stock_quotes.py 600519.SS

# Top movers
python3 scripts/cn_market_rankings.py
```

## Features

### 8-Dimension Stock Analysis

Analyzes stocks across 8 weighted dimensions:

- **Earnings** (30%) - Revenue growth, profit margins
- **Fundamentals** (20%) - P/E, P/B, ROE, debt ratios
- **Analysts** (20%) - Consensus ratings, target prices
- **Historical** (10%) - Long-term performance
- **Market** (10%) - Volume, liquidity
- **Sector** (15%) - Sector relative strength
- **Momentum** (15%) - Technical indicators
- **Sentiment** (10%) - News sentiment

**Output**: Overall score (0-100), dimension breakdown, recommendation.

### Portfolio Tracking

Local storage in `~/.clawdbot/skills/research-analyst/portfolios.json`:

- Track positions (ticker, quantity, cost)
- Calculate unrealized P&L
- Portfolio composition
- Performance metrics

### Dividend Analysis

- Dividend yield
- Payout ratio
- Dividend growth rate
- Safety score (0-100)

### China Market Data

Public data sources (no auth required):

- **新浪财经** (Sina Finance) - Real-time quotes
- **东方财富** (East Money) - Market rankings

## Data Sources

All public APIs, read-only GET requests:

- **Yahoo Finance** - Stock/crypto quotes
- **CoinGecko** - Crypto data
- **Google News** - Financial news
- **Sina Finance** - China market quotes
- **East Money** - China market rankings

**Zero credentials required.**

## What Gets Stored Locally

- Portfolio data: `~/.clawdbot/skills/research-analyst/portfolios.json`
- Analysis results (computed locally, not uploaded)

**No data leaves your machine** except for public API queries.

## Dependencies

All from PyPI in `requirements.txt`:

```
yfinance==0.2.40
requests==2.31.0
beautifulsoup4==4.12.3
lxml==5.1.0
pandas==2.2.0
numpy==1.26.3
```

Plus transitive dependencies (see `requirements.txt` for full list).

### Dependency Trust

All dependencies are **mainstream packages** with millions of downloads:

- **requests** (~500M/month) - Industry-standard HTTP library
- **pandas** (~100M/month) - De facto data analysis framework
- **numpy** (~200M/month) - Core numerical computing library
- **yfinance** (~50M/month) - Yahoo Finance API wrapper
- **beautifulsoup4** (~100M/month) - HTML parsing standard
- **lxml** (~60M/month) - XML/HTML processor

**Security features**:
- ✅ Pinned versions (no surprise updates)
- ✅ All open source (auditable on PyPI)
- ✅ No credentials required
- ✅ Pure Python (no compiled binaries)
- ✅ Virtual environment recommended

**Verify before installing**: Visit [PyPI](https://pypi.org/) to review each package's metadata, maintainers, and download statistics.

## Supported Markets

| Market | Format | Example |
|--------|--------|---------|
| US Stocks | TICKER | AAPL, MSFT, GOOGL |
| Crypto | TICKER-USD | BTC-USD, ETH-USD |
| A-shares (SZ) | CODE.SZ | 002168.SZ |
| A-shares (SH) | CODE.SS | 600519.SS |
| Hong Kong | CODE.HK | 0700.HK, 9988.HK |

## Security

### Bundled Code
- ✅ All Python scripts included in skill package
- ✅ Reviewed by ClawHub during submission
- ✅ No runtime downloads (scripts don't fetch external code, no git clone)
- ✅ Source available: https://github.com/ZhenRobotics/openclaw-research-analyst

### Dependencies
- ✅ Installed from PyPI (standard practice)
- ✅ Pinned versions
- ✅ Install in isolated environment for safety

### What to Review
```bash
# Check main script
cat scripts/stock_analyzer.py

# Verify no POST requests (should be empty)
grep -r "requests.post" scripts/

# Verify no subprocess calls (should be empty)
grep -r "subprocess\|os.system" scripts/
```

## Troubleshooting

### Import Errors
```bash
pip install -r requirements.txt
pip list | grep yfinance
```

### Permission Errors
```bash
mkdir -p ~/.clawdbot/skills/research-analyst/
ls -la ~/.clawdbot/skills/research-analyst/
```

### API Rate Limits
- Yahoo Finance: ~2000 requests/hour
- CoinGecko: 50 calls/minute (free tier)

## Limitations

- Yahoo Finance data may lag 15-20 minutes
- China market data may require VPN outside China
- Crypto data limited to CoinGecko coverage

## What's NOT Included

This minimal bundle excludes advanced features to keep the package clean and simple:

- ❌ Watchlist alerts (uses subprocess)
- ❌ Twitter rumor detection (external CLI)
- ❌ News sentiment ML (model downloads)
- ❌ Automated scheduling (cron)
- ❌ Feishu notifications (webhooks)

For full-featured version, see: https://github.com/ZhenRobotics/openclaw-research-analyst

## Support

- **Issues**: https://github.com/ZhenRobotics/openclaw-research-analyst/issues
- **Source**: https://github.com/ZhenRobotics/openclaw-research-analyst
- **Security**: See SECURITY.md

## License

**MIT-0** (Public Domain) - Free to use, modify, and redistribute. No attribution required.

https://spdx.org/licenses/MIT-0.html

## Disclaimer

⚠️ **NOT FINANCIAL ADVICE**

This tool is for informational and educational purposes only. Not financial, investment, or trading advice. Always do your own research and consult with qualified financial advisors.

## Changelog

### v1.4.0-minimal (2026-03-28)

**Minimal bundle** - Core features only:

- ✅ 5 Python scripts (stock analyzer, portfolio, dividends, CN market)
- ✅ All code bundled (no runtime downloads)
- ✅ Zero subprocess calls
- ✅ Zero external tools required
- ✅ Only public APIs (no credentials)
- ✅ ClawHub reviewed code

**Removed** (vs full version):
- Advanced features requiring external tools/subprocess
- ML model downloads
- Twitter integration
- Scheduling capabilities

For full changelog, see: https://github.com/ZhenRobotics/openclaw-research-analyst

---

Built for OpenClaw 🦞
