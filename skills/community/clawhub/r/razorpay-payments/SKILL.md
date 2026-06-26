---
name: razorpay-payments
description: Manage Razorpay customers, orders, invoices, payment links, refunds, payouts, and payment operations via the Razorpay API. Use when users want to inspect or manage payments, create and track invoices, process refunds, or automate payout workflows.
---

# Razorpay

![Razorpay](https://raw.githubusercontent.com/ClawLink-HQ/clawlink/main/public/images/brand-logos/razorpay.svg?v=2)

Manage Razorpay from chat — customers, orders, invoices, payment links, refunds, payouts, and payment operations via the Razorpay API.

This skill uses [ClawLink](https://claw-link.dev/?utm_source=clawhub&utm_medium=referral&utm_content=razorpay-payments) for hosted connection flows and credentials so you do not need to configure Razorpay API access yourself.

### Setup in 3 Steps

| Step 1: Install | Step 2: Pair Account | Step 3: Connect Razorpay |
|:---:|:---:|:---:|
| ![Install](https://raw.githubusercontent.com/ClawLink-HQ/clawlink/main/public/images/pairing/initialstep_1.gif) | ![Pair](https://raw.githubusercontent.com/ClawLink-HQ/clawlink/main/public/images/approve_process.gif) | *App-specific connection GIF coming soon* |
| Run the install command in OpenClaw | Sign in and approve the device | Open the dashboard and connect Razorpay |

## How It Works

```
┌─────────────────┐     ┌──────────────┐     ┌──────────────────┐
│   OpenClaw      │────▶│   ClawLink   │────▶│ Razorpay         │
│   (User Chat)   │     │   (OAuth)    │     │ (Payments API)    │
└─────────────────┘     └──────────────┘     └──────────────────┘
          │                       │                       │
          │  1. Install Plugin    │                       │
          │  2. Pair Device      │                       │
          │  3. Connect Razorpay  │                       │
          │                      │  4. Secure Token       │
          │                      │  5. Proxy Requests     │
          │                      │                       │
          ▼                      ▼                       ▼
    ┌──────────┐          ┌──────────┐          ┌──────────┐
    │  SKILL   │          │ Dashboard│          │ Razorpay │
    │  File    │          │ Auth     │          │ Dashboard│
    └──────────┘ └──────────┘          └──────────┘
```

## Install

Install the verified ClawLink plugin from ClawHub. After the user confirms, complete the full setup so ClawLink tools are visible in the next OpenClaw chat.

```bash
openclaw plugins install clawhub:clawlink-plugin
openclaw config set tools.alsoAllow '["clawlink-plugin"]' --strict-json
openclaw gateway restart
```

Then tell the user: "OpenClaw has been restarted. Send `/new` as a standalone message to start a fresh chat, then ask for Razorpay again."

## Quick Start

```bash
# List all payments
clawlink_call_tool --tool "razorpay_fetch_all_payments" --params '{"count": 10}'

# Create an order
clawlink_call_tool --tool "razorpay_create_an_order" --params '{"amount": 5000, "currency": "INR"}'

# Create an invoice
clawlink_call_tool --tool "razorpay_create_invoice" --params '{"amount": 5000, "currency": "INR", "description": "Invoice for services"}'
```

## Authentication

All Razorpay tool calls are authenticated automatically by ClawLink using the user's connected Razorpay account.

**No API key is required in chat.** ClawLink stores the credentials securely and injects them into every Razorpay API request on the user's behalf.

### Getting Connected

1. Install the ClawLink plugin (see Install above).
2. Pair the plugin with `clawlink_begin_pairing` if it is not configured yet.
3. Open https://claw-link.dev/dashboard?add=razorpay and connect Razorpay.
4. Call `clawlink_list_integrations` to verify the connection is active.

## Connection Management

### List Connections

```bash
clawlink_list_integrations
```

**Response:** Returns all connected integrations. Look for `razorpay` in the list.

### Verify Connection

```bash
clawlink_list_tools --integration razorpay
```

**Response:** Returns the live tool catalog for Razorpay.

### Reconnect

If Razorpay tools are missing or the connection shows an error:

1. Direct the user to https://claw-link.dev/dashboard?add=razorpay
2. After they confirm, call `clawlink_list_integrations` to verify
3. Then call `clawlink_list_tools --integration razorpay`

## Security& Permissions

- Access is scoped to the Razorpay account data accessible via the connected account.
- **All write operations require explicit user confirmation.** Before executing any create, update, or delete call, confirm the target resource and intended effect with the user.
- Destructive actions (cancel invoice, delete payment link, issue refund) are marked as high-impact and must be confirmed.
- Payment operations affect real money — confirm amounts, customer details, and intent before any write.

## Tool Reference

### Customers

| Tool | Description | Mode |
|------|-------------|------|
| `razorpay_create_customer` | Register a new customer | Write |
| `razorpay_get_customer` | Fetch customer details | Read |
| `razorpay_update_customer` | Update customer details | Write |
| `razorpay_fetch_all_customers` | List all customers | Read |

### Orders

| Tool | Description | Mode |
|------|-------------|------|
| `razorpay_create_an_order` | Create a payment order | Write |
| `razorpay_fetch_orders` | List orders with filters | Read |
| `razorpay_fetch_orders_by_id` | Fetch a specific order | Read |
| `razorpay_update_order` | Update order notes/metadata | Write |
| `razorpay_fetch_payments_by_order` | Get payments for an order | Read |

### Payments

| Tool | Description | Mode |
|------|-------------|------|
| `razorpay_fetch_all_payments` | List all payments | Read |
| `razorpay_fetch_all_refunds_for_a_payment` | List refunds for a payment | Read |
| `razorpay_list_disputes` | List payment disputes | Read |
| `razorpay_list_payment_downtimes` | Check payment method status | Read |

### Invoices

| Tool | Description | Mode |
|------|-------------|------|
| `razorpay_create_invoice` | Create a new invoice | Write |
| `razorpay_fetch_invoice_by_id` | Fetch invoice details | Read |
| `razorpay_fetch_all_invoices` | List all invoices | Read |
| `razorpay_update_invoice` | Update a draft invoice | Write |
| `razorpay_issue_an_invoice` | Issue/send a draft invoice | Write |
| `razorpay_cancel_invoice` | Cancel an issued invoice | Write |
| `razorpay_delete_invoice` | Delete a draft invoice | Write |
| `razorpay_send_or_resend_notification` | Send invoice notification | Write |

### Payment Links

| Tool | Description | Mode |
|------|-------------|------|
| `razorpay_create_payment_link` | Create a shareable payment link | Write |
| `razorpay_fetch_a_payment_link` | Fetch a payment link | Read |
| `razorpay_fetch_all_payment_links` | List all payment links | Read |
| `razorpay_update_payment_link` | Update a payment link | Write |
| `razorpay_cancel_payment_link` | Cancel a payment link | Write |
| `razorpay_notify_payment_link` | Send payment link reminder | Write |

### Refunds

| Tool | Description | Mode |
|------|-------------|------|
| `razorpay_fetch_refunds` | List all refunds | Read |
| `razorpay_fetch_all_refunds_for_a_payment` | List refunds for a payment | Read |

### Contacts & Fund Accounts (RazorpayX)

| Tool | Description | Mode |
|------|-------------|------|
| `razorpay_create_contact` | Create a contact | Write |
| `razorpay_get_contact` | Fetch contact details | Read |
| `razorpay_update_contact` | Update contact details | Write |
| `razorpay_list_fund_accounts` | List fund accounts | Read |
| `razorpay_get_fund_account` | Fetch a fund account | Read |
| `razorpay_list_fund_validations` | List account validations | Read |

### Items

| Tool | Description | Mode |
|------|-------------|------|
| `razorpay_create_item` | Create an invoice item | Write |
| `razorpay_get_item` | Fetch item details | Read |
| `razorpay_list_items` | List all items | Read |
| `razorpay_update_item` | Update an item | Write |
| `razorpay_delete_item` | Delete an item | Write |

### Settlements

| Tool | Description | Mode |
|------|-------------|------|
| `razorpay_get_settlement_recon` | Fetch settlement reconciliation | Read |
| `razorpay_get_transfer_reversals` | List transfer reversals | Read |

## Code Examples

### Create a payment order

```bash
clawlink_call_tool --tool "razorpay_create_an_order" \
  --params '{
    "amount": 250000,
    "currency": "INR",
    "receipt": "order_rcptid_1"
  }'
```

### Create an invoice

```bash
clawlink_call_tool --tool "razorpay_create_invoice" \
  --params '{
    "amount": 250000,
    "currency": "INR",
    "description": "Invoice for project services",
    "customer_id": "CUSTOMER_ID"
  }'
```

### Fetch all payments

```bash
clawlink_call_tool --tool "razorpay_fetch_all_payments" \
  --params '{
    "count": 20,
    "skip": 0
  }'
```

### Create a payment link

```bash
clawlink_call_tool --tool "razorpay_create_payment_link" \
  --params '{
    "amount": 50000,
    "currency": "INR",
    "description": "Payment for Order #1234",
    "customer_email": "customer@example.com"
  }'
```

## Discovery Workflow

1. Call `clawlink_list_integrations` to confirm Razorpay is connected.
2. Call `clawlink_list_tools --integration razorpay` to see the live catalog.
3. Treat the returned list as the source of truth. Do not guess or assume what tools exist.
4. If the user describes a capability but the exact tool is unclear, call `clawlink_search_tools` with a short query and integration `razorpay`.
5. If no Razorpay tools appear, direct the user to https://claw-link.dev/dashboard?add=razorpay.

## Execution Workflow

```
┌─────────────────────────────────────────────────────────────┐
│  READ OPERATIONS (Safe)                                      │
│  list → fetch → get → call                                   │
│                                                             │
│  Example: List payments → Fetch details → Show results       │
└─────────────────────────────────────────────────────────────┘
                               │
                               ▼
┌─────────────────────────────────────────────────────────────┐
│  WRITE OPERATIONS (Require Confirmation)                    │
│  list → describe → preview → confirm → call                  │
│                                                             │
│  Example: Describe tool → Preview changes → User approves  │
│           → Execute create                                   │
└─────────────────────────────────────────────────────────────┘
```

1. For unfamiliar tools, ambiguous requests, or any write action, call `clawlink_describe_tool` first.
2. Use the returned guidance, schema, `whenToUse`, `askBefore`, `safeDefaults`, `examples`, and `followups` to shape the call.
3. Prefer read, list, and get operations before writes when that reduces ambiguity.
4. For writes or anything marked as requiring confirmation, call `clawlink_preview_tool` first.
5. Execute with `clawlink_call_tool`. Pass confirmation only after the preview matches the user's intent.
6. If the tool call fails, report the real error. Do not invent results or restate the failure as a missing capability unless the live catalog supports that conclusion.

## Notes

- Razorpay amounts are in paise (smallest currency unit) — `amount: 5000` = ₹50.00.
- Only invoices in `draft` status can be updated or deleted.
- Only invoices in `issued` status can be cancelled.
- Payment links cannot be modified after expiry.
- Customer tokens (saved cards) require 2FA verification for retrieval.

## Error Handling

| Status / Error | Meaning |
|----------------|---------|
| Tool not found | The tool name does not exist in the current catalog. Verify with `clawlink_list_tools --integration razorpay`. |
| Missing connection | Razorpay is not connected. Direct the user to https://claw-link.dev/dashboard?add=razorpay. |
| `INVOICE_NOT_DRAFT` | Invoice is not in draft state — only draft invoices can be updated or deleted. |
| `PAYMENT_LINK_NOT_ACTIVE` | Payment link has expired or been cancelled. |
| `BAD_REQUEST` | Invalid parameters or missing required fields. Check the tool schema. |
| Write rejected | User did not confirm a write action. Always confirm before executing writes. |

### Troubleshooting: Tools Not Visible

1. Check that the ClawLink plugin is installed:
   ```bash
   openclaw plugins list
   ```
2. If the plugin is installed but tools are missing, tell the user to send `/new` as a standalone message to reload the catalog.
3. If a fresh chat does not help, run:
   ```bash
   openclaw config set tools.alsoAllow '["clawlink-plugin"]' --strict-json
   openclaw gateway restart
   ```
4. After restart, tell the user to send `/new` again and retry.

### Troubleshooting: Invalid Tool Call

1. Ensure the integration slug is exactly `razorpay`.
2. Use `clawlink_describe_tool` to verify parameter names and types before calling.
3. For write operations, always call `clawlink_preview_tool` first.

## Resources

- [Razorpay API Documentation](https://razorpay.com/docs/api/)
- [Razorpay Orders API](https://razorpay.com/docs/api/payments/orders/)
- [Razorpay Invoices API](https://razorpay.com/docs/api/invoices/)
- ClawLink: https://claw-link.dev/?utm_source=clawhub&utm_medium=referral&utm_content=razorpay-payments
- ClawLink Docs: https://docs.claw-link.dev/openclaw
- ClawLink Verification: https://claw-link.dev/verify

## Related Skills

- [Stripe](https://clawhub.ai/hith3sh/stripe-payments) — For global payment processing
- [QuickBooks](https://clawhub.ai/hith3sh/quickbooks-finance) — For accounting and bookkeeping

---

![ClawLink Logo](https://raw.githubusercontent.com/ClawLink-HQ/clawlink/main/public/images/logo/link_logo_black_small.png)
