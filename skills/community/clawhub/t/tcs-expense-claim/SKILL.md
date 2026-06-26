---
name: expense-claim
description: >
  End-to-end business travel expense claim processor. Use this skill whenever
  a user uploads receipts, bills, invoices, or screenshots of expenses and wants
  to organize, categorize, or submit a claim. Triggers include: "process my
  bills", "help me file expenses", "sort my receipts", "create expense PDFs",
  "how much did I spend", "organize my travel bills", "prepare claim for TCS /
  SAP Concur / iExpense", or any upload of multiple receipt images/PDFs with
  intent to claim reimbursement. Also triggers when user asks for a daily spend
  summary, category-wise breakdown, or currency conversion of travel expenses.
  Always use this skill — even if the user only uploads a single receipt — if
  reimbursement or expense filing is the goal.
---

# Expense Claim Skill

Automates the full workflow of turning a pile of receipt images and PDFs into
clean, submission-ready expense claim packages — sorted by date and category,
with currency conversions and a summary table.

---

## Workflow Overview

Run these five phases in order. Never skip a phase.

```
Phase 1 → Ingest & Parse all uploaded files
Phase 2 → Classify each bill (date, vendor, category, currency, amount)
Phase 3 → Generate per-day per-category PDFs
Phase 4 → Generate the expense spreadsheet (XLSX)
Phase 5 → Output summary tables for manual form entry
```

---

## Phase 1 — Ingest & Parse

1. List every file in `/mnt/user-data/uploads/`
2. For each file:
   - **Images** (`.png`, `.jpg`, `.jpeg`): read visually — extract date, vendor,
     amount, currency, bill number, and any GST/VAT breakdown
   - **PDFs** (`.pdf`): use `pypdf` to extract text; if text is sparse, treat
     as scanned and read visually
3. Ask the user if any files are missing or unreadable before proceeding

---

## Phase 2 — Classify

Map every bill to this schema:

```
date        : DD-Mon-YY   (e.g. 13-Feb-26)
vendor      : string
location    : city / airport / country
category    : one of the TCS categories below
currency    : INR | USD | EUR | GBP | SGD | AED | ...
amount_orig : float (as printed on bill)
bill_no     : string (from receipt; use "attached" if none)
notes       : brief description of items
```

### TCS Expense Categories (map every bill to one)

| TCS Category | What goes here |
|---|---|
| Travel Expenses – Conveyance | Uber, Ola, Lyft, taxis, local cabs, airport transfers |
| Ticket Expenses – Air Tickets | Airline tickets, excess baggage fees (keep SEPARATE per bill) |
| Ticket Expenses – Train Tickets | Rail bookings |
| Ticket Expenses – Bus Tickets | Bus / coach bookings |
| Hotel Accommodation | Hotel folios, checkout invoices (NOT room dining — that's Meal) |
| Travel Expenses – Meal | All food, beverages, airport snacks, restaurant bills, delivery (Zomato/Swiggy), cafe receipts |
| Client Entertainment – Travel | Meals/entertainment where clients were present |
| Car Expenses | Fuel, parking, tolls |
| Communication Expenses | SIM cards, roaming, internet dongles |
| Conference and Training Courses | Registration fees, course materials |

### Special Rules

- **Room dining** at a hotel → Meal (NOT Hotel Accommodation)
- **Zomato/Swiggy orders**: bundle restaurant bill + platform fee + delivery fee
  into ONE line item with the combined total
- **Delta / airline excess baggage** → Air Tickets (separate PDF per bill)
- **Airport retail** (water, snacks, chocolates) → Meal
- **Sweets / gifts** (e.g. Kantis, mithai shops) → Meal (flag with note:
  *"verify if gift policy applies"*)
- **Multiple bills same day same category** → merged into one PDF

---

## Phase 3 — Generate PDFs

Read `/mnt/skills/public/pdf/SKILL.md` before running this phase.

**Naming convention:**
```
DD_Mon_YYYY_<TCS_Category_Underscored>.pdf
```
Examples:
```
13_Feb_2026_Travel_Expenses_Conveyance.pdf
13_Feb_2026_Travel_Expenses_Meal.pdf
13_Feb_2026_Ticket_Expenses_Air_Tickets.pdf
20_Feb_2026_Hotel_Accommodation.pdf
```

**Script to use:** `scripts/build_pdfs.py`
- Converts images → PDF pages using `img2pdf` + `Pillow`
- Merges existing PDFs using `pypdf`
- Outputs to `/mnt/user-data/outputs/bills_by_category/`

Run: `python3 scripts/build_pdfs.py`

Present all generated PDFs to the user using `present_files`.

---

## Phase 4 — Generate XLSX Summary

Read `/mnt/skills/public/xlsx/SKILL.md` before running this phase.

**Script to use:** `scripts/build_xlsx.py`

The spreadsheet has two sheets:

### Sheet 1: "All Expenses"
Columns: `#, Date, Vendor, Location, Category, Currency, Amount (Original),
Amount (INR equiv.), Notes`

Color coding:
- Blue fill → Travel / Conveyance / Air Tickets
- Green fill → Food & Meal
- Orange fill → Accommodation
- Purple fill → Other

### Sheet 2: "Summary"
Rows = TCS categories; Columns = `Category, # Items, Original Amounts, INR Equiv.`
Plus a Grand Total row with all-in USD equivalent.

**Currency conversion** — use rates from `references/fx_rates.md` or fetch live
rates if web search is available. Always show the rate used and its date.

Output to `/mnt/user-data/outputs/expense_claim.xlsx`

---

## Phase 5 — Summary Tables for Manual Entry

Always output three tables in chat so the user can fill their expense portal
directly:

### Table A: Conveyance entries
`Bill Date | From Location | To Location | Bill No | Currency | Amount | Remarks`

### Table B: Meal entries
`Bill Date | Name of Hotel/Restaurant | Bill No | Currency | Amount | Remarks`

### Table C: Hotel entries
`Bill Date | From Date | To Date | Bill No | Currency | Amount | Remarks`

### Table D: Air Ticket entries
`Bill Date | Bill No | Currency | Amount | Remarks`

### Table E: Day-wise spend summary
`Date | Conveyance | Air Ticket | Hotel | Meal (local currency) | Day Total (USD)`
— Include a GRAND TOTAL row at the bottom.

---

## Currency Conversion Rules

See `references/fx_rates.md` for standard rates.

- Always convert everything to **INR** for Indian domestic claims
- Always convert everything to **USD** for international / global summary
- Show the exchange rate used in every table and in the XLSX notes
- If the trip spans multiple currencies, show original + converted in the XLSX
- Flag any bill where the currency on the receipt doesn't match the card
  currency (possible forex fee)

---

## Output Checklist

Before finishing, confirm all of these exist:

- [ ] One PDF per day per category in `/mnt/user-data/outputs/bills_by_category/`
- [ ] `expense_claim.xlsx` with both sheets
- [ ] Table A–E printed in chat
- [ ] Grand total in USD stated clearly
- [ ] Any flagged items noted (gift policy, missing bills, illegible receipts)

---

## Error Handling

| Problem | Action |
|---|---|
| Can't read a receipt | Note it, ask user to confirm amount manually |
| Date missing from bill | Infer from surrounding bills or ask user |
| Currency ambiguous | Default to country of purchase; flag for user |
| Bill number not on receipt | Use "attached" |
| Multiple receipts same vendor same day | Merge into one line, note qty |

---

## Reference Files

- `references/fx_rates.md` — Standard FX rates for common travel corridors
- `references/tcs_categories.md` — Full TCS category eligibility rules
- `scripts/build_pdfs.py` — PDF generation script
- `scripts/build_xlsx.py` — Excel generation script
