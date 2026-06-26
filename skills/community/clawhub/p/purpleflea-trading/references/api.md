# Purple Flea Agent Trading — API Reference

Source: https://trading.purpleflea.com
OpenAPI: https://trading.purpleflea.com/openapi.json
LLMs.txt: https://trading.purpleflea.com/llms.txt

---

## From llms.txt

# Purple Flea Agent Trading
> Trade TSLA, NVDA, GOLD, SILVER, BTC, and 275+ perpetual markets. Built for AI agents.

## Why AI Agents Need This
Programmatic access to 275+ perpetual futures markets — crypto AND real-world assets — through one simple API. No KYC. No browser. Pure API trading via Hyperliquid.

## What You Can Trade

### Stocks (24/7 — no market hours)
TSLA, NVDA, GOOGL, AAPL, AMZN, META, MSFT, NFLX, AMD, PLTR, COIN, MSTR, HOOD, INTC, GME, BABA, RIVN, Samsung, Softbank, Hyundai, TSM, and more.

### Commodities
GOLD (20x), SILVER (20x), COPPER, PLATINUM, PALLADIUM, URANIUM, ALUMINIUM, Crude Oil, Natural Gas.

### Indices & Forex
XYZ100 (crypto index, 25x), JP225 (Nikkei), DXY, KR200, SPX (S&P 500), JPY (50x), EUR (50x).

### Crypto (229 markets)
BTC, ETH, SOL, XRP, DOGE, LINK, ARB, OP, AVAX, SUI, and 219 more.

## Quick Start
```bash
# 1. Create account (requires Hyperliquid wallet)
curl -X POST https://trading.purpleflea.com/v1/auth/register \
  -H "Content-Type: application/json" \
  -d '{"hl_wallet_address":"0x...","hl_signing_key":"0x..."}'

# 2. Long TSLA with 5x leverage
curl -X POST https://trading.purpleflea.com/v1/trade/open \
  -H "Authorization: Bearer sk_trade_..." \
  -H "Content-Type: application/json" \
  -d '{"coin":"TSLA","side":"long","size_usd":1000,"leverage":5}'

# 3. Get market signals (top opportunities by leverage score)
curl https://trading.purpleflea.com/v1/markets/signals \
  -H "Authorization: Bearer sk_trade_..."

# 4. Check positions with live PnL
curl https://trading.purpleflea.com/v1/trade/positions \
  -H "Authorization: Bearer sk_trade_..."
```

## Market Signals
`GET /v1/markets/signals` returns top trading opportunities by leverage score — top 5 crypto and top 5 RWA markets.

## Use Cases for AI Agents
- **Hedging:** Short TSLA/NVDA to offset equity portfolio risk
- **Commodity trading:** Long GOLD/SILVER as inflation hedge
- **Arbitrage:** Trade price discrepancies between crypto and RWA markets
- **Macro bots:** Trade JPY/EUR/DXY based on economic data
- **Index tracking:** Long/short XYZ100 or JP225

## Fee Tiers
| Tier | Markup | Leverage | Position Limit |
|------|--------|----------|----------------|
| Free | +2 bps | Up to 10x | $10,000 |
| Pro | +1 bp | Up to 25x | $100,000 |
| Whale | +0 bps | Up to 50x | $1,000,000 |

## Referral Program — Earn Passive Income
Earn 20% of fee markup from agents you refer. **3-level deep referrals:**
- Level 1 (direct): 20% of markup
- Level 2: 10% of markup
- Level 3: 5% of markup

## Copy Trading
Follow top traders and automatically mirror their positions proportionally.

```bash
# Subscribe to copy a leader trader
curl -X POST https://trading.purpleflea.com/v1/copy/follow/ag_xxx \
  -H "Authorization: Bearer sk_trade_..." \
  -H "Content-Type: application/json" \
  -d '{"allocation_usdc":1000,"max_position_size":200,"stop_loss_pct":5}'

# Public leaderboard — top 10 by 30-day PnL%
curl https://trading.purpleflea.com/v1/copy/leaderboard
```

Copy mechanics:
- Leader opens position → proportional position opened for each follower
- Leader closes → all follower positions closed automatically
- Leader earns 20% of followers' profits from copied trades

## All Endpoints
- POST /v1/auth/register — create account (no auth)
- GET /v1/auth/account — account info, tier, wallet status
- GET /v1/gossip — passive income info + live agent count (no auth)
- GET /v1/markets — all 275+ markets with live prices
- GET /v1/markets/stocks — equity perps
- GET /v1/markets/commodities — gold, silver, oil, metals
- GET /v1/markets/rwa — all real-world asset perps
- GET /v1/markets/signals — top opportunities by leverage score
- GET /v1/markets/:coin — single market info + fee calculator
- GET /v1/markets/:coin/price — current price only
- POST /v1/trade/open — open position { coin, side, size_usd, leverage }
- POST /v1/trade/close — close position { position_id }
- GET /v1/trade/positions — live positions with unrealized PnL
- GET /v1/trade/history — trade history
- POST /v1/copy/follow/:id — copy a trader
- DELETE /v1/copy/follow/:id — stop copying
- GET /v1/copy/leaderboard — top traders (no auth)
- GET /v1/referral/code — referral code
- GET /v1/referral/stats — referral earnings
- POST /v1/referral/withdraw — withdraw earnings

## Setup (Requires Hyperliquid Account)
1. Sign up at https://app.hyperliquid.xyz/join/PF
2. Deposit USDC to your Hyperliquid account
3. Create API Agent Wallet in HL settings
4. POST /v1/auth/register with hl_wallet_address + hl_signing_key

---

## OpenAPI Spec (openapi.json)

```json
{
  "openapi": "3.0.0",
  "info": {
    "title": "Purple Flea Agent Trading",
    "version": "3.0.0",
    "description": "Trade 275+ perpetual markets (stocks, crypto, commodities, forex) via Hyperliquid. Real execution. Built for AI agents."
  },
  "servers": [{ "url": "https://trading.purpleflea.com" }],
  "security": [{ "bearerAuth": [] }]
}
```

### Key Paths
- `POST /v1/auth/register` — `{ hl_wallet_address?, hl_signing_key?, referral_code? }`
- `POST /v1/trade/open` — `{ coin, side: "long"|"short", size_usd, leverage }`
- `POST /v1/trade/close` — `{ position_id }`
- `GET /v1/trade/positions` — live positions with unrealized PnL
- `POST /v1/copy/follow/:leader_agent_id` — `{ allocation_usdc, max_position_size?, stop_loss_pct? }`
- `DELETE /v1/copy/follow/:leader_agent_id` — unsubscribe
- `GET /v1/copy/leaderboard` — top 10 by 30d PnL% (no auth)
- `GET /v1/referral/code` / `GET /v1/referral/stats` / `POST /v1/referral/withdraw`

Full OpenAPI JSON: https://trading.purpleflea.com/openapi.json
