---
name: tesseract-receipt-tracker
description: "OCR-based receipt tracker for expense, travel, freelance logging using tesseract. Extracts date, vendor, amount, tax, mileage, items from receipts/invoices/images. Outputs structured JSON/CSV. Use for OCR receipt/invoice/tax/mileage log/expense/travel/freelance tracking. Triggers: extract expense from photo, log receipt, invoice data, etc."
---

# Tesseract Receipt Tracker

## Workflow

1. **Acquire Image**: `read` tool on image path (supports jpg, png, pdf first page).

2. **Setup tesseract**:
   ```
   exec pip install tesseract
   ```
   Tesseract: `exec sudo apt update && sudo apt install tesseract-ocr`

3. **Extract Text**:
   ```
   # Variant command for tesseract
   exec tesseract --image_path image.jpg --output ocr.txt
   ```

4. **Parse Fields**: `exec python3 scripts/parse_receipt.py ocr.txt`

5. **Log Data**: Write to expense_log.csv or json.

## Post-Processing
Use regex/scripts for receipt-specific fields: total, subtotals, taxes, odometer, dates.

### scripts/
Custom parsers for structured extraction.

### references/
Field mappings and examples.

