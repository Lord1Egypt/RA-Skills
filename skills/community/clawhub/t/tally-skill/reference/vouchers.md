# Vouchers (Create / Alter / Cancel) — TallyPrime XML

This file contains **full voucher XML templates** for CA workflows, including returns (Credit/Debit Notes), Contra, bill-wise allocation, and safe update/cancel patterns.

## Conventions (must follow)

- Always set `SVCURRENTCOMPANY`.
- Always set `DATE` as `YYYYMMDD`.
- Always include a unique `GUID` for idempotency.
- For bills/outstanding tracking, include `BILLALLOCATIONS.LIST` on the **party ledger entry**.
- Ensure voucher totals match (sum of amounts = 0).
- Escape XML special characters (`&` → `&amp;`).

## Voucher class — decision rules

Follow this decision tree **every time** before posting a Purchase or Sales voucher. Do not skip steps.

```
Does the company's voucher type have a class configured?
│
├─ YES → What is the exact class name?
│         │
│         ├─ Confirmed (e.g. "Purchase @ 18 %")
│         │   → Use Accounting Invoice Mode with class template below.
│         │   → Set CLASSNAME, CMPGSTIN, PARTYGSTIN, GSTREGISTRATIONTYPE, PLACEOFSUPPLY.
│         │   → Use LEDGERENTRIES.LIST (not ALLLEDGERENTRIES.LIST).
│         │
│         └─ Not confirmed / unsure
│             → STOP. Ask user: "What is the exact class name configured in Tally
│               for this voucher type?" Do not post until confirmed.
│
├─ NO  → Use ledger-only mode (no CLASSNAME in header).
│         → Choose mode based on inventory:
│             Item invoice  → Mode 1 (Invoice Voucher View + ALLINVENTORYENTRIES)
│             Ledger-only   → Mode 2 (Accounting Invoice Mode, no inventory)
│
└─ UNKNOWN → STOP. Ask user: "Does this company use voucher classes for GST
              (e.g. 'Purchase @ 18%')?" Do not guess.
```

### How to check if a voucher type uses a class

Export voucher type masters and look for `<CLASSNAME>` entries under the relevant voucher type, or ask the user to confirm in Tally UI via **Accounts Info → Voucher Types → Alter → [Voucher Type] → Default Class**.

### Class mode — required header fields

When `CLASSNAME` is set, always include all four GST header fields. Missing any one of them will cause Tally to reject the voucher or save it with incorrect GST treatment.

```xml
<CLASSNAME>Purchase @ 18 %</CLASSNAME>   <!-- exact name as configured in Tally -->
<CMPGSTIN>COMPANY_GSTIN</CMPGSTIN>
<PARTYGSTIN>PARTY_GSTIN</PARTYGSTIN>
<GSTREGISTRATIONTYPE>Regular</GSTREGISTRATIONTYPE>
<PLACEOFSUPPLY>STATE_NAME</PLACEOFSUPPLY>
```

### Class mode — full Purchase template (Invoice Voucher View)

Use this when `CLASSNAME` is confirmed. Note: ledger blocks use `LEDGERENTRIES.LIST`, not `ALLLEDGERENTRIES.LIST`.

```xml
<?xml version="1.0" encoding="utf-8"?>
<ENVELOPE>
  <HEADER><TALLYREQUEST>Import Data</TALLYREQUEST></HEADER>
  <BODY>
    <IMPORTDATA>
      <REQUESTDESC>
        <REPORTNAME>Vouchers</REPORTNAME>
        <STATICVARIABLES>
          <SVCURRENTCOMPANY>COMPANY_NAME</SVCURRENTCOMPANY>
        </STATICVARIABLES>
      </REQUESTDESC>
      <REQUESTDATA>
        <TALLYMESSAGE xmlns:UDF="TallyUDF">
          <VOUCHER VCHTYPE="Purchase" ACTION="Create" OBJVIEW="Invoice Voucher View">
            <GUID>GUID_VALUE</GUID>
            <DATE>YYYYMMDD</DATE>
            <VOUCHERTYPENAME>Purchase</VOUCHERTYPENAME>
            <VOUCHERNUMBER>INVOICE_NO</VOUCHERNUMBER>
            <PARTYLEDGERNAME>VENDOR_LEDGER</PARTYLEDGERNAME>
            <ISINVOICE>Yes</ISINVOICE>

            <!-- Class and GST header — required when class mode is active -->
            <CLASSNAME>Purchase @ 18 %</CLASSNAME>
            <CMPGSTIN>COMPANY_GSTIN</CMPGSTIN>
            <PARTYGSTIN>PARTY_GSTIN</PARTYGSTIN>
            <GSTREGISTRATIONTYPE>Regular</GSTREGISTRATIONTYPE>
            <PLACEOFSUPPLY>STATE_NAME</PLACEOFSUPPLY>

            <!-- Party (vendor) — use LEDGERENTRIES.LIST in Invoice Voucher View -->
            <LEDGERENTRIES.LIST>
              <LEDGERNAME>VENDOR_LEDGER</LEDGERNAME>
              <ISPARTYLEDGER>Yes</ISPARTYLEDGER>
              <ISDEEMEDPOSITIVE>No</ISDEEMEDPOSITIVE>
              <AMOUNT>TOTAL_AMOUNT</AMOUNT>
              <BILLALLOCATIONS.LIST>
                <NAME>INVOICE_NO</NAME>
                <BILLTYPE>New Ref</BILLTYPE>
                <AMOUNT>TOTAL_AMOUNT</AMOUNT>
                <BILLDATE>YYYYMMDD</BILLDATE>
              </BILLALLOCATIONS.LIST>
            </LEDGERENTRIES.LIST>

            <!-- Purchase ledger (taxable value) -->
            <LEDGERENTRIES.LIST>
              <LEDGERNAME>PURCHASE_LEDGER</LEDGERNAME>
              <ISDEEMEDPOSITIVE>Yes</ISDEEMEDPOSITIVE>
              <AMOUNT>-TAXABLE_VALUE</AMOUNT>
            </LEDGERENTRIES.LIST>

            <!-- GST Input CGST -->
            <LEDGERENTRIES.LIST>
              <LEDGERNAME>Input Cgst @ 9 %</LEDGERNAME>
              <ISDEEMEDPOSITIVE>Yes</ISDEEMEDPOSITIVE>
              <AMOUNT>-CGST_AMOUNT</AMOUNT>
            </LEDGERENTRIES.LIST>

            <!-- GST Input SGST -->
            <LEDGERENTRIES.LIST>
              <LEDGERNAME>Input Sgst @ 9 %</LEDGERNAME>
              <ISDEEMEDPOSITIVE>Yes</ISDEEMEDPOSITIVE>
              <AMOUNT>-SGST_AMOUNT</AMOUNT>
            </LEDGERENTRIES.LIST>
          </VOUCHER>
        </TALLYMESSAGE>
      </REQUESTDATA>
    </IMPORTDATA>
  </BODY>
</ENVELOPE>
```

### `LEDGERENTRIES.LIST` vs `ALLLEDGERENTRIES.LIST` — when to use which

| OBJVIEW | Correct tag | Wrong tag (silent failure) |
|---|---|---|
| `Invoice Voucher View` | `LEDGERENTRIES.LIST` | `ALLLEDGERENTRIES.LIST` |
| `Accounting Voucher View` | `ALLLEDGERENTRIES.LIST` | `LEDGERENTRIES.LIST` |

Using the wrong tag causes Tally to silently save the voucher with no ledger entries, producing the error "No accounting or inventory entries are available."

---

## Base template (Import Voucher)

```xml
<?xml version="1.0" encoding="utf-8"?>
<ENVELOPE>
  <HEADER><TALLYREQUEST>Import Data</TALLYREQUEST></HEADER>
  <BODY>
    <IMPORTDATA>
      <REQUESTDESC>
        <REPORTNAME>Vouchers</REPORTNAME>
        <STATICVARIABLES>
          <SVCURRENTCOMPANY>COMPANY_NAME</SVCURRENTCOMPANY>
        </STATICVARIABLES>
      </REQUESTDESC>
      <REQUESTDATA>
        <TALLYMESSAGE xmlns:UDF="TallyUDF">
          <VOUCHER VCHTYPE="VOUCHER_TYPE" ACTION="Create" OBJVIEW="Accounting Voucher View">
            <!-- voucher body -->
          </VOUCHER>
        </TALLYMESSAGE>
      </REQUESTDATA>
    </IMPORTDATA>
  </BODY>
</ENVELOPE>
```

## Amount sign conventions (rule of thumb)

Tally’s sign conventions can vary by persisted view and voucher configuration. The most reliable method is: **create the voucher in Tally UI once, export to XML, and replicate the tags/signs**.

That said, many setups follow:

| Voucher | Party entry | Counter-ledger entry |
|---|---|---|
| Sales | Party debit (receivable) | Sales/GST credit |
| Purchase | Party credit (payable) | Purchase/GST debit |
| Receipt | Bank/Cash debit | Party credit |
| Payment | Party debit | Bank/Cash credit |

If Tally returns “Voucher totals do not match!”, adjust sign conventions to match the exported “known good” format.

## Bill-wise allocation snippet (attach to party ledger entry)

Use this on party ledger entries (customers/vendors) to keep outstandings accurate.

```xml
<BILLALLOCATIONS.LIST>
  <NAME>INVOICE_OR_REF</NAME>
  <BILLTYPE>New Ref</BILLTYPE>
  <AMOUNT>AMOUNT_SIGNED</AMOUNT>
</BILLALLOCATIONS.LIST>
```

Bill types: `New Ref`, `Agst Ref`, `Advance`, `On Account`.

## Sales (Invoice) — accounting-only

```xml
<?xml version="1.0" encoding="utf-8"?>
<ENVELOPE>
  <HEADER><TALLYREQUEST>Import Data</TALLYREQUEST></HEADER>
  <BODY>
    <IMPORTDATA>
      <REQUESTDESC>
        <REPORTNAME>Vouchers</REPORTNAME>
        <STATICVARIABLES>
          <SVCURRENTCOMPANY>COMPANY_NAME</SVCURRENTCOMPANY>
        </STATICVARIABLES>
      </REQUESTDESC>
      <REQUESTDATA>
        <TALLYMESSAGE xmlns:UDF="TallyUDF">
          <VOUCHER VCHTYPE="Sales" ACTION="Create" OBJVIEW="Accounting Voucher View">
            <GUID>UNIQUE_GUID</GUID>
            <DATE>YYYYMMDD</DATE>
            <VOUCHERTYPENAME>Sales</VOUCHERTYPENAME>
            <VOUCHERNUMBER>INVOICE_NO</VOUCHERNUMBER>
            <NARRATION>NARRATION_TEXT</NARRATION>
            <ISINVOICE>Yes</ISINVOICE>
            <PARTYLEDGERNAME>CUSTOMER_LEDGER</PARTYLEDGERNAME>

            <!-- Party (customer) -->
            <ALLLEDGERENTRIES.LIST>
              <LEDGERNAME>CUSTOMER_LEDGER</LEDGERNAME>
              <ISPARTYLEDGER>Yes</ISPARTYLEDGER>
              <ISDEEMEDPOSITIVE>Yes</ISDEEMEDPOSITIVE>
              <AMOUNT>-TOTAL_AMOUNT</AMOUNT>
              <BILLALLOCATIONS.LIST>
                <NAME>INVOICE_NO</NAME>
                <BILLTYPE>New Ref</BILLTYPE>
                <AMOUNT>-TOTAL_AMOUNT</AMOUNT>
              </BILLALLOCATIONS.LIST>
            </ALLLEDGERENTRIES.LIST>

            <!-- Sales ledger -->
            <ALLLEDGERENTRIES.LIST>
              <LEDGERNAME>SALES_LEDGER</LEDGERNAME>
              <ISDEEMEDPOSITIVE>No</ISDEEMEDPOSITIVE>
              <AMOUNT>BASE_AMOUNT</AMOUNT>
            </ALLLEDGERENTRIES.LIST>

            <!-- GST Output (optional) -->
            <ALLLEDGERENTRIES.LIST>
              <LEDGERNAME>GST_OUTPUT_LEDGER</LEDGERNAME>
              <ISDEEMEDPOSITIVE>No</ISDEEMEDPOSITIVE>
              <AMOUNT>GST_AMOUNT</AMOUNT>
            </ALLLEDGERENTRIES.LIST>
          </VOUCHER>
        </TALLYMESSAGE>
      </REQUESTDATA>
    </IMPORTDATA>
  </BODY>
</ENVELOPE>
```

## Purchase — three modes

Choose the mode based on what the client needs. All three use `VCHTYPE="Purchase"`.

| Mode | `OBJVIEW` | `ISINVOICE` | Has inventory | Use when |
|---|---|---|---|---|
| Item Invoice | `Invoice Voucher View` | Yes | Yes (`ALLINVENTORYENTRIES`) | Stock items with Rate/Qty/Amount columns |
| Accounting Invoice | `Invoice Voucher View` | Yes | No | Invoice layout but ledger-only (services, expenses) |
| As Voucher | `Accounting Voucher View` | No | No | Classic By/To accounting view; best fallback |

### Mode 1 — Item Invoice (stock-based, Rate/Qty/Amount)

`OBJVIEW="Invoice Voucher View"` + `ISINVOICE=Yes` + `ALLINVENTORYENTRIES.LIST`. Use when you want full stock-item detail and the invoice layout.

```xml
<?xml version="1.0" encoding="utf-8"?>
<ENVELOPE>
  <HEADER><TALLYREQUEST>Import Data</TALLYREQUEST></HEADER>
  <BODY>
    <IMPORTDATA>
      <REQUESTDESC>
        <REPORTNAME>Vouchers</REPORTNAME>
        <STATICVARIABLES>
          <SVCURRENTCOMPANY>COMPANY_NAME</SVCURRENTCOMPANY>
        </STATICVARIABLES>
      </REQUESTDESC>
      <REQUESTDATA>
        <TALLYMESSAGE xmlns:UDF="TallyUDF">
          <VOUCHER VCHTYPE="Purchase" ACTION="Create" OBJVIEW="Invoice Voucher View">
            <GUID>GUID_VALUE</GUID>
            <DATE>YYYYMMDD</DATE>
            <VOUCHERTYPENAME>Purchase</VOUCHERTYPENAME>
            <VOUCHERNUMBER>INVOICE_NO</VOUCHERNUMBER>
            <PARTYLEDGERNAME>VENDOR_LEDGER</PARTYLEDGERNAME>
            <ISINVOICE>Yes</ISINVOICE>

            <!-- Party (vendor) — credit side -->
            <ALLLEDGERENTRIES.LIST>
              <LEDGERNAME>VENDOR_LEDGER</LEDGERNAME>
              <ISPARTYLEDGER>Yes</ISPARTYLEDGER>
              <ISDEEMEDPOSITIVE>No</ISDEEMEDPOSITIVE>
              <AMOUNT>TOTAL_AMOUNT</AMOUNT>
              <BILLALLOCATIONS.LIST>
                <NAME>INVOICE_NO</NAME>
                <BILLTYPE>New Ref</BILLTYPE>
                <AMOUNT>TOTAL_AMOUNT</AMOUNT>
                <BILLDATE>YYYYMMDD</BILLDATE>
              </BILLALLOCATIONS.LIST>
            </ALLLEDGERENTRIES.LIST>

            <!-- Stock item line(s) — repeat for each item -->
            <ALLINVENTORYENTRIES.LIST>
              <STOCKITEM>STOCK_ITEM_NAME</STOCKITEM>
              <ISDEEMEDPOSITIVE>No</ISDEEMEDPOSITIVE>
              <RATE>RATE_PER_UNIT</RATE>
              <AMOUNT>LINE_AMOUNT</AMOUNT>
              <ACTUALQTY>QUANTITY</ACTUALQTY>
              <BILLEDQTY>QUANTITY</BILLEDQTY>
              <BATCHALLOCATIONS.LIST>
                <GODOWNNAME>Main Location</GODOWNNAME>
                <BATCHNAME>Primary Batch</BATCHNAME>
                <QUANTITY>QUANTITY</QUANTITY>
              </BATCHALLOCATIONS.LIST>
            </ALLINVENTORYENTRIES.LIST>

            <!-- Purchase ledger (taxable value) -->
            <ALLLEDGERENTRIES.LIST>
              <LEDGERNAME>PURCHASE_LEDGER</LEDGERNAME>
              <ISDEEMEDPOSITIVE>Yes</ISDEEMEDPOSITIVE>
              <AMOUNT>-TAXABLE_VALUE</AMOUNT>
            </ALLLEDGERENTRIES.LIST>

            <!-- GST Input CGST -->
            <ALLLEDGERENTRIES.LIST>
              <LEDGERNAME>Input Cgst @ 9 %</LEDGERNAME>
              <ISDEEMEDPOSITIVE>Yes</ISDEEMEDPOSITIVE>
              <AMOUNT>-CGST_AMOUNT</AMOUNT>
            </ALLLEDGERENTRIES.LIST>

            <!-- GST Input SGST -->
            <ALLLEDGERENTRIES.LIST>
              <LEDGERNAME>Input Sgst @ 9 %</LEDGERNAME>
              <ISDEEMEDPOSITIVE>Yes</ISDEEMEDPOSITIVE>
              <AMOUNT>-SGST_AMOUNT</AMOUNT>
            </ALLLEDGERENTRIES.LIST>
          </VOUCHER>
        </TALLYMESSAGE>
      </REQUESTDATA>
    </IMPORTDATA>
  </BODY>
</ENVELOPE>
```

### Mode 2 — Accounting Invoice (invoice layout, no inventory)

`OBJVIEW="Invoice Voucher View"` + `ISINVOICE=Yes` + ledger entries only (no `ALLINVENTORYENTRIES`). Renders the party header and invoice columns without requiring stock items. Supports round-off entry.

> **Critical — use `LEDGERENTRIES.LIST`, not `ALLLEDGERENTRIES.LIST`**
> When `OBJVIEW="Invoice Voucher View"` is set, Tally silently ignores every `<ALLLEDGERENTRIES.LIST>` block and saves the voucher with no accounting entries, producing the error "No accounting or inventory entries are available." Switch every ledger block to `<LEDGERENTRIES.LIST>` for this mode.

```xml
<?xml version="1.0" encoding="utf-8"?>
<ENVELOPE>
  <HEADER><TALLYREQUEST>Import Data</TALLYREQUEST></HEADER>
  <BODY>
    <IMPORTDATA>
      <REQUESTDESC>
        <REPORTNAME>Vouchers</REPORTNAME>
        <STATICVARIABLES>
          <SVCURRENTCOMPANY>COMPANY_NAME</SVCURRENTCOMPANY>
        </STATICVARIABLES>
      </REQUESTDESC>
      <REQUESTDATA>
        <TALLYMESSAGE xmlns:UDF="TallyUDF">
          <VOUCHER VCHTYPE="Purchase" ACTION="Create" OBJVIEW="Invoice Voucher View">
            <GUID>GUID_VALUE</GUID>
            <DATE>YYYYMMDD</DATE>
            <VOUCHERTYPENAME>Purchase</VOUCHERTYPENAME>
            <VOUCHERNUMBER>INVOICE_NO</VOUCHERNUMBER>
            <PARTYLEDGERNAME>VENDOR_LEDGER</PARTYLEDGERNAME>
            <ISINVOICE>Yes</ISINVOICE>
            <NARRATION>NARRATION_TEXT</NARRATION>

            <!-- Party (vendor) — credit side -->
            <LEDGERENTRIES.LIST>
              <LEDGERNAME>VENDOR_LEDGER</LEDGERNAME>
              <ISPARTYLEDGER>Yes</ISPARTYLEDGER>
              <ISDEEMEDPOSITIVE>No</ISDEEMEDPOSITIVE>
              <AMOUNT>TOTAL_AMOUNT</AMOUNT>
              <BILLALLOCATIONS.LIST>
                <NAME>INVOICE_NO</NAME>
                <BILLTYPE>New Ref</BILLTYPE>
                <AMOUNT>TOTAL_AMOUNT</AMOUNT>
                <BILLDATE>YYYYMMDD</BILLDATE>
              </BILLALLOCATIONS.LIST>
            </LEDGERENTRIES.LIST>

            <!-- Purchase / expense ledger -->
            <LEDGERENTRIES.LIST>
              <LEDGERNAME>PURCHASE_LEDGER</LEDGERNAME>
              <ISDEEMEDPOSITIVE>Yes</ISDEEMEDPOSITIVE>
              <AMOUNT>-TAXABLE_VALUE</AMOUNT>
            </LEDGERENTRIES.LIST>

            <!-- GST Input CGST -->
            <LEDGERENTRIES.LIST>
              <LEDGERNAME>Input Cgst @ 9 %</LEDGERNAME>
              <ISDEEMEDPOSITIVE>Yes</ISDEEMEDPOSITIVE>
              <AMOUNT>-CGST_AMOUNT</AMOUNT>
            </LEDGERENTRIES.LIST>

            <!-- GST Input SGST -->
            <LEDGERENTRIES.LIST>
              <LEDGERNAME>Input Sgst @ 9 %</LEDGERNAME>
              <ISDEEMEDPOSITIVE>Yes</ISDEEMEDPOSITIVE>
              <AMOUNT>-SGST_AMOUNT</AMOUNT>
            </LEDGERENTRIES.LIST>

            <!-- Round off (optional) -->
            <LEDGERENTRIES.LIST>
              <LEDGERNAME>Round Off</LEDGERNAME>
              <ISDEEMEDPOSITIVE>Yes</ISDEEMEDPOSITIVE>
              <AMOUNT>-ROUND_OFF</AMOUNT>
            </LEDGERENTRIES.LIST>
          </VOUCHER>
        </TALLYMESSAGE>
      </REQUESTDATA>
    </IMPORTDATA>
  </BODY>
</ENVELOPE>
```

### Mode 2 variant — Accounting Invoice with a voucher class

If the Purchase voucher type is configured to use a **voucher class** (e.g. `Purchase @ 18 %`) for automatic GST splits, the XML must declare the class and supply the GST identification fields. Without `<CLASSNAME>`, Tally assumes the class will provide ledger entries and rejects a ledger-only payload with "No accounting or inventory entries are available."

Required additions when a class is in use:

| Field | Where | Purpose |
|---|---|---|
| `<CLASSNAME>` | `<VOUCHER>` header | Activates the voucher class (exact name as defined in Tally) |
| `<CMPGSTIN>` | `<VOUCHER>` header | Company GSTIN (15-char) |
| `<PARTYGSTIN>` | `<VOUCHER>` header | Vendor GSTIN |
| `<GSTREGISTRATIONTYPE>` | `<VOUCHER>` header | e.g. `Regular` |
| `<PLACEOFSUPPLY>` | `<VOUCHER>` header | State name for IGST/CGST+SGST determination |

```xml
<VOUCHER VCHTYPE="Purchase" ACTION="Create" OBJVIEW="Invoice Voucher View">
  <GUID>GUID_VALUE</GUID>
  <DATE>YYYYMMDD</DATE>
  <VOUCHERTYPENAME>Purchase</VOUCHERTYPENAME>
  <CLASSNAME>Purchase @ 18 %</CLASSNAME>
  <VOUCHERNUMBER>INVOICE_NO</VOUCHERNUMBER>
  <PARTYLEDGERNAME>VENDOR_LEDGER</PARTYLEDGERNAME>
  <ISINVOICE>Yes</ISINVOICE>
  <NARRATION>NARRATION_TEXT</NARRATION>

  <!-- GST header fields required when a class is active -->
  <CMPGSTIN>COMPANY_GSTIN</CMPGSTIN>
  <PARTYGSTIN>VENDOR_GSTIN</PARTYGSTIN>
  <GSTREGISTRATIONTYPE>Regular</GSTREGISTRATIONTYPE>
  <PLACEOFSUPPLY>STATE_NAME</PLACEOFSUPPLY>

  <!-- Party (vendor) — credit side; use LEDGERENTRIES.LIST in Invoice Voucher View -->
  <LEDGERENTRIES.LIST>
    <LEDGERNAME>VENDOR_LEDGER</LEDGERNAME>
    <ISPARTYLEDGER>Yes</ISPARTYLEDGER>
    <ISDEEMEDPOSITIVE>No</ISDEEMEDPOSITIVE>
    <AMOUNT>TOTAL_AMOUNT</AMOUNT>
    <BILLALLOCATIONS.LIST>
      <NAME>INVOICE_NO</NAME>
      <BILLTYPE>New Ref</BILLTYPE>
      <AMOUNT>TOTAL_AMOUNT</AMOUNT>
      <BILLDATE>YYYYMMDD</BILLDATE>
    </BILLALLOCATIONS.LIST>
  </LEDGERENTRIES.LIST>

  <!-- Purchase / expense ledger (taxable value) -->
  <LEDGERENTRIES.LIST>
    <LEDGERNAME>PURCHASE_LEDGER</LEDGERNAME>
    <ISDEEMEDPOSITIVE>Yes</ISDEEMEDPOSITIVE>
    <AMOUNT>-TAXABLE_VALUE</AMOUNT>
  </LEDGERENTRIES.LIST>

  <!-- GST ledgers — class drives the split, but entries must still be explicit -->
  <LEDGERENTRIES.LIST>
    <LEDGERNAME>Input Cgst @ 9 %</LEDGERNAME>
    <ISDEEMEDPOSITIVE>Yes</ISDEEMEDPOSITIVE>
    <AMOUNT>-CGST_AMOUNT</AMOUNT>
  </LEDGERENTRIES.LIST>

  <LEDGERENTRIES.LIST>
    <LEDGERNAME>Input Sgst @ 9 %</LEDGERNAME>
    <ISDEEMEDPOSITIVE>Yes</ISDEEMEDPOSITIVE>
    <AMOUNT>-SGST_AMOUNT</AMOUNT>
  </LEDGERENTRIES.LIST>
</VOUCHER>
```

### Mode 3 — As Voucher (classic accounting entry, fallback)

`OBJVIEW="Accounting Voucher View"` + `ISINVOICE=No`. Tally renders this with By/To columns. **Party entry must come first** so the Day Book "Particulars" column shows the vendor name.

```xml
<?xml version="1.0" encoding="utf-8"?>
<ENVELOPE>
  <HEADER><TALLYREQUEST>Import Data</TALLYREQUEST></HEADER>
  <BODY>
    <IMPORTDATA>
      <REQUESTDESC>
        <REPORTNAME>Vouchers</REPORTNAME>
        <STATICVARIABLES>
          <SVCURRENTCOMPANY>COMPANY_NAME</SVCURRENTCOMPANY>
        </STATICVARIABLES>
      </REQUESTDESC>
      <REQUESTDATA>
        <TALLYMESSAGE xmlns:UDF="TallyUDF">
          <VOUCHER VCHTYPE="Purchase" ACTION="Create" OBJVIEW="Accounting Voucher View">
            <GUID>GUID_VALUE</GUID>
            <DATE>YYYYMMDD</DATE>
            <VOUCHERTYPENAME>Purchase</VOUCHERTYPENAME>
            <VOUCHERNUMBER>INVOICE_NO</VOUCHERNUMBER>
            <PARTYLEDGERNAME>VENDOR_LEDGER</PARTYLEDGERNAME>
            <ISINVOICE>No</ISINVOICE>
            <NARRATION>NARRATION_TEXT</NARRATION>

            <!-- Party (vendor) — FIRST so Particulars shows vendor name -->
            <ALLLEDGERENTRIES.LIST>
              <LEDGERNAME>VENDOR_LEDGER</LEDGERNAME>
              <ISPARTYLEDGER>Yes</ISPARTYLEDGER>
              <ISDEEMEDPOSITIVE>No</ISDEEMEDPOSITIVE>
              <AMOUNT>TOTAL_AMOUNT</AMOUNT>
            </ALLLEDGERENTRIES.LIST>

            <!-- Purchase / expense ledger -->
            <ALLLEDGERENTRIES.LIST>
              <LEDGERNAME>PURCHASE_LEDGER</LEDGERNAME>
              <ISDEEMEDPOSITIVE>Yes</ISDEEMEDPOSITIVE>
              <AMOUNT>-TAXABLE_VALUE</AMOUNT>
            </ALLLEDGERENTRIES.LIST>

            <!-- GST Input CGST -->
            <ALLLEDGERENTRIES.LIST>
              <LEDGERNAME>Input Cgst @ 9 %</LEDGERNAME>
              <ISDEEMEDPOSITIVE>Yes</ISDEEMEDPOSITIVE>
              <AMOUNT>-CGST_AMOUNT</AMOUNT>
            </ALLLEDGERENTRIES.LIST>

            <!-- GST Input SGST -->
            <ALLLEDGERENTRIES.LIST>
              <LEDGERNAME>Input Sgst @ 9 %</LEDGERNAME>
              <ISDEEMEDPOSITIVE>Yes</ISDEEMEDPOSITIVE>
              <AMOUNT>-SGST_AMOUNT</AMOUNT>
            </ALLLEDGERENTRIES.LIST>

            <!-- Round off (optional) -->
            <ALLLEDGERENTRIES.LIST>
              <LEDGERNAME>Round Off</LEDGERNAME>
              <ISDEEMEDPOSITIVE>Yes</ISDEEMEDPOSITIVE>
              <AMOUNT>-ROUND_OFF</AMOUNT>
            </ALLLEDGERENTRIES.LIST>
          </VOUCHER>
        </TALLYMESSAGE>
      </REQUESTDATA>
    </IMPORTDATA>
  </BODY>
</ENVELOPE>
```

## Receipt (money received)

```xml
<?xml version="1.0" encoding="utf-8"?>
<ENVELOPE>
  <HEADER><TALLYREQUEST>Import Data</TALLYREQUEST></HEADER>
  <BODY>
    <IMPORTDATA>
      <REQUESTDESC>
        <REPORTNAME>Vouchers</REPORTNAME>
        <STATICVARIABLES>
          <SVCURRENTCOMPANY>COMPANY_NAME</SVCURRENTCOMPANY>
        </STATICVARIABLES>
      </REQUESTDESC>
      <REQUESTDATA>
        <TALLYMESSAGE xmlns:UDF="TallyUDF">
          <VOUCHER VCHTYPE="Receipt" ACTION="Create" OBJVIEW="Accounting Voucher View">
            <GUID>UNIQUE_GUID</GUID>
            <DATE>YYYYMMDD</DATE>
            <VOUCHERTYPENAME>Receipt</VOUCHERTYPENAME>
            <NARRATION>NARRATION_TEXT</NARRATION>
            <ISINVOICE>No</ISINVOICE>
            <PARTYLEDGERNAME>CUSTOMER_LEDGER</PARTYLEDGERNAME>

            <!-- Bank/Cash (money in) -->
            <ALLLEDGERENTRIES.LIST>
              <LEDGERNAME>BANK_OR_CASH_LEDGER</LEDGERNAME>
              <ISDEEMEDPOSITIVE>Yes</ISDEEMEDPOSITIVE>
              <AMOUNT>-AMOUNT</AMOUNT>
            </ALLLEDGERENTRIES.LIST>

            <!-- Customer -->
            <ALLLEDGERENTRIES.LIST>
              <LEDGERNAME>CUSTOMER_LEDGER</LEDGERNAME>
              <ISPARTYLEDGER>Yes</ISPARTYLEDGER>
              <ISDEEMEDPOSITIVE>No</ISDEEMEDPOSITIVE>
              <AMOUNT>AMOUNT</AMOUNT>
            </ALLLEDGERENTRIES.LIST>
          </VOUCHER>
        </TALLYMESSAGE>
      </REQUESTDATA>
    </IMPORTDATA>
  </BODY>
</ENVELOPE>
```

## Payment (money paid)

```xml
<?xml version="1.0" encoding="utf-8"?>
<ENVELOPE>
  <HEADER><TALLYREQUEST>Import Data</TALLYREQUEST></HEADER>
  <BODY>
    <IMPORTDATA>
      <REQUESTDESC>
        <REPORTNAME>Vouchers</REPORTNAME>
        <STATICVARIABLES>
          <SVCURRENTCOMPANY>COMPANY_NAME</SVCURRENTCOMPANY>
        </STATICVARIABLES>
      </REQUESTDESC>
      <REQUESTDATA>
        <TALLYMESSAGE xmlns:UDF="TallyUDF">
          <VOUCHER VCHTYPE="Payment" ACTION="Create" OBJVIEW="Accounting Voucher View">
            <GUID>UNIQUE_GUID</GUID>
            <DATE>YYYYMMDD</DATE>
            <VOUCHERTYPENAME>Payment</VOUCHERTYPENAME>
            <NARRATION>NARRATION_TEXT</NARRATION>
            <ISINVOICE>No</ISINVOICE>
            <PARTYLEDGERNAME>VENDOR_OR_EXPENSE_LEDGER</PARTYLEDGERNAME>

            <!-- Payee (vendor/expense) -->
            <ALLLEDGERENTRIES.LIST>
              <LEDGERNAME>VENDOR_OR_EXPENSE_LEDGER</LEDGERNAME>
              <ISDEEMEDPOSITIVE>Yes</ISDEEMEDPOSITIVE>
              <AMOUNT>-AMOUNT</AMOUNT>
            </ALLLEDGERENTRIES.LIST>

            <!-- Bank/Cash (money out) -->
            <ALLLEDGERENTRIES.LIST>
              <LEDGERNAME>BANK_OR_CASH_LEDGER</LEDGERNAME>
              <ISDEEMEDPOSITIVE>No</ISDEEMEDPOSITIVE>
              <AMOUNT>AMOUNT</AMOUNT>
            </ALLLEDGERENTRIES.LIST>
          </VOUCHER>
        </TALLYMESSAGE>
      </REQUESTDATA>
    </IMPORTDATA>
  </BODY>
</ENVELOPE>
```

## Journal (adjustments)

```xml
<?xml version="1.0" encoding="utf-8"?>
<ENVELOPE>
  <HEADER><TALLYREQUEST>Import Data</TALLYREQUEST></HEADER>
  <BODY>
    <IMPORTDATA>
      <REQUESTDESC>
        <REPORTNAME>Vouchers</REPORTNAME>
        <STATICVARIABLES>
          <SVCURRENTCOMPANY>COMPANY_NAME</SVCURRENTCOMPANY>
        </STATICVARIABLES>
      </REQUESTDESC>
      <REQUESTDATA>
        <TALLYMESSAGE xmlns:UDF="TallyUDF">
          <VOUCHER VCHTYPE="Journal" ACTION="Create" OBJVIEW="Accounting Voucher View">
            <GUID>UNIQUE_GUID</GUID>
            <DATE>YYYYMMDD</DATE>
            <VOUCHERTYPENAME>Journal</VOUCHERTYPENAME>
            <NARRATION>NARRATION_TEXT</NARRATION>
            <ISINVOICE>No</ISINVOICE>

            <!-- Debit -->
            <ALLLEDGERENTRIES.LIST>
              <LEDGERNAME>DEBIT_LEDGER</LEDGERNAME>
              <ISDEEMEDPOSITIVE>Yes</ISDEEMEDPOSITIVE>
              <AMOUNT>-AMOUNT</AMOUNT>
            </ALLLEDGERENTRIES.LIST>

            <!-- Credit -->
            <ALLLEDGERENTRIES.LIST>
              <LEDGERNAME>CREDIT_LEDGER</LEDGERNAME>
              <ISDEEMEDPOSITIVE>No</ISDEEMEDPOSITIVE>
              <AMOUNT>AMOUNT</AMOUNT>
            </ALLLEDGERENTRIES.LIST>
          </VOUCHER>
        </TALLYMESSAGE>
      </REQUESTDATA>
    </IMPORTDATA>
  </BODY>
</ENVELOPE>
```

## Credit Note (sales return)

Credit Note is commonly a separate voucher type configured in Tally. If your voucher type name differs, set `VCHTYPE` and `VOUCHERTYPENAME` accordingly.

```xml
<?xml version="1.0" encoding="utf-8"?>
<ENVELOPE>
  <HEADER><TALLYREQUEST>Import Data</TALLYREQUEST></HEADER>
  <BODY>
    <IMPORTDATA>
      <REQUESTDESC>
        <REPORTNAME>Vouchers</REPORTNAME>
        <STATICVARIABLES>
          <SVCURRENTCOMPANY>COMPANY_NAME</SVCURRENTCOMPANY>
        </STATICVARIABLES>
      </REQUESTDESC>
      <REQUESTDATA>
        <TALLYMESSAGE xmlns:UDF="TallyUDF">
          <VOUCHER VCHTYPE="Credit Note" ACTION="Create" OBJVIEW="Accounting Voucher View">
            <GUID>UNIQUE_GUID</GUID>
            <DATE>YYYYMMDD</DATE>
            <VOUCHERTYPENAME>Credit Note</VOUCHERTYPENAME>
            <VOUCHERNUMBER>CN_NO</VOUCHERNUMBER>
            <NARRATION>NARRATION_TEXT</NARRATION>
            <ISINVOICE>No</ISINVOICE>
            <PARTYLEDGERNAME>CUSTOMER_LEDGER</PARTYLEDGERNAME>

            <!-- Reduce sales / reverse tax as per configuration -->
            <ALLLEDGERENTRIES.LIST>
              <LEDGERNAME>SALES_RETURN_LEDGER</LEDGERNAME>
              <ISDEEMEDPOSITIVE>Yes</ISDEEMEDPOSITIVE>
              <AMOUNT>-BASE_AMOUNT</AMOUNT>
            </ALLLEDGERENTRIES.LIST>

            <ALLLEDGERENTRIES.LIST>
              <LEDGERNAME>GST_OUTPUT_LEDGER</LEDGERNAME>
              <ISDEEMEDPOSITIVE>Yes</ISDEEMEDPOSITIVE>
              <AMOUNT>-GST_AMOUNT</AMOUNT>
            </ALLLEDGERENTRIES.LIST>

            <ALLLEDGERENTRIES.LIST>
              <LEDGERNAME>CUSTOMER_LEDGER</LEDGERNAME>
              <ISPARTYLEDGER>Yes</ISPARTYLEDGER>
              <ISDEEMEDPOSITIVE>No</ISDEEMEDPOSITIVE>
              <AMOUNT>TOTAL_AMOUNT</AMOUNT>
            </ALLLEDGERENTRIES.LIST>
          </VOUCHER>
        </TALLYMESSAGE>
      </REQUESTDATA>
    </IMPORTDATA>
  </BODY>
</ENVELOPE>
```

## Debit Note (purchase return)

```xml
<?xml version="1.0" encoding="utf-8"?>
<ENVELOPE>
  <HEADER><TALLYREQUEST>Import Data</TALLYREQUEST></HEADER>
  <BODY>
    <IMPORTDATA>
      <REQUESTDESC>
        <REPORTNAME>Vouchers</REPORTNAME>
        <STATICVARIABLES>
          <SVCURRENTCOMPANY>COMPANY_NAME</SVCURRENTCOMPANY>
        </STATICVARIABLES>
      </REQUESTDESC>
      <REQUESTDATA>
        <TALLYMESSAGE xmlns:UDF="TallyUDF">
          <VOUCHER VCHTYPE="Debit Note" ACTION="Create" OBJVIEW="Accounting Voucher View">
            <GUID>UNIQUE_GUID</GUID>
            <DATE>YYYYMMDD</DATE>
            <VOUCHERTYPENAME>Debit Note</VOUCHERTYPENAME>
            <VOUCHERNUMBER>DN_NO</VOUCHERNUMBER>
            <NARRATION>NARRATION_TEXT</NARRATION>
            <ISINVOICE>No</ISINVOICE>
            <PARTYLEDGERNAME>VENDOR_LEDGER</PARTYLEDGERNAME>

            <ALLLEDGERENTRIES.LIST>
              <LEDGERNAME>PURCHASE_RETURN_LEDGER</LEDGERNAME>
              <ISDEEMEDPOSITIVE>No</ISDEEMEDPOSITIVE>
              <AMOUNT>BASE_AMOUNT</AMOUNT>
            </ALLLEDGERENTRIES.LIST>

            <ALLLEDGERENTRIES.LIST>
              <LEDGERNAME>GST_INPUT_LEDGER</LEDGERNAME>
              <ISDEEMEDPOSITIVE>No</ISDEEMEDPOSITIVE>
              <AMOUNT>GST_AMOUNT</AMOUNT>
            </ALLLEDGERENTRIES.LIST>

            <ALLLEDGERENTRIES.LIST>
              <LEDGERNAME>VENDOR_LEDGER</LEDGERNAME>
              <ISPARTYLEDGER>Yes</ISPARTYLEDGER>
              <ISDEEMEDPOSITIVE>Yes</ISDEEMEDPOSITIVE>
              <AMOUNT>-TOTAL_AMOUNT</AMOUNT>
            </ALLLEDGERENTRIES.LIST>
          </VOUCHER>
        </TALLYMESSAGE>
      </REQUESTDATA>
    </IMPORTDATA>
  </BODY>
</ENVELOPE>
```

## Contra (bank transfers / cash deposit / withdrawal)

Contra vouchers are highly configuration-dependent. Use as a template and validate signs by exporting a known-good contra voucher from the client’s Tally.

```xml
<?xml version="1.0" encoding="utf-8"?>
<ENVELOPE>
  <HEADER><TALLYREQUEST>Import Data</TALLYREQUEST></HEADER>
  <BODY>
    <IMPORTDATA>
      <REQUESTDESC>
        <REPORTNAME>Vouchers</REPORTNAME>
        <STATICVARIABLES>
          <SVCURRENTCOMPANY>COMPANY_NAME</SVCURRENTCOMPANY>
        </STATICVARIABLES>
      </REQUESTDESC>
      <REQUESTDATA>
        <TALLYMESSAGE xmlns:UDF="TallyUDF">
          <VOUCHER VCHTYPE="Contra" ACTION="Create" OBJVIEW="Accounting Voucher View">
            <GUID>UNIQUE_GUID</GUID>
            <DATE>YYYYMMDD</DATE>
            <VOUCHERTYPENAME>Contra</VOUCHERTYPENAME>
            <NARRATION>NARRATION_TEXT</NARRATION>
            <ISINVOICE>No</ISINVOICE>

            <!-- From account -->
            <ALLLEDGERENTRIES.LIST>
              <LEDGERNAME>FROM_LEDGER</LEDGERNAME>
              <ISDEEMEDPOSITIVE>Yes</ISDEEMEDPOSITIVE>
              <AMOUNT>-AMOUNT</AMOUNT>
            </ALLLEDGERENTRIES.LIST>

            <!-- To account -->
            <ALLLEDGERENTRIES.LIST>
              <LEDGERNAME>TO_LEDGER</LEDGERNAME>
              <ISDEEMEDPOSITIVE>No</ISDEEMEDPOSITIVE>
              <AMOUNT>AMOUNT</AMOUNT>
            </ALLLEDGERENTRIES.LIST>
          </VOUCHER>
        </TALLYMESSAGE>
      </REQUESTDATA>
    </IMPORTDATA>
  </BODY>
</ENVELOPE>
```

## Voucher alteration (edit existing)

Voucher identification typically requires a stable identifier (GUID or master ID). If you created the voucher via integration with a GUID, you can re-send with the same GUID and `ACTION="Alter"` (or use the documented alteration approach for your Tally setup).

Template (fill in the exact identifiers based on exported voucher XML):

```xml
<?xml version="1.0" encoding="utf-8"?>
<ENVELOPE>
  <HEADER><TALLYREQUEST>Import Data</TALLYREQUEST></HEADER>
  <BODY>
    <IMPORTDATA>
      <REQUESTDESC>
        <REPORTNAME>Vouchers</REPORTNAME>
        <STATICVARIABLES>
          <SVCURRENTCOMPANY>COMPANY_NAME</SVCURRENTCOMPANY>
        </STATICVARIABLES>
      </REQUESTDESC>
      <REQUESTDATA>
        <TALLYMESSAGE xmlns:UDF="TallyUDF">
          <VOUCHER VCHTYPE="Sales" ACTION="Alter" OBJVIEW="Accounting Voucher View">
            <GUID>EXISTING_GUID</GUID>
            <!-- Include the full altered voucher content -->
          </VOUCHER>
        </TALLYMESSAGE>
      </REQUESTDATA>
    </IMPORTDATA>
  </BODY>
</ENVELOPE>
```

## Voucher cancellation (void)

Cancellation is similar to alteration, but uses `ACTION="Cancel"` for the identified voucher.

```xml
<?xml version="1.0" encoding="utf-8"?>
<ENVELOPE>
  <HEADER><TALLYREQUEST>Import Data</TALLYREQUEST></HEADER>
  <BODY>
    <IMPORTDATA>
      <REQUESTDESC>
        <REPORTNAME>Vouchers</REPORTNAME>
        <STATICVARIABLES>
          <SVCURRENTCOMPANY>COMPANY_NAME</SVCURRENTCOMPANY>
        </STATICVARIABLES>
      </REQUESTDESC>
      <REQUESTDATA>
        <TALLYMESSAGE xmlns:UDF="TallyUDF">
          <VOUCHER VCHTYPE="Sales" ACTION="Cancel" OBJVIEW="Accounting Voucher View">
            <GUID>EXISTING_GUID</GUID>
          </VOUCHER>
        </TALLYMESSAGE>
      </REQUESTDATA>
    </IMPORTDATA>
  </BODY>
</ENVELOPE>
```

## Multi-line item invoices (inventory)

For itemized invoices using `ALLINVENTORYENTRIES.LIST` and `ACCOUNTINGALLOCATIONS.LIST`, see `reference/inventory.md`.

## Bank Statement Import Workflow

When importing transactions from a bank statement, map each bank entry to the appropriate voucher type:

### Bank statement debit/credit rule

Bank statements show entries from the **bank's perspective**, but Tally entries must be posted from the **business's books**:

| Bank statement entry | Meaning in business books | Tally posting |
|----------------------|---------------------------|---------------|
| Bank statement **Credit** | Money received into bank | **Debit** the bank ledger |
| Bank statement **Debit** | Money paid out of bank | **Credit** the bank ledger |

For contra vouchers, debit the account that receives funds and credit the account that gives funds:

| Contra transaction | Debit | Credit |
|--------------------|-------|--------|
| Cash deposited into bank | Bank | Cash |
| Cash withdrawn from bank / ATM withdrawal | Cash | Bank |
| Bank A to Bank B transfer | Destination Bank | Source Bank |

### Mapping Rules

| Bank Entry | Voucher Type | Debit Ledger | Credit Ledger |
|------------|--------------|--------------|---------------|
| Deposit / NEFT Credit / RTGS Credit / UPI Credit | **Receipt** | Bank/Cash | Customer/Party ledger (Sundry Debtors) |
| Withdrawal / NEFT Debit / RTGS Debit / UPI Debit / Cheque Issued | **Payment** | Supplier/Expense ledger | Bank/Cash |
| ATM Withdrawal | **Contra** | Cash | Bank |
| Cash Deposit | **Contra** | Bank | Cash |
| Bank-to-Bank Transfer | **Contra** | Destination Bank | Source Bank |
| Interest Credit | **Receipt** | Bank | Interest Income ledger |
| Bank Charges | **Payment** | Bank Charges ledger | Bank |
| GST/TDS Payment | **Payment** | GST/TDS Duty ledger | Bank |

### Pre-flight Checklist

Before importing bank statement transactions:

1. **Verify bank ledger exists** in Tally (create if missing)
2. **Verify cash ledger exists** if importing ATM/deposit transactions
3. **Verify party ledgers exist** — create unknown parties from statement first
4. **Fetch ledger names** — use `reference/reports.md` → "Ledger Names (all ledgers)" before mapping statement rows
5. **Confirm ledger mapping once** — tell the user “These are the ledgers I will use for the bank entries: ...”

### Example: NEFT Credit (Receipt)

```xml
<?xml version="1.0" encoding="utf-8"?>
<ENVELOPE>
  <HEADER><TALLYREQUEST>Import Data</TALLYREQUEST></HEADER>
  <BODY>
    <IMPORTDATA>
      <REQUESTDESC>
        <REPORTNAME>Vouchers</REPORTNAME>
        <STATICVARIABLES>
          <SVCURRENTCOMPANY>COMPANY_NAME</SVCURRENTCOMPANY>
        </STATICVARIABLES>
      </REQUESTDESC>
      <REQUESTDATA>
        <TALLYMESSAGE xmlns:UDF="TallyUDF">
          <VOUCHER VCHTYPE="Receipt" ACTION="Create" OBJVIEW="Accounting Voucher View">
            <GUID>bankstmt-bob-20260401-001</GUID>
            <DATE>20260401</DATE>
            <VOUCHERTYPENAME>Receipt</VOUCHERTYPENAME>
            <NARRATION>NEFT Credit from ABC Traders Ref NEFT/123456</NARRATION>
            <ISINVOICE>No</ISINVOICE>
            <PARTYLEDGERNAME>ABC Traders</PARTYLEDGERNAME>

            <!-- Bank (credit to account = negative in Tally) -->
            <ALLLEDGERENTRIES.LIST>
              <LEDGERNAME>Bank Of Baroda </LEDGERNAME>
              <ISDEEMEDPOSITIVE>Yes</ISDEEMEDPOSITIVE>
              <AMOUNT>-50000</AMOUNT>
            </ALLLEDGERENTRIES.LIST>

            <!-- Customer (debit) -->
            <ALLLEDGERENTRIES.LIST>
              <LEDGERNAME>ABC Traders</LEDGERNAME>
              <ISPARTYLEDGER>Yes</ISPARTYLEDGER>
              <ISDEEMEDPOSITIVE>No</ISDEEMEDPOSITIVE>
              <AMOUNT>50000</AMOUNT>
            </ALLLEDGERENTRIES.LIST>
          </VOUCHER>
        </TALLYMESSAGE>
      </REQUESTDATA>
    </IMPORTDATA>
  </BODY>
</ENVELOPE>
```

### Example: NEFT Debit to Supplier (Payment)

```xml
<?xml version="1.0" encoding="utf-8"?>
<ENVELOPE>
  <HEADER><TALLYREQUEST>Import Data</TALLYREQUEST></HEADER>
  <BODY>
    <IMPORTDATA>
      <REQUESTDESC>
        <REPORTNAME>Vouchers</REPORTNAME>
        <STATICVARIABLES>
          <SVCURRENTCOMPANY>COMPANY_NAME</SVCURRENTCOMPANY>
        </STATICVARIABLES>
      </REQUESTDESC>
      <REQUESTDATA>
        <TALLYMESSAGE xmlns:UDF="TallyUDF">
          <VOUCHER VCHTYPE="Payment" ACTION="Create" OBJVIEW="Accounting Voucher View">
            <GUID>bankstmt-bob-20260401-002</GUID>
            <DATE>20260401</DATE>
            <VOUCHERTYPENAME>Payment</VOUCHERTYPENAME>
            <NARRATION>Payment to XYZ Suppliers via NEFT Ref NEFT/789012</NARRATION>
            <ISINVOICE>No</ISINVOICE>
            <PARTYLEDGERNAME>XYZ Suppliers</PARTYLEDGERNAME>

            <!-- Supplier (expense = debit) -->
            <ALLLEDGERENTRIES.LIST>
              <LEDGERNAME>XYZ Suppliers</LEDGERNAME>
              <ISPARTYLEDGER>Yes</ISPARTYLEDGER>
              <ISDEEMEDPOSITIVE>Yes</ISDEEMEDPOSITIVE>
              <AMOUNT>-25000</AMOUNT>
            </ALLLEDGERENTRIES.LIST>

            <!-- Bank (credit from account = positive in Tally) -->
            <ALLLEDGERENTRIES.LIST>
              <LEDGERNAME>Bank Of Baroda</LEDGERNAME>
              <ISDEEMEDPOSITIVE>No</ISDEEMEDPOSITIVE>
              <AMOUNT>25000</AMOUNT>
            </ALLLEDGERENTRIES.LIST>
          </VOUCHER>
        </TALLYMESSAGE>
      </REQUESTDATA>
    </IMPORTDATA>
  </BODY>
</ENVELOPE>
```

### Example: Bank Charges (Payment, no party)

```xml
<?xml version="1.0" encoding="utf-8"?>
<ENVELOPE>
  <HEADER><TALLYREQUEST>Import Data</TALLYREQUEST></HEADER>
  <BODY>
    <IMPORTDATA>
      <REQUESTDESC>
        <REPORTNAME>Vouchers</REPORTNAME>
        <STATICVARIABLES>
          <SVCURRENTCOMPANY>COMPANY_NAME</SVCURRENTCOMPANY>
        </STATICVARIABLES>
      </REQUESTDESC>
      <REQUESTDATA>
        <TALLYMESSAGE xmlns:UDF="TallyUDF">
          <VOUCHER VCHTYPE="Payment" ACTION="Create" OBJVIEW="Accounting Voucher View">
            <GUID>bankstmt-bob-20260401-003</GUID>
            <DATE>20260401</DATE>
            <VOUCHERTYPENAME>Payment</VOUCHERTYPENAME>
            <NARRATION>Bank Charges for Q1 FY 2026-27</NARRATION>
            <ISINVOICE>No</ISINVOICE>

            <!-- Bank Charges Expense -->
            <ALLLEDGERENTRIES.LIST>
              <LEDGERNAME>Bank Charges</LEDGERNAME>
              <ISDEEMEDPOSITIVE>Yes</ISDEEMEDPOSITIVE>
              <AMOUNT>-150</AMOUNT>
            </ALLLEDGERENTRIES.LIST>

            <!-- Bank -->
            <ALLLEDGERENTRIES.LIST>
              <LEDGERNAME>Bank Of Baroda</LEDGERNAME>
              <ISDEEMEDPOSITIVE>No</ISDEEMEDPOSITIVE>
              <AMOUNT>150</AMOUNT>
            </ALLLEDGERENTRIES.LIST>
          </VOUCHER>
        </TALLYMESSAGE>
      </REQUESTDATA>
    </IMPORTDATA>
  </BODY>
</ENVELOPE>
```



