---
name: wimm
description: Manage your money with WIMM — add and search transactions, check balances, set budgets, and get spending reports from chat.
version: 1.0.0
metadata:
  openclaw:
    emoji: "💰"
    homepage: https://wimm.my/docs/mcp
    requires:
      env:
        - WIMM_API_KEY
      bins:
        - curl
        - jq
    primaryEnv: WIMM_API_KEY
    envVars:
      - name: WIMM_API_KEY
        required: true
        description: >-
          Your WIMM API key (starts with "wimm_live_"). Create one at
          https://wimm.my → Settings → Developer. Requires a WIMM PRO account.
---

# WIMM — personal finance from chat

Use this skill to manage the user's money in their WIMM account: accounts,
transactions, budgets, categories, tags, and spending reports.

## Connection

- Base host: `https://wimm.my` — every path below begins with `/v1`
  (e.g. `https://wimm.my/v1/accounts`). Note: it is `/v1`, NOT `/api/v1`.
- Auth: send the header `Authorization: Bearer $WIMM_API_KEY` on every request.
- Responses are JSON. Pipe through `jq` to read fields.
- Money amounts are decimal numbers (sometimes strings) in the account's currency.

Helper pattern (use in every call):

```bash
curl -s -H "Authorization: Bearer $WIMM_API_KEY" \
  -H "Content-Type: application/json" \
  https://wimm.my/v1/<resource>
```

## Safety rules (important)

- Before creating, editing, or deleting anything (any POST/PATCH/DELETE),
  briefly confirm with the user in one line (e.g. "Add $40 'groceries' to
  Checking?") and proceed only on a yes.
- Never invent an account, category, or transaction id. Look it up first
  (GET the relevant list) and use the real id.
- If `WIMM_API_KEY` is missing or a call returns 401, tell the user to create
  a key at https://wimm.my (Settings → Developer) and set `WIMM_API_KEY`.

## What you can do

### Read
- Profile: `GET /v1/me`
- Accounts & balances: `GET /v1/accounts`
- Transactions (filterable via query params, e.g.
  `?account=<id>&category=<id>&query=text&limit=20&offset=0`):
  `GET /v1/transactions` — returns `{ data: [...], total, limit, offset }`
- Categories: `GET /v1/categories`
- Budgets: `GET /v1/budgets`
- Tags: `GET /v1/tags`
- Reports:
  - Spending by category: `GET /v1/reports/spend-by-category?from=YYYY-MM-DD&to=YYYY-MM-DD`
    (the date range params are `from` / `to`; both optional)
  - Monthly summary: `GET /v1/reports/monthly-summary?year=YYYY&month=M`
    (`year` / `month` optional; defaults to the current month)
- Natural-language question over their data: `POST /v1/ai/query` with body
  `{ "query": "how much did I spend on food last month?" }` → returns
  `{ answer, model, usage, ... }`

### Write (confirm first)
- Add a transaction: `POST /v1/transactions` with body
  `{ "accountId": "<id>", "amount": 40, "type": "EXPENSE", "description": "groceries", "date": "2026-06-29", "categoryId": "<id-optional>" }`
  — **`date` is required** (ISO-8601, e.g. `2026-06-29`); omitting it returns 400.
  `type` is `EXPENSE` or `INCOME`.
- Update a transaction: `PATCH /v1/transactions/<id>` with the changed fields
  (balances recompute automatically).
- Delete a transaction: `DELETE /v1/transactions/<id>`
- Create an account: `POST /v1/accounts` with `{ "name": "...", "type": "CHECKING", "currency": "USD" }`
  · update `PATCH /v1/accounts/<id>` · delete `DELETE /v1/accounts/<id>`
- Create a category: `POST /v1/categories` with
  `{ "name": "...", "type": "EXPENSE" }` (`type` ∈ INCOME|EXPENSE|TRANSFER;
  optional `icon`, `color` as `#RRGGBB`).
- Create a budget: `POST /v1/budgets` with
  `{ "name": "...", "amount": 500, "period": "MONTHLY" }`
  (`period` ∈ WEEKLY|MONTHLY|YEARLY|CUSTOM; optional `categoryId`).
- Create a tag: `POST /v1/tags` with `{ "name": "...", "color": "#FF5733" }`
  — **both `name` and `color` (`#RRGGBB`) are required.**
  Each of categories/budgets/tags supports `PATCH /<id>` and `DELETE /<id>`.

## Examples

Add an expense to the user's first account:

```bash
# 1) find the account id
ACC=$(curl -s -H "Authorization: Bearer $WIMM_API_KEY" \
  https://wimm.my/v1/accounts | jq -r '.[0].id')

# 2) create the transaction (after confirming with the user)
curl -s -X POST -H "Authorization: Bearer $WIMM_API_KEY" \
  -H "Content-Type: application/json" \
  -d "{\"accountId\":\"$ACC\",\"amount\":40,\"type\":\"EXPENSE\",\"description\":\"groceries\",\"date\":\"$(date +%F)\"}" \
  https://wimm.my/v1/transactions | jq
```

Check this month's spending by category:

```bash
curl -s -H "Authorization: Bearer $WIMM_API_KEY" \
  "https://wimm.my/v1/reports/spend-by-category" | jq
```

Ask a natural-language question:

```bash
curl -s -X POST -H "Authorization: Bearer $WIMM_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"query":"how much did I spend this month?"}' \
  https://wimm.my/v1/ai/query | jq -r '.answer'
```

## About WIMM

WIMM (Where Is My Money) is a multi-currency personal-finance app for expats,
nomads, and crypto users — bank, exchange (e.g. Bybit), and cash tracking.
Docs: https://wimm.my/docs/mcp
