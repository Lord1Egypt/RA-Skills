---
name: supah-pulse
description: "Real-time crypto market intelligence briefing. One command gives any agent the full picture: market regime, fear/greed, BTC/ETH dominance, gas costs, trending tokens, top movers, DeFi TVL shifts, liquidations, and a Market Pulse Score (0-100). The context layer every agent needs before making decisions. x402 USDC micropayments on Base."
metadata:
  {
    "openclaw":
      {
        "emoji": "📡",
        "requires": { "bins": ["curl", "node"], "env": ["SUPAH_API_BASE"] },
        "network": { "outbound": ["api.supah.ai", "api.coingecko.com", "api.alternative.me", "api.llama.fi"] },
        "x402": { "enabled": true, "currency": "USDC", "network": "base", "maxPerCall": "0.03", "payTo": "0xD3B2eCfe77780bFfDFA356B70DC190C914521761" }
      }
  }
---

# SUPAH Pulse

**The context layer every crypto agent needs.**

Before your agent trades, allocates, or advises — it needs to know what's happening RIGHT NOW. One command. Full market picture. Updated in real-time.

**$0.03 USDC per pulse** — paid via x402 micropayment on Base. Your agent pays automatically per call. No API keys. Just USDC in your agent wallet on Base. [How x402 works](https://www.x402.org)

## Why Every Agent Needs This

AI agents making crypto decisions without market context are flying blind. They'll buy into fear, sell into rallies, and miss regime shifts. SUPAH Pulse gives any agent instant situational awareness:

- Is the market risk-on or risk-off?
- Is it a good time to trade or sit tight?
- What's trending? What's crashing?
- Are gas fees going to eat my profits?
- Where's the smart money flowing?

## What It Returns

A **Market Pulse Score (0-100)** built from 6 weighted intelligence layers:

1. **ETH Momentum** (20%) — Multi-timeframe price deltas (10m/30m/1h/3h/6h), range position, acceleration state
2. **Trend Health** (20%) — Pattern detection: bottom forming, recovering, accelerating, all-green/all-red, volume surges
3. **Sentiment** (15%) — Fear & Greed Index with daily/weekly comparison and trend direction
4. **Macro Signals** (20%) — BTC correlation, funding rates, long/short ratio, taker buy/sell, liquidation risk, squeeze setups
5. **Mean Reversion** (10%) — Z-score vs EMA20/EMA50, overbought/oversold detection
6. **Prediction** (15%) — ML-powered direction forecast with confidence score and expected move

Plus full tactical briefing:
- **Key Levels** — Support/resistance, EMA crossovers, volume POC, value area
- **Trading Parameters** — Min score thresholds, stop loss levels, position scaling
- **SUPAH Regime Signals** — Proprietary regime classification with confidence
- **DeFi TVL** — Chain-by-chain breakdown (Ethereum, Base, Arbitrum, Solana)
- **Base Chain Activity** — Volume, wallets, transactions

Returns a clear **RISK-ON / LEAN BULLISH / NEUTRAL / LEAN BEARISH / RISK-OFF** market call with specific tactical suggestions.

## Usage

Ask your agent naturally:

```
"What's the market doing right now?"
"Give me a pulse check before I trade"
"Market briefing"
"Is it a good time to buy?"
"What's trending in crypto today?"
"Market pulse"
"Should I be risk-on or risk-off right now?"
```

## Example Output

```
📡 SUPAH PULSE — Market Intelligence Briefing
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🕐 2026-03-19 20:05 UTC

MARKET PULSE: 62/100 ⚡ NEUTRAL-BULLISH

REGIME: Accumulation Phase
SENTIMENT: Neutral (Fear & Greed: 48)

┌──────────────────────────────────────┐
│ BTC Trend          ██████░░ 65     │
│ Market Breadth     █████░░░ 58     │
│ Sentiment          ████░░░░ 48     │
│ Volume Strength    ██████░░ 70     │
│ DeFi Health        █████░░░ 62     │
│ Network Activity   ██████░░ 68     │
└──────────────────────────────────────┘

💰 MAJOR ASSETS:
  BTC  $67,234  +2.1% (24h)  -3.4% (7d)
  ETH  $3,456   +1.8% (24h)  -5.1% (7d)
  SOL  $142.30  +4.2% (24h)  +1.2% (7d)
  BTC Dominance: 52.3% (rising → altcoin caution)

⛽ GAS:
  ETH: 12 gwei ($0.42/swap) | Base: 0.001 gwei ($0.01)

🔥 TOP MOVERS (24h):
  🟢 $OTTIE +231% | $VIRTUAL +18% | $AERO +12%
  🔴 $DEGEN -14% | $BRETT -9% | $TOSHI -7%

📊 TRENDING: $VIRTUAL, $OTTIE, $MORPHO, $AERO

🏦 DeFi TVL: $89.2B (+1.2% 24h)
  Base TVL: $3.1B | Arbitrum: $2.8B

💡 MARKET CALL: NEUTRAL-BULLISH
  → BTC holding above key support
  → Volume recovering
  → Altcoins mixed — be selective
  → Base ecosystem showing strength

SUGGESTION: Moderate risk. Small positions on dips.
Favor Base ecosystem tokens. Keep stops tight.
```

## How It Works

The skill calls api.supah.ai via **x402 USDC micropayments** on Base. Your agent pays $0.03 per pulse automatically — no API keys, no setup.

SUPAH's backend aggregates data from multiple sources:
- **SUPAH Regime Engine** — Proprietary market regime detection, momentum analysis, ML predictions
- **CoinGecko** — Prices, market cap, volume, dominance
- **Alternative.me** — Fear & Greed Index
- **DeFiLlama** — TVL, protocol data, chain comparisons
- **Moralis** — On-chain activity metrics and transaction volume

SUPAH is built on and utilizes **Moralis** for on-chain data that feeds into the regime engine's market analysis, providing real-time Base chain activity metrics alongside traditional market data.

All data fetched in parallel (<8 seconds).

## Requirements

- **`curl`** — HTTP client (pre-installed on most systems)
- **`node`** — Node.js v18+ runtime (for JSON parsing)
- **USDC on Base** — Your agent wallet must hold USDC on Base network for x402 micropayments ($0.03/pulse)
- **x402-compatible HTTP client** — Payment happens automatically per call via the [x402 protocol](https://www.x402.org)

Optional: Set `SUPAH_API_BASE` environment variable to override the default API endpoint (default: `https://api.supah.ai`).

## Install

```bash
clawhub install supah-pulse
```
