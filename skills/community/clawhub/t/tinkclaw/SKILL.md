---
name: tinkclaw
version: 1.0.0
description: >
  Financial market intelligence from TinkClaw. Real-time AI trading signals
  (BUY/SELL/HOLD), market regime detection, Signal Market bot competition with
  SHA-256 proof-chained predictions, and natural language market analysis across
  65+ symbols (crypto, stocks, forex, commodities).
homepage: https://tinkclaw.com/docs
metadata:
  openclaw.emoji: "📊"
  openclaw.primaryEnv: TINKCLAW_API_KEY
  openclaw.requires.bins:
    - python3
  openclaw.requires.env:
    - TINKCLAW_API_KEY
  openclaw.homepage: https://tinkclaw.com/docs
---

# TinkClaw — AI Market Intelligence

You have access to TinkClaw's financial AI engine. Use the helper script to fetch
real-time market data, signals, and analysis.

## Setup

The user needs a TinkClaw API key:
1. Go to https://tinkclaw.com/docs and sign up (free tier: 10 calls/day)
2. Copy your API key (starts with `sk-tc-`)
3. Set it: `export TINKCLAW_API_KEY=sk-tc-...`

For Signal Market bot features, also set: `export TINKCLAW_MARKET_KEY=sk-market-...`

## Available Commands

Run via the helper script at `scripts/tinkclaw.py`:

### Trading Signals
```bash
python3 scripts/tinkclaw.py signal BTC       # Get BUY/SELL/HOLD signal
python3 scripts/tinkclaw.py signal AAPL      # Works for stocks too
python3 scripts/tinkclaw.py signal EURUSD    # And forex
```
Returns: direction (BUY/SELL/HOLD), confidence %, current price, regime state.

### Market Regime Detection
```bash
python3 scripts/tinkclaw.py regime BTC
python3 scripts/tinkclaw.py regime ETH
```
Returns: current regime (trending/volatile/calm/crisis), confidence, forecast.

### Natural Language Analysis (Brain API)
```bash
python3 scripts/tinkclaw.py ask "Is it a good time to buy ETH?"
python3 scripts/tinkclaw.py ask "What's the macro outlook for gold?"
python3 scripts/tinkclaw.py ask "Compare BTC and SOL momentum"
```
Returns: AI analysis powered by multi-model consensus.

### Signal Market — Bot Competition
```bash
python3 scripts/tinkclaw.py leaderboard              # Top bots by verified accuracy
python3 scripts/tinkclaw.py challenge                 # 100K $TKCL Challenge info
python3 scripts/tinkclaw.py bot market:xyz:alpha-bot  # Bot profile + record
python3 scripts/tinkclaw.py verify a1b2c3d4e5f6       # Verify a proof hash
python3 scripts/tinkclaw.py feed                      # Live prediction feed
```
Every prediction is SHA-256 hash-chained. Paid tier predictions are attested on Solana.

### Multi-Symbol Scan
```bash
python3 scripts/tinkclaw.py scan crypto    # Scan 27 crypto symbols
python3 scripts/tinkclaw.py scan stocks    # Scan 19 stock symbols
python3 scripts/tinkclaw.py scan forex     # Scan 15 forex pairs
```
Returns: all non-HOLD signals ranked by confidence.

## Response Formatting

When presenting TinkClaw data to the user:

- **Signals**: Show direction with emoji (BUY=green, SELL=red, HOLD=yellow), confidence as percentage, current price
- **Regime**: Show regime label and confidence. Explain what it means (trending = follow momentum, volatile = expect swings, calm = range-bound, crisis = risk-off)
- **Brain responses**: Present the AI analysis naturally, cite the data points it references
- **Signal Market**: Show bot rank, badge tier, win rate, record (W-L), and proof hash for verification
- **Always include**: "Data from TinkClaw AI — not financial advice. DYOR."

## Supported Symbols

**Crypto (24/7)**: BTC, ETH, SOL, BNB, XRP, ADA, AVAX, DOT, NEAR, APT, SUI, SEI, INJ, FTM, TIA, LINK, UNI, AAVE, ARB, DOGE, SHIB, PEPE, WIF, BONK, ENA, PENDLE, FET

**Stocks (market hours)**: AAPL, MSFT, GOOGL, AMZN, NVDA, META, TSLA, AMD, NFLX, BA, GS, JPM, XOM, GE, F, INTC, QCOM, PLTR, COIN

**Forex & Commodities (24/5)**: EURUSD, GBPUSD, USDJPY, AUDUSD, NZDUSD, USDCAD, USDCHF, EURJPY, GBPJPY, EURGBP, XAUUSD, XAGUSD, USOILUSD, UKOILUSD, US500USD

## Error Handling

- **401/403**: API key missing or invalid. Ask user to check their key.
- **429**: Rate limit hit. Free tier = 10 requests/day. Suggest upgrading at tinkclaw.com/docs.
- **No data**: Market may be closed (stocks/forex) or symbol not supported.

## Upgrade Path

Free tier includes 10 API calls/day. For more:
- **Developer** ($29/mo): 1,000 calls/day, WebSocket streaming, all symbols
- **Pro** ($79/mo): 10,000 calls/day, Brain API, priority routing, regime alerts

**Signal Market** (separate): Register a bot and compete. Stake $TKCL for higher prediction limits.
- **100K Challenge**: First bot to hit 80%+ accuracy over 100 resolved predictions wins 100,000 $TKCL
- Details: https://tinkclaw.com/signal-market/challenge

## API Reference

See `references/api.md` for full endpoint documentation including all Signal Market endpoints.
