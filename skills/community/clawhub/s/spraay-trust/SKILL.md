---
name: spraay-trust
description: >-
  Verify before you pay. Free address safety screening (phishing, sanctions,
  exploits, mixers), free token safety checks (honeypot, sell tax, blacklist),
  free transaction decoding, and paid multi-dimensional agent trust scores
  via ProofLayer — all through the Spraay x402 gateway. Use when the user
  asks to verify an agent or wallet, check a trust score or reputation, vet
  a counterparty before a payment or escrow, screen an address for safety,
  check if a token is a honeypot, or decode a transaction.
version: 1.0.0
homepage: https://spraay.app
metadata:
  openclaw:
    emoji: "💧"
    requires:
      bins:
        - curl
        - jq
      env:
        - SPRAAY_GATEWAY_URL
    primaryEnv: SPRAAY_GATEWAY_URL
    envVars:
      - name: SPRAAY_GATEWAY_URL
        required: true
        description: >-
          Spraay x402 gateway base URL (https://gateway.spraay.app).
          All API calls go exclusively to this endpoint.
---

# Spraay Trust & Safety 💧

Verify before you pay. Free safety screening plus ProofLayer trust scoring
for agent-to-agent commerce, via the Spraay x402 gateway.

All requests in this skill go exclusively to the user's configured
`SPRAAY_GATEWAY_URL`. No data is sent to any other external endpoint.

## Important Notes

**A trust score is a signal, not a guarantee.** Scores are derived from
on-chain signals, reliability history, and reputation data. A high score
reduces risk; it does not eliminate it. For meaningful amounts, combine a
trust check with escrow (see the `spraay-escrow` skill) rather than relying
on either alone.

**New agents score low by default.** An unscored or low-scored agent is not
necessarily malicious — it may simply be new. Treat "no history" and "bad
history" differently when advising the user.

## Setup

The gateway URL must be set in your environment or `openclaw.json`:

```
SPRAAY_GATEWAY_URL=https://gateway.spraay.app
```

No API key is needed. The paid trust score endpoint uses the x402 HTTP
payment protocol (HTTP 402 → pay → retry). An x402-compatible wallet
(Coinbase CDP or similar) handles this automatically. The three safety
endpoints are completely free.

## Workflows

### Address Safety Screen — FREE

Screen any recipient before sending funds: phishing, sanctions, exploit
involvement, mixer usage, malicious contracts.

```bash
curl "$SPRAAY_GATEWAY_URL/api/v1/address/safety?address=0xABC...123"
```

Run this before every first-time payment. It costs nothing.

### Token Safety Check — FREE

Pre-trade token check: honeypot detection, sell tax, mint/blacklist
functions, proxy risk. GoPlus-powered with Spraay severity scoring.

```bash
curl "$SPRAAY_GATEWAY_URL/api/v1/token/safety?address=0xTOKEN...&chain=base"
```

### Decode a Transaction — FREE

Plain-English summary plus structured token transfers for any EVM
transaction — swaps, transfers, approvals, wraps, NFTs, batch payments.
Use it to verify what a transaction actually did.

```bash
curl "$SPRAAY_GATEWAY_URL/api/v1/tx/decode?hash=0xTXHASH...&chain=base"
```

### Agent Trust Score — $0.03

Multi-dimensional wallet/agent trust score via ProofLayer: financial,
reliability, trust, and social axes, plus XMTP reputation and on-chain
signals. Counterparty due diligence for agent-to-agent payments.

```bash
curl "$SPRAAY_GATEWAY_URL/api/v1/trust/score?address=0xABC...123"
```

If you receive HTTP 402, the response body contains payment instructions. Pay
the facilitator, then retry with the `X-PAYMENT` header containing the proof.

### Interpreting Results

- **Safety screen fails** (sanctions, phishing, exploits) — recommend
  against transacting, full stop.
- **Safety clean + strong trust score** — established counterparty. Direct
  payment is reasonable for routine amounts.
- **Safety clean + weak or moderate score** — some history. Use escrow for
  anything non-trivial.
- **Safety clean + no score / no history** — new agent. Not a red flag by
  itself; use escrow and small amounts first.

### Recommended Pre-Payment Flow

1. Run the free address safety screen. Hard stop on sanctions/phishing hits.
2. For agent counterparties or larger amounts, fetch the trust score
   ($0.03).
3. Based on results: pay directly (`spraay-payments`), escrow first
   (`spraay-escrow`), or decline.
4. After payment, decode the transaction (free) to confirm what happened
   on-chain.

## Free Endpoints

These require no x402 payment:

- `GET /api/v1/address/safety` — Address safety screen
- `GET /api/v1/token/safety` — Token honeypot/risk check
- `GET /api/v1/tx/decode` — Transaction decoder
- `GET /health` — Gateway health check

## x402 Payment Flow

1. Call the trust score endpoint.
2. Receive HTTP 402 with payment details (`accepts` array with amount,
   asset, and payment address).
3. Agent wallet sends the micropayment ($0.03 in USDC on Base).
4. Retry the request with the `X-PAYMENT` proof header.
5. Receive the response.

## Error Handling

- `402` — Payment required. Follow instructions in response body.
- `400` — Bad request. Check the address/hash format.
- `404` — No record for this address (new agent — see interpretation notes).
- `500` — Server error. Retry after a moment.

## Tips

- The safety screen is free — run it before every first payment, always.
- Reserve the paid trust score for agent counterparties and larger amounts.
- Pair a weak/no-score result with `spraay-escrow` instead of refusing
  outright.
- Decode transactions after the fact to verify delivery of on-chain work.

## Links

- App: https://spraay.app
- ProofLayer: https://prooflayer.net
- Docs: https://docs.spraay.app
- GitHub: https://github.com/plagtech
