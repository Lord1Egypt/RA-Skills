---
name: report-builder
description: Use when the main operator needs to turn the nightly shortlist into a Telegram morning report with inline approve/reject/later buttons.
metadata: { "openclaw": { "emoji": "📨", "requires": { "bins": ["node", "openclaw"] } } }
---

# report-builder

Use `{baseDir}/scripts/send_report.mjs` to send the 09:00 Telegram report.
Use `{baseDir}/scripts/build_report.mjs` to deterministically build the payload file before send time.

## Input shape

Pass a JSON file with:

- `date`
- `summary`
- `reportUrl` (optional)
- `ideas`: array of `{ id, title, score, reason, notionUrl }`

See `{baseDir}/references/report-schema.md`.

## Usage

```bash
node {baseDir}/scripts/build_report.mjs workspace/reports/latest-nightly-report.json
node {baseDir}/scripts/send_report.mjs report.json
node {baseDir}/scripts/send_report.mjs report.json 1565027149
```

## Rules

- Keep the report short.
- Build phase must leave behind a JSON payload file, even when blocked by missing env or a Notion query error.
- Include buttons only for the shortlisted ideas.
- Button callbacks must be:
  - `approve:<ideaId>`
  - `reject:<ideaId>`
  - `later:<ideaId>`
