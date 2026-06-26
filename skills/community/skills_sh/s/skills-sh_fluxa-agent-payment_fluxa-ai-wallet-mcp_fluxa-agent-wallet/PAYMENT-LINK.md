# Payment Link — CLI Reference

## Overview

Payment Links allow the agent to create shareable payment URLs to **receive** USDC. Useful for invoicing, selling content, collecting tips, or any scenario where the agent needs to get paid.

## End-to-End Flow

```
1. Agent creates a payment link via CLI
2. Agent shares the returned URL with payers
3. Payers open the URL and pay (or agent pays programmatically via x402)
4. Agent checks payments received via CLI
```

## Command Reference

### Create Payment Link

```bash
fluxa-wallet paymentlink-create \
  --amount "5000000" \
  --desc "AI Research Report" \
  --max-uses 100 \
  --expires "2026-02-11T00:00:00.000Z"
```

**Options:**

| Option | Required | Default | Description |
|--------|----------|---------|-------------|
| `--amount` | Yes | — | Amount in atomic units |
| `--desc` | No | — | Description |
| `--resource` | No | — | Resource content delivered after payment |
| `--expires` | No | — | Expiry date (ISO 8601) |
| `--max-uses` | No | — | Maximum number of payments |
| `--network` | No | `base` | Network |

**Output:**

```json
{
  "success": true,
  "data": {
    "paymentLink": {
      "linkId": "lnk_a1b2c3d4e5",
      "amount": "5000000",
      "currency": "USDC",
      "network": "base",
      "description": "AI Research Report",
      "status": "active",
      "expiresAt": "2026-02-11T00:00:00.000Z",
      "maxUses": 100,
      "useCount": 0,
      "url": "https://wallet.fluxapay.xyz/pay/lnk_a1b2c3d4e5",
      "createdAt": "2026-02-04T12:00:00.000Z"
    }
  }
}
```

Share the `url` value with payers.

### List Payment Links

```bash
fluxa-wallet paymentlink-list --limit 20
```

**Options:**

| Option | Required | Default | Description |
|--------|----------|---------|-------------|
| `--limit` | No | — | Max number of results |

### Get Payment Link Details

```bash
fluxa-wallet paymentlink-get --id lnk_a1b2c3d4e5
```

### Update Payment Link

```bash
# Disable a link
fluxa-wallet paymentlink-update --id lnk_a1b2c3d4e5 --status disabled

# Update description
fluxa-wallet paymentlink-update --id lnk_a1b2c3d4e5 --desc "SOLD OUT"

# Remove expiry limit
fluxa-wallet paymentlink-update --id lnk_a1b2c3d4e5 --expires null

# Remove max uses limit
fluxa-wallet paymentlink-update --id lnk_a1b2c3d4e5 --max-uses null
```

**Options (all optional except `--id`):**

| Option | Required | Description |
|--------|----------|-------------|
| `--id` | Yes | Payment link ID |
| `--desc` | No | New description |
| `--resource` | No | New resource content |
| `--status` | No | `active` or `disabled` |
| `--expires` | No | New expiry (ISO 8601), `null` to clear |
| `--max-uses` | No | New max uses, `null` to clear |

### Delete Payment Link

```bash
fluxa-wallet paymentlink-delete --id lnk_a1b2c3d4e5
```

### View Payments Received

```bash
fluxa-wallet paymentlink-payments --id lnk_a1b2c3d4e5 --limit 10
```

**Options:**

| Option | Required | Default | Description |
|--------|----------|---------|-------------|
| `--id` | Yes | — | Payment link ID |
| `--limit` | No | — | Max number of results |

**Output:**

```json
{
  "success": true,
  "data": {
    "payments": [
      {
        "id": 1,
        "payerAddress": "0xBuyerAddr...",
        "amount": "5000000",
        "currency": "USDC",
        "settlementStatus": "settled",
        "settlementTxHash": "0xabcdef...",
        "createdAt": "2026-02-05T10:30:00.000Z"
      }
    ]
  }
}
```

### List All Received Records

List all received payment records across all payment links (including Unify Payment Links).

```bash
fluxa-wallet received-records --limit 20 --offset 0
```

**Options:**

| Option | Required | Default | Description |
|--------|----------|---------|-------------|
| `--limit` | No | 20 | Max number of results (max 100) |
| `--offset` | No | 0 | Pagination offset |

**Output:**

```json
{
  "success": true,
  "data": {
    "payments": [
      {
        "id": 1,
        "payerAddress": "0xPayerAddr...",
        "amount": "1000000",
        "currency": "USDC",
        "settlementStatus": "settled",
        "settlementTxHash": "0xabc123...",
        "sourceType": "payment_link",
        "description": "Premium API Access",
        "paymentLinkId": "pl_abc123xyz456",
        "payerEmail": "payer@example.com",
        "createdAt": "2026-03-24T13:00:00.000Z"
      }
    ]
  }
}
```

### Get Received Record Detail

Get a single received payment record by ID.

```bash
fluxa-wallet received-record --id 1
```

**Options:**

| Option | Required | Description |
|--------|----------|-------------|
| `--id` | Yes | Payment record ID |

**Output includes extra fields:** `network`, `payTo` (in addition to list fields).

## Refunds

Refund a previously received payment-link payment. Requires user approval via `refundUrl` (same UX as payout approval). Only the receiving agent can initiate a refund.

### Refund status lifecycle

```
pending ─► settled    (user signed refundUrl, tx on-chain)
        ├► cancelled  (agent cancelled before signing)
        └► expired    (user didn't sign within 24h)
```

### Initiate a Refund

```bash
# Full refund
fluxa-wallet paymentlink-refund-create --payment-id 49217

# Partial refund with reason
fluxa-wallet paymentlink-refund-create \
  --payment-id 49217 \
  --amount 500000 \
  --reason "Partial refund — customer returned half"
```

**Options:**

| Option | Required | Description |
|--------|----------|-------------|
| `--payment-id` | Yes | Payment record ID (numeric, from `received-records` or `paymentlink-payments`) |
| `--amount` | No | Amount in atomic units — omit for full refund |
| `--reason` | No | Free-form text, stored with the refund |

**Output:**

```json
{
  "success": true,
  "data": {
    "refundId": "plr_2UpZ54a6t2HTXsDTfiz_nZ-V",
    "refundUrl": "https://walletapi.fluxapay.xyz/refundlink/plr_2UpZ54a6t2HTXsDTfiz_nZ-V",
    "paymentId": 49217,
    "amount": "10000",
    "currency": "USDC",
    "refundFrom": "0x...agent",
    "refundTo": "0x...payer",
    "refundType": "partial",
    "status": "pending",
    "expiresAt": "2026-04-20T14:36:34.082Z",
    "createdAt": "2026-04-19T14:36:34.082Z"
  }
}
```

`refundId` is a string (e.g. `plr_xxx`) — pass it as-is to `paymentlink-refund-get` and `paymentlink-refund-cancel`.

**Next step:** share `refundUrl` with the user so they can sign — use the "Opening Authorization URLs" pattern from `SKILL.md`. Without user signature the refund will expire in 24h.

### List Refunds

```bash
fluxa-wallet paymentlink-refund-list --limit 20 --offset 0
```

| Option | Required | Default | Description |
|--------|----------|---------|-------------|
| `--limit` | No | 20 | Max results (max 100) |
| `--offset` | No | 0 | Pagination offset |

### Get Refund Detail

```bash
fluxa-wallet paymentlink-refund-get --id plr_2UpZ54a6t2HTXsDTfiz_nZ-V
```

Returns the full refund object including `status`, `refundTxHash` (once settled), `originalAmount`, `originalTxHash`.

### Cancel a Pending Refund

```bash
fluxa-wallet paymentlink-refund-cancel --id plr_2UpZ54a6t2HTXsDTfiz_nZ-V
```

Only `pending` refunds can be cancelled. Settled refunds cannot be reversed (they're on-chain).

### Scripted Example — Refund the latest payment

```bash
#!/bin/bash
CLI="fluxa-wallet"

# Find the most recent settled payment
PAYMENT_ID=$($CLI received-records --limit 1 | jq -r '.data.payments[0].id')

# Initiate full refund
RESULT=$($CLI paymentlink-refund-create --payment-id "$PAYMENT_ID" --reason "Duplicate charge")
REFUND_ID=$(echo "$RESULT" | jq -r '.data.refundId')
REFUND_URL=$(echo "$RESULT" | jq -r '.data.refundUrl')

echo "Refund $REFUND_ID created. Ask the user to sign: $REFUND_URL"

# Poll status (after user signs)
$CLI paymentlink-refund-get --id "$REFUND_ID" | jq '.data.status'
```

## Paying TO a Payment Link

To pay a payment link programmatically (agent-to-agent payments), use the x402 flow documented in [X402-PAYMENT.md](X402-PAYMENT.md).

**Quick reference:**
```
1. curl -s <payment_link_url>                    → Get 402 payload
2. mandate-create --desc "..." --amount <amount> → Create mandate
3. User signs at authorizationUrl                → Mandate becomes "signed"
4. x402 --mandate <id> --payload "$PAYLOAD"       → Get xPaymentB64
5. curl -H "X-Payment: <x402 object>" <url>            → Submit payment
```

Payment link URL format: `https://walletapi.fluxapay.xyz/paymentlink/<link_id>`

## Scripted Example

```bash
#!/bin/bash
CLI="fluxa-wallet"

# Create a payment link
RESULT=$($CLI paymentlink-create --amount "1000000" --desc "Test payment link")

LINK_ID=$(echo "$RESULT" | jq -r '.data.paymentLink.linkId')
URL=$(echo "$RESULT" | jq -r '.data.paymentLink.url')

echo "Created payment link: $URL"

# Check for payments
$CLI paymentlink-payments --id "$LINK_ID" | jq
```

## Use Cases

| Scenario | Configuration |
|----------|--------------|
| One-time invoice | `--max-uses 1` |
| Limited-time sale | `--expires "<date>"` |
| Tip jar / donation | No limits |
| Digital goods | `--resource "Download link: ..."` |
| Batch collection | High `--max-uses`, track via `paymentlink-payments` |
| Agent-to-agent payment | Use x402 flow above |
