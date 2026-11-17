---
name: woocommerce-spraay-payouts
version: 1.1.0
description: Batch USDC payouts for WooCommerce stores via Spraay Protocol — read vendor commissions, build batches, estimate fees, and prepare payouts for merchant approval
publisher: plagtech
categories:
  - Finance
  - Integrations
  - E-commerce
keywords:
  - woocommerce
  - spraay
  - batch-payouts
  - usdc
  - vendor-payouts
  - supplier-payments
  - base
  - crypto-payouts
  - e-commerce
  - merchant
---

# WooCommerce Spraay Batch Payouts

Automate USDC batch payouts for WooCommerce merchants. This skill lets agents read pending vendor or supplier payment obligations from a WooCommerce store running the Spraay Batch Payouts plugin, build payout batches, estimate fees, and prepare transactions for merchant wallet approval.

## User Control & Approval Requirements

**All destructive or mutating actions on stored records require explicit merchant approval.** The agent MUST confirm with the merchant before:

- **Creating** a new recipient
- **Updating** any recipient field (especially wallet addresses)
- **Deleting** a recipient record

The agent must present a clear summary of the proposed change and wait for the merchant to confirm before executing. Example:

```
Agent: "I'd like to update Supplier A's wallet address from 0xabc...123 to 0xdef...456. Confirm? (yes/no)"
Merchant: "yes"
Agent: [executes PUT]
```

**Never silently modify or delete recipient records.** A changed wallet address routes real funds to a different destination — this is equivalent to changing a bank account number and must be treated with the same care as a payout.

**Recovery:** If a recipient is accidentally deleted, the agent should notify the merchant immediately with the deleted record's details (label, wallet address, email) so it can be recreated. The agent should retrieve recipient details with GET before executing a DELETE, and retain them in the conversation for recovery purposes.

## What This Skill Does

- Reads pending vendor commissions from WooCommerce (supports Product Vendors, Dokan, and manual suppliers)
- Builds batch payout proposals with recipient addresses and amounts
- Estimates Spraay protocol fees (0.3%) before execution
- Prepares unsigned transactions for merchant wallet signing
- Tracks batch status and on-chain confirmation

## Requirements

- A WooCommerce store with the **Spraay Batch Payouts for WooCommerce** plugin installed and activated
- The store must have a Spraay API key configured in plugin settings
- WordPress REST API must be accessible
- Merchant must have a browser wallet (MetaMask, Coinbase Wallet) for signing

## Architecture

This skill interacts with a WooCommerce store's REST API, NOT directly with the Spraay gateway. The plugin handles all gateway communication server-side via an API key.

```
Agent (this skill)
  → WooCommerce REST API (store's WordPress site)
    → Spraay plugin (PHP, server-side)
      → Spraay gateway (gateway.spraay.app)
        → Base blockchain (USDC settlement)
```

The agent never needs blockchain credentials. All on-chain operations require the merchant's explicit wallet signature.

## Authentication

The WooCommerce REST API requires authentication. Use one of:

- **Application Passwords** (recommended): WordPress 5.6+ built-in. The merchant generates one at Users → Profile → Application Passwords.
- **WooCommerce REST API keys**: Generated at WooCommerce → Settings → Advanced → REST API.

Use a dedicated store account with the minimum required WordPress role (`manage_woocommerce` capability). Do not use the site administrator account for routine agent operations.

```bash
# Application Password auth
curl -u "username:xxxx xxxx xxxx xxxx" \
  https://store.example.com/wp-json/spraay/v1/recipients
```

## Endpoints

All endpoints are under the `spraay/v1` namespace on the store's WordPress REST API.

### Recipients

**⚠ Approval required:** Agents MUST confirm with the merchant before creating, updating, or deleting recipients. See "User Control & Approval Requirements" above.

```bash
# List all recipients (read-only, no approval needed)
GET /wp-json/spraay/v1/recipients

# Get a single recipient (read-only, no approval needed)
GET /wp-json/spraay/v1/recipients/{id}

# Create a recipient (REQUIRES merchant approval first)
POST /wp-json/spraay/v1/recipients
Content-Type: application/json
{
  "label": "Supplier A",
  "wallet_address": "0x1234...abcd",
  "email": "supplier@example.com",
  "default_amount": "250.00"
}

# Update a recipient (REQUIRES merchant approval first — show old and new values)
PUT /wp-json/spraay/v1/recipients/{id}
{
  "label": "Supplier A (updated)",
  "default_amount": "300.00"
}

# Delete a recipient (REQUIRES merchant approval first — show what will be deleted)
# Always GET the recipient first to retain details for recovery
DELETE /wp-json/spraay/v1/recipients/{id}
```

### WooCommerce Data

```bash
# Get pending vendor commissions (if Product Vendors or Dokan is active)
GET /wp-json/spraay/v1/wc/commissions?status=unpaid

# Get supplier payment obligations from orders
GET /wp-json/spraay/v1/wc/suppliers?date_from=2026-10-01&date_to=2026-10-31
```

### Batches

```bash
# Create a new batch (draft)
POST /wp-json/spraay/v1/batches
Content-Type: application/json
{
  "items": [
    {"recipient_id": 1, "amount": "250.00"},
    {"recipient_id": 2, "amount": "400.00"},
    {"recipient_id": 3, "amount": "175.00"}
  ]
}
# Returns: batch object with id, status "draft", items, totals

# Estimate fees for a batch
POST /wp-json/spraay/v1/batches/{id}/estimate
# Returns: fee breakdown (payout total, 0.3% fee, total with fee, chain, supported status)

# Get batch details
GET /wp-json/spraay/v1/batches/{id}

# List all batches
GET /wp-json/spraay/v1/batches?status=confirmed&page=1&per_page=10

# Get batch history with filters
GET /wp-json/spraay/v1/batches?date_from=2026-10-01&date_to=2026-10-31
```

### Batch Lifecycle

A batch moves through these statuses:

1. **draft** — created, items added, not yet estimated
2. **estimated** — fee estimate received from Spraay gateway
3. **approved** — merchant has reviewed and approved (checkbox in admin UI)
4. **pending** — transaction signed and broadcast, awaiting on-chain confirmation
5. **confirmed** — on-chain settlement verified, tx_hash recorded
6. **failed** — transaction reverted or dropped

The agent can create batches and request estimates. The **approve → sign → submit** step requires the merchant's browser wallet and happens in the WordPress admin UI, not through the API. The agent should notify the merchant when a batch is ready for approval.

## Example Workflows

### Workflow 1: Weekly vendor payouts

```
1. Agent queries GET /wp-json/spraay/v1/wc/commissions?status=unpaid
2. Agent groups commissions by vendor wallet address
3. Agent creates a batch: POST /wp-json/spraay/v1/batches with the grouped items
4. Agent estimates fees: POST /wp-json/spraay/v1/batches/{id}/estimate
5. Agent notifies merchant: "Batch #42 ready for approval: 15 vendors, 4,250 USDC total, 12.75 USDC fee. Review at [admin link]."
6. Merchant approves and signs in WordPress admin
7. Agent checks status: GET /wp-json/spraay/v1/batches/{id} — sees "confirmed"
8. Agent reports: "Batch #42 confirmed on Base. Tx: 0xabc...def. All 15 vendors paid."
```

### Workflow 2: One-time supplier payment (with recipient approval)

```
1. Merchant tells agent: "Pay Acme Corp 500 USDC to 0x1234...abcd"
2. Agent checks if recipient exists: GET /wp-json/spraay/v1/recipients?search=acme
3. If not found, agent asks: "I'll create a new recipient — Acme Corp at 0x1234...abcd. Confirm?"
4. Merchant confirms → Agent creates: POST /wp-json/spraay/v1/recipients
5. Creates batch with single item
6. Estimates and notifies merchant for approval and signing
```

### Workflow 3: CSV bulk import (with recipient approval)

```
1. Merchant provides a CSV file with wallet addresses and amounts
2. Agent parses CSV and presents summary: "Found 12 new recipients. Here's the list: [table]. Create all?"
3. Merchant confirms → Agent creates recipients via POST /wp-json/spraay/v1/recipients (one per row)
4. Creates a batch with all items
5. Estimates and presents summary for approval
```

## Important Notes

- **Amounts are in human-readable USDC** (e.g., "250.00"), NOT raw base units. The plugin handles conversion internally.
- **The agent cannot execute payouts.** Only the merchant can sign transactions with their wallet. The agent's role is to prepare and present batches.
- **The agent must not silently modify records.** All recipient creates, updates, and deletes require explicit merchant confirmation before execution.
- **Noncustodial.** Neither the plugin, the agent, nor Spraay ever holds merchant funds or private keys.
- **Duplicate prevention.** The plugin tracks which WooCommerce orders have been included in confirmed batches and prevents double-payment.
- **Fee: 0.3%** of the batch total, collected on-chain by the Spraay smart contract. Shown in the estimate before approval.
- **Chain: Base (8453)** by default. USDC on Base: `0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913`.
- **Max 200 recipients per batch.**
- **Verify before every payout.** Before presenting a batch for signing, the agent should cross-check recipient wallet addresses against the stored records to ensure no unexpected changes occurred.

## Not Affiliated

This skill is published by Plagtech, the developer of Spraay Protocol. It is not affiliated with or endorsed by WooCommerce, Automattic, WordPress, Circle, Coinbase, or Base.

## Links

- Plugin: https://github.com/plagtech/spraay-batch-payouts-for-woocommerce
- Spraay Protocol: https://spraay.app
- Gateway docs: https://docs.spraay.app
- Privacy: https://spraay.app/privacy
- Terms: https://spraay.app/terms
