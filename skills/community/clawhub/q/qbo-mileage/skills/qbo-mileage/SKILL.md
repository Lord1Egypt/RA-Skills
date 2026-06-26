---
name: qbo-mileage
description: Generate QuickBooks Online mileage CSV files from Airtable, Outlook, or Google Calendar records using the local qbo-mileage CLI and user-owned credentials.
metadata: {"openclaw":{"requires":{"bins":["python"]}}}
---

# QuickBooks Mileage CSV

Use this skill when the user wants to generate, review, or schedule a
QuickBooks Online mileage CSV from calendar or inspection data.

Do not infer or hand-edit mileage rows in the prompt. Run the deterministic CLI
from the plugin root so trip pairing, distance caching, CSV formatting, and run
reports are produced by code.

## Common commands

Dry run:

```bash
python -m qbo_mileage generate --config config.json --month YYYY-MM --dry-run
```

Generate files:

```bash
python -m qbo_mileage generate --config config.json --month YYYY-MM
```

If `python` is not on PATH (common on macOS/Linux), use `python3`. If the
`qbo_mileage` package is not installed, run the bundled entry point instead,
which adds the plugin's `src/` folder to the path automatically:

```bash
python3 skills/qbo-mileage/scripts/run.py generate --config config.json --month YYYY-MM
```

Outputs are written under the configured output directory, normally
`quickbooks_mileage/YYYY-MM/`.

## Review checklist

- Confirm the requested month is correct.
- Confirm the configured home base and vehicle.
- Read `run_report.md` before telling the user the CSV is ready.
- Surface skipped events, missing addresses, and distance API failures.
- Confirm PERSONAL legs show a 0.00 deduction in the report.
- Remind the user that GitHub Actions or cloud/email output is not local-only.

## Setup guidance

For first-time setup, point the user to:

- `config.example.json`
- `docs/setup-airtable.md`
- `docs/setup-maps.md`
- `docs/setup-scheduling.md`
