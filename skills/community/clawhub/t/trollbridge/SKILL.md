---
name: trollbridge-x402-intel
description: Pay-per-call crypto intel API — 100 tolled lanes (markets, token safety, scam detection, Polymarket odds, DeFi yields) paid in USDC on Base via x402.
metadata: {"openclaw":{"emoji":"🌉","homepage":"https://mini-tollbooth.onrender.com","requires":{"bins":["curl"]}}}
---

# TrollBridge — pay-per-call crypto intel for agents

TrollBridge is a live x402 pay-per-call API: 100 intel lanes covering markets data,
token safety screens, scam detection, DeFi yields, Polymarket odds, and audit tools.
You pay per call in USDC on Base (or Solana). No API key, no signup — the 402
response itself is the invoice.

Base URL: `https://mini-tollbooth.onrender.com`

## How x402 payment works

1. Call any lane without payment. You get HTTP `402` with a JSON body describing
   the price and where to pay.
2. Sign a USDC transfer for the quoted amount to the quoted address
   (EIP-3009 / x402 payment scheme — your x402 client library handles this;
   see https://x402.org for client docs).
3. Retry the same request with the `X-PAYMENT` header set to the
   base64-encoded payment payload. You get HTTP `200` with the data.

If you don't have an x402 client, the 402 body is human-readable: it tells you
the exact amount, token, network, and recipient. Any wallet that can sign a
USDC transfer on Base can pay.

Free endpoints (no payment needed): `GET /health`, `GET /tools`.

## Pricing tiers (USDC)

- **$0.02** — standard lanes (default): most intel feeds
- **$0.05** — premium data lanes: /token-check, /markets, /yields, /search,
  /enrich, /new-pairs, /preflight, /road-pack, /trust, and others
- **$0.10** — protection tier: /contract-check, /approval-screen,
  /tx-plain-english, /airlock, /verdict, /honeypot-check, /tx-simulate, and others
- **$1.00–$30.00** — heavyweight lanes: /audit-prep, /datasets ($1),
  /scam-scan ($5 deep scan), /audit ($25), /scam-scan-subscribe ($30)

The 402 response always states the exact price before you pay. Never guess.

## Lanes agents actually use

**Before you move money (safety screens):**
- `GET /token-check?token=0x...&chain=base` — $0.05 — liquidity, holders,
  rug-pull heuristics, verdict
- `GET /honeypot?token=0x...&chain=base` — $0.02 — can you sell after you buy
- `GET /honeypot-check?token=0x...&chain=base` — $0.10 — deeper DEX buy/sell
  flow simulation + holder concentration
- `GET /contract-check?contract=0x...&chain=base` — $0.10 — verification,
  proxy/owner heuristics, holder concentration
- `GET /approval-screen?wallet=0x...&chain=base` — $0.10 — risky token approvals
  on a wallet (NOT AN AUDIT — heuristic screen)
- `GET /preflight?token=0x...&chain=base` — $0.05 — honeypot + rug + contract +
  approvals in one call

**Market intel:**
- `GET /polymarket-odds?market=<slug-or-id>` — $0.02 — live Polymarket odds,
  prices, volume
- `GET /markets` — $0.05 — prediction-market overview
- `GET /top-movers` — $0.02 — biggest gainers/losers right now
- `GET /yields` — $0.05 — best stablecoin yields (DeFiLlama)
- `GET /whale-watch` — $0.02 — large-wallet movement flags
- `GET /fear-greed` — $0.02 — Fear & Greed index
- `GET /gas` — $0.02 — current gas prices

**Deep scans (priced accordingly):**
- `GET /scam-scan?url=<url>` — $5.00 — full 10-flag scam smell-test with
  prize-vs-cost math and a CLEAN / CAUTION / LIKELY_SCAM verdict
- `GET /audit-prep?repo=<url>` — $1.00 — pre-audit checklist for a repo

**Discovery (free):**
- `GET /tools` — free third-party tool directory on the bridge
- `GET /health` — `{"status":"ok","lanes":100}` — liveness check

## Worked example: check a token before swapping

```bash
# 1. Unpaid call → 402 with payment details
curl -s https://mini-tollbooth.onrender.com/token-check?token=0x...&chain=base

# 2. Pay the quoted USDC amount on Base, get the payment payload
#    (via your x402 client library)

# 3. Retry with payment
curl -s -H "X-PAYMENT: <base64-payment-payload>" \
  "https://mini-tollbooth.onrender.com/token-check?token=0x...&chain=base"
# → 200 with { verdict, liquidity, holders, flags }
```

## Honest notes

- This is a live service on a hobby host (Render free tier): expect occasional
  cold starts of ~30–60s on the first request after idle.
- Screens are heuristic, not audits. Every screen lane's copy leads with
  "NOT AN AUDIT" where applicable — treat verdicts as one input, not a guarantee.
- Paid crossings settle on-chain via the Coinbase CDP facilitator; volume is
  publicly enumerable on the x402 Bazaar leaderboard.
- Lane list and prices can change; the 402 response is always the source of
  truth for the current price.
