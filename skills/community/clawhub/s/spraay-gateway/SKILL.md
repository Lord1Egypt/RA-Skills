---
name: spraay-gateway
description: Instruction skill for the Spraay x402 payment gateway (gateway.spraay.app). Guides the agent to call documented Spraay HTTPS endpoints with curl for batch stablecoin payouts, escrow, payroll, token prices, and chain status, always with a free dry run and explicit user confirmation before any fund-moving call. The only bundled script, scripts/check-access.sh, checks gateway reachability and whether SPRAAY_API_KEY is valid; it moves no funds. Use when the user wants to validate, price, or send a batch payment, run crypto payroll, create escrow, or query a Spraay Gateway endpoint. Free endpoints need no credentials; paid endpoints need a Spraay subscription API key (external paid service) or per-call x402 payment the user approves.
version: 1.0.2
metadata:
  openclaw:
    requires:
      bins:
        - curl
    primaryEnv: SPRAAY_API_KEY
    envVars:
      - name: SPRAAY_API_KEY
        required: false
        description: >-
          Spraay Gateway subscription API key. NOT required to install or use
          free endpoints. Obtained by subscribing at https://spraay.app/pricing
          (external paid service — Starter $29/mo for 1,000 API calls/day, Pro $99/mo for 10,000 calls/day + priority support; billed by Stripe; key delivered by email on signup).
          Without it, paid endpoints require per-call x402 payment from a funded
          wallet instead.
      - name: SPRAAY_WALLET_ADDRESS
        required: false
        description: >-
          Optional. The user's own public address, used only for read-only
          lookups via GET /api/v1/balances.
    emoji: "💧"
    homepage: https://gateway.spraay.app
---

# Spraay Gateway

Spraay is a multi-chain x402 payment gateway. Its core capability is **batch payments**: pay up to 200 recipients in a single transaction with roughly 80% gas savings versus individual transfers. Around that core it exposes 190 endpoints (32 free, 150+ paid) across 37 categories on 15 mainnet chains (Base, Solana, Ethereum, Polygon, Arbitrum, XRP Ledger, Stellar, Bitcoin, Stacks, and more) — escrow, crypto payroll, robot task payments (RTP), GPU/compute, token data, and research.

Provenance: the Spraay payment toolset (batch, escrow, RTP) is merged into NVIDIA's NeMo-Agent-Toolkit-Examples (#27), ships as a community integration on the official Strands Agents documentation site (strandsagents.com/docs/integrations/tools/strands-spraay), and is merged into google/adk-python-community (#95) and aaif-goose/goose (#7525). Those projects are not affiliated with or endorsing Spraay; the citations describe where the tooling has been merged.

## Cost disclosure (read before using paid endpoints)

This skill is free and MIT-0. The Spraay Gateway it connects to is an **external paid service**. Free endpoints cost nothing and need no account. Paid endpoints require ONE of:

1. **Subscription API key** — Starter $29/mo (1,000 API calls/day) or Pro $99/mo (10,000 calls/day, priority support, Stripe customer portal), billed by Stripe. Checkout links: Starter https://buy.stripe.com/5kQcN675ndDa41Pce7enS00 · Pro https://buy.stripe.com/28EcN60GZ56EdCp91VenS01. Key arrives by email on signup. The human subscribes in their own browser; this skill never initiates or completes a purchase.
2. **x402 pay-per-call** — per-request USDC micropayment (typically $0.001–$0.50 per call, each 402 response states its exact price in its `accepts` array) from a wallet the user controls.

Note: batch payouts, payroll, and escrow move the **user's own funds** on top of any access fee. A subscription covers gateway access, not the capital being sent.

## Permissions and network access (explicit declaration)

This skill's full capability surface, stated so nothing is inferred:

- **Network:** outbound HTTPS to `gateway.spraay.app` only. The host is hardcoded and cannot be changed by environment variables, so `SPRAAY_API_KEY` is only ever sent to the official gateway. Requests are HTTPS-only and redirects are not followed. No other hosts, ever. The Stripe checkout links in this document are opened by the human in their own browser, never fetched by the skill.
- **Binaries:** `curl` only, for plain GET/POST requests. No pipes to shell, no downloaded code, no eval.
- **Filesystem:** `scripts/check-access.sh` writes nothing to disk. Batch workflows read a recipient file only when the user explicitly provides one.
- **Credentials:** reads `SPRAAY_API_KEY` from the environment and sends it only as an `X-API-Key` header to the gateway host above. Never logs, stores, or transmits it elsewhere. Private keys and seed phrases are never requested or handled.
- **Spending:** the skill itself cannot move money. Fund-moving gateway endpoints require the human-approval flow below; subscription checkout is always a human action in their own browser.

## Access check (run first)

Run `scripts/check-access.sh` before any paid operation. It reports which mode is active:

- **FREE MODE** (no `SPRAAY_API_KEY` set): free endpoints only. Fully usable for validating payouts, estimating gas savings, checking prices and chain status.
- **SUBSCRIBED** (`SPRAAY_API_KEY` set and valid): all 190 endpoints, no per-call payment.
- **KEY INVALID**: tell the user their key was rejected and to check their subscription in the Stripe customer portal (link in their signup email).

## Gating flow — what to do when a paid endpoint is needed and no key is set

1. Complete as much of the task as possible with free endpoints first (validate the batch, estimate savings, fetch prices). Show the user the concrete result — e.g. "Your 47-recipient payout validates cleanly and batching saves ~$X in gas."
2. Then present BOTH unlock options neutrally, exactly once:
   - "Subscribe (Starter, $29/mo, card, ~60 seconds): open https://spraay.app/#pricing in your browser, complete checkout, then set `SPRAAY_API_KEY` from your account page."
   - "Or pay per call with x402 from a funded wallet (no subscription)."
3. **Never** open the checkout URL yourself, simulate a purchase, or nag. If the user declines, continue in free mode without raising it again this session.
4. After the user reports subscribing, re-run `scripts/check-access.sh` to confirm the key works before proceeding.

## Human approval rules (non-negotiable)

- **Never initiate any payment, subscription, or checkout autonomously.** Subscribing is a human-in-browser action. x402 per-call payments require the user's explicit "yes" for each spend, with the amount stated.
- **Any endpoint that moves funds** (`/api/v1/batch/execute`, `/api/v1/escrow/create`, payroll runs, robot task dispatch) requires: (a) a prior dry run via `POST /free/validate-batch` and `GET /free/estimate-batch`, (b) a plain-language preview shown to the user — recipient count, total amount, token, chain, estimated fees — and (c) the user's explicit confirmation of that exact preview. No confirmation, no execution.
- Never request, read, or handle private keys or seed phrases. Signing happens in the user's own wallet tooling.

## Endpoint reference

Base URL: `https://gateway.spraay.app`

**Free (no key, no payment):**

| Endpoint | Purpose |
|---|---|
| `POST /free/validate-batch` | Dry-run validation of a batch payout (addresses, amounts, token, chain) |
| `GET /free/estimate-batch` | Gas/fee estimate and savings vs. individual transfers |
| `GET /free/prices` | Token price feed (ETH/USDC/SOL; full 100+ token feed is the paid `GET /api/v1/oracle/prices`) |
| `GET /free/chain-status` | Live status of all supported chains |

**Paid (subscription key or x402 per call) — most-used:**

| Endpoint | Purpose |
|---|---|
| `POST /api/v1/batch/execute` | Execute a batch payout (up to 200 recipients/tx) — CONFIRMATION REQUIRED |
| `POST /api/v1/escrow/create` | Create an escrow — CONFIRMATION REQUIRED |
| `GET /api/v1/tokens` | Supported token registry (currently open, no key needed) |
| `GET /api/v1/balances` | Balance lookups |
| `GET /api/v1/robots/list` | RTP robot registry |

The full 190-endpoint catalog (payroll, GPU/compute, search/RAG, supply chain, Bittensor, and more) is at https://docs.spraay.app. See `references/endpoints.md` in this skill for curl examples of the endpoints above.

**Authentication for subscribed calls:** send the key as the `X-API-Key` header. Verify a key any time with `GET /api/v1/usage` (200 = valid, also returns your daily-quota usage; 401 = invalid).

## Typical workflows

**Validate and price a payout (free, no signup):**
1. `POST /free/validate-batch` with the recipient list → confirm it's clean.
2. `GET /free/estimate-batch` → show the user their gas savings.
3. If they want to execute → gating flow above.

**Recurring payroll (subscribed):** validate → preview → user confirms → `POST /api/v1/batch/execute`. Never schedule autonomous future runs; each run gets its own confirmation.

**Escrowed job payment:** `POST /api/v1/escrow/create` after preview + confirmation; funds release per the escrow terms the user set.
