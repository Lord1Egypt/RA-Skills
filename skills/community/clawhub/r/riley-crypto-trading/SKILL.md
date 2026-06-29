---
name: crypto-trading
description: |
  The pre-trade data stack for crypto trading and sniping agents: discover new/trending token
  launches, run a safety/rug-check on any token BEFORE buying, and pull live DEX price,
  liquidity and buy/sell flow. All live, all pay-per-call over x402.

  USE FOR:
  - Finding newly launched / boosted tokens to evaluate (discovery feed to poll)
  - Rug-checking a token before buying: honeypot, buy/sell tax, mint/owner risk, blacklist
  - Live DEX data for any token: USD price, 24h volume, liquidity, buy/sell counts, momentum

  TRIGGERS:
  - "new tokens", "new launches", "trending tokens", "what just launched", "snipe"
  - "is this token safe", "rug check", "honeypot", "can I sell", "token tax", "is it a scam"
  - "token price", "dex data", "liquidity", "volume", "buy sell pressure"

  Recommended flow per candidate: launches -> security (rug check) -> dex (data) = decide.
  Use x402 GET calls. Never guess paths — use the exact URLs below or GET /samples first.
mcp:
  - agentcash
---

# Crypto Trading Lane with the x402 Agent Store

> All endpoints are GET on `https://store.agentexchange.work`. Paid calls return HTTP 402;
> your x402 client signs USDC on Base and retries. Free preview: `GET /samples`.

This is the funnel sniping/trading bots run on every token. Poll launches, rug-check each
candidate, then pull market data — three cheap calls, one decision.

## Quick Reference

| Task | Endpoint | Price |
|------|----------|-------|
| New & trending token launches (poll this) | `https://store.agentexchange.work/crypto/launches?chain=solana&limit=15` | $0.003 |
| Pre-trade rug / safety check | `https://store.agentexchange.work/crypto/security?address=0x6982508145454ce325ddbe47a25d4ec3d2311933&chain=ethereum` | $0.001 |
| Live DEX token data | `https://store.agentexchange.work/crypto/dex?q=WIF` | $0.002 |
| Live prediction-market odds (Polymarket) | `https://store.agentexchange.work/markets/prediction?q=bitcoin&top=5` | $0.01 |
| Token prices (CoinGecko ids) | `https://store.agentexchange.work/crypto/prices?ids=bitcoin,ethereum` | $0.001 |
| Top DeFi yields by chain/TVL | `https://store.agentexchange.work/defi/yields?chain=Base&min_tvl=10000000` | $0.003 |

## Notes
- `/crypto/security` returns a DANGER/HIGH_RISK/CAUTION/OK verdict + flags (honeypot, taxes,
  mintable, owner-can-reclaim, transfer-pausable, blacklist). Call it BEFORE any buy.
- `/crypto/launches` items include `next_calls` that point at the security + dex endpoints for
  that exact token — chain them automatically.
- `chain` accepts ethereum, base, bsc, polygon, arbitrum, optimism, avalanche (security) and
  solana/base/ethereum/bsc (launches). `q` accepts symbol, name, or contract address (dex).
