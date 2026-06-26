# PDF to Markdown Conversion

Convert PDF documents to structured Markdown using Mistral OCR API.

## Overview

Mistral OCR processes PDFs **directly** - no need to convert to images first! This makes the process simple and requires no external dependencies.

## Quick Example

```bash
curl -s "https://api.mistral.ai/v1/ocr" \
  -H "Authorization: Bearer $MISTRAL_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "mistral-ocr-latest",
    "document": {
      "type": "document_url",
      "document_url": "https://example.com/document.pdf"
    }
  }' | jq -r '.pages[].markdown' > output.md
```

That's it! No pdftoppm, no ImageMagick, no dependencies.

---

## Methods

### Method 1: PDF from URL

Best for publicly accessible PDFs:

```bash
curl -s "https://api.mistral.ai/v1/ocr" \
  -H "Authorization: Bearer $MISTRAL_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "mistral-ocr-latest",
    "document": {
      "type": "document_url",
      "document_url": "https://arxiv.org/pdf/2201.04234"
    }
  }'
```

### Method 2: Local PDF (Base64 Data URL)

For local files, encode as base64 and use a data URL (works on all platforms):

```bash
BASE64=$(base64 -w0 document.pdf)

curl -s "https://api.mistral.ai/v1/ocr" \
  -H "Authorization: Bearer $MISTRAL_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "mistral-ocr-latest",
    "document": {
      "type": "document_url",
      "document_url": "data:application/pdf;base64,'"$BASE64"'"
    }
  }' | jq -r '.pages[].markdown' > output.md
```

---

## Response Structure

The API returns structured JSON:

```json
{
  "pages": [
    {
      "index": 0,
      "markdown": "# Page Title\n\nContent here...",
      "images": [],
      "tables": [],
      "dimensions": {"dpi": 200, "height": 842, "width": 595}
    },
    {
      "index": 1,
      "markdown": "## Second Page\n\nMore content...",
      "images": [],
      "tables": []
    }
  ],
  "model": "mistral-ocr-latest",
  "usage_info": {
    "pages_processed": 2,
    "doc_size_bytes": 45678
  }
}
```

---

## Multi-Page Documents

### Combine all pages with separators

```bash
curl -s "https://api.mistral.ai/v1/ocr" \
  -H "Authorization: Bearer $MISTRAL_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{...}' \
  | jq -r '.pages[] | "## Page \(.index + 1)\n\n\(.markdown)\n\n---\n"' > full_document.md
```

### Extract specific page

```bash
# Get page 3 only (index 2)
... | jq -r '.pages[2].markdown'
```

---

## Table Handling

For documents with tables, use HTML format:

```bash
curl -s "https://api.mistral.ai/v1/ocr" \
  -H "Authorization: Bearer $MISTRAL_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "mistral-ocr-latest",
    "document": {...},
    "table_format": "html"
  }'
```

Mistral OCR 3 supports proper `colspan` and `rowspan` for complex tables.

---

## Quality Tips

| Issue | Solution |
|-------|----------|
| Blurry text | Use higher quality PDF source |
| Tables broken | Use `"table_format": "html"` |
| Headers missed | OCR 3 has improved header detection |
| Columns merged | OCR 3 better handles multi-column layouts |

---

## Prompt Variations (via Document QnA)

For specialized extraction, combine OCR with Mistral's Document QnA:

### Legal Documents
```
"Extract all article numbers, sections, and subsections. Keep citations intact."
```

### Academic Papers
```
"Extract content preserving equations (LaTeX notation) and figure references."
```

### Invoices/Forms
```
"Extract as structured data: invoice number, date, line items, totals."
```

---

## Comparison: Old vs New Approach

| Aspect | Old (Vision API) | New (OCR API) |
|--------|------------------|---------------|
| Dependencies | pdftoppm/ImageMagick required | None |
| Steps | PDF → Images → OCR | PDF → OCR directly |
| Speed | Slow (convert + multiple calls) | Fast (single call) |
| Cost | Higher (per-image) | Lower ($2/1000 pages) |
| Table quality | Basic | HTML with colspan/rowspan |

---

## Limitations

- **Maximum file size:** Check current limits at Mistral docs
- **Encrypted PDFs:** Must be unencrypted
- **Handwritten text:** Works but accuracy varies
- **Very complex layouts:** May need post-processing

---

## Output Example

**Input:** Scanned contract page

**Output:**
```markdown
# Service Agreement

**Date:** January 15, 2026
**Parties:** Company A and Company B

## Article 1: Scope of Services

The Provider agrees to deliver the following services:

1. Software development
2. Technical support
3. Monthly maintenance

## Article 2: Payment Terms

| Milestone | Amount | Due Date |
|-----------|--------|----------|
| Signing | $5,000 | Jan 20 |
| Delivery | $10,000 | Mar 15 |
```
