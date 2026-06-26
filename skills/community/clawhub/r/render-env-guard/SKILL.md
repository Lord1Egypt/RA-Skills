---
name: render-env-guard
description: Preflight-check Render service environment variables before deploys; catches missing keys and placeholder/template values that commonly break production rollouts.
version: 1.0.0
metadata: {"openclaw":{"requires":{"bins":["curl","python3"],"env":["RENDER_API_KEY"]}}}
---

# Render Env Guard

Use this skill when a deployment is failing because environment variables are missing, placeholder values leaked from templates, or service selection is ambiguous.

## What this skill does
- Resolves a Render service by ID or name
- Pulls service environment variables through Render API
- Validates required keys exist and are non-empty
- Flags suspicious values (template placeholders, localhost DB URLs, unexpanded `${VAR}` refs)
- Exits non-zero on any blocking issue so CI/deploy scripts can fail fast

## When to use
- Before `render deploy` / `render blueprint` updates
- After onboarding a new environment
- When runtime is showing config-related 5xx errors

## Inputs
- `RENDER_API_KEY` (required)
- one of:
  - `RENDER_SERVICE_ID`
  - `RENDER_SERVICE_NAME`
- optional:
  - `RENDER_API_BASE_URL` (default `https://api.render.com/v1`)
  - `REQUIRED_ENV_KEYS` (comma-separated, default: `DATABASE_URL,DIRECT_URL,SHADOW_DATABASE_URL,NEXT_PUBLIC_APP_URL`)

## Run

```bash
bash scripts/check-render-env.sh
```

or with explicit values:

```bash
RENDER_SERVICE_NAME=my-service \
REQUIRED_ENV_KEYS="DATABASE_URL,NEXT_PUBLIC_APP_URL,STRIPE_SECRET_KEY" \
bash scripts/check-render-env.sh
```

## Output contract
- Prints a short report with `PASS`/`FAIL`
- Returns exit code `0` when all required keys are valid
- Returns exit code `1` when any key is missing/invalid or service lookup fails

## Notes
- This checker is intentionally strict to prevent bad deploys.
- It validates values at the service level (what Render will inject at runtime), not local `.env` files.
