# Google Sheet Runtime Instructions Schema

Sheet tab name: `job_instructions`

Required columns (header row):
- `job_id`
- `job_name`
- `enabled` (true/false)
- `department` (sales/marketing)
- `area`
- `goal`
- `priority_actions` (comma-separated)
- `do_not_do` (comma-separated)
- `platform_scope` (comma-separated)
- `kpi_focus` (comma-separated)
- `max_actions_per_run`
- `notes`
- `config_version`
- `updated_at` (ISO-8601)

Environment variables needed by loader:
- `GOOGLE_SHEETS_SPREADSHEET_ID`
- `GOOGLE_SERVICE_ACCOUNT_EMAIL`
- `GOOGLE_SERVICE_ACCOUNT_PRIVATE_KEY`
- Optional: `GOOGLE_SHEETS_RANGE` (default: `job_instructions!A1:Z2000`)

Alternative auth mode (via gcloud CLI token):
- If service-account env vars are not set, loader will run `gcloud auth print-access-token`.
- In that mode, only `GOOGLE_SHEETS_SPREADSHEET_ID` is required.
- Share the sheet with the active gcloud identity (user or service account).

Command example:

```bash
node /Users/danielsinewe/.openclaw/workspace/scripts/load-sheet-instructions.mjs \
  --job-id 68111c3b-27c6-44a9-9f84-b0b46eb9d4a2 \
  --job-name "LinkedIn Top Voice - daily content engine"
```

Output cache files:
- `/Users/danielsinewe/.openclaw/memory/runtime-instructions/<job-id>.json`
- `/Users/danielsinewe/.openclaw/memory/runtime-instructions/<job-id>.md`

Behavior:
- Fresh read from Google Sheet if API succeeds.
- Falls back to last cached config if API fails.
- Fails only when both sheet and cache are unavailable.
