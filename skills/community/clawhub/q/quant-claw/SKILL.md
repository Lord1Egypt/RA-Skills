---
name: quantclaw
description: "LLM-driven crypto perpetual futures trading on Bybit. Analyzes 200+ market features across 8 timeframes with strategy-aware output, then you decide whether to trade. Supports DEMO and LIVE modes."
homepage: "https://anomalysystems.gumroad.com/l/wugjom"
license: "Proprietary — purchase required for full access"
metadata:
  openclaw:
    emoji: "📈"
    requires:
      bins: ["uv", "quantclaw"]
      env: ["BYBIT_API_KEY", "BYBIT_API_SECRET"]
    primaryEnv: "BYBIT_API_KEY"
    os: ["darwin", "linux"]
    install:
      - id: uv-brew
        kind: brew
        formula: uv
        bins: ["uv"]
        label: "Install uv via Homebrew (recommended)"
      - id: uv-pip
        kind: shell
        command: "pip install uv"
        label: "Install uv via pip (alternative)"
      - id: quantclaw-purchase
        kind: manual
        label: "Purchase QuantClaw ($97) — download includes the quantclaw CLI and a SHA256 checksum for verification"
        url: "https://anomalysystems.gumroad.com/l/wugjom"
    envDocs:
      BYBIT_API_KEY: "Bybit API key — use demo/testnet keys unless trading live"
      BYBIT_API_SECRET: "Bybit API secret — use demo/testnet keys unless trading live"
    safetyNote: "DEMO mode is the default. Switching to LIVE requires an explicit interactive confirmation typed by the user — this cannot be satisfied by environment variables, flags, or autonomous agent decisions. Never supply live keys with withdrawal permissions."
---

# QuantClaw — Crypto Perpetual Futures Analysis

QuantClaw is an LLM-driven analysis interface for Bybit perpetual futures. It pulls 200+ quantitative features across 8 timeframes — RSI, MACD, ADX, Bollinger Bands, CVD, order book depth, funding rate z-scores, open interest deltas, volume profile, market structure, pivot points, and more — and presents them in a structured, strategy-aware format designed for AI-assisted decision making.

**Full version available at:** https://anomalysystems.gumroad.com/l/wugjom — $97 one-time.

---

## Strategies

Four built-in strategies operating on different timeframes and hold periods:

| Strategy | Chart | Hold Period | Focus |
|----------|-------|-------------|-------|
| FAST | 5m | 10–60 min | Scalps, momentum |
| SWING | 15m | 2–8 hours | Default, intraday |
| MEDIUM | 30m | 4–12 hours | Overnight holds |
| POSITION | Daily | 1–4 weeks | Macro-driven |

Each strategy runs its own indicator stack, CVD window, and enforces its own SL/TP/R:R constraints at execution time.

---

## What It Analyzes

- **Momentum:** RSI, MACD, Stochastic, CCI, Williams %R
- **Trend:** EMA 20/50/200, ADX, DI+/DI−, multi-TF EMA separation
- **Volatility:** ATR (%), Bollinger Band %, Choppiness Index
- **Order Flow:** CVD, buy/sell ratio, flow imbalance, large trade ratio
- **Market Microstructure:** Bid/ask spread, L1/L5 depth, microprice, queue imbalance
- **Derivatives:** Funding rate z-score, OI delta (5m/1h/24h), OI spike detection
- **Volume Profile:** POC, VAH, VAL, HVN/LVN, key level detection
- **Market Structure:** Swing highs/lows, breakout strength, momentum
- **Support/Resistance:** Pivot points, 1h/4h/Daily S&R levels
- **Risk Gates:** Per-strategy pass/fail on spread, liquidity, and choppiness

---

## Safety Model

- **DEMO mode by default** — all orders are paper trades on Bybit's demo environment (real market prices, no real money)
- Switching to LIVE requires an explicit interactive confirmation typed by the user (cannot be bypassed by env vars, CLI flags, or agent-autonomous decisions)
- Stop loss is mandatory on every order; CLI enforces it
- Strategy constraints (min SL, min TP, R:R bounds) enforced at execution
- Emergency close command available at any time
- Risk gate failures surface warnings before you size in

---

## Commands (Full Version)

```bash
# Market analysis
quantclaw analyze BTCUSDT --strategy swing
quantclaw analyze ETHUSDT --strategy fast
quantclaw analyze BTCUSDT --quick

# Account
quantclaw balance
quantclaw positions
quantclaw orders
quantclaw pnl --days 7

# Trading (DEMO by default)
quantclaw buy BTCUSDT 1000 --leverage 3 --sl 1.5 --tp 3.0 --strategy swing
quantclaw sell ETHUSDT 500 --leverage 2 --sl 1.5 --tp 2.5
quantclaw close BTCUSDT
```

---

## Requirements

- macOS or Linux
- `uv` — Python package/project manager by Astral (https://github.com/astral-sh/uv). Install via `brew install uv` (macOS/Linux) or `pip install uv`. Used to run QuantClaw's Python environment without polluting your system Python.
- Bybit API keys — demo (paper trading) or live

---

## Purchase & Verification

This is a stub listing. The full skill with source code is available at:

**https://anomalysystems.gumroad.com/l/wugjom** — $97 one-time, personal use license.

The download includes:
- Full Python source code (auditable before running)
- SHA256 checksum file for download verification
- No compiled binaries — QuantClaw runs as a `uv`-managed Python project

**Recommended**: review the source before supplying live API keys. Use Bybit demo/paper trading keys first.
