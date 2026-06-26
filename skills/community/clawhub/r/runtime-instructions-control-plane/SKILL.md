---
name: runtime-instructions-control-plane
description: Load per-job runtime instructions from Google Sheets, cache them locally, and reconcile cron job enablement flags safely for OpenClaw operations.
metadata: { "openclaw": { "emoji": "🧭", "requires": { "bins": ["node"] } } }
---

# Runtime Instructions Control Plane

Use this skill to run OpenClaw jobs from a Google Sheet control plane without editing `cron/jobs.json` manually.

## What this provides
- Fetches per-job instructions from Google Sheets and writes local runtime cache files.
- Supports local-only fallback from cache when Sheets or auth is unavailable.
- Reconciles cron job `enabled` flags from sheet rows in dry-run or apply mode.
- Includes a schema reference and starter CSV template for sheet setup.

## Included files
- `scripts/load-sheet-instructions.mjs`
- `scripts/reconcile-cron-from-sheet.mjs`
- `references/google-sheet-instructions-schema.md`
- `templates/job_instructions_template.csv`

## Environment
Set these before running:
- `GOOGLE_SHEETS_SPREADSHEET_ID`
- `GOOGLE_SHEETS_RANGE` (optional, default in scripts)
- Either service account creds:
  - `GOOGLE_SERVICE_ACCOUNT_EMAIL`
  - `GOOGLE_SERVICE_ACCOUNT_PRIVATE_KEY`
- Or authenticated `gcloud` for token fallback in loader script.

Optional path overrides:
- `OPENCLAW_ROOT` (default: `~/.openclaw`)
- `OPENCLAW_RUNTIME_INSTRUCTIONS_DIR` (default: `$OPENCLAW_ROOT/memory/runtime-instructions`)
- `OPENCLAW_CRON_JOBS_PATH` (default: `$OPENCLAW_ROOT/cron/jobs.json`)

## Usage

Load one job's runtime instructions:
```bash
node scripts/load-sheet-instructions.mjs \
  --job-id "<job-id>" \
  --job-name "<job-name>"
```

Load from cache only (no network):
```bash
node scripts/load-sheet-instructions.mjs --job-id "<job-id>" --local-only
```

Preview cron enable/disable changes from sheet:
```bash
node scripts/reconcile-cron-from-sheet.mjs
```

Apply cron enable/disable changes:
```bash
node scripts/reconcile-cron-from-sheet.mjs --apply
```

## Safety notes
- Always run dry-run first before `--apply`.
- Reconcile script creates a timestamped backup before writing `jobs.json`.
- Keep this focused on operational control-plane toggles, not content generation.
