---
name: invoice-extractor
description: >
  Extract structured data from invoices and receipts (PDFs and images). Output JSON, CSV,
  or build a running expense ledger. Use when someone shares an invoice to process, asks
  to track expenses, categorize spending, or prepare tax documents.
---

# Invoice Extractor 📄

Turn invoices and receipts into structured expense data. Extract from PDFs and images, auto-categorize spending, and maintain a running CSV ledger.

**Hybrid approach:** A Python script handles PDF text extraction and ledger management, while **you (the agent)** parse the invoice content — LLMs understand varied formats far better than regex.

---

## When to Use

- "Extract data from this invoice"
- "Track my expenses" / "Add to my expense ledger"
- "Categorize this receipt"
- "Process these invoices" / "Batch process receipts"
- "Show me my spending summary"
- "Prepare tax documents" / "Get my expenses for April"

---

## Setup

```bash
pip install pdfplumber
# Fallback: PyPDF2 (auto-used if pdfplumber unavailable)
```

Script: `scripts/extract.py` (relative to this skill directory)
Config: `expense-config.json` (same directory)

---

## ⚡ Single Invoice Workflow

### PDF Invoices

```bash
python3 scripts/extract.py pdf <file-path>
```

Read the output text, parse it into structured JSON (see schema below), then **confirm with the user before adding to ledger**.

### Image Invoices (jpg, png, webp, gif)

Use the `image` tool with a prompt like:
*"Extract all invoice/receipt data from this image. Return vendor, invoice number, date, line items, subtotal, tax, total, and currency."*

Parse the result into structured JSON, then **confirm with the user before adding to ledger**.

### 🔒 Confirm Then Add

Always present extracted data for user review before writing to the ledger:

```
📋 Invoice Extracted
Vendor: Amazon
Date: 2026-04-01
Invoice #: INV-2026-001
Description: Office supplies — keyboard and monitor
Total: €539.96 (incl. €100.97 tax)
Category: office (auto)

Add to ledger? (yes/edit/skip)
```

Format output for the current channel — adapt formatting to match what the platform supports. See [references/formatting.md](references/formatting.md) for platform-specific examples.

**On confirmation**, write the JSON to a temp file and run:

```bash
python3 scripts/extract.py ledger add /tmp/invoice-entry.json
```

Or pipe via stdin:

```bash
echo '<json>' | python3 scripts/extract.py ledger add -
```

If the user says **"edit"**, modify the requested fields and re-confirm. If **"skip"**, discard.

---

## 📦 Batch Processing

```bash
python3 scripts/extract.py batch <folder-path>
```

1. Run the batch command to get a JSON list of all PDFs and images
2. Process each file one at a time (PDFs via `pdf` command, images via `image` tool)
3. **Collect all results** — do NOT confirm each one individually
4. Present a summary of ALL extracted data at the end
5. Ask the user to confirm once: add all, edit specific entries, or skip

**Show this summary after processing all files:**

```
📦 Batch Results — 8 files processed

1. Amazon EU S.a.r.l.  —  €191.84  —  office
2. Tesco              —  €25.26   —  food
3. DigitalOcean LLC    —  €35.81   —  software
4. Insomnia Coffee     —  €9.84    —  food
5. ACME Solutions Ltd  —  €3,867.11 —  uncategorized ⚠️
... (errors shown separately)

Total: €4,129.86 across 5 entries (1 error)

Add all to ledger? (yes/edit/skip)
```

On confirmation, add all entries at once. If the user wants to edit, modify specific entries and re-confirm.

---

## 📊 Viewing Expenses & Summaries

**View entries** with optional filters:

```bash
python3 scripts/extract.py ledger view [filters]
```

```
--from DATE       Entries from this date (YYYY-MM-DD)
--to DATE         Entries up to this date
--category CAT    Filter by category name
--vendor VENDOR   Filter by vendor (partial match)
--format json|csv Output format (default: json)
```

**Edit an entry:**

```bash
python3 scripts/extract.py ledger edit --id N --vendor "New Name"
python3 scripts/extract.py ledger edit --id N --total 250.00 --category software
python3 scripts/extract.py ledger edit --id N --date 2026-04-02
```

Editable fields: `--vendor`, `--total`, `--date`, `--description`, `--category`, `--currency`, `--subtotal`, `--tax`. Multiple fields in one command. Auto-recalculates the dedup hash.

**Delete an entry:**

```bash
python3 scripts/extract.py ledger delete --id N
```

Removes the entry, renumbers remaining IDs, creates a backup.

**Undo last add:**

```bash
python3 scripts/extract.py ledger undo
```

Removes the most recently added entry (highest ID). One-level undo only.

**Category summaries:**

```bash
python3 scripts/extract.py ledger summary [--period week|month|year]
```

---

## JSON Schema

Structure all extracted invoice data as:

```json
{
  "vendor": "Amazon",
  "invoiceNumber": "INV-2026-001",
  "date": "2026-04-01",
  "dueDate": "2026-04-30",
  "description": "Office supplies — keyboard and monitor",
  "lineItems": [
    {"description": "Mechanical Keyboard", "quantity": 1, "unitPrice": 89.99},
    {"description": "USB-C Monitor", "quantity": 1, "unitPrice": 349.00}
  ],
  "subtotal": 438.99,
  "tax": 100.97,
  "total": 539.96,
  "currency": "EUR",
  "category": "office"
}
```

**Required for ledger:** `vendor`, `total`, `date`
**Optional:** everything else — the script handles missing fields gracefully

---

## 🏷️ Auto-Categorization

Auto-categorizes based on keyword matching in `expense-config.json`. Checks `vendor` name and `description` against category keywords (case-insensitive).

```bash
python3 scripts/extract.py categories
```

Users can customize by editing the config. Suggest adding new keywords when a vendor doesn't match.

---

## 📤 Exporting the Ledger

Export ledger entries in platform-specific CSV formats for direct import into accounting software.

```bash
python3 scripts/extract.py ledger export --platform <name> [filters] [--output FILE]
```

**Filters:** `--from DATE`, `--to DATE`, `--category CAT`, `--vendor VENDOR`

### Built-in Platforms

| Platform | Use Case | Notes |
|----------|----------|-------|
| `xero` | Bills/Expenses import | DD/MM/YYYY dates, includes AccountCode & TaxRate |
| `freeagent` | Out-of-pocket expenses | No header row, needs `claimantName` in config |
| `wave` | Bank transactions | Negative amounts for expenses |
| `generic` | Excel/Google Sheets | Full detail, clean format |

### Examples

```bash
# Export all entries for Xero
python3 scripts/extract.py ledger export --platform xero

# Export April expenses to a file
python3 scripts/extract.py ledger export --platform xero --from 2026-04-01 --to 2026-04-30 --output /tmp/xero-export.csv

# Filter by category for FreeAgent
python3 scripts/extract.py ledger export --platform freeagent --category travel --output /tmp/freeagent-travel.csv
```

### Custom Presets

Define custom export formats in `expense-config.json` under `exportPresets`:

```json
{
  "exportPresets": {
    "my-accounting": {
      "columns": ["date", "vendor", "amount", "category", "notes"],
      "headerRow": true,
      "dateFormat": "%m/%d/%Y",
      "amountHandling": "positive",
      "fieldMapping": {
        "date": "date",
        "vendor": "vendor",
        "amount": "total",
        "category": "category",
        "notes": "description"
      }
    }
  }
}
```

The `fieldMapping` maps CSV column names → ledger field names. Use: `--platform my-accounting`

### Sending the File

If no `--output` is specified, CSV goes to stdout. For file attachments:

1. Use `--output /tmp/invoice-export-<platform>-<timestamp>.csv`
2. Send via `MEDIA:<path-to-csv>`

```
Here's your Xero import file (12 entries, April 2026).
MEDIA:/tmp/invoice-export-xero-20260406.csv
```

### 🔍 Unknown Platform? (LLM Discovery Flow)

If the user names a platform that isn't built-in and isn't in their custom presets:

1. Use `web_search` to find "[platform name] CSV import format expenses"
2. Identify the required columns and their format
3. Create a `fieldMapping` from our ledger fields to their columns
4. Add the preset to the user's `expense-config.json` under `exportPresets`
5. Tell the user the preset was created and saved
6. Proceed with the export using the new preset

---

## ⚙️ Config

The config file (`expense-config.json`) lives in the skill root directory. See [references/configuration.md](references/configuration.md) for the full config reference.

```bash
# Use a custom config
python3 scripts/extract.py --config /path/to/config.json <command>
```

---

## ⚠️ Important Notes

- **Always confirm before adding to ledger** — never auto-add extracted data
- **Duplicate detection** — entries are auto-checked against existing ledger (vendor + date + total hash). Duplicates are skipped with a warning. Use `--force` to override
- **Dates must be YYYY-MM-DD** — convert if the invoice uses a different format
- **Currency symbols** — normalize to ISO codes (€ → EUR, £ → GBP, $ → USD)
- **Backups** — the script automatically backs up the ledger before each write (keeps last 5)

For edge cases (encrypted PDFs, scanned/image-only PDFs, dependency errors), see [references/notes.md](references/notes.md).

---

## Edge Cases

### Ambiguous Dates

- "03/04/2026" is ambiguous (March 4 US, April 3 EU)
- If the invoice doesn't specify a format, check the config `defaults.dateFormat`
- If still unclear, ask the user: "Is this March 4th or April 3rd?"
- Common formats: DD/MM/YYYY (Ireland, UK, EU), MM/DD/YYYY (US), YYYY-MM-DD (ISO — always prefer this)

### Missing Fields

- If no invoice number: leave blank in JSON, the script handles it
- If no line items: just use the description field
- If no tax breakdown: set tax to 0 and note "tax not specified"
- If no currency: use the config default (EUR)
- If no vendor name but there's a company logo in the image: best effort from context
- Always show the user what was extracted — even incomplete data — and let them confirm or edit

### Credit Notes and Refunds

- Negative totals indicate a credit/refund
- Still add to ledger — negative entries are valid expenses (they reduce totals)
- Category as normal based on vendor
- In the confirmation prompt, note it's a credit: "⚠️ Credit note detected (negative total)"

### Multi-page PDFs

- pdfplumber extracts text from all pages into one output
- The LLM sees all text and can find totals on any page
- No special handling needed — it just works

### Non-invoice PDFs

- If the extracted text doesn't look like an invoice (no vendor, no amounts, no date), tell the user: "This doesn't appear to be an invoice or receipt. Want to skip it?"
- Don't force extraction on something that clearly isn't an invoice

### Very Small Receipts

- Coffee receipts, parking tickets — often low-quality images or tiny text
- The LLM should still attempt extraction but flag low confidence: "⚠️ Low confidence — please verify the amounts"
