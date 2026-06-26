# Hyperliquid Trading Agent — Smart Money Signals & Autonomous Execution

An [OpenClaw](https://openclaw.io) skill (v2.3.6) — autonomous Hyperliquid trading agent powered by smart money signals from **500+ whale wallets**. Create, backtest, and deploy AI trading agents on **Hyperliquid** (perps, spot, HIP-3 stocks) and **Polymarket** (prediction markets). Real-time composite AI signals (Smart Money + Technical Analysis + Derivatives), multi-timeframe analysis, and a self-learning execution engine — all from your AI assistant.

## Features

- **Smart Money Signals** — Track top traders (>75% win-rate) across Polymarket predictions and HyperLiquid perpetuals
- **AI Dashboard** — Composite signals combining SM (40%), TA (35%), and Market data (25%) across perp, spot, HIP-3, and prediction markets
- **Technical Analysis** — Multi-timeframe TA indicators (RSI, MACD, SuperTrend, Bollinger Bands, etc.) via TAAPI.io
- **Derivatives Data** — Open interest, funding rates, long/short ratios, liquidation maps via CoinGlass
- **Trading Agents** — Create, configure, deploy, and monitor automated Perp agents on HyperLiquid with customizable trigger conditions
- **Human-in-the-Loop (HITL)** — Agent creates trade plans for your approval via chat or Telegram
- **HIP-3 Trading** — Stocks (TSLA, NVDA), commodities (GOLD), indices on Hyperliquid DEXs
- **Backtesting** — Run historical simulations with streaming progress and performance reports
- **Telegram Notifications** — Instant trade plan alerts with one-tap approve/reject buttons
- **Wallet Tracking** — Look up any trader's profile, PnL, categories, and open positions

> **Note:** Polymarket data reading works. PM trading agents are not yet supported.

## Prerequisites

- Python 3
- A Zonein API key (starts with `zn_`)

## Setup

1. Go to [app.zonein.xyz](https://app.zonein.xyz) → Log in → Click **"Get API Key"**
2. Set the key via one of:
   - **OpenClaw Gateway Dashboard** → `/skills` → Enable **zonein** → paste key
   - Environment variable: `export ZONEIN_API_KEY="zn_your_key_here"`
   - Config file: `~/.openclaw/openclaw.json` under `skills.entries.zonein.apiKey`

## Usage

All commands run through the bundled CLI script:

```bash
python3 skills/zonein/scripts/zonein.py <command> [options]
```

### Commands Overview

| Category | Commands |
|----------|----------|
| **Polymarket** | `signals`, `leaderboard`, `consensus`, `trader`, `pm-top`, `smart-bettors`, `trader-positions`, `trader-trades` |
| **Perp (HyperLiquid)** | `perp-signals`, `perp-traders`, `perp-top`, `perp-coins`, `perp-trader`, `perp-categories`, `perp-category-stats` |
| **AI Dashboard** | `dashboard`, `dashboard-latest`, `dashboard-asset`, `agent-signal` |
| **Technical Analysis** | `ta`, `ta-single` |
| **Derivatives** | `derivatives`, `fear-greed`, `derivatives-pairs`, `liquidation-map` |
| **Agent Management** | `agents`, `agent-get`, `agent-create`, `agent-update`, `agent-deploy`, `agent-enable`, `agent-disable`, `agent-pause`, `agent-delete` |
| **Agent Trading** | `agent-open`, `agent-close`, `agent-update-sl-tp`, `agent-fund`, `agent-withdraw`, `agent-positions`, `agent-balance`, `agent-orders` |
| **Agent Analytics** | `agent-overview`, `agent-stats`, `agent-performance`, `agent-trades`, `agent-vault`, `agent-backtest`, `agent-backtests` |
| **HITL Trade Plans** | `agent-check`, `agent-plans`, `agent-plan-detail`, `agent-plan-action`, `agent-plan-history` |
| **HIP-3** | `hip3-dexs`, `hip3-assets` |
| **Telegram** | `telegram-setup-init`, `telegram-setup`, `telegram-config`, `telegram-disable` |
| **Utility** | `agent-templates`, `agent-assets`, `agent-categories`, `agent-deposit`, `status` |

See [SKILL.md](./SKILL.md) for full command parameters, agent creation flow, and reference documents.

## Security

- Only your API key is sent externally (as `X-API-Key` header to `https://mcp.zonein.xyz/api/v1`)
- All API response data is sanitized (truncated to 500 chars/field) and treated as untrusted
- Financial commands are programmatically gated behind a `--confirm` flag — script refuses execution without it
- No local files are written; only `~/.openclaw/openclaw.json` is read (API key fallback)
- Prompt injection defense: response fields are never interpreted as instructions

## Links

- **Dashboard:** [app.zonein.xyz](https://app.zonein.xyz)
- **API Docs:** [mcp.zonein.xyz/docs](https://mcp.zonein.xyz/docs)
- **Homepage:** [zonein.xyz](https://zonein.xyz)

## Disclaimer

Signals reflect smart money activity — not guaranteed outcomes. Past performance does not predict future results. Never invest more than you can afford to lose.
