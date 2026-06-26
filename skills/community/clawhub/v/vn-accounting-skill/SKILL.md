---
name: accounting-skill
description: >
  Process accounting documents — invoices (hóa đơn GTGT), purchase orders, and bank statements.
  Extract structured data from PDF (digital and scanned), JPG, and PNG files using OCR.
  Output Excel tracking sheets and JSON backups. Classify unknown documents and route to the
  correct extractor. Supports Vietnamese and international formats. Use when asked to extract,
  process, classify, or track invoices, POs, bank statements, or accounting documents.
---

# Accounting Skill

Extract structured data from accounting documents (invoices, POs, bank statements) into Excel tracking sheets with JSON backups. Handles digital PDFs, scanned PDFs, and images via automatic OCR.

## Prerequisites

Install system OCR dependencies before first use. See `{baseDir}/references/ocr-setup.md` for full guide.

```bash
# Ubuntu / Debian
sudo apt install tesseract-ocr tesseract-ocr-vie poppler-utils

# Verify
uv run {baseDir}/scripts/ocr_utils.py check
```

## Quick Start

### 1. Classify an unknown document

```bash
uv run {baseDir}/scripts/classify_document.py /path/to/document.pdf
```

Returns JSON with `type` (invoice / po / statement / other), `confidence`, and a ready-to-run extraction `command`.

### 2. Extract an invoice

```bash
uv run {baseDir}/scripts/extract_invoice.py /path/to/invoice.pdf -o invoice_tracking.xlsx
```

Appends to the Excel tracking sheet. Use `--dry-run` to preview parsed data without writing.

### 3. Extract a bank statement

```bash
uv run {baseDir}/scripts/extract_statement.py /path/to/statement.pdf
```

Creates `statement_{bank}_{date}.xlsx` with transactions. Use `-o` to specify output path.

### 4. Extract a purchase order

```bash
uv run {baseDir}/scripts/extract_po.py /path/to/po.pdf -o po_tracking.xlsx
```

Tracks delivery dates and flags overdue/urgent POs.

### 5. Generate empty Excel templates

```bash
uv run {baseDir}/scripts/generate_templates.py all -o ~/accounting/
```

Creates blank tracking sheets: `invoice_tracking.xlsx`, `po_tracking.xlsx`, `statement_template.xlsx`.

## Common Options (all extractors)

| Flag | Description |
|------|-------------|
| `--format excel\|json\|both` | Output format (default: `both`) |
| `--dry-run` | Parse and validate only, print JSON to stdout |
| `--json-dir DIR` | Directory for JSON backup files |
| `-o FILE` | Output Excel file path |

## Workflow

### Single Document
```
File → classify_document.py → route → extract_*.py → Excel + JSON
```

### Batch Processing
For a folder of mixed documents, classify first, then route:
```bash
for f in /path/to/docs/*; do
  uv run {baseDir}/scripts/classify_document.py "$f" --output-dir ~/accounting/
done
```

Then run the suggested extraction commands from each classification result.

## OCR Strategy

All scripts share `{baseDir}/scripts/ocr_utils.py` which auto-selects the best extraction method:

1. **Digital PDFs** → pdfplumber (fast, no OCR needed)
2. **Scanned PDFs** → pdf2image + pytesseract at 300 DPI (fallback when pdfplumber gets <50 chars/page)
3. **Images** (JPG/PNG/TIFF) → pytesseract with grayscale preprocessing

Each result includes `ocr_confidence` and `extraction_confidence` percentages. Documents below 85% are automatically flagged `needs_review`.

## Validation Rules

- **Invoices**: Subtotal + VAT = Total (auto-checks math), duplicate detection by invoice number + vendor
- **Bank statements**: Opening balance + credits − debits = closing balance
- **POs**: Delivery date tracking with overdue/urgent alerts

## Reference Documents

Read these for field schemas, Vietnamese format details, and validation logic:

- `{baseDir}/references/invoice-fields.md` — Vietnamese VAT invoice fields, tax rates, patterns
- `{baseDir}/references/bank-formats.md` — Vietnamese bank names, transaction formats, amount patterns
- `{baseDir}/references/po-fields.md` — PO fields, delivery status logic, payment terms
- `{baseDir}/references/ocr-setup.md` — OCR installation, troubleshooting, confidence scoring
