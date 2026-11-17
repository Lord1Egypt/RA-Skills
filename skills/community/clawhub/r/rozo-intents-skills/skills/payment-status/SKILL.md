---
name: payment-status
description: >
  Check the status of a Rozo cross-chain payment. Supports lookup by
  payment ID, source transaction hash, or deposit address + memo. Use
  when user asks about a Rozo/crypto payment — "check my crypto payment",
  "payment status", "where is my payment", "track payment", "is my
  payment done" — or provides a payment UUID, transaction hash, or
  deposit address. NOT for bank transfers, card payments, or other fiat
  payment tracking.
metadata:
  author: rozo
  version: 0.2.0
---

# Check Payment Status

## Runtime

All `node scripts/dist/*.js` commands below MUST run from the **plugin root**
(the directory containing `.claude-plugin/plugin.json`), not from this
skill's directory. When installed as a Claude Code plugin, the plugin root
is `${CLAUDE_PLUGIN_ROOT}`. If that env var isn't set, `cd` to the directory
that contains `scripts/dist/`, `skills/`, and `.claude-plugin/`.

**Do not `sleep` between polls.** Some harnesses block `sleep` in Bash
commands. If the payment is still processing, just re-run `get-payment.js`
again — Rozo typically confirms within 10–15 seconds end-to-end.

## Instructions

Check the status of a Rozo payment. Three lookup methods are supported.

### Step 1: Determine lookup method

The user may provide:
- **Payment ID** — a UUID (e.g., `550e8400-e29b-41d4-a716-446655440000`)
- **Transaction hash** — a source chain tx hash (Stellar, EVM, or Solana)
- **Deposit address + memo** — the receiverAddress and receiverMemo from the payment

If none is clear, ask:
> "How would you like to look up the payment? You can provide a payment ID, transaction hash, or deposit address with memo."

### Step 2: Check status

**By payment ID:**
```bash
node scripts/dist/get-payment.js --payment-id <uuid>
# or, equivalently:
node scripts/dist/get-payment.js --id <uuid>
```

**By source transaction hash:**
```bash
node scripts/dist/get-payment.js --tx-hash <hash>
```

**By deposit address + memo:**
```bash
node scripts/dist/get-payment.js --receiver-address <address> --receiver-memo <memo>
```

Note: Transaction hash and address+memo lookups search the last 7 days and return the most recent matching payment.

### Step 3: Present status

Display the payment details:
- **Payment ID**
- **Status** (see flow below)
- **Amount**: source and destination
- **Fee**
- **Created / Expires at** — convert UTC timestamps from the API to the user's local timezone
- **Transaction hashes** (if available)

**Important:** All timestamps from the Rozo API are in UTC. Always convert and display them in the local timezone of the machine (e.g., `new Date(utcString).toLocaleString()`).

### Payment Status Flow

```
payment_unpaid → payment_started → payment_payin_completed → payment_payout_completed → payment_completed
```

Other statuses: `payment_bounced`, `payment_expired`, `payment_refunded`

| Status | Meaning |
|--------|---------|
| payment_unpaid | Created, awaiting funding |
| payment_started | Funding detected, processing |
| payment_payin_completed | Source funds received |
| payment_payout_completed | Destination funds sent |
| payment_completed | Fully complete |
| payment_bounced | Payout failed |
| payment_expired | Not funded in time |
| payment_refunded | Funds returned to sender |

## Examples

### Example 1: By payment ID
User: "Check payment 550e8400-e29b-41d4-a716-446655440000"

1. Fetch by ID → "payment_started"
2. Show: "Your payment is processing. Source funds have been detected."

### Example 2: By transaction hash
User: "What's the status of this tx? 0x767f62ca..."

1. Detected as a transaction hash (starts with `0x`)
2. Fetch by tx hash → "payment_completed"
3. Show: "Payment complete! Destination received [amount] [token]."

### Example 3: By Stellar deposit address + memo
User: "Check payment to GB4CLV3U... with memo 83589538"

1. Detected as address + memo
2. Fetch by address+memo → "payment_payin_completed"
3. Show: "Source funds received, payout is being processed."

### Example 4: User unsure
User: "Is my payment done?"

1. Ask what info they have (payment ID, tx hash, or deposit address+memo)
2. Proceed with the appropriate lookup
