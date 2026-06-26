---
name: ripe-scanner
description: Free stock and crypto momentum scanner with social sentiment analysis. Scans S&P 500, Nasdaq 100, and crypto for momentum signals using RSI, EMA, Bollinger Squeeze, volume, and social sentiment from StockTwits and Reddit. Use when asked about momentum, hot stocks, ripe signals, social sentiment, market scanning, or stock screening.
---

# Ripe Scanner — Free Momentum + Social Sentiment Scanner

Zero-cost, fully local momentum scanner covering 600+ stocks and 15 crypto assets.
Combines technical scoring (RSI, EMA, Bollinger Squeeze, volume) with social sentiment
(StockTwits + Reddit WSB). Tracks signal history for win rate verification.

No API keys required. No rate limits. Runs entirely on your machine.

## Requirements

```bash
pip install yfinance pandas numpy
```

## Commands

All scripts: `~/.openclaw/workspace/skills/ripe-scanner/scripts/`

### Scan Top Signals
```bash
python3 scripts/ripe-scan.py top [--limit 10] [--min-score 70] [--sentiment] [--no-crypto]
```
Ranked table of highest-scoring momentum signals across the full universe.

### Individual Lookup
```bash
python3 scripts/ripe-scan.py lookup TSLA NVDA BTC-USD
```
Full profile per ticker: score, technicals, sentiment breakdown, key drivers.

### Social Sentiment Only
```bash
python3 scripts/ripe-scan.py sentiment TSLA AAPL
```
StockTwits bull/bear ratio + Reddit WSB mention frequency and sentiment.

### Market Pulse
```bash
python3 scripts/ripe-scan.py pulse [--sentiment]
```
Bird's-eye market overview: badge distribution, top ripe signals, overbought warnings, biggest movers.

### Score Changes (vs Previous Day)
```bash
python3 scripts/ripe-scan.py changes
```
Detects newly ripe signals, big upgrades/downgrades, and score jumps vs the last snapshot.

### Save Daily Snapshot
```bash
python3 scripts/ripe-scan.py snapshot [--sentiment]
```
Saves today's scores to disk. Run daily (e.g., via cron) to build history for win rate tracking.

### Signal History & Win Rate
```bash
python3 scripts/ripe-scan.py history
```
Shows cumulative win rate for past "ripe" signals (1-day and 5-day returns).

## Scoring System (0–100)

| Component | Weight | Source |
|-----------|--------|--------|
| RSI (14) trend zone | 20% | yfinance |
| EMA 20/50 alignment | 20% | yfinance |
| Bollinger Squeeze | 15% | yfinance |
| Volume surge vs 20d avg | 15% | yfinance |
| 52-week high proximity | 10% | yfinance |
| Social sentiment | 20% | StockTwits + Reddit |

## Badges

| Badge | Score | Meaning |
|-------|-------|---------|
| 🍌 **Ripe** | 80–100 | Strong momentum + positive sentiment |
| 🟡 **Ripening** | 60–79 | Building momentum, watchlist candidate |
| 🟠 **Overripe** | 80–100 (RSI>75) | Overbought — caution |
| ⚪ **Neutral** | 40–59 | No clear signal |
| 🔴 **Rotten** | 0–39 | Weak momentum + negative sentiment |

## Coverage

- **Stocks**: S&P 500 + Nasdaq 100 + popular watchlist names (~600)
- **Crypto**: BTC, ETH, SOL, BNB, XRP, ADA, DOGE, AVAX, DOT, MATIC, LINK, UNI, ATOM, LTC, NEAR
- Easily extensible — add tickers to `WATCHLIST_EXTRA` or `CRYPTO_TICKERS` in the script

## Data Sources (All Free)

| Source | Data | Rate Limit |
|--------|------|------------|
| **yfinance** | Price, volume, technicals | ~2000 req/hr (batched) |
| **StockTwits API** | Bull/bear sentiment | No key needed, ~200 req/hr |
| **Reddit JSON** | WSB mentions + upvotes | No key needed, ~60 req/min |

## Performance

- Full scan (~600 tickers): **3–5 minutes** (with sentiment for top 50)
- Individual lookup: **~5 seconds** per ticker
- Results cached for 30 minutes at `/tmp/ripe_scanner_cache.json`

## History & Snapshots

Daily snapshots stored in `~/.openclaw/workspace/memory/ripe_scanner/snapshots/`.
Signal log at `~/.openclaw/workspace/memory/ripe_scanner/signals_log.json`.

Run `snapshot` daily to:
1. Save all scores to disk
2. Log "ripe" signals with entry prices
3. Enable `changes` command (vs previous day comparison)
4. Build win rate history over time

## Example Output

```
🏆 TOP 5 MOMENTUM SIGNALS
Symbol     Score Badge               Price       1d       5d   RSI  Sent
------------------------------------------------------------------------
 $MU          94 🍌 ripe         $  426.13   +5.1%   +9.4%    51   100
          ↳ Price above EMA20 & EMA50, Bollinger Squeeze, RSI 51 healthy
 $XOM         91 🍌 ripe         $  156.12   +1.7%   +3.8%    61   100
          ↳ Uptrend confirmed, Squeeze detected, Near 52-week high
₿$BTC-USD    78 🟡 ripening     $67432.10   +2.3%   -1.2%    55    72
          ↳ RSI 55 healthy momentum, Strong bullish social sentiment
```

## Tips

- Use `--sentiment` flag on `top` and `pulse` for more accurate scores (adds ~2 min)
- Without `--sentiment`, social score defaults to 50 (neutral) — technicals only
- Use `--no-crypto` to exclude crypto assets from scans
- Schedule `python3 ripe-scan.py snapshot --sentiment` via cron for daily tracking
- Compare with `changes` to catch breakout transitions early

## License

MIT — free for personal and commercial use.
