# Accounting Skill

Extract structured data from accounting documents (invoices, purchase orders, bank statements) using OCR. Outputs Excel tracking sheets and JSON backups with confidence scores and validation alerts.

## Features

- **Multi-format OCR**: Digital PDFs (pdfplumber), scanned PDFs + images (pytesseract), automatic fallback
- **Vietnamese + International Support**: Hóa đơn GTGT (VAT invoices), Vietnamese bank formats, multilingual extraction
- **Intelligent Document Classification**: Automatically classify documents and route to correct extractor
- **Data Validation**: Math checks (invoices), balance continuity (statements), delivery tracking (POs)
- **Duplicate Detection**: Prevents re-entry of duplicate invoices/POs
- **Batch Processing**: Classify folders of mixed documents, then extract each type
- **Confidence Scoring**: OCR confidence + extraction confidence for every document

## Installation

### System Dependencies

Install OCR and PDF tools (required):

```bash
# Ubuntu / Debian
sudo apt install tesseract-ocr tesseract-ocr-vie poppler-utils

# macOS (Homebrew)
brew install tesseract tesseract-lang poppler
```

### Verify Installation

```bash
uv run scripts/ocr_utils.py check
```

Should output:
```
✓ tesseract found at /usr/bin/tesseract
✓ poppler found at /usr/bin/pdftoimage
✓ Vietnamese language pack available
```

### Python Requirements

- Python 3.10+
- `uv` package manager (for running scripts with auto-dependency install)

All scripts use [PEP 723](https://peps.python.org/pep-0723/) inline dependencies, so dependencies are auto-installed with `uv run`.

## Quick Start

### 1. Classify a Document

```bash
uv run scripts/classify_document.py /path/to/document.pdf
```

Output:
```json
{
  "type": "invoice",
  "confidence": 92,
  "action": "extract",
  "command": "uv run scripts/extract_invoice.py /path/to/document.pdf --output invoice_tracking.xlsx",
  "ocr_method": "pdfplumber",
  "ocr_confidence": 95
}
```

### 2. Extract an Invoice

```bash
uv run scripts/extract_invoice.py /path/to/invoice.pdf -o invoice_tracking.xlsx
```

Appends row to Excel tracking sheet and saves JSON backup. Output:
```json
{
  "invoice_number": "2024-001",
  "vendor": "ABC Trading",
  "total": 10100000,
  "status": "processed",
  "ocr_confidence": 94,
  "extraction_confidence": 98
}
```

### 3. Extract Bank Statement

```bash
uv run scripts/extract_statement.py /path/to/statement.pdf
```

Creates `statement_vcb_20260319.xlsx` with all transactions. Validates opening + credits − debits = closing balance.

### 4. Extract Purchase Order

```bash
uv run scripts/extract_po.py /path/to/po.pdf -o po_tracking.xlsx
```

Tracks delivery dates, flags overdue (red) and urgent (yellow) POs.

### 5. Generate Empty Templates

```bash
uv run scripts/generate_templates.py all -o ~/accounting/
```

Creates blank Excel sheets:
- `invoice_tracking.xlsx`
- `po_tracking.xlsx`
- `statement_template.xlsx`

## Usage Guide

### Common Options

All extraction scripts support these flags:

| Option | Default | Description |
|--------|---------|-------------|
| `--output, -o` | Type-specific | Output Excel file path |
| `--format` | `both` | `excel`, `json`, or `both` |
| `--json-dir` | Same as Excel | Directory for JSON backup files |
| `--dry-run` | — | Parse only, print JSON to stdout (no file writes) |

### Dry-Run Mode (Preview Results)

```bash
uv run scripts/extract_invoice.py invoice.pdf --dry-run
```

Parses and validates, outputs JSON to stdout without modifying files. Useful for debugging or testing.

### Batch Processing

Process a folder of mixed documents:

```bash
for file in ~/documents/*.pdf; do
  echo "Classifying: $file"
  result=$(uv run scripts/classify_document.py "$file")
  command=$(echo "$result" | jq -r '.command')
  echo "Running: $command"
  eval "$command"
done
```

### Custom Output Paths

```bash
# Invoice with custom path
uv run scripts/extract_invoice.py invoice.pdf -o ~/accounting/2024/invoices.xlsx

# Statement with JSON backup to specific directory
uv run scripts/extract_statement.py statement.pdf -o statement.xlsx --json-dir ~/accounting/json/

# PO with both formats
uv run scripts/extract_po.py po.pdf --format both --output-dir ~/accounting/
```

## Data Output

### Excel Format

Each extraction script appends to Excel tracking sheets:

**Invoice Tracking** (`invoice_tracking.xlsx`):
```
Invoice#  Date        Vendor          TaxCode    Subtotal    VAT    Total         Status          OCR%  Extract%
2024-001  2024-03-15  ABC Trading     0100000001 10000000    100000 10100000      processed       94    98
2024-002  2024-03-16  XYZ Corp        0203000001 5000000     500000 5500000       needs_review    82    85
```

**Bank Statement** (`statement_vcb_20260319.xlsx`):
```
Date        Description       Debit      Credit     Balance        Status
2024-03-01  Opening Balance                          500000000      ✓
2024-03-01  Deposit           50000000              550000000      reconciled
```

**PO Tracking** (`po_tracking.xlsx`):
```
PO#       Vendor      Total       Delivery    Days Left  Status    Priority
PO-2024-1 Supplier A  50000000    2024-03-25  6         ✓ OK      normal
PO-2024-2 Supplier B  30000000    2024-03-20  1         ⚠ URGENT urgent
```

### JSON Format

Each extraction also saves JSON backup (default: same directory as Excel):

```json
{
  "invoice_number": "2024-001",
  "vendor_name": "ABC Trading",
  "vendor_tax_code": "0100000001",
  "invoice_date": "2024-03-15",
  "subtotal_amount": 10000000,
  "vat_rate": 10,
  "vat_amount": 100000,
  "total_amount": 10100000,
  "items": [
    {
      "description": "Product A",
      "quantity": 10,
      "unit_price": 500000,
      "amount": 5000000,
      "vat_rate": 10
    }
  ],
  "ocr_confidence": 94,
  "extraction_confidence": 98,
  "ocr_method": "pdfplumber",
  "source_file": "/path/to/invoice.pdf",
  "processed_at": "2024-03-19T10:30:45"
}
```

## OCR & Confidence Scoring

### OCR Strategy

The skill automatically selects the best extraction method per file:

1. **Digital PDFs** (text layer present)
   - Method: `pdfplumber` (fast, accurate)
   - Typical confidence: > 90%

2. **Scanned PDFs** (image-based)
   - Method: `pdf2image` + `pytesseract` at 300 DPI
   - Typical confidence: 70-85%

3. **Images** (JPG, PNG, TIFF, BMP)
   - Method: `pytesseract` with grayscale preprocessing
   - Typical confidence: 75-90%

### Confidence Thresholds

| OCR % | Meaning | Action |
|-------|---------|--------|
| > 90% | Excellent | Trust result |
| 85-90% | Good | Minor review |
| 70-85% | Fair | Review amounts |
| < 70% | Poor | Manual review required |

Documents with `extraction_confidence < 85` are automatically flagged `needs_review`.

### Example: Low Confidence Debug

```bash
uv run scripts/extract_invoice.py scanned_invoice.pdf --dry-run
```

Output shows:
```json
{
  "ocr_confidence": 72,
  "ocr_method": "pytesseract",
  "extraction_confidence": 65,
  "status": "needs_review",
  "warnings": [
    "OCR confidence below 85%",
    "Missing vendor tax code",
    "Could not parse delivery date"
  ]
}
```

## Validation Rules

### Invoices (extract_invoice.py)

- **Math validation**: `subtotal + VAT = total` (auto-checked)
- **VAT rates**: 0%, 5%, 8%, 10% (Vietnamese standards)
- **Duplicate detection**: Checks invoice # + vendor combo in existing Excel
- **Required fields**: Invoice number, date, vendor, total amount

### Bank Statements (extract_statement.py)

- **Balance continuity**: `opening + credits − debits = closing` (validates statement integrity)
- **Transaction parsing**: Handles multi-bank formats (VCB, TCB, BIDV, VComBank, etc.)
- **Amount format**: Detects VND format (dots as thousands: `1.000.000`)
- **Date format**: Handles dd/mm/yyyy, dd-mm-yyyy, Vietnamese labels

### Purchase Orders (extract_po.py)

- **Delivery tracking**: Calculates `days_left = delivery_date - today`
- **Status flags**:
  - ✓ OK: 7+ days left
  - ⚠ URGENT: 1-6 days left (yellow highlight)
  - ✗ OVERDUE: delivery date passed (red highlight)
- **Duplicate detection**: Checks PO # + vendor

## File Structure

```
accounting-skill/
├── README.md                    ← This file
├── SKILL.md                     ← OpenClaw skill metadata & quick start
├── scripts/
│   ├── ocr_utils.py             ← Shared OCR module (pdfplumber + pytesseract)
│   ├── extract_invoice.py       ← Invoice extraction → Excel + JSON
│   ├── extract_statement.py     ← Bank statement extraction
│   ├── extract_po.py            ← PO extraction with delivery tracking
│   ├── classify_document.py     ← Document classifier & router
│   └── generate_templates.py    ← Blank Excel template generator
└── references/
    ├── invoice-fields.md        ← Vietnamese VAT invoice field reference
    ├── bank-formats.md          ← Vietnamese bank format patterns
    ├── po-fields.md             ← PO field reference & logic
    └── ocr-setup.md             ← OCR installation & troubleshooting
```

## Troubleshooting

### "tesseract is not installed"

```bash
# Ubuntu / Debian
sudo apt install tesseract-ocr tesseract-ocr-vie

# macOS
brew install tesseract tesseract-lang
```

### Vietnamese text garbled or missing

Vietnamese language pack is required:

```bash
# Ubuntu / Debian
sudo apt install tesseract-ocr-vie

# Verify
tesseract --list-langs | grep vie
```

### "No text extracted from file"

Usually means:
- PDF is password-protected (decrypt first)
- Scanned image is too faint (try preprocessing)
- Missing `poppler-utils` (needed to convert PDF to image)

```bash
sudo apt install poppler-utils
```

### Low OCR confidence on clean document

Likely a digital PDF — pdfplumber handles these better than OCR. Check logs:

```bash
uv run scripts/extract_invoice.py invoice.pdf --dry-run 2>&1 | grep "OCR method"
```

If shows `pytesseract`, it means pdfplumber found <50 chars/page. Verify PDF isn't corrupted.

### Script fails to find output file

Ensure directory exists:

```bash
# Create directory first
mkdir -p ~/accounting/2024/

# Then run extraction
uv run scripts/extract_invoice.py invoice.pdf -o ~/accounting/2024/invoices.xlsx
```

Or use absolute paths:

```bash
uv run scripts/extract_invoice.py /path/to/invoice.pdf -o /home/user/accounting/invoices.xlsx
```

### "Duplicate detected" error

Document already exists in Excel. Options:

1. **Replace it**: Delete the row from Excel, re-run extraction
2. **Skip it**: Mark status as `duplicate` and move on
3. **Force update**: Use `--format json` to save JSON only, then manually update Excel

## Performance Tips

- **Batch classification first**: Classify all documents, then extract only the ones you need
- **Dry-run for testing**: Always use `--dry-run` to preview results before writing to Excel
- **Separate output directories**: Keep invoices, statements, and POs in different folders
- **Monitor OCR confidence**: Set up alerts when `ocr_confidence < 80` for manual review

## References

- See `references/invoice-fields.md` for complete Vietnamese VAT invoice field schema
- See `references/bank-formats.md` for supported bank formats and pattern details
- See `references/po-fields.md` for PO field definitions and delivery logic
- See `references/ocr-setup.md` for OCR installation and confidence scoring guide

## License

Part of OpenClaw Skills collection.

## Support

For issues or feature requests, refer to:
- System dependency issues: `references/ocr-setup.md`
- Field mapping questions: `references/invoice-fields.md`, `references/bank-formats.md`
- PO logic: `references/po-fields.md`
