---
name: receipts
description: Extract structured transaction data from image or PDF receipts using the ReceiptExtract API (https://www.receiptextract.com). Use when the user wants merchant/date/items/tax/total parsed from a receipt photo, scan, or PDF; wants to test ReceiptExtract on sample files; wants JSON/CSV output; or wants help wiring ReceiptExtract into automations, scripts, or agent workflows.
required_env_vars:
  - RECEIPTEXTRACT_API_TOKEN
secrets:
  - RECEIPTEXTRACT_API_TOKEN
network_access:
  - https://www.receiptextract.com
---

# Receipts

Extract transaction data from receipt images or PDFs with ReceiptExtract.

Keep the workflow simple: locate the API token, upload one receipt file (or a directory for bulk mode), inspect the JSON, then present either raw JSON or a cleaned summary. Prefer the bundled helper script for repeatable usage.

## Quick workflow

1. Identify the input file
   - Accept common image formats (`.jpg`, `.jpeg`, `.png`, `.webp`) and PDFs.
   - If the file came from chat, use the attached local path.

2. Locate the API token
   - Set `RECEIPTEXTRACT_API_TOKEN` in your environment before running commands.
   - Do not paste the token back into chat.

3. Call the upload endpoint
   - Endpoint: `POST https://www.receiptextract.com/api/receipt/upload`
   - Auth header: `Authorization: Bearer <token>`
   - Multipart form field: `file`

4. Parse the response
   - Success shape typically includes:
     - `success`
     - `data.merchant`
     - `data.date`
     - `data.items[]`
     - `data.tax`
     - `data.total`
     - `data.correctnessCheck`
     - `data.taxBreakdown[]`
     - `creditInfo`
     - `savedReceiptId`

5. Present the result
   - For humans: summarize merchant, date, items, tax, total, and any anomalies.
   - For integrations: return raw JSON or convert to CSV.

## Preferred command

Use the helper script:

```bash
export RECEIPTEXTRACT_API_TOKEN="your-token"
python3 scripts/extract_receipt.py /path/to/receipt.png
```

Optional flags:

```bash
python3 scripts/extract_receipt.py /path/to/receipt.pdf --format summary
python3 scripts/extract_receipt.py /path/to/receipt.jpg --format csv
python3 scripts/extract_receipt.py --input-dir /path/to/receipts --format summary
python3 scripts/extract_receipt.py --input-dir /path/to/receipts --recursive --format json
```

## Bulk processing

Use `--input-dir` to process multiple receipts in one run. The helper script sends one API request per file and continues even if some files fail.

- Supported file types: `.jpg`, `.jpeg`, `.png`, `.webp`, `.pdf`
- Use `--recursive` to include nested folders
- Exit code is non-zero when one or more files fail
- Each receipt consumes credits independently

## Fallback command

Use curl when the helper script is unnecessary:

```bash
curl -sS -X POST "https://www.receiptextract.com/api/receipt/upload" \
  -H "Authorization: Bearer $RECEIPTEXTRACT_API_TOKEN" \
  -F "file=@/path/to/receipt.png"
```

## Output handling

### JSON

Prefer JSON when the user wants the full extracted payload or when another tool will consume the result. In bulk mode, JSON includes `processed`, `succeeded`, `failed`, and per-file results.

### Summary

In bulk mode, summary prints one status line per file followed by total counts.

Use a concise format like:

```text
Merchant: Walmart
Date: 2023-06-09
Total: 76.37
Tax: 8.18
Items:
- BEDDING — 39.97
- STEAMER — 27.97
```

### CSV

When the user asks for CSV, output line-item rows with these columns when available:

- `source_file` (bulk mode)
- `merchant`
- `date`
- `description`
- `quantity`
- `total_price`
- `item_tax`
- `sku`
- `receipt_tax`
- `receipt_total`
- `saved_receipt_id`
- `http_status` (bulk mode)
- `success` (bulk mode)
- `error` (bulk mode)

## Error handling

Interpret common failures like this:

- `400` — invalid input, missing file, unsupported type, or file too large
- `401` — missing/invalid token
- `402` — insufficient credits
- `429` — rate limited; retry with backoff
- `500` — server error; safe to retry carefully

If the response is malformed or `success` is false:
- show the error plainly
- do not invent extracted data
- mention likely causes if obvious (bad token, no credits, unsupported file)

## Practical notes

- Treat the API result as the source of truth, but sanity-check obvious issues.
- Flag suspicious output instead of silently "fixing" it.
  - Example: Canadian receipt with tax currency labeled `USD`.
- `correctnessCheck: true` is a useful confidence signal, not a guarantee.
- Preserve the original file path and `savedReceiptId` when useful for traceability.
- In bulk mode, keep one request per file and preserve each source file path for traceability.

## Security

- Keep the token out of chat replies.
- Prefer environment variables or secret managers over embedding tokens in scripts.
- Do not commit tokens, raw headers, or secret-bearing examples into git.

## Resources

- Helper script: `scripts/extract_receipt.py`
- API reference notes: `references/api.md`
