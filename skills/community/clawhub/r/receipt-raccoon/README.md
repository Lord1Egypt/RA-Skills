# Receipt Raccoon 🦝

Extract structured data from receipts and generate spending reports. No more manual data entry.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## The Problem

Nobody likes manually entering receipt data for expense tracking. Every receipt has the same fields — merchant, date, items, prices, tax, total — but typing them all in is tedious and error-prone.

## The Solution

**Receipt Raccoon** takes raw receipt text (from OCR, a photo description, or copy-paste) and automatically:
1. **Extracts** merchant, date, line items, prices, subtotal, tax, and total
2. **Categorises** every item using keyword matching (groceries, dining, electronics, etc.)
3. **Accumulates** receipts in a JSONL ledger for ongoing tracking
4. **Generates** spending reports with top merchants, category breakdown, and monthly trends

## Quick Start

```bash
# Parse a receipt from text
python3 scripts/receipt_parser.py parse --text "$(cat receipt.txt)"

# Parse from a file
python3 scripts/receipt_parser.py parse --file receipt.txt

# Parse and save to ledger
python3 scripts/receipt_parser.py parse --file receipt.txt --append my_receipts.jsonl

# Generate a spending report
python3 scripts/receipt_parser.py report --ledger my_receipts.jsonl

# Filter by month
python3 scripts/receipt_parser.py report --ledger my_receipts.jsonl --month 2024-01

# Run the demo with sample receipts
python3 scripts/receipt_parser.py demo
```

## Example Output

### Parsed Receipt (JSON)
```json
{
  "merchant": "WHOLE FOODS MARKET #12345",
  "date": "2024-01-15",
  "items": [
    {"name": "ORGANIC BANANAS", "price": 2.99, "category": "groceries"},
    {"name": "ALMOND MILK", "price": 3.49, "category": "groceries"},
    {"name": "FREE RANGE EGGS", "price": 5.99, "category": "groceries"}
  ],
  "subtotal": 49.93,
  "tax": 4.00,
  "total": 53.93,
  "currency": "USD"
}
```

### Spending Report
```
============================================================
  🦝 RECEIPT RACCOON — Spending Report
============================================================

  Total spend:      $186.16
  Receipts:         5
  Average/receipt:  $37.23
  Total tax:        $13.87

  📊 TOP MERCHANTS
     1. WHOLE FOODS MARKET #12345  —  $53.93  (1 visits)
     2. BEST BUY #09999  —  $59.37  (1 visits)
     3. TRADER JOE'S #444  —  $27.47  (1 visits)

  🏷️  CATEGORY BREAKDOWN
     groceries      $  49.93  ( 26.8%)  █████  [7 items]
     electronics    $  54.97  ( 29.5%)  █████  [3 items]
     dining         $   9.00  (  4.8%)  █  [2 items]
```

## Features

- **Smart parser** — handles US, EU, ISO, and written date formats
- **9 spending categories** — groceries, dining, electronics, clothing, health, household, transport, entertainment, office (+ "other" fallback)
- **Weighted keyword matching** — longer keyword matches score higher for better accuracy
- **JSONL ledger** — append-only storage, easy to version control or import elsewhere
- **Monthly filtering** — generate reports for any month
- **Summary stats** — top merchants, category breakdown with percentages, monthly trends, tax totals
- **Demo mode** — 5 sample receipts show the full workflow
- **Stdlib only** — no pip installs, runs on any Python 3.10+

## Categorisation

Items are matched against 9 categories with hundreds of keywords:

| Category | Example Items |
|----------|--------------|
| Groceries | Bananas, milk, chicken, bread |
| Dining | Coffee, burger, pizza, restaurant |
| Electronics | USB cable, charger, phone case |
| Clothing | T-shirt, jeans, shoes |
| Health | Vitamins, toothpaste, bandages |
| Household | Detergent, paper towels, soap |
| Transport | Gas, parking, Uber |
| Entertainment | Movie tickets, video games |
| Office | Pens, notebooks, printer ink |

See `references/categories.md` for the full keyword list.

## Files

| File | Description |
|------|-------------|
| `SKILL.md` | Skill definition and agent workflow |
| `scripts/receipt_parser.py` | Parser + report generator |
| `references/categories.md` | Full category keyword reference |
| `references/receipt_formats.md` | Supported formats and parsing logic |

## License

MIT © Denis Voronin
