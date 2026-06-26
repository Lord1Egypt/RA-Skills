---
name: readme-env-table-sync
description: Generate and sync a README environment-variable table from .env.example using marker blocks, with drift detection for CI.
version: 1.0.0
metadata: {"openclaw":{"requires":{"bins":["bash","python3"]}}}
---

# README Env Table Sync

Use this skill to keep README environment-variable docs aligned with the real `.env.example` file.

## What this skill does
- Parses env keys from `.env.example` (or another env template file)
- Generates a markdown table with key/default values
- Detects doc drift by comparing generated table with the README marker block
- Optionally applies the update directly into README

## Inputs
Optional:
- `ENV_FILE` (default: `.env.example`)
- `README_FILE` (default: `README.md`)
- `SYNC_MODE` (`report` or `apply`, default: `report`)
- `TABLE_START_MARKER` (default: `<!-- ENV_TABLE_START -->`)
- `TABLE_END_MARKER` (default: `<!-- ENV_TABLE_END -->`)

## Run

Drift report (CI-friendly):

```bash
ENV_FILE=.env.example \
README_FILE=README.md \
bash skills/readme-env-table-sync/scripts/sync-readme-env-table.sh
```

Apply sync:

```bash
ENV_FILE=.env.example \
README_FILE=README.md \
SYNC_MODE=apply \
bash skills/readme-env-table-sync/scripts/sync-readme-env-table.sh
```

Run against included fixtures:

```bash
ENV_FILE=skills/readme-env-table-sync/fixtures/.env.sample \
README_FILE=skills/readme-env-table-sync/fixtures/README.sample.md \
SYNC_MODE=apply \
bash skills/readme-env-table-sync/scripts/sync-readme-env-table.sh
```

## Output contract
- Exit `0` when table is already in sync (report) or update is applied (apply)
- Exit `1` on invalid inputs, missing markers, parse errors, or detected drift in report mode
- Prints a short summary with key count and mode
