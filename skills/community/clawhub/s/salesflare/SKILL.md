---
name: salesflare
description: Full Salesflare API operations skill for reading, searching, creating, and updating CRM data (accounts, contacts, opportunities, tasks, pipelines, users, tags, workflows, and more). Use when a user asks to query or mutate Salesflare data via API, build API-driven automations, inspect available endpoints/fields, or troubleshoot Salesflare API requests. Supports practical/basic filters out of the box and raw advanced query parameters; does not provide a dedicated high-level builder for Salesflare's complex query-builder payloads.
metadata:
  {
    "openclaw":
      {
        "emoji": "📈",
        "requires": { "env": ["SALESFLARE_API_KEY"], "bins": ["python3"] },
        "primaryEnv": "SALESFLARE_API_KEY",
      },
  }
---

# Salesflare API

## Overview

Use this skill to work with the Salesflare REST API safely and consistently.

Default approach:
1. Discover endpoint shape and required fields
2. Do a read/check request first
3. Ask confirmation before mutating data
4. Execute mutation and return compact result with IDs

## Quick Start

Set API key before requests:

```bash
export SALESFLARE_API_KEY='your_key_here'
```

- Base URL: `https://api.salesflare.com` (production, default)
- Auth header: `Authorization: Bearer <API_KEY>`
- Optional local override: set `SALESFLARE_BASE_URL` to a staging URL if needed for local testing.
- Keep local secrets in an ignored `.env.local` or process environment only. Do not publish API keys or smoke-test outputs with the skill.

## Core Scripts

- `scripts/sf.py` — unified CLI wrapper (subcommands: `discover`, `request`, `get`, `post`, `put`, `patch`, `delete`, `smoketest`)
- `scripts/sf_discover.py` — discover/list endpoints and methods from OpenAPI
- `scripts/sf_request.py` — execute GET/POST/PATCH/PUT/DELETE with retry handling; supports query params, JSON body, auto-pagination
- `scripts/sf_smoketest.py` — smoke-test OpenAPI operations. Default mode is read-only; lifecycle writes require `--allow-write`, and cleanup deletes require both `--allow-write --allow-delete`.

## Workflow

### 1) Discover endpoint and shape

```bash
python scripts/sf.py discover --contains opportunities
python scripts/sf.py discover --tag Accounts
```

### 2) Validate with read call

```bash
python scripts/sf.py get --path /accounts --query limit=5 --query search=acme
```

### 3) Confirm before writes

**Always confirm intent with the user before executing POST, PUT, PATCH, or DELETE.**
For DELETE operations, require explicit confirmation regardless of context — do not infer consent from prior conversation.

### 4) Execute write and report

Return:
- action performed
- target entity ID(s)
- key changed fields
- API response summary

### 5) Smoke-test safely

Default smoke test is read-only:

```bash
python scripts/sf.py smoketest
```

Enable lifecycle write-path testing explicitly. This creates controlled test records first, runs GET list and by-ID checks, updates only records created by the same run, then deletes only those records:

```bash
python scripts/sf.py smoketest --allow-write --allow-delete
```

Lifecycle write coverage is intentionally limited to data the smoke test can own and clean up: accounts, contacts, opportunities, tasks, meetings, internal notes/messages, and tags. It also tests account-contact/account-user relationship updates on the test account and feedback on the test message. Other write endpoints are reported as skipped unless they can be safely represented in that lifecycle.

Run write coverage without cleanup only if you intentionally want to keep the created records:

```bash
python scripts/sf.py smoketest --allow-write
```

## Mutation Safety Rules

- **POST/PUT/PATCH**: always require explicit user confirmation before executing. Never infer consent.
- **DELETE**: always require explicit user confirmation before executing. Never infer consent.
- Smoke-test defaults to read-only. Use `--allow-write --allow-delete` for lifecycle write testing with cleanup. `PUT` and `DELETE` are only run on records created by the same smoke-test run.
- If a lifecycle write test is interrupted, search Salesflare for records named `OpenClaw Smoke` or tags starting with `openclaw-smoke-` before rerunning.
- Do not perform bulk mutations without explicit confirmation.
- Prefer single-record updates before bulk updates.
- Include IDs in all write output for traceability.
- On 429, rely on script retry/backoff. If retries exhaust, stop and report clearly.

## Output Rules

- Default: concise summary + key IDs/fields
- Provide raw JSON only when user asks for full payload
- For large result sets, return top N and mention total if available

## Filtering

- Direct support: simple query params via repeated `--query key=value`
- Advanced Salesflare query-builder filters (`q` object/rules): pass as raw serialized query payload when needed
- This skill does **not** implement a high-level DSL for composing complex `q` structures

## Common Endpoints

```
/accounts       /contacts       /opportunities
/accounts/{account_id}/feed
/tasks          /pipelines      /users   /me
/tags           /workflows
```

See `references/endpoints.md` for concrete command examples and write patterns.

## Known Endpoint Caveats

- **`GET /accounts/{account_id}/feed`** — returns an account's feed/timeline when enabled for the workspace. If it is unavailable, contact `support@salesflare.com` and ask Salesflare to turn on account feed API access.
- **`GET /persons`** — bare call can return 500. Use `?search=...` or `?id=...` instead.
- **`GET /tags/{tag_id}`** — returns 500 with valid IDs; use `GET /tags` and `GET /tags/{tag_id}/usage`.
- **`GET /persons` filter fields** — `GET /filterfields/person` returns 400; use `contact` instead.
- See `references/endpoints.md` for the full list of endpoint-specific caveats.

## Resources

### scripts/
- `sf.py` — unified wrapper CLI
- `sf_discover.py` — endpoint discovery from OpenAPI
- `sf_request.py` — authenticated API execution helper
- `sf_smoketest.py` — full operation smoke-test runner

### references/
- `endpoints.md` — practical request examples, write patterns, and endpoint-specific caveats
