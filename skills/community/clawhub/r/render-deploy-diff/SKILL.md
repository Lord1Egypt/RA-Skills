---
name: render-deploy-diff
description: Detect config drift between required local env keys and a Render service before deploy; fails when required keys are missing remotely.
version: 1.0.0
metadata: {"openclaw":{"requires":{"bins":["bash","curl","python3"],"env":["RENDER_API_KEY"]}}}
---

# Render Deploy Diff

Use this skill before deploy to compare required environment keys with what is currently configured on a Render service.

## What this skill does
- Resolves a target Render service by `RENDER_SERVICE_ID` or `RENDER_SERVICE_NAME`
- Reads required env keys from `REQUIRED_ENV_KEYS` or local env template files
- Fetches configured env keys from Render API
- Prints two drift sets:
  - required but missing on Render
  - present on Render but not required locally
- Exits non-zero when required keys are missing on Render

## Inputs
- `RENDER_API_KEY` (required unless using mock JSON)
- one of:
  - `RENDER_SERVICE_ID`
  - `RENDER_SERVICE_NAME`
- optional:
  - `RENDER_API_BASE_URL` (default `https://api.render.com/v1`)
  - `REQUIRED_ENV_KEYS` (comma-separated explicit required keys)
  - `REQUIRED_ENV_FILES` (comma-separated files to parse, default `.env.example,.env.production`)
  - `RENDER_ENV_VARS_JSON_PATH` (path to saved Render env-var API JSON for offline testing)

## Run

```bash
bash scripts/render-deploy-diff.sh
```

With explicit required keys:

```bash
RENDER_SERVICE_NAME=my-service \
REQUIRED_ENV_KEYS="DATABASE_URL,DIRECT_URL,SHADOW_DATABASE_URL,NEXT_PUBLIC_APP_URL" \
bash scripts/render-deploy-diff.sh
```

Offline test with saved API response:

```bash
REQUIRED_ENV_KEYS="DATABASE_URL,NEXT_PUBLIC_APP_URL" \
RENDER_ENV_VARS_JSON_PATH=./fixtures/render-env-vars.json \
bash scripts/render-deploy-diff.sh
```

## Output contract
- Prints service identity, required key count, remote key count, and drift summary
- Returns exit code `0` when all required keys exist on Render
- Returns exit code `1` when required keys are missing or inputs are invalid
