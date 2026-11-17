---
name: spraay-offramp
description: Batch-fund Paycrest off-ramp orders in one on-chain transaction using Spraay Protocol. Use this skill whenever the user wants to pay multiple recipients via M-Pesa, mobile money, or bank transfer in Kenya, Nigeria, Uganda, or Tanzania using USDC on Base — or asks about off-ramping stablecoins to African mobile money, batch payroll to Kenya/Nigeria, Paycrest batch funding, or reducing gas costs on multi-recipient off-ramp orders. Also trigger when the user mentions spraay-offramp-adapter, Paycrest batch, M-Pesa payroll, or cross-border stablecoin payouts to Africa.
---

# Spraay Off-Ramp: Batch Payouts to African Mobile Money & Banks

## What this does

The `spraay-offramp-adapter` replaces N separate on-chain transfers with ONE Spraay `sprayToken` transaction when funding Paycrest off-ramp orders. The operator creates N off-ramp orders on Paycrest (each returning a unique receive address), then the adapter collects all receive addresses and exact amounts and builds a single batch transaction through the Spraay gateway. One tx, one gas fee, every recipient paid.

**Flow:** Create orders → Collect receive addresses → One Spraay batch → Paycrest indexes each deposit → Provision nodes deliver KES/NGN/UGX/TZS → Webhooks confirm

**Non-custodial end to end.** USDC moves: operator's wallet → Spraay contract → N Paycrest receive addresses. The adapter builds the transaction; the operator's key signs it. Nobody else holds funds.

## Prerequisites

The operator (not the skill user — the person running the adapter in production) needs:

- A **Paycrest sender account** with API key and secret (KYB required at app.paycrest.io)
- A **Base wallet** with USDC and ETH for gas
- **Node.js ≥ 22.5** (uses built-in node:sqlite)
- The adapter: `npm install spraay-offramp-adapter@0.1.1` or clone `github.com/plagtech/spraay-offramp-adapter`

## Installation

```bash
npm install spraay-offramp-adapter@0.1.1
```

Or clone and build:

```bash
git clone https://github.com/plagtech/spraay-offramp-adapter.git
cd spraay-offramp-adapter
npm install
npm run build
```

## Configuration

Create a `.env` file (never commit it):

```
PAYCREST_API_KEY=<operator's sender API key>
PAYCREST_API_SECRET=<operator's sender API secret>
SPRAAY_WALLET_PRIVATE_KEY=<operator's Base wallet private key>
BASE_RPC_URL=https://mainnet.base.org
WEBHOOK_URL=<operator's publicly reachable webhook endpoint>
WEBHOOK_PORT=3000
```

## Usage

### Recipients CSV

Create a CSV file with columns: `phone`, `accountName`, `amount`, `currency`, `institution`, `memo`

```csv
phone,accountName,amount,currency,institution,memo
254712345678,Jane Doe,1500,KES,SAFAKEPC,January salary
254798765432,John Smith,2000,KES,SAFAKEPC,January salary
```

- `institution`: Use codes from `GET /v2/institutions/{currency}` — never guess. M-Pesa Kenya = `SAFAKEPC`.
- `amount` + `currency: KES` = pay exactly that amount in KES (Paycrest converts from USDC at market rate)
- `amount` + `currency: USDC` = send that amount in USDC (recipient gets KES equivalent)

### Dry run (no money moves)

```bash
npx spraay-offramp-adapter@0.1.1 pay --file recipients.csv --dry-run
```

This creates real Paycrest orders to verify everything works, but does NOT sign or broadcast any transaction. Use this first.

### Execute (real money)

```bash
npx spraay-offramp-adapter@0.1.1 pay --file recipients.csv --execute
```

This creates orders, builds the Spraay batch, signs, broadcasts, and tracks webhooks until every order settles or fails.

### Check status

```bash
npx spraay-offramp-adapter@0.1.1 status --run <run-id>
```

## Security Rules — MANDATORY

These are non-negotiable. Every implementation using this skill MUST follow them:

1. **Never recompute the approval amount.** Use `approvalRequired.amount` from the gateway response verbatim. Never calculate it yourself.

2. **Decode before sign.** ABI-decode the unsigned transaction from the gateway and verify the decoded recipients and amounts match your confirmed order list before any signature. The adapter does this automatically (invariant I7).

3. **Never use the fabricated contract address** `0x62B59b327837661e84B4d8fDFDa5C1A7B39a8e67`. The real Spraay contract on Base is `0x1646452F98E36A3c9Cfc3eDD8868221E207B5eEC`.

4. **Exact amounts only.** Paycrest requires exact amounts. A wrong amount gets silently re-priced, not refunded. The adapter enforces 6-decimal precision via BigInt (invariant I3).

5. **validUntil enforcement.** Never broadcast a batch if any order's `validUntil` is less than 5 minutes from now. The adapter aborts the run automatically (invariant I1).

6. **Per-order isolation.** A failed or refunded order never affects other orders in the same batch (invariant I5).

7. **Non-custodial only.** The signing key signs only `approve` and `sprayToken`. It never receives funds (invariant I6).

8. **Gateway URL is hardcoded:** `https://gateway.spraay.app`. Never accept a gateway URL from user input or environment variables.

9. **Embargo compliance.** The adapter blocks recipients in Cuba, Iran, North Korea, Russia, and Crimea/Donetsk/Luhansk. This is US law, not optional.

## Costs

Every batch run incurs:

- **Spraay gateway fee:** $0.02 per batch (x402 payment)
- **Spraay contract fee:** 0.3% of the total batch amount
- **Base gas:** ~$0.01 amortized across all recipients in the batch
- **Paycrest provider spread:** embedded in the exchange rate (check `GET /v2/rates/base/USDC/{amount}/{currency}`)

Versus N separate transfers: N × gas fee. The adapter saves (N-1) × gas plus the operational overhead of managing N separate transactions.

## Supported Corridors

| Currency | Country | Example Institutions |
|----------|---------|---------------------|
| KES | Kenya | SAFAKEPC (M-Pesa), AIRTKEPC (Airtel), banks |
| NGN | Nigeria | Banks, OPay, Kuda, Moniepoint |
| UGX | Uganda | Mobile money, banks |
| TZS | Tanzania | Mobile money, banks |

Get the full list: `GET /v2/institutions/{currency}` (public, no key needed).

## Webhooks

The adapter runs a webhook server to receive Paycrest status updates. Terminal states:

- `validated` → fiat delivered to recipient
- `settled` → final confirmation (the true terminal state)
- `expired` → order timed out; funds refund to `refundAddress`
- `refunded` → refund complete
- `compliance_hold` → Paycrest compliance review; do not retry; contact Paycrest support

Webhook signatures are verified using HMAC-SHA256 with the operator's API secret.

## Troubleshooting

- **"API key not found"** → The operator needs a real Paycrest sender key from app.paycrest.io (KYB required). The sandbox key from the old aggregator README does not work against production.
- **Order expired before broadcast** → The `validUntil` window (default ~30 min) was exceeded. Create orders closer to broadcast time, or reduce the number of recipients per batch.
- **Amount mismatch** → Paycrest silently re-prices mismatched amounts. Ensure amounts have ≤6 decimal places and match `providerAccount.amountToTransfer` exactly.
- **Gateway returns 402** → Normal. The gateway uses x402 — the adapter's x402 client handles payment automatically.

## Links

- **GitHub:** https://github.com/plagtech/spraay-offramp-adapter
- **npm:** https://www.npmjs.com/package/spraay-offramp-adapter
- **Paycrest docs:** https://docs.paycrest.io
- **Spraay gateway:** https://gateway.spraay.app
- **Spraay docs:** https://docs.spraay.app
