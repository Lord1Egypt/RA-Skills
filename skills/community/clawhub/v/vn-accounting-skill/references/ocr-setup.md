# OCR Setup Guide

## System Dependencies

The accounting skill requires these system packages for OCR:

### Ubuntu / Debian
```bash
sudo apt install tesseract-ocr tesseract-ocr-vie poppler-utils
```

### macOS (Homebrew)
```bash
brew install tesseract tesseract-lang poppler
```

### Verify Installation
```bash
uv run {baseDir}/scripts/ocr_utils.py check
```

This checks for:
- `tesseract` — OCR engine for scanned documents / images
- `tesseract-ocr-vie` — Vietnamese language pack (critical for hóa đơn)
- `poppler-utils` — PDF-to-image conversion (needed for scanned PDFs)

## How OCR Works in This Skill

### Strategy (automatic per file)

1. **Digital PDFs**: Extracted via `pdfplumber` (fast, high accuracy, no OCR needed)
2. **Scanned PDFs**: If pdfplumber gets <50 chars/page, falls back to `pdf2image` + `pytesseract` at 300 DPI
3. **Images (JPG/PNG/TIFF)**: Direct OCR via `pytesseract` with grayscale preprocessing

### Confidence Reporting

Every extraction reports two confidence scores:
- **OCR Confidence**: Quality of text extraction (pytesseract word-level average)
- **Extraction Confidence**: How many expected fields were successfully parsed

| OCR Confidence | Meaning |
|---------------|---------|
| > 90% | Excellent — clean digital document |
| 85-90% | Good — minor OCR artifacts |
| 70-85% | Fair — some words may be wrong, review amounts |
| < 70% | Poor — likely needs manual review |

## Troubleshooting

| Problem | Solution |
|---------|----------|
| "tesseract is not installed" | `sudo apt install tesseract-ocr` |
| Vietnamese text garbled | `sudo apt install tesseract-ocr-vie` |
| "poppler-utils not installed" | `sudo apt install poppler-utils` |
| Low confidence on clean PDF | Likely a digital PDF — pdfplumber should work fine |
| Amounts parsed as 0 | Check VND format (dots as thousands separators) |
| Scanned PDF gets blank text | Increase DPI or check if PDF is password-protected |
