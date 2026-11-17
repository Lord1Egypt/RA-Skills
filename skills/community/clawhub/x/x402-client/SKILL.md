---
name: x402-client
version: 1.0.0
description: "x402 payment client for AI agents — how to automatically respond to HTTP 402 challenges, pay via CDP/Permit2, retry with PAYMENT-SIGNATURE, and settle the full x402 flow. For consuming pay-per-request APIs without API keys or subscriptions."
metadata:
  openclaw:
    emoji: "⚡"
    requires:
      bins: ["curl"]
    homepage: "https://www.x402.org"
---

# x402 Client

How to consume x402-enabled APIs: when a server returns HTTP 402 PAYMENT-REQUIRED, pay the exact amount and retry with the payment signature.

## What Is x402?

x402 is a payments protocol for the internet built on HTTP. It lets agents pay per request with USDC on Base (eip155:8453), no API keys, no subscriptions, no human in the loop.

Flow:
1. POST to an x402 endpoint without payment
2. Server responds HTTP 402 with payment requirements
3. Agent pays the exact amount (USDC on Base)
4. Agent retries the same request with PAYMENT-SIGNATURE header
5. Server verifies settlement and returns the response

## Step 1: Trigger the 402

```bash
curl -s -X POST https://api.example.com/services/your-service/jobs \
  -H "Content-Type: application/json" \
  -d '{"url": "https://example.de"}'
```

Expected response (HTTP 402):

```json
{
  "x402Version": 2,
  "error": "PAYMENT-SIGNATURE header is required",
  "resource": {"url": "https://api.example.com/services/your-service/jobs"},
  "accepts": [
    {
      "scheme": "exact",
      "network": "eip155:8453",
      "amount": "50000",
      "asset": "0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913",
      "payTo": "0x1c8b3C34Dca2Ba2A71598f1F9E0BC2a04A0Bea36",
      "maxTimeoutSeconds": 3600,
      "extra": {"name": "USD Coin", "version": "2", "priceUsdc": "0.05"}
    }
  ]
}
```

## Step 2: Pay

Amounts are in **atomic units** (6 decimals for USDC): `amount: "50000"` = $0.05.

Send `amount` microunits of `asset` (USDC) on `network` (Base) to `payTo` from your agent wallet.

Ways to pay:
- **CDP Agent Wallet** (Coinbase Developer Platform): `cdp wallet transfer` with USDC
- **Permit2** (Uniswap-style): approve + permit + transferFrom flow
- **Any EVM wallet**: direct USDC ERC-20 transfer

Save the transaction hash — it becomes your PAYMENT-SIGNATURE.

## Step 3: Retry with Signature

```bash
curl -s -X POST https://api.example.com/services/your-service/jobs \
  -H "Content-Type: application/json" \
  -H "PAYMENT-SIGNATURE: 0x<tx_hash>" \
  -d '{"url": "https://example.de"}'
```

The server verifies the tx hash via its facilitator (e.g. CDP `/verify` then `/settle`), confirms the exact amount and payTo match, then queues or returns the result.

## Step 4: Get the Result

Some services return the result directly in the retry response. Others queue a job:

```bash
curl -s https://api.example.com/services/your-service/jobs/<job_id>/result
```

## Idempotency & Retries

Never blindly retry a failed payment call — you can pay twice:
- Rejected before authorization → request a fresh quote
- Authorized but not settled → inspect or safely resubmit
- Settled but response lost → re-fetch the result with the same operation ID
- Fulfillment failed after settlement → invoke the provider's refund/dispute rule

## Discovery

Before paying, check the service's machine-readable manifest:
- `https://service.example/.well-known/x402` or `/.well-known/x402.json`
- `https://service.example/llms.txt`
- `https://service.example/promo/catalog.json`

These list all endpoints, prices (in USDC), payTo addresses, and input schemas — so you know the price before triggering the 402.

## Example Live Services

- **Hermes Commerce (DACH compliance)**: https://agent.kihustle.tech/.well-known/x402 — Impressum/DSGVO/BFSG/cookie checks, $0.01-$0.50, Base USDC
- **VerdictSwarm (token risk)**: https://api.vswarm.io/.well-known/x402 — pre-trade risk verdicts on Solana/Base

## Caveats

- Check `maxTimeoutSeconds` — some services run async jobs after settlement
- Amounts are atomic units (6 decimals USDC)
- Keep your wallet balance sufficient for the exact amount
- Payment is final — no refunds unless the service declares them