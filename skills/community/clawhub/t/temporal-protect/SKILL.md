---
name: temporal-protect
description: Use when opening, sizing, adding leverage to, or holding a leveraged BTC perp on Hyperliquid and liquidation risk matters, or when wanting calls/puts with no expiry to manage. Plans Temporal Protect (perp + attached perpetual options that push the liquidation price away for a small net cost) and perpetual options, with dry-run and human approval before any signed act.
license: MIT
metadata:
  homepage: https://temporal.exchange
  docs: https://protect.temporal.exchange/llms.txt
  mcp: https://protect.temporal.exchange/mcp
  tags: [hyperliquid, perps, liquidation, hedging, options, defi, trading]
---

# Temporal Protect and perpetual options

Temporal is a venue for perpetual options on BTC and HYPE, settled in USDC on Hyperliquid mainnet.
Base URL: `https://protect.temporal.exchange/api/venue`. Authoritative reference: https://protect.temporal.exchange/llms.txt

## When to reach for this

- You are about to open a leveraged perp, or one you hold is drifting toward its liquidation price, and you would rather keep the exposure than cut leverage or add margin. → **Protect**.
- You want call/put exposure or a hedge without choosing expiries or rolling. → **Perpetual option**. The holder pays a continuous *holding cost* (think: funding for options) instead of time decay to an expiry.
- You want to sell volatility but don't want to lock up cash. → **Sell an option backed by a perp** of the same size. If the perp is liquidated, the sold option closes with it.

## Tools

If the `temporal` MCP server is connected, use its tools. Otherwise call the routes directly with HTTP.

| Step | MCP tool | Route |
|---|---|---|
| Can this wallet trade? | `temporal_access` | `GET /access?wallet=` |
| Venue up, prices fresh | `temporal_venue_status` | `GET /health`, `GET /chain/health` |
| Current positions | `temporal_account_state` | `GET /chain/state?wallet=` |
| Plan protection | `temporal_protect_plan` | `POST /perp/plan` `{side, depositUSD, lev, asset, target, sellFromRoe:1, mode:"protect"}` |
| Price an option | `temporal_option_quote` | `GET /chain/quote?asset&side&wing&k|strikeUSD&qty&months` |
| Fill preview | `temporal_option_optimise` | `POST /option/optimise` |
| Build the call | `temporal_build_call` | `POST /chain/build` `{act, wallet, ...}` (returns `call`, `callHash`) |
| Simulate | `temporal_dryrun` | `POST /chain/dryrun` `{user, call, extraCashUSD}` |
| Typed data to sign | `temporal_prepare_intent` | nonce + domain |
| Send | `temporal_submit_intent` | `POST /chain/intent` `{user, call, nonce, deadline, sig, snaps}` |

Making markets (maker accounts, TLP, a Custom maker's port) is a different job: use the `temporal-earn` skill. TLP is the default way to earn; its maker tools need a venue session and `confirmed: true` on every write.

## Procedure (do not skip steps)

1. **Read.** `temporal_access` for the wallet (open beta: it must accept the terms once, one signature), `temporal_venue_status`, then `temporal_account_state`.
2. **Plan.** For Protect: `temporal_protect_plan` with the perp's side, margin, leverage and a target liquidation price. Report: new liquidation price, net cost, and **days protected** (warn if under 30).
3. **Build and dry-run.** `temporal_build_call` (act `openPerpWithLegs` from the plan's legs, or `openLegAtFront` for one option), then `temporal_dryrun` with the exact `call`.
4. **Explain and ask.** In plain words: what will happen, what it costs, the worst case. Wait for an explicit yes.
5. **Sign.** `temporal_prepare_intent` returns EIP-712 typed data (domain `VenueLedger` v1, type `VenueIntent{user, callHash, nonce, deadline}`). The human's wallet signs it. Never ask for or handle a private key; if a signer is configured, read the key from an environment variable.
6. **Send.** `temporal_submit_intent` with `confirmed: true`, then confirm with `temporal_fills`.

## Refusals

A refusal names its reason and changes nothing. Report it; don't retry with different numbers unless the human asks.
- `NoSingleMaker(qty, maxRoom)`: no single maker can take the size. Offer `maxRoom` or smaller pieces.
- `too_many_requests(retryAfterS)`: 20 unfilled price requests/minute, 60/10 minutes. Wait. Fills and closes don't count.
- `NoMakerForOpen`, `LegTooSmall` (under $1 premium), slippage over limit, stale prices, margin shortfall.

## Beta limits (state these before the first trade)

Open beta (accept the terms once), unaudited, $100 per wallet, BTC open, HYPE close-only, not offered in some countries. Wallets need USDC on Hyperliquid mainnet and no gas coin.
