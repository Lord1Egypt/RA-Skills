---
name: receipt-snap
description: >
  Process receipt photos and PDFs, extract vendor date amount currency, convert to EUR,
  upload to Google Drive with proper naming Vendor_Date_EURAmount.pdf, and log to a Google Sheet.
  Use when user sends a receipt with #recibo or processes expense receipts for tax reporting.
  Handles: PDF invoices, photo screenshots, USD to EUR conversion, Spanish expense categories,
  quarterly reporting for tax purposes.
metadata: {"clawdbot":{"emoji":"� 영수증","os":["darwin","linux"],"requires":{"bins":["gog"],"envvars":["RECEIPT_DRIVE_FOLDER_ID","RECEIPT_GOOGLE_SHEET_ID","RECEIPT_LOG_FILE"]},"install":[{"id":"brew","kind":"brew","formula":"faradayhq/gog/gog","bins":["gog"],"label":"Install gog CLI via Homebrew"}]}}
---

# Receipt Snap Skill

Process receipts for tax reporting. Handles receipt capture, currency conversion, Drive storage, and logging to Google Sheets.

## Setup

### 1. Install gog CLI

```bash
brew install faradayhq/gog/gog
gog auth login
```

### 2. Set environment variables

| Variable | Required | Description |
|----------|----------|-------------|
| `RECEIPT_DRIVE_FOLDER_ID` | Yes | Google Drive folder ID for uploads |
| `RECEIPT_GOOGLE_SHEET_ID` | Yes | Google Sheet ID for log rows |
| `RECEIPT_LOG_FILE` | No | Local CSV backup path (default: `~/receipts/log.csv`) |

### 3. Google Drive & Sheets setup

**Drive:** Create a folder, share it with the Google account authenticated in `gog`, copy the folder ID from the URL.

**Sheets:** Create a sheet with a tab named `log`, add headers in row 1: `Date | Vendor | Description | Original Amount | Currency | EUR Amount | Exchange Rate | Category | Drive Link | Notes`. Copy the Sheet ID from the URL.

## Model Usage

Use local model (free) for simple receipts. Escalate to MiniMax for ambiguous receipts (handwritten, poor lighting).

## Workflow

### 1. Receive Receipt
User sends receipt via Telegram with `#recibo` tag. Accepts:
- PDF invoices
- Photo screenshots of receipts
- Text descriptions (`#recibo Description: ...`)

### 2. Extract Data
Extract from receipt:
- **Vendor** (company name)
- **Date** (invoice date)
- **Amount** (total including VAT)
- **Currency** (EUR, USD, etc.)
- **Description** (what was purchased)

### 3. Check for Duplicates
Before processing, check if this receipt already exists:

```bash
gog sheets get "$RECEIPT_GOOGLE_SHEET_ID" "log!A:J" --json
```
Search for matching vendor + date + amount. If duplicate found → warn user and ask before proceeding.

### 4. Currency Conversion
If non-EUR:
- Fetch rate from `https://open.er-api.com/v6/latest/{currency}`
- Convert to EUR
- Log both original and EUR amounts

### 5. Categorize
Spanish tax categories:

- **Software y suscripciones** — SaaS, API credits, subscriptions
- **Telecomunicaciones** — phone, voicemail
- **Combustibles** — fuel, gas
- **Viajes y desplazamientos** — travel, mileage
- **Manutención y restauración** — meals (business)
- **Material informáticos** — hardware
- **Formación** — courses, education
- **Otros gastos** — other

### 6. Upload to Google Drive

```bash
gog drive upload <file> --parent "$RECEIPT_DRIVE_FOLDER_ID"
gog drive rename <file-id> "VendorName_2026-01-15_42.50EUR.pdf"
```

### 7. Log to Google Sheet

```bash
gog sheets append "$RECEIPT_GOOGLE_SHEET_ID" "log!A:J" \
  --values-json '[["2026-01-15","Vendor Name","Description","42.50","EUR","42.50","1.0","Software y suscripciones","https://drive.google.com/...","Notes"]]' \
  --insert INSERT_ROWS
```

### 8. Quarterly Report
At quarter-end:
- Generate category summary: `python3 receipt_snap.py summary`
- Zip receipt images from Drive
- Send summary + ZIP to your tax accountant

## Commands

### Process receipt
```bash
python3 receipt_snap.py process receipt.pdf \
  --vendor "Vendor Name" \
  --date 2026-01-15 \
  --amount 42.50 \
  --currency EUR \
  --category "Software y suscripciones"
```

### Summary
```bash
python3 receipt_snap.py summary
```

### Exchange rate
```bash
python3 receipt_snap.py exchange-rate
```

## Sheet Setup

Create a Google Sheet with a tab named `log`. Add this header row (A through J):

| Date | Vendor | Description | Original Amount | Currency | EUR Amount | Exchange Rate | Category | Drive Link | Notes |

## Security

- Add `receipts/` and `*.csv` to `.gitignore` — contains real financial data
- Never hardcode IDs in source files — use environment variables
- `gog` manages OAuth tokens locally — verify your Google account is secure
- Files uploaded to Drive and rows appended to Sheets leave copies on Google services
