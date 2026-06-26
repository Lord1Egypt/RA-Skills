---
name: xero-accounting
description: Manage invoices, contacts, bills, payments, and accounting records in Xero via the Xero API. Use this skill when users want to create invoices, manage contacts, track payments, or automate Xero accounting workflows.
---

# Xero

![Xero](https://raw.githubusercontent.com/ClawLink-HQ/clawlink/main/public/images/brand-logos/xero.svg?v=2)

Manage Xero invoices, contacts, bills, payments, and accounting records from chat via the Xero API.

This skill uses [ClawLink](https://claw-link.dev/?utm_source=clawhub&utm_medium=referral&utm_content=xero-accounting) for hosted connection flows and credentials so you do not need to configure Xero API access yourself.

### Setup in 3 Steps

| Step 1: Install | Step 2: Pair Account | Step 3: Connect Xero |
|:---:|:---:|:---:|
| ![Install](https://raw.githubusercontent.com/ClawLink-HQ/clawlink/main/public/images/pairing/initialstep_1.gif) | ![Pair](https://raw.githubusercontent.com/ClawLink-HQ/clawlink/main/public/images/approve_process.gif) | *App-specific connection GIF coming soon* |
| Run the install command in OpenClaw | Sign in and approve the device | Open the dashboard and connect Xero |

## How It Works

```
┌─────────────────┐     ┌──────────────┐     ┌──────────────────┐
│   OpenClaw      │────▶│   ClawLink   │────▶│   Xero API       │
│   (User Chat)   │     │   (OAuth)    │     │                  │
└─────────────────┘     └──────────────┘     └──────────────────┘
         │                       │                       │
         │  1. Install Plugin    │                       │
         │  2. Pair Device       │                       │
         │  3. Connect Xero     │                       │
         │                       │  4. Secure Token       │
         │                       │  5. Proxy Requests    │
         │                       │                       │
         ▼                       ▼                       ▼
   ┌──────────┐           ┌──────────┐           ┌──────────┐
   │  SKILL   │           │ Dashboard│           │  Xero   │
   │  File    │           │ Auth     │           │  Tenant │
   └──────────┘           └──────────┘           └──────────┘
```

## Install

Install the verified ClawLink plugin from ClawHub. After the user confirms, complete the full setup so ClawLink tools are visible in the next OpenClaw chat.

```bash
openclaw plugins install clawhub:clawlink-plugin
openclaw config set tools.alsoAllow '["clawlink-plugin"]' --strict-json
openclaw gateway restart
```

Then tell the user: "OpenClaw has been restarted. Send `/new` as a standalone message to start a fresh chat, then ask for Xero again."

## Quick Start

```bash
# List invoices
clawlink_call_tool --tool "xero_list_invoices" --params '{"status": "DRAFT"}'

# Get an invoice
clawlink_call_tool --tool "xero_get_invoice" --params '{"invoice_id": "INVOICE_ID"}'

# List contacts
clawlink_call_tool --tool "xero_list_contacts" --params '{}'
```

## Authentication

All Xero tool calls are authenticated automatically by ClawLink using the user's connected Xero account OAuth token.

**No API credentials are required in chat.** ClawLink stores the OAuth token securely and injects it into every Xero API request on the user's behalf.

### Getting Connected

1. Install the ClawLink plugin (see Install above).
2. Pair the plugin with `clawlink_begin_pairing` if it is not configured yet.
3. Open https://claw-link.dev/dashboard?add=xero and connect Xero.
4. Call `clawlink_list_integrations` to verify the connection is active.

## Connection Management

### List Connections

```bash
clawlink_list_integrations
```

**Response:** Returns all connected integrations. Look for `xero` in the list.

### Verify Connection

```bash
clawlink_list_tools --integration xero
```

**Response:** Returns the live tool catalog for Xero.

### Reconnect

If Xero tools are missing or the connection shows an error:

1. Direct the user to https://claw-link.dev/dashboard?add=xero
2. After they confirm, call `clawlink_list_integrations` to verify
3. Then call `clawlink_list_tools --integration xero`

## Security & Permissions

- Access is scoped to the Xero organization connected during OAuth setup.
- **All write operations (create invoice, approve, delete, payment) require explicit user confirmation.**
- Financial transactions (invoices, bills, payments) affect accounting records — always confirm details.
- Confirm before voiding or deleting invoices, as these actions affect financial reporting.
- Tax and currency amounts should always be verified against the Xero dashboard.

## Tool Reference

### Invoices

| Tool | Description | Mode |
|------|-------------|------|
| `xero_list_invoices` | List all invoices with status filters | Read |
| `xero_get_invoice` | Get invoice details including line items | Read |
| `xero_create_invoice` | Create a new invoice | Write |
| `xero_update_invoice` | Update an existing invoice's details | Write |
| `xero_void_invoice` | Void an invoice (marks as void, keeps record) | Write |
| `xero_delete_invoice` | Delete a draft invoice | Write |
| `xero_email_invoice` | Send an invoice to the contact via email | Write |
| `xero_get_invoice_as_pdf` | Download an invoice as PDF | Read |

### Bills (Purchase Invoices)

| Tool | Description | Mode |
|------|-------------|------|
| `xero_list_bills` | List all bills (purchase invoices) | Read |
| `xero_get_bill` | Get bill details | Read |
| `xero_create_bill` | Create a new bill | Write |
| `xero_update_bill` | Update an existing bill | Write |
| `xero_delete_bill` | Delete a draft bill | Write |
| `xero_approve_bill` | Approve a bill for payment | Write |

### Contacts

| Tool | Description | Mode |
|------|-------------|------|
| `xero_list_contacts` | List all contacts (customers and suppliers) | Read |
| `xero_get_contact` | Get contact details including addresses and contacts | Read |
| `xero_create_contact` | Create a new contact | Write |
| `xero_update_contact` | Update contact information | Write |
| `xero_delete_contact` | Delete a contact | Write |
| `xero_search_contacts` | Search contacts by name, email, or account number | Read |

### Payments

| Tool | Description | Mode |
|------|-------------|------|
| `xero_list_payments` | List all payments on invoices and bills | Read |
| `xero_create_payment` | Record a payment against an invoice or bill | Write |
| `xero_delete_payment` | Delete/void a payment | Write |
| `xero_get_payment` | Get details of a specific payment | Read |

### Items

| Tool | Description | Mode |
|------|-------------|------|
| `xero_list_items` | List all items/products | Read |
| `xero_get_item` | Get item details | Read |
| `xero_create_item` | Create a new item | Write |
| `xero_update_item` | Update an existing item | Write |
| `xero_delete_item` | Delete an item | Write |

### Accounts

| Tool | Description | Mode |
|------|-------------|------|
| `xero_list_accounts` | List all chart of accounts | Read |
| `xero_get_account` | Get account details | Read |
| `xero_create_account` | Create a new account | Write |
| `xero_update_account` | Update an account | Write |

### Bank Transactions

| Tool | Description | Mode |
|------|-------------|------|
| `xero_list_bank_transactions` | List bank transactions (deposits, withdrawals, transfers) | Read |
| `xero_get_bank_transaction` | Get bank transaction details | Read |
| `xero_create_bank_transaction` | Create a bank transaction | Write |
| `xero_delete_bank_transaction` | Delete a draft bank transaction | Write |

### Bank Feeds

| Tool | Description | Mode |
|------|-------------|------|
| `xero_list_bank_transfers` | List bank transfers | Read |
| `xero_create_bank_transfer` | Create a transfer between bank accounts | Write |

### Manual Journals

| Tool | Description | Mode |
|------|-------------|------|
| `xero_list_journals` | List journal entries | Read |
| `xero_get_journal` | Get a specific journal entry | Read |
| `xero_create_journal` | Create a manual journal entry | Write |

### Organisation

| Tool | Description | Mode |
|------|-------------|------|
| `xero_get_organisation` | Get organisation/company details | Read |
| `xero_list_currencies` | List currencies configured in the organisation | Read |

### Tracking Categories

| Tool | Description | Mode |
|------|-------------|------|
| `xero_list_tracking_categories` | List tracking categories (regions, departments) | Read |
| `xero_create_tracking_category` | Create a tracking category | Write |
| `xero_update_tracking_category` | Update a tracking category | Write |

## Code Examples

### List all draft invoices

```bash
clawlink_call_tool --tool "xero_list_invoices" \
  --params '{
    "status": "DRAFT",
    "page": 1
  }'
```

### Get invoice details

```bash
clawlink_call_tool --tool "xero_get_invoice" \
  --params '{
    "invoice_id": "INVOICE_ID"
  }'
```

### Create an invoice

```bash
clawlink_call_tool --tool "xero_create_invoice" \
  --params '{
    "contact_id": "CONTACT_ID",
    "type": "ACCREC",
    "status": "DRAFT",
    "line_items": [
      {
        "description": "Web development services - Phase 1",
        "quantity": 1,
        "unit_amount": 2500,
        "account_code": "200"
      }
    ]
  }'
```

### Record a payment

```bash
clawlink_call_tool --tool "xero_create_payment" \
  --params '{
    "invoice_id": "INVOICE_ID",
    "amount": 2500,
    "payment_date": "2025-06-07",
    "reference": "Payment via bank transfer"
  }'
```

### Create a contact

```bash
clawlink_call_tool --tool "xero_create_contact" \
  --params '{
    "name": "Acme Corporation",
    "email_address": "billing@acme.com",
    "account_number": "ACM-001"
  }'
```

### Get organisation details

```bash
clawlink_call_tool --tool "xero_get_organisation" \
  --params '{}'
```

## Discovery Workflow

1. Call `clawlink_list_integrations` to confirm Xero is connected.
2. Call `clawlink_list_tools --integration xero` to see the live catalog.
3. Treat the returned list as the source of truth. Do not guess or assume what tools exist.
4. If the user describes a capability but the exact tool is unclear, call `clawlink_search_tools` with a short query and integration `xero`.
5. If no Xero tools appear, direct the user to https://claw-link.dev/dashboard?add=xero.

## Execution Workflow

```
┌─────────────────────────────────────────────────────────────┐
│  READ OPERATIONS (Safe)                                     │
│  list → get → search → describe                             │
│                                                             │
│  Example: List invoices → Get invoice → Show line items     │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│  WRITE OPERATIONS (Require Confirmation)                    │
│  describe → preview → confirm → call                      │
│                                                             │
│  Example: Preview invoice creation → User approves → Create│
└─────────────────────────────────────────────────────────────┘
```

1. For unfamiliar tools, ambiguous requests, or any write action, call `clawlink_describe_tool` first.
2. Use the returned guidance, schema, `whenToUse`, `askBefore`, `safeDefaults`, `examples`, and `followups` to shape the call.
3. Prefer read, list, get, and search operations before writes when that reduces ambiguity.
4. For writes or anything marked as requiring confirmation, call `clawlink_preview_tool` first.
5. Execute with `clawlink_call_tool`. Pass confirmation only after the preview matches the user's intent.
6. If the tool call fails, report the real error. Do not invent results or restate the failure as a missing capability unless the live catalog supports that conclusion.

## Notes

- Xero uses `ACCREC` (accounts receivable) for sales invoices and `ACCPAY` (accounts payable) for bills.
- Invoice and bill IDs are unique within an organisation — use them directly for payments.
- Voiding an invoice keeps it in the system as a voided record for audit purposes.
- Currency amounts should match the organisation's configured currencies.
- Tracking categories (regions, departments) can be assigned to line items for reporting.
- Draft invoices must be approved or sent before they appear in financial reports.
- Contact IDs are required for creating invoices and bills — resolve from `xero_list_contacts` first.

## Error Handling

| Status / Error | Meaning |
|----------------|---------|
| Tool not found | The tool name does not exist in the current catalog. Verify with `clawlink_list_tools --integration xero`. |
| Missing connection | Xero is not connected. Direct the user to https://claw-link.dev/dashboard?add=xero. |
| `Invoice not found` | The invoice ID does not exist or belongs to a different organisation. |
| `Contact not found` | The contact ID does not exist. |
| `Account not found` | The account code does not exist in the chart of accounts. |
| `Invalid status transition` | The invoice cannot be updated in its current status (e.g., voiding an already-paid invoice). |
| `Validation error` | A required field is missing or has an invalid value. |
| `Duplicate invoice` | An invoice with the same number already exists. |
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

### Troubleshooting: Invoice Creation Fails

1. Verify the contact ID exists — use `xero_list_contacts` or `xero_search_contacts`.
2. Check that account codes are valid for line items.
3. Confirm the invoice type (`ACCREC` or `ACCPAY`) matches the intended purpose.
4. Ensure date formats are correct (ISO 8601 format recommended).

## Resources

- [Xero API Documentation](https://developer.xero.com/documentation/)
- [Xero API Overview](https://developer.xero.com/documentation/api/overview)
- [Xero OAuth Guide](https://developer.xero.com/documentation/auth-and-reporting/xero-oauth2)
- ClawLink: https://claw-link.dev/?utm_source=clawhub&utm_medium=referral&utm_content=xero-accounting
- ClawLink Docs: https://docs.claw-link.dev/openclaw
- ClawLink Verification: https://claw-link.dev/verify

---

**Powered by [ClawLink](https://claw-link.dev/?utm_source=clawhub&utm_medium=referral&utm_content=xero-accounting)** — an integration hub for OpenClaw

![ClawLink Logo](https://raw.githubusercontent.com/ClawLink-HQ/clawlink/main/public/images/logo/link_logo_black_small.png)