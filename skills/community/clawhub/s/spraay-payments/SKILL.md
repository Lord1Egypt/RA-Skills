---
name: spraay-payments
description: >-
  Send batch crypto payments and payroll using the Spraay x402 gateway.
  Supports Base, Ethereum, Arbitrum, Polygon, BNB Chain, Avalanche, Unichain,
  and more. Use when the user asks to send payments, batch transfer, pay
  multiple wallets, crypto payroll, create invoice, check balance, or resolve
  ENS/Basename addresses.
version: 1.1.0
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

# Spraay Payments 💧

Batch crypto payments and payroll via the Spraay x402 gateway.

All requests in this skill go exclusively to the user's configured
`SPRAAY_GATEWAY_URL`. No data is sent to any other external endpoint.

## Important Warnings

**Blockchain transactions are irreversible.** Once a batch payment or transfer
is executed on-chain, it cannot be undone. Always confirm the following with
the user before executing any payment:

- Recipient addresses are correct
- Token type and chain are intended
- Amounts are accurate
- The user understands x402 micropayment fees will be charged per API call

**Real funds are involved.** Every paid endpoint costs a small USDC
micropayment via the x402 protocol. Batch payments move real tokens on
real blockchains. Do not execute payments without explicit user confirmation.

## Setup

The gateway URL must be set in your environment or `openclaw.json`:

```
SPRAAY_GATEWAY_URL=https://gateway.spraay.app
```

No API key is needed. Payments are made per-request via the x402 HTTP payment
protocol (HTTP 402 → pay → retry). An x402-compatible wallet (Coinbase CDP
or similar) handles this automatically.

## Supported Chains

Base, Ethereum, Arbitrum, Polygon, BNB Chain, Avalanche, Unichain, Plasma, BOB.

Payment contract (Base): `0x1646452F98E36A3c9Cfc3eDD8868221E207B5eEC`

## Workflows

### Batch Payments

Send tokens to multiple wallets in one transaction. Saves 60-80% on gas
compared to individual transfers.

**Always confirm recipients, amounts, token, and chain with the user before
executing.**

```bash
curl -X POST "$SPRAAY_GATEWAY_URL/api/batch-payment" \
  -H "Content-Type: application/json" \
  -d '{
    "recipients": [
      {"address": "0xABC...123", "amount": "10"},
      {"address": "0xDEF...456", "amount": "25"}
    ],
    "token": "USDC",
    "chain": "base"
  }'
```

If you receive HTTP 402, the response body contains payment instructions. Pay
the facilitator, then retry with the `X-PAYMENT` header containing the proof.

### Payroll

Payroll uses the same batch payment endpoint. ENS and Basename addresses
resolve automatically.

**Always confirm the payroll roster with the user before sending.**

```bash
curl -X POST "$SPRAAY_GATEWAY_URL/api/batch-payment" \
  -H "Content-Type: application/json" \
  -d '{
    "recipients": [
      {"address": "alice.eth", "amount": "3000"},
      {"address": "bob.base", "amount": "2500"}
    ],
    "token": "USDC",
    "chain": "base",
    "memo": "March 2026 payroll"
  }'
```

### Check Token Balance

```bash
curl "$SPRAAY_GATEWAY_URL/api/balance?address=0xABC...&chain=base"
```

### Create Invoice

```bash
curl -X POST "$SPRAAY_GATEWAY_URL/api/create-invoice" \
  -H "Content-Type: application/json" \
  -d '{
    "recipient": "0xABC...123",
    "amount": "500",
    "token": "USDC",
    "chain": "base",
    "memo": "March consulting"
  }'
```

### Resolve ENS / Basename (Free — No Payment Required)

```bash
curl "$SPRAAY_GATEWAY_URL/api/resolve?name=vitalik.eth"
```

### Token Price (Free — No Payment Required)

```bash
curl "$SPRAAY_GATEWAY_URL/api/price?symbol=ETH"
```

Use this to show users the USD value of their payment before executing.

## Free Endpoints

These require no x402 payment:

- `GET /api/price?symbol=ETH` — Token prices
- `GET /api/resolve?name=vitalik.eth` — ENS/Basename resolution
- `GET /api/health` — Gateway health check
- `GET /api/chains` — List supported chains

## x402 Payment Flow

1. Call any paid endpoint.
2. Receive HTTP 402 with payment details.
3. Agent wallet sends micropayment to the facilitator.
4. Retry the request with the `X-PAYMENT` proof header.
5. Receive the response.

Typical cost: fractions of a cent in USDC on Base.

## Error Handling

- `402` — Payment required. Follow instructions in response body.
- `400` — Bad request. Check parameters.
- `404` — Endpoint not found.
- `500` — Server error. Retry after a moment.

## Tips

- Always confirm with the user before sending any payment.
- Use `/api/price` to show USD values before executing.
- Resolve ENS/Basenames first to validate addresses.
- Chain defaults to `base` if not specified.
- Token defaults to `USDC` if not specified.

## Links

- App: https://spraay.app
- Docs: https://docs.spraay.app
- GitHub: https://github.com/plagtech
