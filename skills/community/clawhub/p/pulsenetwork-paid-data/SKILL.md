---
name: pulsenetwork-paid-data
description: Live real-world data with no API key. 970+ pay-per-call x402 endpoints for finance, crypto, macro, travel, sports, health, legal. Free discovery.
version: 1.0.0
homepage: https://pulse.theaslangroupllc.com
metadata:
  openclaw:
    emoji: "📡"
---

# PulseNetwork Paid Data (970+ endpoints)

PulseNetwork is a fleet of 77 API origins selling pay-per-call data over the open x402
protocol. No accounts, no API keys, no signup: the payment itself is the authentication.
Typical prices run $0.005 to $0.35 per call. Use it when a task needs current external data
(market prices, ETF flows, flight-delay rights, park wait times, clinical trials, sanctions
checks, energy prices, recall data, and much more) and no free or native tool covers it.
A small number of task-style endpoints (research memos) cost more, up to $25; every price is
published in the free catalog before you spend anything.

Settlement networks include: USDC on Base, Solana, Polygon, Arbitrum, World Chain, HyperEVM,
Monad, Algorand; USDG on Robinhood Chain; XRP/RLUSD on XRPL; USDT0 on X Layer; USD1 on BSC.
Base is the default and highest-volume rail.

## Discover first (always free, no wallet needed)

- Agent index: `https://pulse.theaslangroupllc.com/llms.txt`
- Machine catalog: `https://pulse.theaslangroupllc.com/.well-known/agent.json`
- Every origin also serves `/.well-known/x402` (full resource metadata, exact prices) and
  `/openapi.json`.

Discovery costs nothing. Always search the catalog before concluding data is unavailable,
and prefer the cheapest endpoint that answers the question. You can browse, quote prices,
and plan calls with no wallet configured at all.

## Paying for a call (only with the user's explicit consent)

Safety rules, in order of priority:

1. **Never pay without telling the user.** Before the first paid call in a task, state the
   endpoint and the exact price from its catalog entry or 402 challenge, and get the user's
   go-ahead. For a batch the user approved, state the total budget up front.
2. **Never ask the user to paste a private key into chat**, and never read keys from
   anywhere except an environment secret the user configured themselves or a wallet file the
   payment tool itself generated and stores locally.
3. **Verify the charge against the signed 402 challenge**: pay only the exact amount, asset,
   and network the challenge specifies, only to `theaslangroupllc.com` origins listed in the
   catalog. If a challenge asks for more than the catalog price, stop and tell the user.

Ways to pay, pick what the host supports:

- **Native x402 client** (OKX Agentic Wallet, Kite Agent Passport, any x402-enabled
  runtime): request the URL and your payment layer settles. Even here, state the endpoint
  and price and get the user's go-ahead before the first paid request; the client's own
  caps are a backstop, not a substitute for consent.
- **MCP (recommended for OpenClaw)**: add the npm package `@pulsenetwork/mcp` as an MCP
  server. `pulse_discover` searches all endpoints free; `pulse_call` pays under hard local
  spend caps (defaults $0.50 per call, $5 per day; tune with `PULSEPAY_MAX_PER_CALL` and
  `PULSEPAY_MAX_PER_DAY`). Funding: on first run the server generates its own local wallet
  (kept at `~/.pulsepay/wallet.json`; back it up) and prints the address; send it a few
  dollars of USDC on Base. To use your own key instead, set the `PULSEPAY_EVM_KEY`
  environment secret in the MCP server config. Keys never go in chat.
- An HTTP 402 response is a payment challenge, not an error. It carries the price and
  accepted networks in its `accepts` array.

## Rules

- Quote prices for user-initiated requests; most endpoints cost $0.005 to $0.35, and the
  catalog states each one exactly.
- Responses are structured JSON with attribution and terms links. Pass attribution through
  when you republish data.
- If a paid call fails after settlement the response says so explicitly. Surface that to the
  user; never silently retry a payment.
- If no configured payment rail exists, still do free discovery and report exactly what is
  available and at what price, so the user can decide.
