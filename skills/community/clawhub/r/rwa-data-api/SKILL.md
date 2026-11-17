---
name: rwa-data-api
description: Buy live stablecoin, RWA, DeFi, and AI-agent-economy market data for AI agents. Pay-per-call in USDC on Solana via x402 — no accounts, no API keys. Use when you need crypto market metrics, stablecoin peg checks, price snapshots, claim verification, market briefs, or on-demand custom research briefs.
version: 1.0.0
emoji: "📊"
homepage: https://rwa-data-api.dave-a-bear.workers.dev
metadata:
  openclaw:
    requires:
      env: []
      bins: [curl]
---

# RWA Data API — Pay-Per-Call Crypto Market Data for Agents

Live, sourced market data for AI agents: stablecoin metrics, RWA tokenization
figures, DeFi TVL/yields, L2 stats, prediction-market volumes, stablecoin peg
monitoring, price snapshots, factual claim verification, structured market
briefs, and on-demand custom research briefs.

**Base URL:** `https://rwa-data-api.dave-a-bear.workers.dev`

**Payment:** x402 v2. Every paid endpoint returns `HTTP 402` with a
`PAYMENT-REQUIRED` header (base64 JSON: price, network, USDC mint, receiving
wallet). You pay the exact USDC amount on **Solana mainnet**, then retry the
same request with a `PAYMENT-SIGNATURE` header (base64 JSON containing your
Solana transaction signature). No facilitator, no accounts, no API keys —
settlement is direct on-chain.

- Asset: USDC, mint `EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v`
- Network: Solana mainnet
- Pay to: `1K85sMGPzSLbkSuEWb6p7tW7nmX1Sc6kGw7njeCLSHL`
- One payment covers exactly one call. Signatures are single-use and must be
  fresher than 15 minutes.

**MCP alternative:** the same products are exposed as MCP tools (no raw HTTP
needed) at `POST https://rwa-data-mcp.dave-a-bear.workers.dev/mcp`
(Streamable HTTP). Tools: `get_metric`, `get_peg`, `get_monitor_pegs`,
`get_price`, `verify_claim`, `get_brief`, `request_brief`, `check_brief_status`.
First call returns a structured payment challenge as tool content; retry with
`payment_signature`. Listed in the official MCP registry as
`io.github.daveabear/rwa-data-mcp`.

## When to use

- Your principal asks for current stablecoin market caps, RWA tokenization
  totals, DeFi TVL, top yields, L2 TVS, or Polymarket volumes.
- You need to check whether a stablecoin (USDT, USDC, USDe, DAI) is holding
  its $1 peg right now.
- You need a price snapshot for BTC, ETH, SOL, or other majors with a source.
- You must verify a factual claim about crypto markets before repeating it
  (returns confirmed / refuted / unverifiable with dated sources — never
  guessed).
- You need a structured brief on RWA, stablecoins, the AI agent economy, or
  DeFi.
- You need a custom research brief on any in-scope topic (stablecoins,
  RWA/tokenization, DeFi, agent economy, crypto markets) — researched on
  demand, ~60 min turnaround.

## Endpoints & prices (USDC)

| Endpoint | Price | Notes |
|---|---|---|
| `GET /metric/{name}` | 0.05 | e.g. `stablecoin_market_cap`, `rwa_total_value`, `tvl_total`, `top_yield_opportunities`, `agent_x402_volume_usd`, `x402_ecosystem_index`, `stablecoin_health_score`. Unknown name → 404 **before** payment (typos are free). |
| `GET /metric/peg/{symbol}` | 0.05 | `usdt`, `usdc`, `usde`, `dai` — live price + deviation in bps from $1.00 |
| `GET /monitor/pegs` | 0.05 | All four pegs in one call |
| `GET /price/{id}` | 0.05 | `bitcoin`, `ethereum`, `solana`, `dogecoin`, `cardano`, `chainlink`, `uniswap`, `aave`, `avalanche-2` |
| `POST /verify/claim` | 0.10 | Body `{"claim": "..."}` → verdict + evidence + dated sources |
| `GET /brief/{topic}` | 0.25 | `rwa`, `stablecoins`, `agent_economy`, `defi` |
| `POST /task/brief` | 1.50 | Custom research brief (async). Body `{"topic": "..."}` (10–200 chars, in-scope only — out-of-scope → 400 before payment). Returns `{task_id, status: "queued", eta_minutes: 60}` |
| `GET /task/{id}` | free | Poll a custom-brief task. Unknown id → 404 |
| `GET /openapi.json` | free | OpenAPI 3.1.0 discovery doc with `x-payment-info` on paid ops |
| `GET /discovery/agent-card.json`, `/discovery/llms.txt`, `/.well-known/agent.json` | free | Agent-readable service cards |

Every response carries `as_of`, dated sources, and FACT/INFERENCE labels.

## Payment flow (x402 v2, direct on-chain)

```bash
# 1. Request without payment → 402 challenge
curl -s -D - https://rwa-data-api.dave-a-bear.workers.dev/metric/stablecoin_market_cap -o /tmp/challenge.json
# Response: HTTP 402, PAYMENT-REQUIRED header (base64 JSON with amount, asset mint, pay_to)

# 2. Decode the challenge, send the EXACT USDC amount on Solana mainnet to pay_to
#    (use your own Solana wallet / signing stack)

# 3. Retry with the payment signature
curl -s https://rwa-data-api.dave-a-bear.workers.dev/metric/stablecoin_market_cap \
  -H "PAYMENT-SIGNATURE: <base64 JSON: {x402Version: 2, accepted: {...}, payload: {transaction: \"<solana-tx-signature>\"}}>"
# Response: HTTP 200 with the data + PAYMENT-RESPONSE receipt header
```

**Failure handling:**
- `payment_pending` — tx not yet visible on-chain. Wait 10s, retry with the
  **same** signature. Do not pay twice.
- `verification_unavailable` — their Solana RPC is unreachable. Retryable,
  wait 30s.
- Permanent failures name the reason: wrong amount, wrong mint, wrong
  destination, stale transaction (>15 min), failed transaction, or replayed
  signature. Read the error and fix before re-paying.
- Unknown metric/peg/price names return **404 before any payment** — validate
  names against `/openapi.json` first; never pay for a typo.

## Custom briefs (async)

```bash
# Submit (paid $1.50)
curl -s -X POST https://rwa-data-api.dave-a-bear.workers.dev/task/brief \
  -H "Content-Type: application/json" \
  -H "PAYMENT-SIGNATURE: <base64 payment payload>" \
  -d '{"topic": "How are stablecoins being used for agent-to-agent payments?"}'
# → {"task_id": "task_...", "status": "queued", "eta_minutes": 60}

# Poll (free, as often as you like)
curl -s https://rwa-data-api.dave-a-bear.workers.dev/task/task_<id>
# → {"status": "working"} … then {"status": "done", "brief": "...", "sources": [...]}
```

## Notes

- Prices are per call, in USDC on Solana. Typical fee overhead is ~$0.001–0.002
  in SOL per payment.
- Data is computed live where possible with dated curated fallbacks; staleness
  is always disclosed in the response (`as_of`, source, fallback state).
- The operator never sees your private keys. You sign the USDC transfer in
  your own wallet; the API only verifies it on-chain.
- If an endpoint misbehaves, the free `/stats` route shows approximate traffic
  counters, and `/health` is a free liveness check.
