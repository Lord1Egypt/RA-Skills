# YNAB API Guide

Detailed API reference and best practices for the YNAB Budget Management skill.

## Table of Contents

- [Transfer Transactions](#transfer-transactions)
- [Monthly Spending Calculation](#monthly-spending-calculation)
- [Account ID Management](#account-id-management)
- [API Endpoints](#api-endpoints)
- [Security](#security)

## Transfer Transactions

To create a **real** transfer that YNAB recognizes as linked transactions between accounts, you MUST use the account's `transfer_payee_id`, NOT a payee name.

### How it works

Each YNAB account has a `transfer_payee_id` field — this is the payee ID that represents transfers TO that account.

**Correct approach** — use `payee_id` with the destination's `transfer_payee_id`:
```json
{
  "transaction": {
    "account_id": "SOURCE_ACCOUNT_ID",
    "date": "2026-03-06",
    "amount": -50000,
    "payee_id": "DEST_ACCOUNT_TRANSFER_PAYEE_ID",
    "approved": true
  }
}
```

**Wrong approach** — using `payee_name` creates a regular transaction, not a transfer:
```json
{"payee_name": "Transfer: To Savings"}
```

### Getting transfer_payee_id values

```bash
# List all accounts with their transfer_payee_id
YNAB_API="https://api.ynab.com/v1"
# GET $YNAB_API/budgets/$BUDGET_ID/accounts
# Then extract: .data.accounts[] | {name, transfer_payee_id}
```

Store these IDs in your config for quick reference.

### What happens when done correctly

- YNAB creates **two linked transactions** (one in each account)
- The matching transaction appears automatically in the destination
- Both are marked as transfers (no budget impact)
- Deleting one side deletes both

### Common mistakes

| Mistake | Result |
|---------|--------|
| Using `payee_name` | Regular transaction, not a transfer |
| Creating both sides manually | Duplicates instead of linked pair |
| Setting a category | Transfers shouldn't have categories |

## Monthly Spending Calculation

When calculating monthly spending:

1. Get all transactions for the month
2. Filter: `amount < 0` (expenses only)
3. Exclude configured non-discretionary categories (taxes, transfers, etc.)
4. Expand Split transactions into subcategories
5. Sum by category or total

Consider separating small recurring expenses from large one-time purchases for better analysis.

## Account ID Management

Store account IDs in config (not hardcoded in scripts):

```json
{
  "accounts": {
    "primary_checking": "UUID-HERE",
    "savings": "UUID-HERE",
    "cash": "UUID-HERE"
  },
  "default_account": "primary_checking"
}
```

## API Endpoints

| Resource | Endpoint |
|----------|----------|
| Budgets | `GET /v1/budgets` |
| Accounts | `GET /v1/budgets/{id}/accounts` |
| Categories | `GET /v1/budgets/{id}/categories` |
| Transactions | `GET/POST /v1/budgets/{id}/transactions` |
| Single transaction | `GET/PUT/DELETE /v1/budgets/{id}/transactions/{id}` |
| Month summary | `GET /v1/budgets/{id}/months/current` |
| Scheduled | `GET /v1/budgets/{id}/scheduled_transactions` |
| Payees | `GET /v1/budgets/{id}/payees` |

Auth header: `Authorization: Bearer {YNAB_API_KEY}`

Rate limit: ~200 requests/hour per IP.

## Security

- Store API key in config file with permissions `600` or use environment variables
- Never commit `config.json` to version control
- Add to `.gitignore`: `config/ynab.json`, `.config/ynab/`
- Rotate API tokens periodically
- Never log or display full API keys in output

API docs: https://api.ynab.com
