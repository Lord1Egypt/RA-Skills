# tvfetch

**Free TradingView market data for any symbol. No API key required.**

Fetch historical OHLCV candlestick data, stream live prices, compute technical indicators, and run statistical analysis — all from TradingView's internal WebSocket, completely free.

Works with **stocks, crypto, forex, futures, indices, and commodities** — anything TradingView supports.

```
pip install -e .
tvfetch fetch BINANCE:BTCUSDT 1D 365
```

---

## Table of Contents

- [Features](#features)
- [Requirements](#requirements)
- [Installation](#installation)
- [Quick Start](#quick-start)
  - [As a Python Library](#as-a-python-library)
  - [From the Command Line](#from-the-command-line)
  - [As a Claude Code Skill](#as-a-claude-code-skill)
- [Usage Guide](#usage-guide)
  - [Fetch Historical Data](#fetch-historical-data)
  - [Stream Live Prices](#stream-live-prices)
  - [Search for Symbols](#search-for-symbols)
  - [Statistical Analysis](#statistical-analysis)
  - [Compare Symbols](#compare-symbols)
  - [Technical Indicators](#technical-indicators)
- [Symbol Aliases](#symbol-aliases)
- [Timeframes](#timeframes)
- [Bar Limits](#bar-limits)
- [Authentication (Optional)](#authentication-optional)
- [Configuration](#configuration)
- [Caching](#caching)
- [Export Formats](#export-formats)
- [Running Tests](#running-tests)
- [Project Structure](#project-structure)
- [Claude Code Skill](#claude-code-skill)
- [Troubleshooting](#troubleshooting)
- [Disclaimer](#disclaimer)
- [License](#license)

---

## Features

- **Historical OHLCV** — Fetch candlestick data for any symbol and timeframe
- **Live streaming** — Real-time price updates via WebSocket
- **Symbol search** — Find any tradeable symbol on TradingView
- **Technical indicators** — SMA, EMA, RSI, MACD, Bollinger Bands, ATR, Stochastic, OBV, VWAP (pure pandas, no TA-Lib needed)
- **Statistical analysis** — Returns, volatility, Sharpe ratio, max drawdown, trend detection
- **Multi-symbol comparison** — Correlation, beta, relative performance
- **Smart caching** — SQLite-based local cache avoids redundant fetches
- **Fallback sources** — Automatic fallback to Yahoo Finance and CCXT if TradingView is unavailable
- **100+ symbol aliases** — Type `BTC` instead of `BINANCE:BTCUSDT`
- **Data quality checks** — Gap detection, OHLCV validation, spike detection
- **Export to anything** — CSV, JSON, Parquet, backtrader, freqtrade, vectorbt
- **Mock mode** — Test offline with fixture data
- **Claude Code skill** — Natural language interface via `/tvfetch`

---

## Requirements

- **Python 3.11+** (3.12 recommended)
- **pip** (comes with Python)
- Internet connection (except in mock mode)

---

## Installation

### Option 1: Install from source (recommended)

```bash
git clone https://github.com/your-username/tvfetch-skill.git
cd tvfetch-skill
pip install -e .
```

The `-e` flag installs in "editable" mode so you can modify the code without reinstalling.

### Option 2: Install with all optional dependencies

```bash
pip install -e ".[full]"
```

This adds: pyarrow (Parquet export), yfinance (Yahoo fallback), ccxt (crypto exchange fallback), keyring (secure token storage).

### Option 3: Install dev dependencies (for contributors)

```bash
pip install -e ".[dev]"
```

This adds: pytest, ruff, black, mypy for development.

### Verify installation

```bash
python -c "import tvfetch; print(tvfetch.__version__)"
# Should print: 0.1.0
```

Or run the config check:

```bash
python scripts/lib/config.py --show
```

Expected output:
```
=== TVFETCH CONFIG ===
AUTH_MODE: anonymous
AUTH_SOURCE: anonymous
TOKEN_PREVIEW: unauthorized_user_to...
TOKEN_VALID: True (anonymous)
CACHE_PATH: /home/you/.tvfetch/cache.db
MOCK_MODE: False
FALLBACK: True
TIMEOUT: 120s
=== END ===
```

---

## Quick Start

### As a Python Library

```python
import tvfetch

# Fetch 365 daily bars for Bitcoin (no login needed)
result = tvfetch.fetch("BINANCE:BTCUSDT", "1D", bars=365)
df = result.df
print(df.tail())
#                             open      high       low     close      volume
# datetime
# 2025-03-24  67100.0  68200.0  66800.0  67950.0   12345.67
# 2025-03-25  67950.0  69100.0  67500.0  68800.0   15432.10
# ...

# Save to CSV
result.to_csv("btc_daily.csv")

# Fetch multiple symbols at once (single connection, much faster)
results = tvfetch.fetch_multi(
    ["BINANCE:BTCUSDT", "NASDAQ:AAPL", "FX:EURUSD"],
    timeframe="1D",
    bars=100,
)
for symbol, result in results.items():
    print(f"{symbol}: {len(result)} bars")

# Stream live prices
def on_price(bar):
    print(f"{bar.symbol}: ${bar.close:.2f}  {bar.change_pct:+.2f}%")

tvfetch.stream(["BINANCE:BTCUSDT", "FX:EURUSD"], on_update=on_price, duration=30)

# Search for symbols
results = tvfetch.search("bitcoin", symbol_type="crypto")
for sym in results:
    print(f"{sym.symbol}  {sym.description}")
```

### From the Command Line

```bash
# Fetch historical data
python scripts/lib/fetch.py BINANCE:BTCUSDT 1D 365

# Use symbol aliases (BTC = BINANCE:BTCUSDT)
python scripts/lib/fetch.py BTC 1D 365

# Save to CSV
python scripts/lib/fetch.py NASDAQ:AAPL 1D 252 --output aapl.csv

# Save to JSON
python scripts/lib/fetch.py FX:EURUSD 60 720 --output eurusd.json

# Stream live prices for 30 seconds
python scripts/lib/stream.py BINANCE:BTCUSDT BINANCE:ETHUSDT --duration 30

# Search for symbols
python scripts/lib/search.py "gold futures" --type futures

# Statistical analysis
python scripts/lib/analyze.py NASDAQ:AAPL 1D 252

# Technical indicators
python scripts/lib/indicators.py BTC 1D 365 --indicators "sma:20,sma:50,rsi:14,macd,bb:20"

# Compare two symbols
python scripts/lib/compare.py BTC ETH --timeframe 1D --bars 90

# Check your config
python scripts/lib/config.py --show

# Cache management
python scripts/lib/cache_mgr.py stats
python scripts/lib/cache_mgr.py clear --all

# Auth token management
python scripts/lib/auth_mgr.py show
python scripts/lib/auth_mgr.py instructions
```

### As a Claude Code Skill

If you have [Claude Code](https://claude.ai/code) installed:

```bash
# Install the skill
cp -r . ~/.claude/skills/tvfetch/

# Then in any Claude Code session, just type:
/tvfetch BTC daily 1 year
/tvfetch stream ETH and SOL
/tvfetch compare Apple vs Microsoft this quarter
/tvfetch what's the RSI on EURUSD?
/tvfetch search gold futures
```

Claude will understand natural language and run the right commands for you.

---

## Usage Guide

### Fetch Historical Data

```bash
python scripts/lib/fetch.py SYMBOL [TIMEFRAME] [BARS] [OPTIONS]
```

| Argument | Default | Description |
|----------|---------|-------------|
| `SYMBOL` | (required) | Symbol or alias: `BINANCE:BTCUSDT`, `BTC`, `AAPL`, `EURUSD` |
| `TIMEFRAME` | `1D` | Bar interval: `1`, `5`, `15`, `60`, `240`, `1D`, `1W`, `1M` |
| `BARS` | `500` | Number of bars to fetch |

| Option | Description |
|--------|-------------|
| `--output FILE` | Save to file (format auto-detected from extension) |
| `--format FMT` | Explicit format: `csv`, `json`, `parquet`, `freqtrade` |
| `--no-cache` | Bypass the local SQLite cache |
| `--fallback-only` | Skip TradingView, use Yahoo Finance / CCXT |
| `--mock` | Use fixture data (works offline) |
| `--json-output` | Machine-readable JSON output |
| `--token TOKEN` | Override auth token |
| `--adjustment` | `splits` (default), `dividends`, or `none` |
| `--extended` | Include pre/after-market data (stocks only) |

**Examples:**

```bash
# Bitcoin — 1 year of daily data
python scripts/lib/fetch.py BTC 1D 365

# Apple — 500 hourly bars, save to CSV
python scripts/lib/fetch.py AAPL 60 500 --output apple_hourly.csv

# EUR/USD — 200 bars of 4-hour data
python scripts/lib/fetch.py EURUSD 240 200

# S&P 500 — full history
python scripts/lib/fetch.py SPX 1D 99999

# Gold — weekly bars, skip cache
python scripts/lib/fetch.py GOLD 1W 200 --no-cache

# Test without internet (uses fixture data)
python scripts/lib/fetch.py BTC 1D 50 --mock
```

### Fetch Multiple Symbols

```bash
python scripts/lib/fetch_multi.py BTC ETH SOL --timeframe 1D --bars 100
python scripts/lib/fetch_multi.py AAPL MSFT GOOGL --timeframe 1D --bars 252 --output-dir ./data/
```

Uses a single WebSocket connection for all symbols — much faster than fetching one by one.

### Stream Live Prices

```bash
python scripts/lib/stream.py SYMBOLS... [OPTIONS]
```

| Option | Description |
|--------|-------------|
| `--duration N` | Stop after N seconds (default: 10) |
| `--timeframe TF` | Bar interval (default: `1` = 1 minute) |
| `--alert-above PRICE` | Print alert when price exceeds threshold |
| `--alert-below PRICE` | Print alert when price falls below threshold |
| `--alert-change-pct N` | Print alert on N% move |

**Examples:**

```bash
# Stream BTC and ETH for 30 seconds
python scripts/lib/stream.py BTC ETH --duration 30

# Stream with price alert
python scripts/lib/stream.py BTC --duration 60 --alert-above 70000

# Stream with change alert
python scripts/lib/stream.py AAPL --duration 120 --alert-change-pct 1.0
```

At the end of a stream session, you get a summary with session high/low, VWAP, and update count.

### Search for Symbols

```bash
python scripts/lib/search.py "QUERY" [OPTIONS]
```

| Option | Description |
|--------|-------------|
| `--type TYPE` | Filter: `stock`, `crypto`, `forex`, `futures`, `index`, `bond`, `cfd` |
| `--exchange EX` | Filter by exchange: `BINANCE`, `NASDAQ`, `NYSE`, etc. |
| `--limit N` | Max results (default: 20) |

**Examples:**

```bash
python scripts/lib/search.py "bitcoin" --type crypto
python scripts/lib/search.py "apple" --exchange NASDAQ
python scripts/lib/search.py "oil futures" --type futures
python scripts/lib/search.py "EURUSD" --type forex
```

### Statistical Analysis

```bash
python scripts/lib/analyze.py SYMBOL [TIMEFRAME] [BARS]
```

Computes and displays:
- **Period return** and **annualized return**
- **Daily and annualized volatility**
- **Sharpe ratio** (risk-free rate = 0)
- **Maximum drawdown** (with peak and trough dates)
- **Period high/low** (with dates)
- **SMA 20 / 50 / 200** and position relative to price
- **RSI 14**
- **Trend direction** (uptrend / downtrend / sideways)
- **Plain-language interpretation**

**Examples:**

```bash
# Analyze Apple's last year
python scripts/lib/analyze.py AAPL 1D 252

# Analyze Bitcoin's last quarter
python scripts/lib/analyze.py BTC 1D 90

# Analyze EUR/USD hourly for 2 weeks
python scripts/lib/analyze.py EURUSD 60 336
```

### Compare Symbols

```bash
python scripts/lib/compare.py SYM1 SYM2 [SYM3...] --timeframe TF --bars N
```

Computes:
- **Period return** for each symbol
- **Annualized return and volatility**
- **Sharpe ratio** comparison
- **Max drawdown** comparison
- **Correlation matrix**
- **Beta** (each symbol vs. the first as benchmark)

**Examples:**

```bash
# Compare BTC and ETH over 90 days
python scripts/lib/compare.py BTC ETH --timeframe 1D --bars 90

# Compare tech stocks
python scripts/lib/compare.py AAPL MSFT GOOGL NVDA --timeframe 1D --bars 252

# Compare crypto vs gold
python scripts/lib/compare.py BTC GOLD --timeframe 1D --bars 365
```

### Technical Indicators

```bash
python scripts/lib/indicators.py SYMBOL [TIMEFRAME] [BARS] --indicators "SPEC"
```

**Indicator specification format:** `name:param,name:param,...`

| Indicator | Spec | Output columns |
|-----------|------|----------------|
| Simple Moving Average | `sma:20` | SMA_20 |
| Exponential Moving Average | `ema:12` | EMA_12 |
| Relative Strength Index | `rsi:14` | RSI_14 |
| MACD | `macd` or `macd:12:26:9` | MACD_LINE, MACD_SIGNAL, MACD_HIST |
| Bollinger Bands | `bb:20` or `bb:20:2` | BB_UPPER, BB_MID, BB_LOWER, BB_PCT_B |
| Average True Range | `atr:14` | ATR_14 |
| Stochastic | `stoch` or `stoch:14:3` | STOCH_K, STOCH_D |
| On-Balance Volume | `obv` | OBV |
| VWAP | `vwap` | VWAP |

**Examples:**

```bash
# Classic setup: SMA crossover + RSI + MACD
python scripts/lib/indicators.py BTC 1D 365 --indicators "sma:20,sma:50,sma:200,rsi:14,macd"

# Bollinger Bands + Stochastic
python scripts/lib/indicators.py AAPL 1D 100 --indicators "bb:20,stoch:14:3"

# Full analysis
python scripts/lib/indicators.py EURUSD 60 500 --indicators "sma:20,ema:12,rsi:14,macd,bb:20,atr:14,stoch,vwap"
```

Each indicator comes with a **signal interpretation** (BULLISH / BEARISH / NEUTRAL) based on standard thresholds.

---

## Symbol Aliases

Instead of typing `BINANCE:BTCUSDT`, just type `BTC`. Over 100 aliases are built in:

| Alias | Resolves to | Category |
|-------|-------------|----------|
| `BTC`, `Bitcoin` | BINANCE:BTCUSDT | Crypto |
| `ETH`, `Ethereum` | BINANCE:ETHUSDT | Crypto |
| `SOL`, `Solana` | BINANCE:SOLUSDT | Crypto |
| `DOGE` | BINANCE:DOGEUSDT | Crypto |
| `XRP` | BINANCE:XRPUSDT | Crypto |
| `AAPL`, `Apple` | NASDAQ:AAPL | Stocks |
| `MSFT`, `Microsoft` | NASDAQ:MSFT | Stocks |
| `TSLA`, `Tesla` | NASDAQ:TSLA | Stocks |
| `NVDA`, `Nvidia` | NASDAQ:NVDA | Stocks |
| `GOOGL`, `Google` | NASDAQ:GOOGL | Stocks |
| `META` | NASDAQ:META | Stocks |
| `SPX`, `S&P500` | SP:SPX | Indices |
| `SPY` | AMEX:SPY | Indices |
| `QQQ` | NASDAQ:QQQ | Indices |
| `VIX` | CBOE:VIX | Indices |
| `DJI`, `Dow` | DJ:DJI | Indices |
| `EURUSD`, `EUR/USD` | FX:EURUSD | Forex |
| `GBPUSD` | FX:GBPUSD | Forex |
| `USDJPY` | FX:USDJPY | Forex |
| `DXY`, `Dollar` | TVC:DXY | Forex |
| `GOLD`, `XAU` | TVC:GOLD | Commodities |
| `SILVER`, `XAG` | TVC:SILVER | Commodities |
| `OIL`, `WTI`, `Crude` | TVC:USOIL | Commodities |

Full list: see [scripts/lib/validators.py](scripts/lib/validators.py)

You can always use the full `EXCHANGE:TICKER` format for any symbol not in the alias list.

---

## Timeframes

| Code | Meaning | Alias |
|------|---------|-------|
| `1` | 1 minute | `1M` |
| `3` | 3 minutes | |
| `5` | 5 minutes | `5M` |
| `10` | 10 minutes | |
| `15` | 15 minutes | `15M` |
| `30` | 30 minutes | `30M` |
| `45` | 45 minutes | |
| `60` | 1 hour | `1H` |
| `120` | 2 hours | `2H` |
| `180` | 3 hours | `3H` |
| `240` | 4 hours | `4H` |
| `1D` | 1 day | `D` |
| `1W` | 1 week | `W` |
| `1M` | 1 month | `M` |

---

## Bar Limits

### Without authentication (anonymous, free)

| Timeframe | Max bars | Coverage |
|-----------|---------|----------|
| 1 min | ~6,500 | ~4 days |
| 5 min | ~5,300 | ~18 days |
| 15 min | ~5,200 | ~55 days |
| 1 hour | ~10,800 | ~15 months |
| 4 hour | ~7,100 | ~4 years |
| **Daily** | **Unlimited** | **Full history** |
| **Weekly** | **Unlimited** | **Full history** |
| **Monthly** | **Unlimited** | **Full history** |

### With paid TradingView plan

| Plan | Intraday bar limit |
|------|-------------------|
| Essential | 10,000 |
| Plus / Premium | 20,000 |
| Ultimate | 40,000 |
| Daily/Weekly/Monthly | Unlimited (all plans) |

Daily, weekly, and monthly data is **always unlimited** regardless of plan. You only need a paid plan for large amounts of intraday data.

---

## Authentication (Optional)

Authentication is **not required** for most use cases. Anonymous mode gives you:
- Full daily/weekly/monthly history for every symbol
- ~6,500 bars of 1-minute data (~4 days)
- ~10,800 bars of hourly data (~15 months)

If you need more intraday data, provide your TradingView auth token:

### Step 1: Get your token

1. Log in to [tradingview.com](https://www.tradingview.com)
2. Open DevTools (`F12`) -> **Console** tab
3. Run this command:
   ```javascript
   document.cookie.split('; ').find(c=>c.startsWith('auth_token=')).split('=').slice(1).join('=')
   ```
4. Copy the long JWT string

### Step 2: Save the token (pick one method)

```bash
# Method A: Environment variable (per session)
export TV_AUTH_TOKEN="eyJhbGciOiJSUzI1NiIs..."

# Method B: Save to config file (persistent)
python scripts/lib/auth_mgr.py set "eyJhbGciOiJSUzI1NiIs..."

# Method C: .env file (manual)
mkdir -p ~/.tvfetch
echo 'TV_AUTH_TOKEN=eyJhbGciOiJSUzI1NiIs...' > ~/.tvfetch/.env
```

### Step 3: Verify

```bash
python scripts/lib/auth_mgr.py test
```

### Step 4: Use it

```bash
# Now you can fetch more intraday data
python scripts/lib/fetch.py BTC 1 20000
```

For full instructions: `python scripts/lib/auth_mgr.py instructions`

---

## Configuration

tvfetch uses a hierarchical configuration system. Settings are resolved in this order (highest priority first):

1. **CLI flags** — `--token`, `--no-cache`, etc.
2. **Environment variables** — `TV_AUTH_TOKEN`, `TVFETCH_CACHE_PATH`, etc.
3. **Config file** — `~/.tvfetch/.env`
4. **System keyring** — `keyring.get_password("tvfetch", "auth_token")` (if `keyring` installed)
5. **Defaults** — anonymous token, `~/.tvfetch/cache.db`, etc.

### Environment variables

| Variable | Default | Description |
|----------|---------|-------------|
| `TV_AUTH_TOKEN` | anonymous | TradingView JWT token |
| `TVFETCH_CACHE_PATH` | `~/.tvfetch/cache.db` | SQLite cache location |
| `TVFETCH_TIMEOUT` | `120` | Fetch timeout in seconds |
| `TVFETCH_FALLBACK` | `true` | Enable Yahoo/CCXT fallback |
| `TVFETCH_MOCK` | `0` | Set to `1` for offline mock mode |
| `TVFETCH_PROXY` | (none) | HTTPS proxy URL |
| `TVFETCH_LOG_LEVEL` | `WARNING` | Logging level |

### Config file format (`~/.tvfetch/.env`)

```ini
TV_AUTH_TOKEN=eyJhbGciOiJSUzI1NiIs...
TVFETCH_CACHE_PATH=/custom/path/cache.db
TVFETCH_TIMEOUT=60
TVFETCH_FALLBACK=true
```

### View current config

```bash
python scripts/lib/config.py --show
```

---

## Caching

tvfetch caches fetched data locally in SQLite to avoid redundant network calls.

| Timeframe | Cache freshness |
|-----------|----------------|
| Intraday (1min - 4hr) | 15 minutes |
| Daily | 24 hours |
| Weekly / Monthly | 7 days |

```bash
# View cache contents
python scripts/lib/cache_mgr.py stats

# Clear cache for one symbol
python scripts/lib/cache_mgr.py clear --symbol BINANCE:BTCUSDT

# Clear all cache
python scripts/lib/cache_mgr.py clear --all

# Bypass cache for a single fetch
python scripts/lib/fetch.py BTC 1D 100 --no-cache
```

Cache location: `~/.tvfetch/cache.db` (configurable via `TVFETCH_CACHE_PATH`).

---

## Export Formats

### From CLI

```bash
# CSV (default for .csv extension)
python scripts/lib/fetch.py BTC 1D 365 --output btc.csv

# JSON
python scripts/lib/fetch.py BTC 1D 365 --output btc.json

# Parquet (requires: pip install tvfetch[parquet])
python scripts/lib/fetch.py BTC 1D 365 --output btc.parquet

# Freqtrade format
python scripts/lib/fetch.py BTC 1D 365 --output btc.json --format freqtrade
```

### From Python

```python
import tvfetch
from tvfetch import exporters

result = tvfetch.fetch("BINANCE:BTCUSDT", "1D", bars=365)

# Pandas DataFrame
df = result.df

# Built-in exports
result.to_csv("btc.csv")
result.to_json("btc.json")
result.to_parquet("btc.parquet")

# Backtesting framework exports
feed = exporters.to_backtrader(result)    # backtrader PandasData feed
candles = exporters.to_freqtrade(result)  # [[ts_ms, o, h, l, c, v], ...]
```

---

## Running Tests

```bash
# Run all tests (296 tests, ~6 seconds, no network needed)
python -m pytest tests/ -x -q

# Run with verbose output
python -m pytest tests/ -v

# Run a specific test file
python -m pytest tests/test_indicators.py -v

# Run tests with coverage
python -m pytest tests/ --cov=tvfetch --cov=scripts --cov-report=term-missing

# Run only the skill-layer tests (new modules)
python -m pytest tests/test_config.py tests/test_validators.py tests/test_indicators.py tests/test_formatter.py tests/test_mock.py tests/test_errors.py -v
```

**All tests run offline** — the `no_real_network` fixture blocks all real socket connections. WebSocket interactions are mocked.

### Test offline with mock mode

```bash
# Every script supports --mock to use fixture data
python scripts/lib/fetch.py BTC 1D 50 --mock
python scripts/lib/search.py bitcoin --type crypto --mock
python scripts/lib/stream.py BTC --duration 3 --mock
```

Mock fixtures are in the [fixtures/](fixtures/) directory.

---

## Project Structure

```
tvfetch-skill/
├── SKILL.md                    # Claude Code skill manifest
├── pyproject.toml              # Package configuration
├── README.md                   # This file
├── SPEC.md                     # Technical specification
├── CLAUDE.md                   # Developer notes
├── CHANGELOG.md                # Version history
├── LICENSE                     # MIT
│
├── tvfetch/                    # Core Python library
│   ├── __init__.py             # Public API (fetch, stream, search)
│   ├── auth.py                 # Authentication (anonymous + JWT)
│   ├── cache.py                # SQLite caching
│   ├── exceptions.py           # Exception hierarchy
│   ├── exporters.py            # CSV, JSON, Parquet, backtrader, freqtrade
│   ├── fallback.py             # Yahoo Finance + CCXT fallback
│   ├── historical.py           # Historical OHLCV fetching
│   ├── live.py                 # Live price streaming
│   ├── models.py               # Bar, FetchResult, SymbolInfo
│   ├── retry.py                # Exponential backoff decorator
│   ├── symbols.py              # Symbol search API
│   └── core/
│       ├── connection.py       # WebSocket connection manager
│       ├── messages.py         # TradingView message builders
│       └── protocol.py         # ~m~ framing protocol
│
├── scripts/                    # Skill-layer scripts
│   ├── main.py                 # Unified CLI entry point
│   └── lib/
│       ├── config.py           # Hierarchical config resolver
│       ├── validators.py       # Symbol aliases, timeframe validation
│       ├── errors.py           # Exit codes + tagged error output
│       ├── formatter.py        # Tagged output for Claude parsing
│       ├── mock.py             # Fixture-based mock mode
│       ├── progress.py         # Progress tracking
│       ├── fetch.py            # Historical fetch (with quality checks)
│       ├── fetch_multi.py      # Multi-symbol fetch
│       ├── stream.py           # Live streaming (with alerts)
│       ├── search.py           # Symbol search
│       ├── analyze.py          # Statistical analysis
│       ├── compare.py          # Multi-symbol comparison
│       ├── indicators.py       # Technical indicators
│       ├── cache_mgr.py        # Cache management
│       └── auth_mgr.py         # Auth token management
│
├── tests/                      # 296 tests (all run offline)
├── fixtures/                   # Mock data for --mock mode
├── examples/                   # Example scripts
├── hooks/                      # Claude Code session hooks
├── variants/                   # Alternative SKILL.md versions
│   ├── quant/SKILL.md          # Quant-focused (always analyzes)
│   ├── minimal/SKILL.md        # Data-only (no analysis)
│   └── backtesting/SKILL.md    # Framework-aware export
├── .claude-plugin/             # Claude Code plugin metadata
├── agents/                     # Agent definitions
└── gemini-extension.json       # Gemini CLI integration
```

---

## Claude Code Skill

tvfetch works as a [Claude Code](https://claude.ai/code) skill — you can talk to it in natural language.

### Install the skill

```bash
# Copy to Claude Code skills directory
cp -r . ~/.claude/skills/tvfetch/
```

### Use it

In any Claude Code session:

```
/tvfetch BTC daily 1 year
/tvfetch get me 3 months of Apple hourly data
/tvfetch stream ETH and SOL for 30 seconds
/tvfetch compare Bitcoin vs Gold this quarter
/tvfetch what's the RSI on EURUSD?
/tvfetch search oil futures on NYMEX
/tvfetch analyze Tesla performance this year
```

Claude understands natural language and runs the right commands. It also:
- Resolves symbol aliases automatically
- Converts time periods ("3 months" -> 90 daily bars)
- Warns about bar limits for intraday data
- Interprets analysis results in plain English
- Suggests follow-up actions
- Recovers from errors automatically (bad symbol -> runs search, no data -> tries higher timeframe)

### Variants

Three alternative SKILL.md implementations for different use cases:

| Variant | Path | Focus |
|---------|------|-------|
| **Default** | `SKILL.md` | Full-featured with follow-ups |
| **Quant** | `variants/quant/SKILL.md` | Always runs analysis + indicators |
| **Minimal** | `variants/minimal/SKILL.md` | Pure data, no analysis |
| **Backtesting** | `variants/backtesting/SKILL.md` | Framework-aware exports |

To use a variant, copy it over the main SKILL.md:
```bash
cp variants/quant/SKILL.md SKILL.md
```

---

## Troubleshooting

### "Could not connect to TradingView within 15s"

- Check your internet connection
- TradingView might be temporarily down
- Try with `--fallback-only` to use Yahoo Finance instead
- If behind a corporate firewall, set `TVFETCH_PROXY`

### "Symbol not found: XXXX"

- Use `python scripts/lib/search.py "your symbol"` to find the correct format
- Make sure to use `EXCHANGE:TICKER` format (e.g., `BINANCE:BTCUSDT` not just `BTCUSDT`)
- Check the [symbol aliases](#symbol-aliases) table

### "No data available for timeframe"

- Not all symbols have data for all timeframes
- Try a larger timeframe (e.g., switch from `1` to `60` or `1D`)
- Some newly listed symbols may only have recent data

### "Rate limited by TradingView"

- Wait 60 seconds and try again
- Avoid making rapid sequential requests
- Consider using `fetch_multi()` for multiple symbols

### Tests fail with "Real network call blocked"

- This means a test is trying to make a real network call
- All tests should use mocked WebSocket via `conftest.py` fixtures
- Check that `monkeypatch` is being used correctly

### Mock mode returns empty data

- Check that fixture files exist in `fixtures/`
- Fixture naming: `fetch_{exchange}_{ticker}_{timeframe}_{bars}bars.json`
- Use `fetch_default.json` as a fallback

---

## Disclaimer

This tool reverse-engineers TradingView's internal WebSocket protocol to provide free market data. It is for **educational and personal use only**.

Using this tool may violate TradingView's Terms of Service. Users are responsible for compliance with applicable terms and conditions.

The authors are not responsible for any consequences of using this tool.

---

## License

MIT License. See [LICENSE](LICENSE) for details.
