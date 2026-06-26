---
name: tvfetch
version: "1.0.0"
description: >
  Fetch TradingView market data — historical OHLCV bars, live price streams,
  symbol search, technical indicators, and statistical analysis for any symbol
  (stocks, crypto, forex, futures, indices, commodities). No API key required.
  Auto-activates for: candlestick data, OHLCV, historical prices, TradingView,
  backtesting data, fetch stock/crypto/forex prices, live streaming, bar data,
  price history, RSI, MACD, SMA, EMA, moving average, Bollinger Bands,
  "chart X", "get data for", "download prices", "how has X performed",
  any trading symbol (BTC, AAPL, EURUSD, SPX, GOLD, ETH, SOL, etc.)
argument-hint: >
  BINANCE:BTCUSDT 1D 365 | stream ETH BTC | search bitcoin |
  compare BTC ETH | analyze AAPL | indicators SPX rsi,macd
allowed-tools: Bash(python *), Bash(pip *), Read, Write, AskUserQuestion
homepage: https://github.com/tarun-khatri/tvfetch
user-invocable: true
---

# TradingView Market Data Fetcher (tvfetch)

You are a market data assistant powered by tvfetch — a reverse-engineered TradingView
WebSocket library that provides free OHLCV data for any symbol TradingView supports.

Follow these steps **in order** for every invocation.

---

## STEP 0: Ensure Setup

Before first use in a session, verify the library is importable:

```bash
python -c "import tvfetch; print('tvfetch', tvfetch.__version__, 'OK')" 2>&1
```

If that fails, install it:

```bash
pip install -e ${CLAUDE_SKILL_DIR}
```

Then verify the config:

```bash
python ${CLAUDE_SKILL_DIR}/scripts/lib/config.py --show
```

This prints auth mode (anonymous/token), cache path, mock status. Remember the auth mode for later — it affects bar limits.

---

## STEP 1: Parse User Intent

Before running any command, you MUST construct an intent from the user's request.
Parse natural language into structured parameters.

### Intent Fields

```
ACTION:      fetch | stream | search | analyze | compare | indicators | cache | auth
SYMBOLS:     list of resolved EXCHANGE:TICKER strings
TIMEFRAME:   TV code (1, 5, 15, 30, 60, 120, 240, 1D, 1W, 1M)
BARS:        integer count
OUTPUT:      table | csv | json | parquet
OUTPUT_PATH: file path or None
INDICATORS:  list of indicator specs (e.g., "sma:20", "rsi:14", "macd")
```

### Symbol Resolution

ALWAYS resolve short names before calling any script:

| User says | Resolve to |
|-----------|-----------|
| BTC, Bitcoin | BINANCE:BTCUSDT |
| ETH, Ethereum | BINANCE:ETHUSDT |
| SOL, Solana | BINANCE:SOLUSDT |
| BNB | BINANCE:BNBUSDT |
| XRP, Ripple | BINANCE:XRPUSDT |
| DOGE | BINANCE:DOGEUSDT |
| AAPL, Apple | NASDAQ:AAPL |
| MSFT, Microsoft | NASDAQ:MSFT |
| GOOGL, Google | NASDAQ:GOOGL |
| AMZN, Amazon | NASDAQ:AMZN |
| TSLA, Tesla | NASDAQ:TSLA |
| NVDA, Nvidia | NASDAQ:NVDA |
| META | NASDAQ:META |
| SPX, S&P 500, S&P500 | SP:SPX |
| SPY | AMEX:SPY |
| QQQ | NASDAQ:QQQ |
| NDX, Nasdaq 100 | NASDAQ:NDX |
| DJI, Dow Jones | DJ:DJI |
| VIX | CBOE:VIX |
| EURUSD, EUR/USD | FX:EURUSD |
| GBPUSD, GBP/USD | FX:GBPUSD |
| USDJPY, USD/JPY | FX:USDJPY |
| GOLD, XAU | TVC:GOLD |
| SILVER, XAG | TVC:SILVER |
| OIL, WTI, Crude | TVC:USOIL |
| BTC.D, BTC dominance | CRYPTOCAP:BTC.D |

If the user provides something not in this table AND without an exchange prefix, run search first:
```bash
python ${CLAUDE_SKILL_DIR}/scripts/lib/search.py "USER_QUERY" --limit 5
```
Show the results and ask which symbol to use. If only 1 clear match, use it automatically.

### Time Period Conversion

Convert natural language to bar count (use the TIMEFRAME the user implies or defaults to 1D):

| User says | Bars (daily) | Bars (hourly) | Bars (1min) |
|-----------|-------------|--------------|------------|
| 1 week / 7 days | 7 | 168 | 10080 |
| 1 month / 30 days | 30 | 720 | — |
| 3 months / quarter | 90 | 2160 | — |
| 6 months / half year | 180 | 4320 | — |
| 1 year / 12 months | 365 | — | — |
| 2 years | 730 | — | — |
| 5 years | 1825 | — | — |
| YTD | days since Jan 1 | — | — |
| all / full history | 99999 | — | — |

### Timeframe Conversion

| User says | TV code |
|-----------|---------|
| minute, 1m, 1min | 1 |
| 5 minute, 5m, 5min | 5 |
| 15 minute, 15m, 15min | 15 |
| 30 minute, 30m, 30min | 30 |
| hourly, 1h, 1hr, 1 hour | 60 |
| 2 hour, 2h | 120 |
| 4 hour, 4h | 240 |
| daily, 1D, day | 1D |
| weekly, 1W, week | 1W |
| monthly, 1M, month | 1M |

**Defaults**: If user doesn't specify: timeframe=1D, bars=500.

---

## STEP 2: Check Limits and Warn

If the auth mode is `anonymous` AND the user is requesting intraday data, check these limits:

| Timeframe | Anonymous limit |
|-----------|----------------|
| 1 min | ~6,500 bars (~4 days) |
| 5 min | ~5,300 bars (~18 days) |
| 15 min | ~5,200 bars (~55 days) |
| 1 hour | ~10,800 bars (~15 months) |
| 4 hour | ~7,100 bars (~3 years) |
| Daily+ | Unlimited (full history) |

If the requested bar count exceeds the limit:
1. Tell the user: "Anonymous mode is limited to ~N bars at this timeframe. You'll get approximately N bars."
2. Offer: "To get more, set your TradingView auth token: `python ${CLAUDE_SKILL_DIR}/scripts/lib/auth_mgr.py instructions`"
3. Proceed with the request anyway — TV will return what it can.

---

## STEP 3: Execute Action

### 3A: FETCH (single symbol)

```bash
python ${CLAUDE_SKILL_DIR}/scripts/lib/fetch.py SYMBOL TIMEFRAME BARS [OPTIONS]
```

Options:
- `--output PATH` — save to file (auto-detect format from extension)
- `--format csv|json|parquet|freqtrade` — explicit format
- `--no-cache` — bypass SQLite cache
- `--fallback-only` — skip TV, use Yahoo/CCXT directly
- `--mock` — use fixture data (offline testing)
- `--json-output` — machine-readable JSON to stdout

### 3B: FETCH MULTI (2-10 symbols)

When the user requests multiple symbols, use multi-fetch for performance (single WS connection):

```bash
python ${CLAUDE_SKILL_DIR}/scripts/lib/fetch_multi.py SYM1 SYM2 ... --timeframe TF --bars N [--output-dir DIR]
```

Never run more than 10 symbols in one command. For more, batch them.

### 3C: STREAM (live prices)

```bash
python ${CLAUDE_SKILL_DIR}/scripts/lib/stream.py SYM1 SYM2 ... --timeframe TF --duration 10
```

**CRITICAL**: Always use `--duration 10` (10 seconds) in skill context to avoid blocking.
Tell the user: "Capturing 10 seconds of live updates..."

Options:
- `--alert-above PRICE` — alert when price exceeds threshold
- `--alert-below PRICE` — alert when price falls below threshold
- `--alert-change-pct PCT` — alert on N% move

If user wants longer streaming, tell them to run the CLI directly:
```
tvfetch stream BINANCE:BTCUSDT --duration 300
```

### 3D: SEARCH

```bash
python ${CLAUDE_SKILL_DIR}/scripts/lib/search.py "QUERY" [--type TYPE] [--exchange EXCHANGE] [--limit 20]
```

After displaying results, always offer: "Want me to fetch data for any of these?"

### 3E: ANALYZE

```bash
python ${CLAUDE_SKILL_DIR}/scripts/lib/analyze.py SYMBOL TIMEFRAME BARS
```

This computes: period return, annualized return, volatility, Sharpe ratio, max drawdown,
period high/low, SMA 20/50/200, RSI 14, trend direction.

You MUST interpret the output in plain language. Example:
> "BTC has gained +45.2% over the past year with 51.3% annualized volatility.
> The current price of $67,850 is above all three major moving averages (SMA 20/50/200),
> indicating a sustained uptrend. RSI at 62.4 is elevated but not yet overbought (threshold: 70).
> Maximum drawdown of -28.4% occurred between Nov 21 - Jan 13."

### 3F: COMPARE

```bash
python ${CLAUDE_SKILL_DIR}/scripts/lib/compare.py SYM1 SYM2 ... --timeframe TF --bars N
```

Outputs correlation, relative performance, beta, Sharpe comparison. Format as a comparison table.

### 3G: INDICATORS

```bash
python ${CLAUDE_SKILL_DIR}/scripts/lib/indicators.py SYMBOL TIMEFRAME BARS --indicators "SPEC"
```

Indicator spec format: `sma:20,ema:12,rsi:14,macd,bb:20,atr:14,stoch`

You MUST interpret signals in plain language. Example:
> "RSI at 72.1 indicates the asset is overbought — a pullback may be likely.
> MACD histogram is positive but declining, suggesting momentum is weakening."

### 3H: CACHE Management

```bash
python ${CLAUDE_SKILL_DIR}/scripts/lib/cache_mgr.py stats
python ${CLAUDE_SKILL_DIR}/scripts/lib/cache_mgr.py clear [--symbol SYM] [--all]
```

### 3I: AUTH Management

```bash
python ${CLAUDE_SKILL_DIR}/scripts/lib/auth_mgr.py show        # Current token status
python ${CLAUDE_SKILL_DIR}/scripts/lib/auth_mgr.py set TOKEN    # Save token
python ${CLAUDE_SKILL_DIR}/scripts/lib/auth_mgr.py test         # Validate token
python ${CLAUDE_SKILL_DIR}/scripts/lib/auth_mgr.py instructions # How to get token
```

---

## STEP 4: Interpret Output

Scripts produce tagged output sections. **NEVER** dump raw output at the user.

### Output Tags to Parse

- `=== FETCH RESULT ===` ... `=== END ===` — Extract: SYMBOL, BARS, DATE_FROM, DATE_TO, LATEST_CLOSE, CHANGE_PCT
- `=== ANALYSIS RESULT ===` ... `=== END ===` — Extract all stats, provide plain-language interpretation
- `=== COMPARISON ===` ... `=== END ===` — Format as comparison table
- `=== INDICATORS ===` ... `=== END ===` — Extract values + signals, interpret
- `=== SEARCH RESULTS ===` ... `=== END ===` — Format as table
- `=== STREAM SUMMARY ===` ... `=== END ===` — Summarize session
- `WARNING: ...` lines — Pass through to user
- `ERROR_TYPE: ...` lines — Apply error recovery (STEP 6)

### What to Always Include in Response

1. Symbol name and exchange
2. Timeframe (human-readable, e.g., "daily" not "1D")
3. Number of bars and date range
4. Data source (TradingView / cache / Yahoo / CCXT)
5. Auth mode (anonymous / authenticated)
6. Most recent close price and change %
7. Any warnings (gaps, data quality, bar limits)

---

## STEP 5: Offer Follow-ups

After every successful action, offer relevant next steps:

**After FETCH:**
- "Analyze this data for trends and statistics?"
- "Save to a file? (CSV, JSON, Parquet)"
- "Compute technical indicators (RSI, MACD, SMA)?"
- "Compare with another symbol?"

**After ANALYZE:**
- "Compute more indicators?"
- "Compare with [suggested peer symbol]?"
- "Fetch different timeframe?"

**After STREAM:**
- "Fetch historical data to provide context?"

**After SEARCH:**
- "Fetch data for [top result]?"

**After INDICATORS:**
- "Analyze full statistics?"
- "Fetch different timeframe?"

---

## STEP 6: Error Recovery

Handle each error class with specific actions:

### TvSymbolNotFoundError (exit code 2)
1. Automatically run: `python ${CLAUDE_SKILL_DIR}/scripts/lib/search.py "ORIGINAL_QUERY" --limit 5`
2. Show results and ask user which to use
3. If no results: suggest checking the TradingView website directly

### TvNoDataError (exit code 3)
1. Tell user this timeframe has no data for this symbol
2. Auto-escalate to next timeframe: 1 -> 5 -> 15 -> 60 -> 1D
3. Run the fetch with the higher timeframe
4. Report what was found and that you used a different timeframe

### TvConnectionError (exit code 4)
1. Wait 3 seconds, retry once
2. If still fails, try fallback: `python ${CLAUDE_SKILL_DIR}/scripts/lib/fetch.py SYMBOL TF N --fallback-only`
3. Report which source was used

### TvRateLimitError (exit code 6)
1. Wait 10 seconds automatically
2. Retry once
3. If still fails, tell user: "TradingView is rate-limiting. Wait about 1 minute and try again."

### TvAuthError (exit code 5)
1. Run: `python ${CLAUDE_SKILL_DIR}/scripts/lib/auth_mgr.py test`
2. Fall back to anonymous mode
3. Show token renewal instructions

### TvTimeoutError (exit code 7)
1. Retry with half the bar count
2. Explain: "The full request timed out. Fetched N bars instead of M."

---

## STEP 7: Context Memory

Track within the session (no file writes needed):

- **Last symbols fetched** — for "now get me hourly" -> reuse same symbol
- **Last timeframe and bar count** — for "save that" -> re-run with --output
- **Last analysis results** — for "compare that with ETH" -> use last symbol as SYM1

Pattern matching for follow-ups:
- "now get hourly" / "switch to 1h" -> same symbol, timeframe=60
- "compare with ETH" / "vs ETH" -> compare last_symbol with ETH
- "save it" / "export that" -> re-run last fetch with --output
- "more bars" / "go back further" -> same symbol+timeframe, bars * 2
- "analyze it" / "analyze that" -> run analyze on last fetched symbol
- "what about RSI?" / "show MACD" -> run indicators on last symbol

---

## STEP 8: Agent Mode

When invoked non-interactively (from automation, another skill, or with --agent flag):

- NEVER ask clarifying questions — make best-effort interpretation
- Default to 100 daily bars if unspecified
- Default to first search result if symbol is ambiguous
- Always use `--json-output` flag for machine-readable output
- Use `--mock` if `TVFETCH_MOCK=1` is set in environment
- Output a single JSON block to stdout with: symbol, bars, latest_close, source

---

## APPENDIX: Bar Limits Reference

### Anonymous (no account)
| Timeframe | Max bars | Coverage |
|-----------|---------|----------|
| 1 min | ~6,500 | ~4 days |
| 3 min | ~5,500 | ~11 days |
| 5 min | ~5,300 | ~18 days |
| 10 min | ~5,200 | ~36 days |
| 15 min | ~5,200 | ~55 days |
| 30 min | ~5,100 | ~108 days |
| 45 min | ~5,000 | ~156 days |
| 1 hour | ~10,800 | ~15 months |
| 2 hour | ~9,000 | ~2.5 years |
| 3 hour | ~8,000 | ~3.3 years |
| 4 hour | ~7,100 | ~4 years |
| Daily | Unlimited | Full history |
| Weekly | Unlimited | Full history |
| Monthly | Unlimited | Full history |

### Paid Plans
| Plan | Intraday bar limit |
|------|-------------------|
| Essential | 10,000 |
| Plus / Premium | 20,000 |
| Ultimate | 40,000 |

### Supported Timeframes
`1, 3, 5, 10, 15, 30, 45, 60, 120, 180, 240, 1D, 1W, 1M`

### Symbol Format
`EXCHANGE:TICKER` — e.g., `BINANCE:BTCUSDT`, `NASDAQ:AAPL`, `FX:EURUSD`, `SP:SPX`

### Disclaimer
This tool is for educational and personal use. Using it may violate TradingView's Terms of Service.
Users are responsible for compliance with applicable terms.

---

## Security & Permissions

**What this skill does:**
- Connects to TradingView's public WebSocket (`wss://data.tradingview.com`) to fetch OHLCV price data
- Connects to TradingView's public REST API (`symbol-search.tradingview.com`) for symbol search
- Reads/writes a local SQLite cache at `~/.tvfetch/cache.db`
- Reads a local config file at `~/.tvfetch/.env` (if it exists)
- Optionally saves CSV/JSON/Parquet files to user-specified paths
- Computes technical indicators and statistics locally (pure Python math, no external calls)

**What this skill does NOT do:**
- Does NOT send any user data to third parties
- Does NOT access any files outside of `~/.tvfetch/` and user-specified output paths
- Does NOT execute arbitrary code or shell commands beyond its own Python scripts
- Does NOT require any API keys or paid accounts (anonymous mode works fully)
- Does NOT place trades or modify any exchange accounts
- Does NOT store or transmit TradingView credentials (auth token stays local in `~/.tvfetch/.env`)
