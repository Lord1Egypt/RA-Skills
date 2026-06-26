---
name: xero
description: Interact with Xero accounting software - manage invoices, contacts, accounts, payments, and bank transactions
metadata: {"clawdbot":{"requires":{"env":["XERO_CLIENT_ID","XERO_CLIENT_SECRET"]},"primaryEnv":"XERO_CLIENT_ID","emoji":"📊","homepage":"https://github.com/TeddyEngel/XeroCli","source":"https://github.com/TeddyEngel/XeroCli"}}
---

# Xero Accounting Skill

Interact with Xero accounting software via CLI. Manage invoices, contacts, payments, bank transactions, and more. All commands output JSON for easy parsing.


## Script Directory

**Agent:** Determine this SKILL.md file's directory as `SKILL_DIR`, then run commands with:

```bash
npx -y bun ${SKILL_DIR}/scripts/cli.ts <command>
```


## Setup

### 1. Get Xero Credentials

Users need a Xero Developer account with API credentials:

1. Go to [developer.xero.com/app/manage](https://developer.xero.com/app/manage)
2. Create a **Web App**
3. Set redirect URI: `http://localhost:5001/callback`
4. Copy the **Client ID** and **Client Secret**

Note: If you see a scopes configuration page, add: `openid`, `offline_access`, `accounting.contacts`, `accounting.settings`, `accounting.invoices`, `accounting.payments`, `accounting.banktransactions`, `accounting.attachments`. If no scopes page is shown, that's fine - scopes are requested during OAuth.

> **Agent note:** If credentials are missing, ask the user for their Client ID and Secret.

### 2. Configure OpenClaw

Add credentials to `openclaw.json`:

```json
{
  "skills": {
    "xero": {
      "env": {
        "XERO_CLIENT_ID": "your_client_id",
        "XERO_CLIENT_SECRET": "your_client_secret"
      }
    }
  }
}
```

### 3. Authenticate

```bash
npx -y bun ${SKILL_DIR}/scripts/cli.ts auth login
```

This opens a browser for OAuth. Once complete, verify with:

```bash
npx -y bun ${SKILL_DIR}/scripts/cli.ts auth status
```


## Quick Reference

**Command prefix:** `npx -y bun ${SKILL_DIR}/scripts/cli.ts`

### Authentication

| Command | Description |
|---------|-------------|
| `auth login` | Start OAuth flow (opens browser) |
| `auth status` | Check authentication status |
| `auth logout` | Clear stored credentials |

### Organizations

| Command | Description |
|---------|-------------|
| `tenants list` | List connected Xero organizations |
| `tenants select <id>` | Switch active organization |

### Invoices

| Command | Description |
|---------|-------------|
| `invoices list` | List all invoices |
| `invoices list --status AUTHORISED` | Filter by status |
| `invoices list --contact <id>` | Filter by contact |
| `invoices get <id>` | Get invoice details |
| `invoices create --contact <id> --items '<json>'` | Create invoice |
| `invoices update <id> --status AUTHORISED` | Update status |

**Statuses:** `DRAFT`, `AUTHORISED`, `PAID`, `VOIDED`

**Types:** `ACCREC` (sales), `ACCPAY` (bills)

### Contacts

| Command | Description |
|---------|-------------|
| `contacts list` | List all contacts |
| `contacts list --search "name"` | Search by name |
| `contacts list --customers` | Only customers |
| `contacts list --suppliers` | Only suppliers |
| `contacts get <id>` | Get contact details |
| `contacts create --name "X" --email "Y"` | Create contact |

### Accounts

| Command | Description |
|---------|-------------|
| `accounts list` | List all accounts |
| `accounts list --type REVENUE` | Filter by type |
| `accounts list --class EXPENSE` | Filter by class |
| `accounts get <id>` | Get account details |

**Types:** `BANK`, `REVENUE`, `EXPENSE`, `FIXED`, `CURRENT`, `LIABILITY`, `EQUITY`, etc.

**Classes:** `ASSET`, `EQUITY`, `EXPENSE`, `LIABILITY`, `REVENUE`

### Bank Transactions

| Command | Description |
|---------|-------------|
| `banktransactions list` | List all transactions |
| `banktransactions list --type SPEND` | Filter by type |
| `banktransactions get <id>` | Get details |
| `banktransactions create ...` | Create transaction |
| `banktransactions attach <id> <file>` | Attach file |

**Types:** `SPEND`, `RECEIVE`, `RECEIVE-OVERPAYMENT`, `SPEND-OVERPAYMENT`

### Payments

| Command | Description |
|---------|-------------|
| `payments list` | List all payments |
| `payments list --invoice <id>` | Filter by invoice |
| `payments get <id>` | Get payment details |
| `payments create ...` | Create payment |
| `payments delete <id>` | Void payment |

### Allocations

| Command | Description |
|---------|-------------|
| `allocations list-overpayments` | List overpayments |
| `allocations list-prepayments` | List prepayments |
| `allocations list-creditnotes` | List credit notes |
| `allocations overpayment -o <id> -i <inv> -a <amt>` | Apply overpayment |
| `allocations prepayment -p <id> -i <inv> -a <amt>` | Apply prepayment |
| `allocations creditnote -c <id> -i <inv> -a <amt>` | Apply credit note |


## Examples

### Create an Invoice

```bash
# 1. Find the contact
npx -y bun ${SKILL_DIR}/scripts/cli.ts contacts list --search "Acme"

# 2. Get revenue account codes
npx -y bun ${SKILL_DIR}/scripts/cli.ts accounts list --type REVENUE

# 3. Create the invoice
npx -y bun ${SKILL_DIR}/scripts/cli.ts invoices create \
  --contact "<contact-id>" \
  --items '[{"description":"Consulting","quantity":10,"unitAmount":150,"accountCode":"200"}]' \
  --reference "INV-001"

# 4. Authorize when ready
npx -y bun ${SKILL_DIR}/scripts/cli.ts invoices update <invoice-id> --status AUTHORISED
```

### Record a Payment

```bash
# 1. Get bank account ID
npx -y bun ${SKILL_DIR}/scripts/cli.ts accounts list --type BANK

# 2. Create payment (marks invoice as paid)
npx -y bun ${SKILL_DIR}/scripts/cli.ts payments create \
  --invoice "<invoice-id>" \
  --account "<bank-account-id>" \
  --amount 500.00 \
  --reconciled
```

### Create a Contact

```bash
npx -y bun ${SKILL_DIR}/scripts/cli.ts contacts create \
  --name "Acme Corporation" \
  --email "billing@acme.com" \
  --customer
```

### Record Bank Transaction with Receipt

```bash
# 1. Create transaction
npx -y bun ${SKILL_DIR}/scripts/cli.ts banktransactions create \
  --type RECEIVE \
  --bank-account "<bank-id>" \
  --contact "<contact-id>" \
  --items '[{"description":"Payment","unitAmount":500,"accountCode":"200"}]'

# 2. Attach receipt
npx -y bun ${SKILL_DIR}/scripts/cli.ts banktransactions attach "<transaction-id>" ./receipt.pdf
```


## Error Handling

Errors return JSON:

```json
{"error": "Not authenticated. Run auth login"}
```

**Common errors:**

| Error | Solution |
|-------|----------|
| Not authenticated | Run `auth login` |
| Token expired | Run `auth login` again |
| No organization selected | Run `tenants list` then `tenants select <id>` |


## Security Notes

**Token Storage:** OAuth tokens are saved to `data/tokens.json` in the working directory. This file contains sensitive access/refresh tokens - treat it as you would other credentials.

**Environment Variables:** The skill reads `XERO_CLIENT_ID` and `XERO_CLIENT_SECRET` from environment (set via OpenClaw config). Optional: `XERO_REDIRECT_URI` (default: `http://localhost:5001/callback`) and `XERO_SCOPES`.

**Source Code:** All skill code is bundled in the `scripts/` directory for inspection. Review before granting access to production Xero organizations.
