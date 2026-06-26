---
emoji: 🧾
name: tally-prime-entry
version: 1.0.1
author: Maxxit
description: >-
  Post purchase, sales, and bank entries in TallyPrime with GST voucher
  classes. Generate sales invoice PDFs via tallyca.
disableModelInvocation: false
requires:
  env:
    - TALLY_URL
metadata:
  openclaw:
    requiredEnv:
      - TALLY_URL
    bins:
      - curl
      - tallyca
      - scribe
    primaryCredential: TALLY_URL
---

# TallyPrime Entry Skill

Connect to a **locally running** TallyPrime instance via **XML-over-HTTP**. All requests are HTTP POST to `$TALLY_URL` (commonly `http://localhost:9000`).

## Scope

This skill handles only:

| Category | Modes / Types |
|---|---|
| **Purchase Voucher** | Item Invoice · Accounting Invoice · As Voucher |
| **Purchase Voucher Classes** | Purchase @ 5 % · Purchase @ 18 % · Purchase @ 28 % |
| **Sales Voucher** | Item Invoice · As Voucher |
| **Sales Voucher Classes** | Sales @ 5 % · Sales @ 18 % · Sales @ 28 % |
| **Bank Statement** | Payment · Receipt · Contra |
| **Sales Invoice PDF** | `tallyca` CLI |

For anything outside this scope, tell the user this skill does not cover that task.

## Critical rules (must follow)

1. **Never assume company** — if not explicit, ask which company before posting.
2. **Never guess ledgers** — verify ledger exists before posting; ask user if unsure.
3. **Dates are `YYYYMMDD`** (no separators).
4. **Unique GUID per voucher** — prevents duplicates on retries.
5. **Voucher totals must balance** — sum of all `AMOUNT` values = 0.
6. **Escape XML** — `&` → `&amp;` in narration and party names.
7. **Confirm before posting** — every Create is a write; confirm company and intent first.
8. **Bill-wise allocations on party ledgers** — include `BILLALLOCATIONS.LIST` to keep outstandings correct.
9. **`LEDGERENTRIES.LIST` in Invoice Voucher View** — never use `ALLLEDGERENTRIES.LIST` when `OBJVIEW="Invoice Voucher View"` is set; Tally silently ignores it.
10. **Post-entry review is mandatory** — after every voucher post, fetch it back and verify before telling the user it is done.
11. **Voucher class — confirm before posting** — run the class decision rules at the top of the relevant purchase/sales reference file before posting.
12. **Check import response** — after every POST, read `CREATED`/`ERRORS` from Tally's response (see `reference/reports.md`). Never confirm success if `ERRORS > 0` or `CREATED = 0`.

## Step 0: Server check

```bash
curl -s --max-time 5 "$TALLY_URL"
```

Expected response:

```xml
<RESPONSE>TallyPrime Server is Running</RESPONSE>
```

If no response, ask the user to open TallyPrime and enable integrations on the correct port.

## Step 1: Company

Ask for the company name if not provided. Use the **exact** spelling in `SVCURRENTCOMPANY`.

## Step 2: Invoice / image extraction (mandatory OCR)

When the user sends a **PDF, JPEG, JPG, or PNG** invoice or bill, use the `scribe` CLI. Do not extract data with the LLM directly.

### PDF extraction

```bash
mkdir -p "scribe-extractions"
scribe type "<input.pdf>"
scribe extract -f txt "<input.pdf>" "scribe-extractions/<id>.txt"
```

Read the `.txt` file and parse the invoice fields. If quality is poor (image-native PDF), run OCR first:

```bash
scribe recognize -h -o "scribe-extractions/<id>-ocr" "<input.pdf>"
scribe extract -f txt "scribe-extractions/<id>-ocr/<stem>.pdf" "scribe-extractions/<id>-recognized.txt"
```

### Image extraction (JPEG / PNG)

1. Try direct extraction:

   ```bash
   scribe extract -f txt "<input.jpeg>" "scribe-extractions/<id>.txt"
   ```

2. If output is empty, run OCR:

   ```bash
   scribe recognize -h -o "scribe-extractions/<id>-ocr" "<input.jpeg>"
   scribe extract -f txt "scribe-extractions/<id>-ocr/<stem>.pdf" "scribe-extractions/<id>-recognized.txt"
   ```

### After extraction

Present a clean summary to the user: supplier/customer, GSTINs, invoice number, date, line items, taxable value, CGST/SGST/IGST, round-off, total. Ask for confirmation before posting.

If extraction fails, say "I could not read this bill clearly. Please resend a clearer photo or PDF." — do not mention CLI, OCR, errors, or paths.

## Step 2b: Verify / create masters

Before posting any voucher, verify that all required ledgers and (for Item Invoice) stock items exist. Use `reference/ledgers.md` and `reference/inventory.md`.

**Ledger check** (`reference/ledgers.md`):
- Fetch `List of Accounts` and confirm party ledger, purchase/sales ledger, and GST ledgers exist.
- If any are missing, create them using the templates in `reference/ledgers.md` before posting.

**Inventory check — Item Invoice only** (`reference/inventory.md`):
- Confirm each stock item referenced in the invoice exists in Tally (fetch Stock Summary).
- If missing, create in order: Stock Group → UOM → Stock Item.
- Confirm godown: default is `Main Location` / `Primary Batch` unless the company has custom godowns.

**Bank statement pre-flight** (`reference/reports.md`):
- Before posting bank entries, fetch all ledger names (Ledger Names query in `reference/reports.md`).
- Present the mapping to the user: "These are the ledgers I will use: [bank], [parties]. Confirm to proceed."
- Do not post until confirmed.

## Step 3: Post vouchers

Load only the file that matches the task — this keeps context lean:

| Task | Reference file |
|---|---|
| Purchase — stock items | `reference/purchase.md` → Item Invoice |
| Purchase — services/expenses (invoice layout) | `reference/purchase.md` → Accounting Invoice |
| Purchase — classic By/To view | `reference/purchase.md` → As Voucher |
| Sales — stock items | `reference/sales.md` → Item Invoice |
| Sales — no items (ledger-only) | `reference/sales.md` → As Voucher |
| Money received from customer | `reference/bank.md` → Receipt |
| Money paid to vendor/expense | `reference/bank.md` → Payment |
| Bank/cash transfer | `reference/bank.md` → Contra |
| Ledger check / create | `reference/ledgers.md` |
| Stock item check / create | `reference/inventory.md` |

**Voucher class decision** — the class decision rules and GST ledger name table are at the top of each purchase/sales reference file. Run them before posting.

**Preflight checklist before any Create:**

| # | Check | Reference | Block if… |
|---|---|---|---|
| 1 | Company confirmed | — | Not given — ask |
| 2 | Server reachable | — | No response |
| 3 | Party ledger exists | `reference/ledgers.md` | Missing — create first |
| 4 | Purchase/Sales/GST ledgers exist | `reference/ledgers.md` | Missing — create first |
| 5 | Stock items exist (Item Invoice only) | `reference/inventory.md` | Missing — create first |
| 6 | Voucher class confirmed (Purchase/Sales) | purchase/sales reference file | Unknown — ask, never guess |
| 7 | GST header fields available (class mode) | — | Any missing — ask |
| 8 | Totals balance | — | Mismatch — fix before posting |

## Step 4: Post-entry review (mandatory)

After every voucher Create:

1. **Read the import response** — check `CREATED` and `ERRORS` fields (`reference/reports.md`). Stop if `ERRORS > 0`.
2. **Fetch the voucher back** — use Voucher Register (preferred) or Day Book as fallback (`reference/reports.md`).
3. **Match against the intended entry** — company, voucher type, number, date, party, all ledgers, amounts, GST split, bill-wise allocations.
4. If everything matches, summarize to the user in accountant language (no XML, no HTTP terms).
5. If anything is off, do not confirm completion — explain the mismatch and ask how to proceed.

Never say "Entry posted" without completing this review.

## PDF Generation — Sales Invoice

Use the `tallyca` CLI. Do **not** build PDFs manually.

### Preflight

```bash
tallyca --version   # must be >= 1.1.0
```

If missing or older: `npm install -g tallyca@latest`

### Minimum user input

Ask the user for only these 4 fields. Everything else is auto-filled from Tally:

| Field | Source |
|---|---|
| `party-name` | User |
| `item` | User — stock item name |
| `qty` | User |
| `rate` | User — per unit |

### Auto-fill sequence (run before calling tallyca)

Execute in this order. Each step reduces what the user needs to provide:

| Field | How to auto-fill | Reference |
|---|---|---|
| `date` | Default to today (`D/M/YYYY`) | — |
| `invoice-no` | Fetch last Sales voucher number → +1 | `reference/reports.md` |
| `unit` | Fetch stock item master → `BASEUNITS` | `reference/inventory.md` |
| `hsn-code` | Fetch stock item master → `HSNDETAILS.LIST > HSNCODE` | `reference/inventory.md` |
| `gst-rate` | Fetch stock item master → IGST rate from `GSTDETAILS.LIST`; or parse `@ XX %` from item name | `reference/inventory.md` |
| `customer-gstin` | Fetch party ledger → `$PARTYGSTIN` | `reference/ledgers.md` |
| `place-of-supply` | Fetch party ledger → `$PriorStateName`; if same state as company → intra-state (CGST+SGST), else IGST | `reference/ledgers.md` |
| `billing-address` | Fetch party ledger → `$Address` (line 1); remaining lines from `ADDRESS.LIST` in any recent voucher to that party | `reference/ledgers.md` |
| `company-gstin` | Parse `<CMPGSTIN>` from any recent Day Book sales voucher export | `reference/reports.md` |
| `company-address` | Fetch company → `$Address`, `$PinCode`, `$StateName` via Company TDL collection | `reference/ledgers.md` |

**Fallback:** if any auto-fill fails, use `--json-errors`. The CLI returns a `missing` array — ask the user only for those specific fields, then retry.

### From structured fields (preferred)

Always use `--no-interactive` and `--json-errors` when running non-interactively:

```bash
tallyca generate:invoice \
  --company "ABC Company" \
  --company-gstin "GSTIN_HERE" \
  --company-address "Full company address, State PIN" \
  --party-name "XYZ Party" \
  --customer-gstin "PARTY_GSTIN" \
  --billing-address "Party address, State" \
  --invoice-no 186 \
  --date "2/1/2026" \
  --place-of-supply "Uttar Pradesh" \
  --item "PQR Item" \
  --qty 140 \
  --unit Bag \
  --rate 279.66 \
  --hsn-code 25322210 \
  --gst-rate 18 \
  --b2b \
  --output invoice_186.pdf \
  --no-interactive \
  --json-errors
```

**On exit code 2 (validation failure):** parse JSON from stderr, read the `missing` array, ask the user only for those fields, then retry. Never hand-build a PDF.

```json
{"error":"validation","message":"Missing required invoice fields","missing":["place-of-supply","unit"],"warnings":[]}
```

### From raw WhatsApp / Telegram text

```bash
tallyca from-text \
  --company "ABC Company" \
  --text "Party Name: XYZ Party
Invoice No.: 186
Date: 2/1/2026
Place of Supply: Uttar Pradesh
Item: PQR Item 2523 @ 18 %
Qty: 140 Bag
Rate: 279.66/Bag
HSN Code: 25322210
Amount: 39152.40
Make sure to use voucher class Sales @ 18 %" \
  --output invoice_186.pdf \
  --no-interactive \
  --json-errors
```

### On Linux / AWS without Chromium

```bash
export TALLYCA_PDF_BACKEND=pdfmake
```

Then run the same command. Do not substitute a hand-built PDF.

## GUID pattern

```
{companyShort}-{voucherType}-{invoiceNo}-{date}
```

Examples: `abc-purchase-inv001-20260115` · `abc-sales-186-20260201`

## Accountant-friendly responses

After posting, do **not** mention XML, HTTP, payloads, status codes, or integration internals. Say:

- "Entry posted" (not "XML import succeeded")
- "Tally is connected" (not "server responded 200")
- Summarize: company, voucher type, date, party/ledger names, amounts, tax split, narration.
