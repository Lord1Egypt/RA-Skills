---
name: sure-api
description: Use the we-promise/sure REST API with X-Api-Key auth. Covers accounts, transactions, categories, tags, merchants, imports, holdings, trades, valuations, chats, official docs URLs, self-update workflow from upstream OpenAPI, and ClawHub publish readiness.
---

# Sure API

Use this skill when the user asks to:
- operate **Sure** through its API
- inspect accounts, transactions, categories, tags, merchants, imports, holdings, trades, valuations, or chats
- create/update/delete supported Sure resources safely
- verify whether the upstream Sure API changed
- keep this skill in sync with the official Sure API docs

## Official source-of-truth URLs

These are the URLs the agent should trust first when updating or validating this skill:

- Sure repo: `https://github.com/we-promise/sure`
- API docs directory: `https://github.com/we-promise/sure/tree/main/docs/api`
- OpenAPI spec page: `https://github.com/we-promise/sure/blob/main/docs/api/openapi.yaml`
- Raw OpenAPI download used by the update script: `https://raw.githubusercontent.com/we-promise/sure/main/docs/api/openapi.yaml`

If behavior and local scripts disagree, **re-check the upstream OpenAPI first**.

## Local config

Read secrets from secure env only:
- `SURE_BASE_URL`
- `SURE_API_KEY`

Single source of truth: `secure/api-fillin.env`

Never paste the API key into chat or into non-secure files.

## Auth

Default auth header:
- `X-Api-Key: <SURE_API_KEY>`

Note: the current upstream OpenAPI snapshot also shows `Authorization` header notes on some valuation endpoints. Treat upstream OpenAPI as authoritative if those endpoints behave differently in practice.

## Skill layout

```text
skills/sure-api/
├── SKILL.md
├── references/
│   ├── openapi.yaml
│   └── api_endpoints_summary.md
└── scripts/
    ├── sure_api_request.sh
    ├── sure_api_smoke.sh
    ├── sure_api_cli.js
    ├── sure_openapi_update.sh
    ├── sure_openapi_summarize.js
    └── sure_api_acceptance.sh
```

## Capability model

This skill has **two layers**:

### Layer 1: high-level wrapped commands
Use these first for common operations.

Implemented in `scripts/sure_api_cli.js`:
- `accounts:list`
- `categories:list`
- `tags:list`
- `tags:create`
- `tags:update`
- `tags:delete`
- `merchants:list`
- `transactions:list`
- `transactions:get`
- `transactions:create`
- `transactions:update`
- `transactions:delete`
- `imports:list`
- `holdings:list`
- `trades:list`

### Layer 2: raw official endpoint access
For any official endpoint not yet wrapped by the high-level CLI, use:
- `bash skills/sure-api/scripts/sure_api_request.sh <METHOD> <PATH> [curl args...]`

This means the skill can still operate against official endpoints such as:
- merchant detail
- holding detail
- import detail / create import
- trade create / retrieve / update / delete
- valuation create / retrieve / update
- chats list / create / retrieve / update / delete / send message / retry
- other official endpoints present in `references/openapi.yaml`

## Quick start

### Smoke test

```bash
bash skills/sure-api/scripts/sure_api_smoke.sh
```

### Common wrapped commands

```bash
node skills/sure-api/scripts/sure_api_cli.js accounts:list
node skills/sure-api/scripts/sure_api_cli.js categories:list --classification expense
node skills/sure-api/scripts/sure_api_cli.js tags:list
node skills/sure-api/scripts/sure_api_cli.js merchants:list
node skills/sure-api/scripts/sure_api_cli.js transactions:list --start_date 2026-03-01 --end_date 2026-03-31 --type expense
node skills/sure-api/scripts/sure_api_cli.js holdings:list --account_id <uuid>
node skills/sure-api/scripts/sure_api_cli.js trades:list --account_id <uuid> --start_date 2026-03-01 --end_date 2026-03-31
```

### Safe write pattern

Always prefer:
1. read current state
2. dry-run if the wrapped command supports it
3. send the real write only with explicit confirmation flags

Example:

```bash
node skills/sure-api/scripts/sure_api_cli.js transactions:create \
  --account_id <uuid> \
  --date 2026-03-01 \
  --amount 12.34 \
  --name "午饭" \
  --nature expense \
  --dry-run

node skills/sure-api/scripts/sure_api_cli.js transactions:create \
  --account_id <uuid> \
  --date 2026-03-01 \
  --amount 12.34 \
  --name "午饭" \
  --nature expense \
  --yes
```

## Raw endpoint examples for official API coverage

### Retrieve a merchant by id

```bash
bash skills/sure-api/scripts/sure_api_request.sh GET /api/v1/merchants/<merchant-id>
```

### Retrieve a holding by id

```bash
bash skills/sure-api/scripts/sure_api_request.sh GET /api/v1/holdings/<holding-id>
```

### Retrieve an import by id

```bash
bash skills/sure-api/scripts/sure_api_request.sh GET /api/v1/imports/<import-id>
```

### Create an import from raw CSV content

```bash
bash skills/sure-api/scripts/sure_api_request.sh POST /api/v1/imports \
  -H 'Content-Type: application/json' \
  -d '{
    "raw_file_content": "date,amount,name\n2026-03-01,12.34,午饭",
    "type": "TransactionImport",
    "account_id": "<account-uuid>",
    "publish": "true"
  }'
```

### Create a trade

```bash
bash skills/sure-api/scripts/sure_api_request.sh POST /api/v1/trades \
  -H 'Content-Type: application/json' \
  -d '{
    "trade": {
      "account_id": "<account-uuid>",
      "date": "2026-03-01",
      "qty": 10,
      "price": 12.5,
      "type": "buy",
      "ticker": "AAPL"
    }
  }'
```

### Create a valuation

```bash
bash skills/sure-api/scripts/sure_api_request.sh POST /api/v1/valuations \
  -H 'Content-Type: application/json' \
  -d '{
    "valuation": {
      "account_id": "<account-uuid>",
      "amount": 10000,
      "date": "2026-03-01",
      "notes": "Month-end valuation"
    }
  }'
```

### Create a chat and send a message

```bash
bash skills/sure-api/scripts/sure_api_request.sh POST /api/v1/chats \
  -H 'Content-Type: application/json' \
  -d '{"title":"Monthly review","message":"Summarize March spending"}'

bash skills/sure-api/scripts/sure_api_request.sh POST /api/v1/chats/<chat-id>/messages \
  -H 'Content-Type: application/json' \
  -d '{"content":"Show biggest merchant changes"}'
```

## Pagination and filtering

Most list endpoints return a resource list plus a pagination block.
Typical filters in the official API include:
- `page`
- `per_page`
- account/category/merchant/tag ids
- date or date ranges
- type/status filters on some resources

For exact parameters, read `references/openapi.yaml`.

## Error handling

- `401` / `403` → auth missing, invalid, or insufficient feature scope
- `404` → wrong path or object not found
- `422` → validation error; inspect request body against `references/openapi.yaml`
- `429` / `5xx` → retry with backoff up to 3 times if the action is idempotent

## Self-update this skill

This skill is designed to be self-maintainable.

### Fast refresh from official API

```bash
bash skills/sure-api/scripts/sure_openapi_update.sh
```

What it does:
1. downloads the latest official OpenAPI from the Sure GitHub repo
2. overwrites `references/openapi.yaml`
3. regenerates `references/api_endpoints_summary.md`

### After updating OpenAPI

Do this in order:
1. re-read `references/api_endpoints_summary.md`
2. compare new endpoints/params with current `sure_api_cli.js`
3. extend high-level wrappers only for endpoints that are common, stable, and worth scripting
4. keep less-common endpoints accessible via `sure_api_request.sh`
5. run acceptance checks

## When to read references

Read `references/openapi.yaml` when you need:
- exact request bodies
- exact response shapes
- enum values
- parameter names
- authoritative behavior after upstream changes

Read `references/api_endpoints_summary.md` when you need:
- a fast endpoint inventory
- a quick check of what the upstream API currently exposes

## ClawHub publish readiness

Before publishing or bumping a version, run:

```bash
bash skills/sure-api/scripts/sure_api_acceptance.sh
```

Optional live API validation:

```bash
bash skills/sure-api/scripts/sure_api_acceptance.sh --with-live-api
```

The acceptance script checks:
- required files exist
- `SKILL.md` frontmatter is valid enough for publishing
- official URLs are present
- self-update instructions are present
- endpoint summary matches the checked-in OpenAPI
- optional live smoke test passes

## ClawHub publish commands

First confirm login:

```bash
clawhub whoami
```

Initial publish example:

```bash
cd /root/.openclaw/workspace
clawhub publish ./skills/sure-api \
  --slug sure-api \
  --name "Sure API" \
  --version 1.0.0 \
  --changelog "Initial public release." \
  --tags latest
```

Update publish example:

```bash
cd /root/.openclaw/workspace
clawhub publish ./skills/sure-api \
  --slug sure-api \
  --name "Sure API" \
  --version 1.0.1 \
  --changelog "Refresh official OpenAPI, tighten docs, and improve publish readiness." \
  --tags latest
```

## Notes for future maintenance

- Keep `SKILL.md` concise; put exact API detail in `references/`.
- Do not add README / CHANGELOG / extra docs just for packaging.
- Only wrap high-value flows in `sure_api_cli.js`; leave long-tail official endpoints to the raw request wrapper.
- If upstream removes or renames endpoints, update examples and acceptance checks in the same commit.
