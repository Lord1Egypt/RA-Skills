---
name: sure-finance-skill
description: "Sure Finance API skill. Use when the user wants personal finance insights, account and transaction operations, tags/categories management, imports, or chat workflows in Sure."
license: "MIT"
metadata: {"openclaw":{"emoji":"📈","primaryCredential":"SURE_API_KEY","requires":{"bins":["curl"],"env":["SURE_API_KEY","SURE_BASE_URL"]}},"clawdbot":{"emoji":"📈","primaryCredential":"SURE_API_KEY","requires":{"bin":["curl"],"env":["SURE_API_KEY","SURE_BASE_URL"]}}}
---

# Sure Finance Skill

This skill provides a reliable workflow to interact with Sure's API.

## Scope

Use this skill for:
- Listing and analyzing accounts, categories, tags, imports, chats, and transactions.
- Creating and updating transactions, tags, chats, and imports.
- Building financial summaries from Sure data.
- Helping users connect self-hosted Sure environments (Docker, compose, external assistant) with API usage.

Do not use this skill for:
- Guessing undocumented endpoints or request shapes.
- Running destructive operations without explicit user confirmation.
- Fabricating financial figures when the API is unavailable.

## Compatibility Contract

Follow these rules strictly to maximize compatibility:
- The skill is instruction-only. Core runtime actions are limited to `curl` requests against `$SURE_BASE_URL` using `X-Api-Key`.
- Optional self-hosting and external-assistant flows (documented in `docs/`) may reference additional URLs and env vars. These flows run only when the user explicitly requests them and never during normal API usage.
- Always use plain Markdown. Do not include HTML entities like `&nbsp;`.
- Keep shell commands copy-paste ready.
- Use only ASCII in examples unless API data requires otherwise.
- Do not require tools beyond `curl` for core operations.
- Read credentials only from environment variables.
- Never print API keys or tokens in output.
- Do not instruct reading unrelated local files, keychains, or secret stores.
- If `SURE_BASE_URL` has no scheme, normalize to `http://` before use.
- For all list endpoints, support pagination via `page` and `per_page`.
- Provide short, deterministic outputs when users request automation-friendly responses.

## Environment Setup

Required variables:

```bash
export SURE_API_KEY="YOUR_API_KEY"
export SURE_BASE_URL="https://app.sure.am"
```

Optional sensitive variables used only for specific self-hosted or external-assistant scenarios:

```bash
# External assistant validation (optional)
export MCP_API_TOKEN="..."
export MCP_USER_EMAIL="you@example.com"
export EXTERNAL_ASSISTANT_URL="https://your-agent/v1/chat/completions"
export EXTERNAL_ASSISTANT_TOKEN="..."

# Self-hosting bootstrap (optional)
export SECRET_KEY_BASE="..."
export POSTGRES_PASSWORD="..."
```

These optional variables are intentionally not listed in `metadata.clawdbot.requires.env` because the core skill runtime does not require them.
Do not request or provide these optional secrets for normal API usage.
Use them only when the user explicitly asks to run self-hosting or external-assistant validation flows.

Validation check:

```bash
curl --silent --show-error --fail \
  --request GET \
  --url "$SURE_BASE_URL/api/v1/accounts?page=1&per_page=1" \
  --header "X-Api-Key: $SURE_API_KEY"
```

If this fails:
- Verify the base URL and API key.
- Confirm Sure server is running and reachable.
- If self-hosted with Docker, verify containers are healthy.

## Authentication

All requests must include:

```bash
--header "X-Api-Key: $SURE_API_KEY"
```

## Core API Quick Reference

### Accounts

List accounts:

```bash
curl --request GET \
  --url "$SURE_BASE_URL/api/v1/accounts?page=1&per_page=25" \
  --header "X-Api-Key: $SURE_API_KEY"
```

### Categories

List categories:

```bash
curl --request GET \
  --url "$SURE_BASE_URL/api/v1/categories" \
  --header "X-Api-Key: $SURE_API_KEY"
```

Retrieve category:

```bash
curl --request GET \
  --url "$SURE_BASE_URL/api/v1/categories/{id}" \
  --header "X-Api-Key: $SURE_API_KEY"
```

### Chats

List chats:

```bash
curl --request GET \
  --url "$SURE_BASE_URL/api/v1/chats" \
  --header "X-Api-Key: $SURE_API_KEY"
```

Create chat:

```bash
curl --request POST \
  --url "$SURE_BASE_URL/api/v1/chats" \
  --header "Content-Type: application/json" \
  --header "X-Api-Key: $SURE_API_KEY" \
  --data '{
    "title": "Monthly budget review",
    "message": "Summarize my spending trends.",
    "model": "default"
  }'
```

Retrieve chat:

```bash
curl --request GET \
  --url "$SURE_BASE_URL/api/v1/chats/{id}" \
  --header "X-Api-Key: $SURE_API_KEY"
```

Update chat:

```bash
curl --request PATCH \
  --url "$SURE_BASE_URL/api/v1/chats/{id}" \
  --header "Content-Type: application/json" \
  --header "X-Api-Key: $SURE_API_KEY" \
  --data '{
    "title": "Updated chat title"
  }'
```

Delete chat:

```bash
curl --request DELETE \
  --url "$SURE_BASE_URL/api/v1/chats/{id}" \
  --header "X-Api-Key: $SURE_API_KEY"
```

Create chat message:

```bash
curl --request POST \
  --url "$SURE_BASE_URL/api/v1/chats/{chat_id}/messages" \
  --header "Content-Type: application/json" \
  --header "X-Api-Key: $SURE_API_KEY" \
  --data '{
    "content": "What changed this month vs last month?",
    "model": "default"
  }'
```

Retry last assistant response:

```bash
curl --request POST \
  --url "$SURE_BASE_URL/api/v1/chats/{chat_id}/messages/retry" \
  --header "X-Api-Key: $SURE_API_KEY"
```

### Imports

List imports:

```bash
curl --request GET \
  --url "$SURE_BASE_URL/api/v1/imports" \
  --header "X-Api-Key: $SURE_API_KEY"
```

Create import:

```bash
curl --request POST \
  --url "$SURE_BASE_URL/api/v1/imports" \
  --header "Content-Type: application/json" \
  --header "X-Api-Key: $SURE_API_KEY" \
  --data '{
    "raw_file_content": "date,amount,name\n2026-01-01,25.00,Coffee",
    "type": "TransactionImport",
    "account_id": "<account_id>",
    "publish": "true",
    "date_col_label": "date",
    "amount_col_label": "amount",
    "name_col_label": "name",
    "category_col_label": "category",
    "tags_col_label": "tags",
    "notes_col_label": "notes",
    "date_format": "YYYY-MM-DD",
    "number_format": "1,234.56",
    "signage_convention": "inflows_positive",
    "col_sep": ","
  }'
```

Retrieve import:

```bash
curl --request GET \
  --url "$SURE_BASE_URL/api/v1/imports/{id}" \
  --header "X-Api-Key: $SURE_API_KEY"
```

### Tags

List tags:

```bash
curl --request GET \
  --url "$SURE_BASE_URL/api/v1/tags" \
  --header "X-Api-Key: $SURE_API_KEY"
```

Create tag:

```bash
curl --request POST \
  --url "$SURE_BASE_URL/api/v1/tags" \
  --header "Content-Type: application/json" \
  --header "X-Api-Key: $SURE_API_KEY" \
  --data '{
    "tag": {
      "name": "Travel",
      "color": "#3B82F6"
    }
  }'
```

Retrieve tag:

```bash
curl --request GET \
  --url "$SURE_BASE_URL/api/v1/tags/{id}" \
  --header "X-Api-Key: $SURE_API_KEY"
```

Update tag:

```bash
curl --request PATCH \
  --url "$SURE_BASE_URL/api/v1/tags/{id}" \
  --header "Content-Type: application/json" \
  --header "X-Api-Key: $SURE_API_KEY" \
  --data '{
    "tag": {
      "name": "Travel Updated",
      "color": "#2563EB"
    }
  }'
```

Delete tag:

```bash
curl --request DELETE \
  --url "$SURE_BASE_URL/api/v1/tags/{id}" \
  --header "X-Api-Key: $SURE_API_KEY"
```

### Transactions

List transactions:

```bash
curl --request GET \
  --url "$SURE_BASE_URL/api/v1/transactions?page=1&per_page=25" \
  --header "X-Api-Key: $SURE_API_KEY"
```

Create transaction:

```bash
curl --request POST \
  --url "$SURE_BASE_URL/api/v1/transactions" \
  --header "Content-Type: application/json" \
  --header "X-Api-Key: $SURE_API_KEY" \
  --data '{
    "transaction": {
      "account_id": "<account_id>",
      "date": "2026-03-01",
      "amount": 123.45,
      "name": "Groceries",
      "description": "Weekly grocery shopping",
      "notes": "",
      "currency": "USD",
      "category_id": "<category_id>",
      "merchant_id": "<merchant_id>",
      "nature": "expense",
      "tag_ids": ["<tag_id>"]
    }
  }'
```

Retrieve transaction:

```bash
curl --request GET \
  --url "$SURE_BASE_URL/api/v1/transactions/{id}" \
  --header "X-Api-Key: $SURE_API_KEY"
```

Update transaction:

```bash
curl --request PATCH \
  --url "$SURE_BASE_URL/api/v1/transactions/{id}" \
  --header "Content-Type: application/json" \
  --header "X-Api-Key: $SURE_API_KEY" \
  --data '{
    "transaction": {
      "name": "Groceries - updated",
      "amount": 130.00,
      "notes": "adjusted amount"
    }
  }'
```

Delete transaction:

```bash
curl --request DELETE \
  --url "$SURE_BASE_URL/api/v1/transactions/{id}" \
  --header "X-Api-Key: $SURE_API_KEY"
```

## Recommended Agent Workflow

When asked to perform analytics:
1. List accounts and transactions with pagination.
2. Aggregate monthly totals by category and account.
3. Validate suspicious outliers against raw transactions.
4. Return clear assumptions and confidence level.

When asked to mutate data:
1. Confirm target resource ID and intended change.
2. Execute create or update call.
3. Re-fetch the resource to verify success.
4. Summarize fields changed.

## Self-Hosted Sure Notes

> **Scope note:** The commands below fetch compose files from the Sure project repository on GitHub. Review any downloaded file before running `docker compose up`. These flows are optional and only relevant when the user explicitly requests self-hosting setup.

For Docker-based self-hosting:
- Official image tags include `latest` and `stable`.
- Default local URL is `http://localhost:3000`.
- API key is generated in Sure account settings.

For AI and external assistant mode:
- Sure supports external assistant integration.
- Pipelock can proxy and inspect AI and MCP traffic.
- In AI compose mode, external agents should target the Pipelock reverse proxy when applicable.

## Error Handling

For HTTP 401 or 403:
- Verify `SURE_API_KEY`.
- Confirm the key belongs to the active Sure user.

For HTTP 404:
- Verify resource ID and base URL.

For HTTP 422:
- Validate JSON payload shape and enum values.

For network errors:
- Confirm host reachability.
- If self-hosted, verify `docker compose ps` status.

## Data Safety

- Treat all finance data as sensitive.
- Do not expose full account numbers or secrets in logs.
- Prefer redacting personally identifiable information in shared outputs.

## Additional Files

Use the supporting files in this skill package:
- `docs/openclaw-compatibility.md`
- `docs/api-playbooks.md`
- `docs/self-hosting-quickstart.md`
