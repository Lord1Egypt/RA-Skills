---
name: statementedge
description: Convert PDF bank statements to CSV / Excel / QuickBooks / Xero / Sage / OFX via StatementEdge. Auto-reconciled, EU-hosted, 100+ banks across 22 countries (UK, EU, US, India, APAC, MENA, LATAM, Africa). No model training on uploads.
version: 1.1.0
metadata:
  openclaw:
    requires:
      env:
        - STATEMENTEDGE_API_KEY
      bins:
        - curl
    primaryEnv: STATEMENTEDGE_API_KEY
    envVars:
      - name: STATEMENTEDGE_API_KEY
        required: true
        description: Bearer token issued at https://www.statementedge.com/dashboard/api-keys. Same allowance whether called from browser or API.
      - name: STATEMENTEDGE_BASE_URL
        required: false
        description: Override the default https://www.statementedge.com endpoint. Useful only for staging or self-hosted deployments.
    homepage: https://www.statementedge.com
    emoji: "📄"
---

# StatementEdge Skill

Convert PDF bank statements into structured data (CSV, Excel, QuickBooks, Xero, Sage, OFX) using StatementEdge — EU-hosted, auto-reconciled, 100+ banks across 22 countries spanning UK, EU, US, India, APAC (Singapore, Hong Kong, New Zealand, Australia, Philippines), MENA (UAE), LATAM (Mexico, Brazil), and Africa (South Africa). No model training on your uploads.

## Free, no credit card — 30 seconds to your first conversion

API access is on **every plan, free included**. The free tier gives you 7 pages/day to test the integration end-to-end before deciding whether to upgrade — same allowance whether you call from the web app, this skill, or anywhere else.

1. Sign up at https://www.statementedge.com — email or Google, **no card required**
2. Open **Dashboard → API keys → Create key** — token is shown once, looks like `se_live_…`
3. Drop it into your shell:

```bash
export STATEMENTEDGE_API_KEY="se_live_…"
```

That's it. Run the curl example in the next section and you'll have a parsed bank statement in JSON within ~30 seconds.

## What the key can access

Your token is **scoped to your own account only** — it can convert PDFs you upload, fetch the conversions back, and read your job history. It can't see other users' data, change your plan, or touch billing. Stored as a sha256 hash on our side, so we can't recover a lost key (revoke + regenerate from the dashboard at any time).

## Requirements

- `STATEMENTEDGE_API_KEY` — your bearer token from the steps above. The skill won't run without it.

## Privacy and data handling

What StatementEdge processes when you call this skill:

- **The PDF you upload to `/v1/convert`**. Stored encrypted at rest in Supabase Storage (EU-Frankfurt region) and deleted automatically within one hour of a successful conversion via the `purge_after` job timestamp.
- **The PDF password if you supply one**. Held only in memory inside the Trigger.dev conversion task; never written to our database, never logged, never sent to Sentry. Our Sentry initialisation scrubs `Authorization` and cookie headers from every event before it leaves us.
- **No environment variables or other files from your machine**. The skill only reads `STATEMENTEDGE_API_KEY` and the file path you pass to it.

Where the data lives:

- Storage and compute: Vercel `fra1` (Frankfurt) plus Supabase EU
- AI extraction: Google Gemini API. Google's published terms commit to not using paid-tier API input for model training.
- Error monitoring: Sentry, hosted in their DE region (ingest.de.sentry.io)

Extracted transactions remain on your StatementEdge account until you remove them from `/dashboard`. Closing your account triggers a 30-day deletion of any remaining records, except where retention is required for invoicing under Irish/EU tax law.

Full sub-processor list and retention windows: <https://www.statementedge.com/privacy>. A signed Data Processing Addendum is available on the Business plan for GDPR compliance reviews.

## APIs

### Upload a PDF bank statement

```bash
curl -s -X POST \
  -H "Authorization: Bearer $STATEMENTEDGE_API_KEY" \
  -F "file=@/path/to/statement.pdf" \
  https://www.statementedge.com/v1/convert | jq
```

Example response:

```json
{
  "jobId": "5f3a8b9c-…",
  "status": "queued",
  "statusUrl": "https://www.statementedge.com/v1/jobs/5f3a8b9c-…"
}
```

Save the `jobId` for the next step.

### Check job status and fetch the converted data

```bash
curl -s \
  -H "Authorization: Bearer $STATEMENTEDGE_API_KEY" \
  https://www.statementedge.com/v1/jobs/$JOB_ID | jq
```

Returns the job state plus the parsed transactions once it's `done`:

```json
{
  "id": "5f3a8b9c-…",
  "status": "done",
  "pageCount": 3,
  "reconcileStatus": "reconciled",
  "statement": {
    "bank_name": "AIB",
    "account_masked": "•••• 1234",
    "currency": "EUR",
    "opening_balance": 1234.56,
    "closing_balance": 2345.67,
    "period_start": "2026-02-01",
    "period_end": "2026-02-28",
    "transactions": [
      {
        "row_index": 0,
        "date_iso": "2026-02-03",
        "description": "Tesco 12345",
        "amount": -42.10,
        "balance": 1192.46,
        "direction": "debit",
        "flagged": false
      }
      // …
    ]
  }
}
```

Poll every ~2 seconds while `status` is `queued` or `processing`.

### Pass a password for an encrypted PDF

For password-protected statements (common with Indian banks and some EU corporate accounts), send the password as form field on upload:

```bash
curl -s -X POST \
  -H "Authorization: Bearer $STATEMENTEDGE_API_KEY" \
  -F "file=@statement.pdf" \
  -F "password=YOUR_PDF_PASSWORD" \
  https://www.statementedge.com/v1/convert | jq
```

The password is held only for the duration of the conversion and never written to logs or the database.

### Export to a specific format — native endpoint

Once the job is `done`, request the native file format directly. No client-side transformation needed; the same builder code that powers the web UI's download buttons runs on the API:

```
GET /v1/jobs/$JOB_ID/export?format=<csv|xlsx|qbo|qfx|ofx|xero-csv|sage-csv>
```

| Format | Content-Type | Use for |
|---|---|---|
| `csv` | text/csv | Universal — Excel, Numbers, Sheets |
| `xlsx` | spreadsheetml.sheet | Native Excel workbook (Summary + Transactions) |
| `qbo` | application/vnd.intu.qbo | QuickBooks Online + Desktop (no column mapping) |
| `qfx` | application/vnd.intu.qfx | Quicken |
| `ofx` | application/x-ofx | GnuCash, MoneyDance, Beancount |
| `xero-csv` | text/csv | Xero manual statement import |
| `sage-csv` | text/csv | Sage 50 |

```bash
# QuickBooks .qbo (recommended — imports without manual column mapping)
curl https://www.statementedge.com/v1/jobs/$JOB_ID/export?format=qbo \
  -H "Authorization: Bearer $STATEMENTEDGE_API_KEY" \
  --output statement.qbo

# Native Excel workbook
curl https://www.statementedge.com/v1/jobs/$JOB_ID/export?format=xlsx \
  -H "Authorization: Bearer $STATEMENTEDGE_API_KEY" \
  --output statement.xlsx
```

The response is the file itself — no JSON wrapping, no base64. The `Content-Disposition` header carries the suggested filename. Returns 409 if the job isn't `done` yet.

For an end-to-end agentic flow that converts AND writes the file in a single MCP call, use the `convert_bank_statement` tool with `export_to: "qbo"` (or any of the formats above).

## What you get vs. raw OCR

- **Auto-reconciled**: every statement is balance-checked (opening + Σtransactions = closing). The `reconcileStatus` field tells you whether the result is `reconciled`, `reconciled_with_flags`, or `needs_review`. No more silent off-by-one errors.
- **Locale-aware**: USD or EUR, comma vs period decimals, DD/MM vs MM/DD dates, Money-In/Out columns, Dr/Cr suffixes — handled natively.
- **Vision-native**: text-layer PDFs use a cheap text path; scanned PDFs are sent to Gemini's vision model directly. No per-bank templates that go stale.
- **EU-hosted**: storage and compute in EU-Frankfurt. GDPR DPA available for European customers on the Business plan.

## Limits & pricing

| Plan | Pages | Price |
|---|---|---|
| Free | 7 / day | €0 |
| Starter | 500 / month | €19 |
| Pro | 2,500 / month | €49 |
| Business | 6,000 / month | €99 |

Unused pages on paid plans roll forward 3 months. Full details at https://www.statementedge.com/pricing.

## Help

- API docs: https://www.statementedge.com/docs/api
- Contact: https://www.statementedge.com/contact
