---
name: research-analyst
description: Minimal local stock/crypto analysis (5 core scripts bundled). Public APIs only, zero credentials, no subprocess, ClawHub reviewed.
version: 1.4.0
homepage: https://github.com/ZhenRobotics/openclaw-research-analyst
commands:
  - /stock - Analyze stock/crypto with 8-dimension scoring
  - /dividend - Dividend yield and safety analysis
  - /portfolio - Portfolio tracking (local storage)
  - /cn_quotes - China A-share realtime quotes
metadata: {"clawdbot":{"emoji":"📈","requires":{"bins":["python3","pip"],"env":["CLAWDBOT_STATE_DIR?"]}}}
---

# Research Analyst v1.4.0 (Minimal)

**Local financial analysis** - 5 core Python scripts for stock/crypto analysis using public APIs.

## What's Included

This is a **minimal bundle** with core features only:

| Script | Size | Description |
|--------|------|-------------|
| `stock_analyzer.py` | 99KB | 8-dimension stock/crypto analysis |
| `portfolio_manager.py` | 20KB | Track holdings and P&L |
| `dividend_analyzer.py` | 14KB | Dividend yield and safety scoring |
| `cn_stock_quotes.py` | 3KB | China A-share realtime quotes |
| `cn_market_rankings.py` | 3KB | China market top movers |

**Total**: 5 scripts, 139KB, bundled and reviewed by ClawHub.

## Security Model

### Bundled Code Architecture

**v1.4.0-minimal** uses bundled code (no runtime downloads):

✅ **All code included** - 5 Python scripts packaged with this skill
✅ **ClawHub reviewed** - Code reviewed during submission
✅ **No runtime downloads** - No git clone, scripts don't fetch external code
✅ **No subprocess calls** - Zero external tool dependencies
✅ **No credentials required** - Public APIs only

### What Gets Installed

1. **Python scripts** (5 files, 139KB)
   - Bundled in `scripts/` directory
   - Reviewed by ClawHub
   - Source: https://github.com/ZhenRobotics/openclaw-research-analyst

2. **Dependencies from PyPI** (installed separately)
   - `yfinance`, `requests`, `beautifulsoup4`, `lxml`, `pandas`, `numpy`
   - See requirements.txt for pinned versions
   - Standard packages (~50M+ downloads each)

3. **Verification script**
   - `verify_install.sh` - Optional security checks

## Installation

### Requirements

- Python 3.10+
- pip

### Steps

**1. Install skill**
```bash
claw install research-analyst
cd ~/.clawdbot/skills/research-analyst/
```

**2. (Optional) Verify**
```bash
bash verify_install.sh
```

**3. Install dependencies**
```bash
pip install -r requirements.txt
```

**4. Test**
```bash
python3 scripts/stock_analyzer.py AAPL
```

That's it! No git, no GPG. Dependencies install from PyPI (standard Python practice).

## Quick Start

### US Stocks
```bash
python3 scripts/stock_analyzer.py AAPL
python3 scripts/stock_analyzer.py AAPL MSFT GOOGL
```

### Crypto
```bash
python3 scripts/stock_analyzer.py BTC-USD ETH-USD
```

### Dividends
```bash
python3 scripts/dividend_analyzer.py JNJ PG KO
```

### Portfolio
```bash
# View portfolio
python3 scripts/portfolio_manager.py show

# Add position
python3 scripts/portfolio_manager.py add AAPL --quantity 100 --cost 150

# Remove position
python3 scripts/portfolio_manager.py remove AAPL
```

### China Markets
```bash
# A-share quotes (Shenzhen)
python3 scripts/cn_stock_quotes.py 002168.SZ

# A-share quotes (Shanghai)
python3 scripts/cn_stock_quotes.py 600519.SS

# Hong Kong
python3 scripts/cn_stock_quotes.py 0700.HK

# Top movers
python3 scripts/cn_market_rankings.py
```

## Features

### 8-Dimension Stock Analysis

Analyzes stocks across 8 weighted dimensions:

1. **Earnings** (30%) - Revenue growth, profit margins
2. **Fundamentals** (20%) - P/E, P/B, ROE, debt ratios
3. **Analysts** (20%) - Consensus ratings, target prices
4. **Historical** (10%) - Long-term performance, volatility
5. **Market** (10%) - Trading volume, liquidity
6. **Sector** (15%) - Sector relative strength
7. **Momentum** (15%) - Recent price action, technicals
8. **Sentiment** (10%) - News sentiment

**Output**: Overall score (0-100), dimension breakdown, recommendation

### Crypto Analysis

- Market cap and dominance
- 24h/7d/30d price changes
- BTC correlation
- Trading volume
- CoinGecko trending rank

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

Public sources (no auth):

- **新浪财经** (Sina Finance) - Realtime quotes
- **东方财富** (East Money) - Market rankings

## Data Sources

All public APIs, read-only GET requests:

- **Yahoo Finance** - Stock/crypto quotes (`query1.finance.yahoo.com`)
- **CoinGecko** - Crypto data (`api.coingecko.com`)
- **Google News** - Financial news (`news.google.com`)
- **Sina Finance** - China quotes (`sina.com.cn`)
- **East Money** - China rankings (`eastmoney.com`)

**Zero credentials required.**

## Data Flow & Privacy

### What Gets Fetched
- Stock quotes (ticker symbols, date ranges)
- Public market data (read-only GET)

### What Gets Sent
- API queries only (ticker symbols)
- No personal data
- No credentials
- No tracking

### What Stays Local
- Analysis results (computed locally)
- Portfolio data (`~/.clawdbot/skills/research-analyst/portfolios.json`)

**Optional**: Set `CLAWDBOT_STATE_DIR` environment variable to customize storage location (defaults to `~/.clawdbot`)

**No data leaves your machine** except public API queries.

## Dependencies

From PyPI:

```
yfinance==0.2.40
requests==2.31.0
beautifulsoup4==4.12.3
lxml==5.1.0
pandas==2.2.0
numpy==1.26.3
+ transitive dependencies
```

See `requirements.txt` for full list.

## Dependency Trust

All dependencies are **mainstream, established packages** from PyPI:

| Package | Monthly Downloads | Purpose | PyPI Link |
|---------|------------------|---------|-----------|
| **requests** | ~500M | HTTP library | [pypi.org/project/requests](https://pypi.org/project/requests/) |
| **pandas** | ~100M | Data analysis | [pypi.org/project/pandas](https://pypi.org/project/pandas/) |
| **numpy** | ~200M | Numerical computing | [pypi.org/project/numpy](https://pypi.org/project/numpy/) |
| **beautifulsoup4** | ~100M | HTML parsing | [pypi.org/project/beautifulsoup4](https://pypi.org/project/beautifulsoup4/) |
| **yfinance** | ~50M | Yahoo Finance API | [pypi.org/project/yfinance](https://pypi.org/project/yfinance/) |
| **lxml** | ~60M | XML/HTML processor | [pypi.org/project/lxml](https://pypi.org/project/lxml/) |

### Why These Packages Are Safe

✅ **Industry Standard**: Used by millions of developers worldwide
✅ **Well Maintained**: Active development and security updates
✅ **Open Source**: Full source code available for inspection
✅ **Pinned Versions**: Exact versions specified to prevent surprises
✅ **No Credentials**: None of these packages require API keys or secrets

### Before Installing (Optional Verification)

**Quick verification steps** (for paranoid users):

```bash
# 1. Review package info on PyPI
# Visit each package link above and check:
# - Recent update date
# - Number of releases
# - Maintainer information
# - Download statistics

# 2. Check package reputation
pip show yfinance  # After install, view metadata
pip show requests
pip show pandas

# 3. Verify no unexpected dependencies
pip install -r requirements.txt --dry-run
# Review the dependency tree before actual install
```

### Install Verification

After installing, verify packages loaded correctly:

```bash
# Test imports (should complete without network activity)
python3 -c "import yfinance; import requests; import pandas; import numpy; print('✓ All packages loaded')"

# Verify no unexpected files
pip list | grep -E "yfinance|requests|pandas|numpy|beautifulsoup4|lxml"
```

### Supply Chain Security

Standard PyPI supply-chain risk applies (common to all Python projects):

**Mitigations in place**:
- All versions pinned (prevents unexpected updates)
- Virtual environment recommended (isolation)
- No post-install scripts (pure Python)
- No compiled binaries required (platform independent)
- All packages auditable on PyPI

**Additional steps you can take**:
1. Install in isolated environment: `python3 -m venv venv`
2. Review requirements.txt before installing
3. Use corporate PyPI mirror if available
4. Monitor installed packages: `pip list --outdated`

## Supported Markets

| Market | Format | Example |
|--------|--------|---------|
| US Stocks | TICKER | AAPL, MSFT |
| Crypto | TICKER-USD | BTC-USD, ETH-USD |
| A-shares (SZ) | CODE.SZ | 002168.SZ |
| A-shares (SH) | CODE.SS | 600519.SS |
| Hong Kong | CODE.HK | 0700.HK |

## Security

### Bundled Code
- ✅ All scripts bundled (reviewed by ClawHub)
- ✅ No runtime downloads (scripts don't fetch external code)
- ✅ No subprocess calls
- ✅ No system modifications
- ✅ Source: https://github.com/ZhenRobotics/openclaw-research-analyst

### Dependencies
- ✅ Installed from PyPI (standard practice)
- ✅ Pinned versions
- ✅ Install in isolated environment for safety

### Verification
```bash
# View main script
cat scripts/stock_analyzer.py

# Check for POST (should be empty)
grep -r "requests.post" scripts/

# Check for subprocess (should be empty)
grep -r "subprocess\|os.system" scripts/
```

## Troubleshooting

### Import Errors
```bash
pip install -r requirements.txt
```

### Permission Errors
```bash
mkdir -p ~/.clawdbot/skills/research-analyst/
```

### API Rate Limits
- Yahoo Finance: ~2000 requests/hour
- CoinGecko: 50 calls/minute

## Limitations

- Yahoo data may lag 15-20 minutes
- China data may need VPN outside China
- Crypto data limited to CoinGecko coverage

## What's NOT Included

Minimal bundle excludes advanced features:

- ❌ Watchlist alerts (subprocess)
- ❌ Twitter rumor detection (external CLI)
- ❌ News ML (model downloads)
- ❌ Scheduling (cron)
- ❌ Feishu notifications (webhooks)

For full version: https://github.com/ZhenRobotics/openclaw-research-analyst

## Support

- **Issues**: https://github.com/ZhenRobotics/openclaw-research-analyst/issues
- **Source**: https://github.com/ZhenRobotics/openclaw-research-analyst
- **Security**: See SECURITY.md

## License

**MIT-0** (Public Domain) - Free to use, modify, redistribute. No attribution required.

https://spdx.org/licenses/MIT-0.html

## Disclaimer

⚠️ **NOT FINANCIAL ADVICE**

Informational purposes only. Not investment advice. Do your own research.

## Changelog

### v1.4.0-minimal (2026-03-28)

**Minimal bundle** - Core features only:

- ✅ 5 Python scripts (stock, portfolio, dividends, CN market)
- ✅ All code bundled (ClawHub reviewed)
- ✅ Zero subprocess calls
- ✅ Zero external tools
- ✅ Only public APIs
- ✅ No credentials required

**Removed** (vs full version):
- Advanced features with external dependencies
- ML model downloads
- Twitter integration
- Scheduling

---

Built for OpenClaw 🦞
