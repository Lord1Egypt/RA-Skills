---
name: unlock-pdf
description: "Remove password protection from encrypted PDFs via the PDFAPIHub cloud API. Your PDF and password are sent to pdfapihub.com for decryption. Requires a CLIENT-API-KEY header."
---

# Unlock PDF

## What It Does
Removes password protection from an encrypted PDF via the PDFAPIHub hosted API. Your PDF file and the decryption password are uploaded to PDFAPIHub servers, where the service decrypts the document and returns the unlocked PDF.

## When to Use
- Decrypt a password-protected PDF for further processing
- Remove read restrictions from a PDF you own

## Required Inputs
- `password` — the password to unlock the PDF
- Plus one of: `url`, `base64_pdf`, or multipart `file` upload

## Authentication
This skill calls the PDFAPIHub hosted API at `https://pdfapihub.com/api`. Your PDF and password are sent to PDFAPIHub servers for decryption.

Send your API key in the `CLIENT-API-KEY` header.

Get your **free API key** at [https://pdfapihub.com](https://pdfapihub.com). Full API documentation is available at [https://pdfapihub.com/docs](https://pdfapihub.com/docs).

**Security & Privacy:**
- Your PDF file and decryption password are transmitted to PDFAPIHub's cloud service over HTTPS
- Do not send highly sensitive documents or passwords you use elsewhere without understanding this risk
- Files are auto-deleted from PDFAPIHub servers after 30 days
- PDFAPIHub does not store or log passwords after processing

## Use Cases
- **Legacy Document Access** — Unlock old password-protected PDFs when you have the password
- **Workflow Automation** — Decrypt PDFs in an automated pipeline before merging, splitting, or parsing
- **Print Enablement** — Remove print restrictions from PDFs you own for printing
- **Content Extraction** — Unlock PDFs before running OCR or text extraction
- **Pre-Processing** — Decrypt encrypted PDFs before further PDF operations (merge, compress, watermark)

## Example Usage
```bash
curl -X POST https://pdfapihub.com/api/v1/unlockPdf \
  -H "CLIENT-API-KEY: your_api_key" \
  -H "Content-Type: application/json" \
  -d '{
    "url": "https://pdfapihub.com/sampleprotected.pdf",
    "password": "secret123",
    "output": "url"
  }'
```
