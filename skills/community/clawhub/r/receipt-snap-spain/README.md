# Receipt Snap

> Process expense receipts for Spanish tax — extract data, convert currencies, upload to Google Drive, log to Google Sheets.

Designed for freelancers and small businesses in Spain who need to track expenses for their *gestora fiscal* (tax accountant). Works with any AI assistant that supports the OpenClaw skill format.

## What it does

1. **Receive** — receipts come in via Telegram (photo, PDF, or text)
2. **Extract** — AI extracts vendor, date, amount, currency
3. **Convert** — converts USD/EUR/etc. to EUR using live exchange rates
4. **Upload** — saves receipt PDF to Google Drive with standardized naming
5. **Log** — appends a row to a Google Sheet (date, vendor, amount, category, etc.)
6. **Report** — generates quarterly summaries for your tax accountant

## Setup

### Prerequisites

- macOS or Linux
- [gog CLI](https://github.com/faradayhq/gog) — `brew install faradayhq/gog/gog`
- Google account with Google Drive and Google Sheets
- OpenClaw or compatible AI assistant

### Google Drive Setup

1. Create a folder in Google Drive for receipts
2. Copy the folder ID from the URL: `drive.google.com/drive/folders/YOUR_FOLDER_ID_HERE`
3. Share the folder with your gog-connected Google account

### Google Sheets Setup

1. Create a new Google Sheet
2. Name the first sheet tab `log`
3. Add this header row in row 1:

| A | B | C | D | E | F | G | H | I | J |
|---|---|---|---|---|---|---|---|---|---|
| Date | Vendor | Description | Original Amount | Currency | EUR Amount | Exchange Rate | Category | Drive Link | Notes |

4. Copy the Sheet ID from the URL: `docs.google.com/spreadsheets/d/YOUR_SHEET_ID_HERE/edit`

### Installation

Copy this skill to your OpenClaw skills directory:

```bash
cp -r receipt-snap ~/.openclaw/skills/
```

### Configuration

Copy `.env.example` to `.env` and fill in your values:

```bash
cp .env.example .env
# Edit .env:
# RECEIPT_DRIVE_FOLDER_ID="1abc123XYZ..."
# RECEIPT_GOOGLE_SHEET_ID="1abc123XYZ..."
```

Or set environment variables in your shell:

```bash
export RECEIPT_DRIVE_FOLDER_ID="YOUR_FOLDER_ID"
export RECEIPT_GOOGLE_SHEET_ID="YOUR_SHEET_ID"
export RECEIPT_LOG_FILE="~/receipts/log.csv"
```

## Usage

### Via Telegram (with OpenClaw)

Send any receipt with the tag `#recibo`:

```
#recibo [attach receipt photo or PDF]
```

The AI assistant will:
1. Extract the data automatically
2. Ask you for the category (if not obvious)
3. Upload to Drive and log to Sheets
4. Confirm with a summary

### Via Command Line

```bash
# Process a receipt
python3 receipt_snap.py process receipt.pdf \
  --vendor "Adobe Systems" \
  --date 2026-02-16 \
  --amount 15.12 \
  --currency EUR \
  --category "Software y suscripciones"

# Check summary
python3 receipt_snap.py summary

# Check current exchange rate
python3 receipt_snap.py exchange-rate
```

## Spanish Tax Categories

For *Castilla y León* fiscal requirements (adjust for your region):

| Category | Use for |
|---|---|
| Software y suscripciones | SaaS, API credits, subscriptions |
| Telecomunicaciones | Phone, internet |
| Combustibles | Fuel, gas |
| Viajes y desplazamientos | Travel, mileage |
| Manutención y restauración | Meals (business only) |
| Material informático | Hardware |
| Formación | Courses, education |
| Otros gastos | Miscellaneous |

## Quarterly Reporting

At the end of each quarter:

```bash
# Generate summary
python3 receipt_snap.py summary

# All receipts are in Google Drive in folder: YOUR_FOLDER_ID
# Sheet is at: https://docs.google.com/spreadsheets/d/YOUR_SHEET_ID
```

Download the Drive folder as a ZIP, attach the Google Sheet summary, and send to yourgestora fiscal.

## File Structure

```
receipt-snap/
├── SKILL.md              # OpenClaw skill definition
├── receipt_snap.py       # Core processing script (env vars, see .env.example)
├── .env.example          # Template — copy to .env and fill in IDs
├── .gitignore            # Excludes .env and local CSV logs
├── README.md
└── log.csv               # Local backup log (NOT committed — contains financial data)
```

## Security Notes

- **Google credentials**: Managed by `gog` CLI — never hardcode OAuth tokens
- **Drive/Sheet IDs**: Replace with your own before using
- **Local log**: Add `log.csv` to `.gitignore` — it contains real financial data
- **Receipt photos**: Stored in your Google Drive — not in this repo

## License

MIT — use freely, adapt to your workflow.
