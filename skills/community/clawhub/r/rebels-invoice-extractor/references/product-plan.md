# Invoice Extractor — Product Plan

## Product Overview

- **Name:** Invoice Extractor
- **One-liner:** Extract structured data from invoices and receipts — output JSON, CSV, or append to a running expense ledger
- **Target users:** Freelancers, small businesses, contractors who deal with invoices/receipts regularly
- **Pain point:** Manually typing invoice data into accounting software, or paying €15-30/month for tools like Dext/Hubdoc/Expensify

## ClawHub Competition

| Skill | Downloads | Focus | Gap |
|-------|-----------|-------|-----|
| finance-automation | 940 | Stripe webhooks + Telegram | Different product entirely |
| invoice-collector | 623 | Collects PDFs from Gmail | Doesn't extract data from them |
| receipt-expense-workbench | 198 | Normalizes receipts into ledger | No batch processing, limited extraction |
| receipt-expense-reconciler | 100 | Parses receipts, categorizes, tax summaries | Smaller scope, no configurable categories |

**Our gap:** None focus on high-quality structured extraction with batch processing and configurable categories. We sit between "collect" and "reconcile" — the actual extraction step.

## Completed Versions

### v1.0.0 — Core Extraction
- Single PDF extraction (text-based PDFs via pdfplumber)
- Single image extraction (via LLM vision)
- Batch folder processing with single-confirmation workflow
- JSON output (per invoice)
- CSV running expense ledger (append mode)
- Configurable expense categories with keyword matching
- Filter/view ledger by date range, category, vendor
- Category summaries with time periods
- Zero external APIs required

### v1.1.0 — Platform Export
- `ledger export --platform <name>` with built-in presets: xero, freeagent, wave, generic
- Custom export presets via `exportPresets` in config (user-defined column mappings)
- LLM-powered discovery flow — agent searches docs for unknown platforms, creates preset, saves permanently
- Filter support for exports (--from, --to, --category, --vendor)
- File output via `--output` flag + MEDIA: attachment delivery

### v1.2.0 — Duplicate Detection
- Hash-based duplicate detection on `ledger add` (vendor + date + total → SHA-256[:12])
- `dedup_hash` column auto-migrated on existing ledgers
- `--force` flag to bypass duplicate check
- Exit code 2 on duplicate (for scripting)

## Technical Architecture

- **Language:** Python 3.13
- **Script:** `scripts/extract.py` — single entry point
- **Dependencies:** pdfplumber (pip), stdlib for everything else
- **Config:** `expense-config.json` in skill directory or user-configurable path
- **Data:** `data/ledger.csv` (user's accumulated expenses)
- **Commands:** extract, batch, ledger, categories

### Design Philosophy

The script is a **tool**, not a brain. It handles:
- PDF text extraction (pdfplumber)
- CSV ledger management (CRUD, backups, queries)
- Batch file discovery
- Config loading

The **agent (LLM)** handles the actual parsing/extraction because it's far better at understanding varied invoice formats than regex. This hybrid approach gives us:
- Robust text extraction from PDFs
- Intelligent parsing of any invoice format
- Vision support for image receipts
- No external API dependencies

## Commands

### `pdf <file>`
Extract raw text from a PDF. The agent then parses this text into structured data.

### `batch <folder>`
Recursively list all PDFs and images in a folder as JSON. The agent processes each one.

### `ledger add [--force] [json-file|-]`
Append a structured expense entry to the CSV ledger. Auto-categorizes based on config keywords. Detects duplicates unless `--force`.

### `ledger view [--from DATE] [--to DATE] [--category CAT] [--vendor VENDOR] [--format csv|json]`
Query the ledger with filters.

### `ledger summary [--period week|month|year]`
Aggregate totals by category.

### `ledger export --platform <name> [--from DATE] [--to DATE] [--category CAT] [--vendor VENDOR] [--output FILE]`
Export ledger entries in platform-specific CSV format. Built-in: xero, freeagent, wave, generic. Supports custom presets.

### `categories`
List current categories from config.

## Config (expense-config.json)

```json
{
  "categories": {
    "software": ["github", "aws", "google cloud", "vercel", "openai", "anthropic", "azure"],
    "travel": ["ryanair", "airbnb", "hotel", "taxi", "uber", "bus éireann", "irish rail"],
    "office": ["staples", "amazon", "equipment", "monitor", "keyboard"],
    "utilities": ["electric", "gas", "internet", "phone", "vodafone", "virgin", "eir"],
    "food": ["restaurant", "cafe", "tesco", "supervalu", "lidl", "aldi", "insomnia", "starbucks"],
    "professional": ["accountant", "legal", "insurance", "subscription", "membership"]
  },
  "defaults": {
    "currency": "EUR",
    "taxRate": 0.23,
    "dateFormat": "%Y-%m-%d"
  },
  "ledger": {
    "path": "data/ledger.csv",
    "backupCount": 5
  }
}
```

## CSV Ledger Format

```csv
id,date,vendor,description,category,subtotal,tax,total,currency,source_file,extracted_at,dedup_hash
1,2026-04-01,Amazon,Office supplies,office,45.00,9.22,54.22,EUR,receipt_amazon_20260401.pdf,2026-04-01T10:30:00Z,a1b2c3d4e5f6
```

## File Structure

```
invoice-extractor/
├── SKILL.md
├── references/
│   └── product-plan.md
├── scripts/
│   └── extract.py
├── data/
│   └── .gitkeep
└── expense-config.json
```

## Changelog

### v1.2.1 — Bulletproofing
- `ledger delete --id N` — remove entries with ID renumbering
- `ledger edit --id N` — update fields with auto hash recalculation
- `ledger undo` — remove last entry (one-level undo)
- CSV quoting safety (explicit `csv.QUOTE_MINIMAL` on all writers)
- `write_ledger_all()` helper for full-rewrite operations
- Edge case guidance in SKILL.md (ambiguous dates, missing fields, credit notes, non-invoices)
- Config `dateFormat` now uses display format (DD/MM/YYYY) instead of Python strftime

### v1.2 — Duplicate Detection
- Hash-based duplicate detection on `ledger add` (vendor + date + total → SHA-256[:12])
- `dedup_hash` column added to ledger CSV
- Existing ledgers auto-migrated on first write
- `--force` flag to bypass duplicate check

### v1.1 — Platform CSV Export
- `ledger export --platform <name>` with built-in presets: xero, freeagent, wave, generic
- Custom export presets via `exportPresets` in config
- Filter support for exports (--from, --to, --category, --vendor)
- LLM-powered discovery flow for unknown platforms

## Roadmap

### v1.3.0 — Multi-Currency
- Store original currency per entry
- Convert to a base currency (configurable, e.g., EUR) for summaries
- Use exchange rates from a free API or manual rate entry
- Export with currency column preserved

### v2.0.0 — Direct API Push
- OAuth integration with Xero, FreeAgent, Wave APIs
- Push expenses directly from ledger → accounting software (no CSV download needed)
- Credential management via config (encrypted token storage)
- Error handling: rate limits, API failures, retry logic
- This is the "magic" experience — process receipts and they just appear in Xero

### v2.1.0 — Email Integration
- Auto-process invoice PDF attachments from Gmail
- Pair with the gmail-checker skill for inbound processing
- Cron-based: daily scan for new invoices, extract, categorize, push to accounting software
- Full pipeline: email arrives → extracted → categorized → in Xero

### v2.2.0 — Receipt Photo Capture
- Mobile-friendly flow: user takes photo → sends to agent via Signal/WhatsApp → extracted and added
- No file upload needed — the messaging app IS the capture tool
- Already partially supported via image tool

### v3.0.0 — Smart Insights
- Spending trends over time (weekly/monthly/yearly)
- Anomaly detection ("your software spend doubled this month")
- Budget tracking per category
- Tax season preparation (auto-generate expense summaries by tax category)
- Predictive: "based on your spending patterns, expect €X this month"

### Nice-to-Have (No ETA)
- Receipt OCR for heavily scanned/image-only PDFs (current fallback: LLM vision)
- Multi-user support (shared ledger for small teams)
- Recurring invoice detection (same vendor, similar amounts monthly)
- Vendor relationship insights (total spend per vendor over time)
