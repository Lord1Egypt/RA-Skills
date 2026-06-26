---
name: upbank
description: Read-only access to Up Bank accounts, transactions, categories, and tags
metadata:
  {
    "openclaw": {
      "requires": { "env": ["UP_API_TOKEN"] },
      "primaryEnv": "UP_API_TOKEN",
      "emoji": "🏦"
    }
  }
---

# Up Bank API Skill

Read-only access to your Up Bank account data including accounts, transactions, categories, and tags.

## When to use this skill

Use this skill when you need to:
- Check account balances
- Review recent transactions
- Search transaction history
- View spending categories
- Analyze tags and attachments
- Test API connectivity with ping

## Authentication

All requests require a Personal Access Token from Up Bank. Get yours from the Up app:
1. Swipe right to the Up tab → Data sharing → Personal Access Token

The token must be provided as a Bearer token in the Authorization header.

**Environment Variable:** Set `UP_API_TOKEN` before making API calls.

## Available Endpoints (Read-Only)

### Accounts
- `GET /api/v1/accounts` — List all accounts
- `GET /api/v1/accounts/{id}` — Get single account details

### Transactions
- `GET /api/v1/transactions` — List transactions (paginated)
- `GET /api/v1/transactions/{id}` — Get single transaction
- `GET /api/v1/accounts/{accountId}/transactions` — List transactions for specific account

### Categories
- `GET /api/v1/categories` — List all categories
- `GET /api/v1/categories/{id}` — Get category details

### Tags
- `GET /api/v1/tags` — List all tags

### Attachments
- `GET /api/v1/attachments` — List attachments
- `GET /api/v1/attachments/{id}` — Get attachment details

### Webhooks
- `GET /api/v1/webhooks` — List webhooks
- `GET /api/v1/webhooks/{id}` — Get webhook details
- `GET /api/v1/webhooks/{webhookId}/logs` — Get webhook delivery logs

### Utility
- `GET /api/v1/util/ping` — Test API authentication

## Security Requirements

**JIT Access Required** — Each API call requires explicit user approval. Do not make requests without user confirmation.

**Time-Based Access** — Access tokens should have an expiration. Prompt for re-authentication if the token appears expired or if more than 1 hour has passed since the token was provided.

## Rate Limiting

Up Bank implements rate limiting. If you receive 429 responses, wait before retrying and inform the user of the rate limit.

## Error Handling

- 401: Invalid or expired token — ask for new token
- 403: Access forbidden — check token permissions
- 404: Resource not found
- 429: Rate limited — wait and retry
- 5xx: Server error — try again later

## Data Notes

- All monetary values are in cents (base units) — divide by 100 for display
- Transaction amounts: negative = money out, positive = money in
- Attachments have expiry times for URLs — handle accordingly
- Pagination uses `prev` and `next` links in the response

## Important Notes

- This skill provides **read-only** access only. No write operations (create/update/delete) are permitted.
- Do not store tokens permanently — request them fresh per session
- Respect user privacy — only show transaction details when explicitly requested
- Cash withdrawals show as `CASH_WITHDRAWAL` in transaction description