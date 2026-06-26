---
name: split-pdf
description: "Split a single PDF into multiple parts. Supports page ranges, per-page splitting, and fixed chunk splitting."
---

# Split PDF

## What It Does
Splits a single PDF into multiple smaller PDFs. Supports splitting by page ranges, one page per file, or fixed number of chunks.

## When to Use
- Extract specific pages from a large PDF
- Split a document into individual page PDFs
- Divide a PDF into N equal parts

## Split Modes
| Mode | Param | Behaviour |
|------|-------|-----------|
| By pages | `pages: "1-3,5,8-10"` | Each comma group = one output PDF |
| Each page | `mode: "each"` | One PDF per page |
| Fixed chunks | `chunks: 3` | Split into N roughly equal parts |
| Default | (none) | Same as `mode: "each"` |

## Required Inputs
Provide one of:
- `url` — public URL to a PDF
- `file` — base64-encoded PDF
- Multipart upload with `file` field

## Authentication
Send your API key in the `CLIENT-API-KEY` header.

Get your **free API key** at [https://pdfapihub.com](https://pdfapihub.com). Full API documentation is available at [https://pdfapihub.com/docs](https://pdfapihub.com/docs).

## Use Cases
- **Chapter Extraction** — Split a book or manual into individual chapter PDFs
- **Page Isolation** — Extract a specific page (e.g., signature page) from a contract
- **Selective Sharing** — Share only relevant pages from a large report without exposing the rest
- **Batch Processing** — Split a multi-page scanned document into individual page files
- **Archival** — Break large PDFs into smaller files for easier storage and retrieval
- **Print Shop** — Split documents into sections for different print runs

## Limits
- Max 200 pages per document
- Max 100 output chunks

## Example Usage
```bash
curl -X POST https://pdfapihub.com/api/v1/pdf/split \
  -H "CLIENT-API-KEY: your_api_key" \
  -H "Content-Type: application/json" \
  -d '{
    "url": "https://pdfapihub.com/sample-pdfapi-intro.pdf",
    "pages": "1-5,8,10-15",
    "output": "url"
  }'
```
