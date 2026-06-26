# Sales Vouchers — TallyPrime XML Templates

Covers: Item Invoice · As Voucher (with and without voucher class).

## Conventions

- Always set `SVCURRENTCOMPANY` and `GUID`.
- Dates as `YYYYMMDD`. Escape `&` → `&amp;`.
- Include `BILLALLOCATIONS.LIST` on the customer entry. Voucher totals must sum to zero.
- `Invoice Voucher View` → use `LEDGERENTRIES.LIST`
- `Accounting Voucher View` → use `ALLLEDGERENTRIES.LIST`

## Voucher class — decision rules

Run this **every time** before posting.

```
Does the company's Sales voucher type have a class configured?
│
├─ YES → Exact class name confirmed?
│         ├─ Yes → Use "with class" template. Set CLASSNAME + all 4 GST header fields.
│         └─ No  → STOP. Ask: "What is the exact class name in Tally?"
│
├─ NO  → Use "no class" template (As Voucher only for Sales).
│
└─ UNKNOWN → STOP. Ask: "Does this company use voucher classes (e.g. Sales @ 18 %)?"
```

### GST ledger names per class rate

| Class | CGST % | SGST % | Output CGST ledger | Output SGST ledger |
|---|---|---|---|---|
| Sales @ 5 % | 2.5 | 2.5 | `Output Cgst @ 2.5 %` | `Output Sgst @ 2.5 %` |
| Sales @ 18 % | 9 | 9 | `Output Cgst @ 9 %` | `Output Sgst @ 9 %` |
| Sales @ 28 % | 14 | 14 | `Output Cgst @ 14 %` | `Output Sgst @ 14 %` |

Ledger names must match **exactly** as configured in Tally.

### Class mode — required header fields

```xml
<CLASSNAME>Sales @ 18 %</CLASSNAME>
<CMPGSTIN>COMPANY_GSTIN</CMPGSTIN>
<PARTYGSTIN>CUSTOMER_GSTIN</PARTYGSTIN>
<GSTREGISTRATIONTYPE>Regular</GSTREGISTRATIONTYPE>
<PLACEOFSUPPLY>STATE_NAME</PLACEOFSUPPLY>
```

## Mode selection

| Mode | `OBJVIEW` | `ISINVOICE` | Use when |
|---|---|---|---|
| Item Invoice | `Invoice Voucher View` | Yes | Stock items with Qty/Rate/Amount |
| As Voucher | `Accounting Voucher View` | No | Ledger-only, classic view |

---

## Item Invoice — with class (5 / 18 / 28 %)

Replace `Sales @ 18 %` and GST ledger names per the rate table above.

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
          <VOUCHER VCHTYPE="Sales" ACTION="Create" OBJVIEW="Invoice Voucher View">
            <GUID>GUID_VALUE</GUID>
            <DATE>YYYYMMDD</DATE>
            <VOUCHERTYPENAME>Sales</VOUCHERTYPENAME>
            <VOUCHERNUMBER>INVOICE_NO</VOUCHERNUMBER>
            <REFERENCE>INVOICE_NO</REFERENCE>
            <REFERENCEDATE>YYYYMMDD</REFERENCEDATE>
            <PARTYLEDGERNAME>CUSTOMER_LEDGER</PARTYLEDGERNAME>
            <ISINVOICE>Yes</ISINVOICE>
            <PERSISTEDVIEW>Invoice Voucher View</PERSISTEDVIEW>
            <VCHENTRYMODE>Item Invoice</VCHENTRYMODE>

            <CLASSNAME>Sales @ 18 %</CLASSNAME>
            <CMPGSTIN>COMPANY_GSTIN</CMPGSTIN>
            <PARTYGSTIN>CUSTOMER_GSTIN</PARTYGSTIN>
            <GSTREGISTRATIONTYPE>Regular</GSTREGISTRATIONTYPE>
            <PLACEOFSUPPLY>STATE_NAME</PLACEOFSUPPLY>

            <!-- Repeat for each stock item -->
            <ALLINVENTORYENTRIES.LIST>
              <STOCKITEMNAME>ITEM_NAME</STOCKITEMNAME>
              <ISDEEMEDPOSITIVE>No</ISDEEMEDPOSITIVE>
              <RATE>RATE_PER_UNIT</RATE>
              <AMOUNT>TAXABLE_VALUE</AMOUNT>
              <ACTUALQTY>QUANTITY</ACTUALQTY>
              <BILLEDQTY>QUANTITY</BILLEDQTY>
              <BATCHALLOCATIONS.LIST>
                <GODOWNNAME>Main Location</GODOWNNAME>
                <BATCHNAME>Primary Batch</BATCHNAME>
                <AMOUNT>TAXABLE_VALUE</AMOUNT>
                <ACTUALQTY>QUANTITY</ACTUALQTY>
                <BILLEDQTY>QUANTITY</BILLEDQTY>
              </BATCHALLOCATIONS.LIST>
              <ACCOUNTINGALLOCATIONS.LIST>
                <LEDGERNAME>SALES_LEDGER</LEDGERNAME>
                <ISDEEMEDPOSITIVE>No</ISDEEMEDPOSITIVE>
                <AMOUNT>TAXABLE_VALUE</AMOUNT>
              </ACCOUNTINGALLOCATIONS.LIST>
            </ALLINVENTORYENTRIES.LIST>

            <!-- LEDGERENTRIES.LIST required in Invoice Voucher View -->
            <LEDGERENTRIES.LIST>
              <LEDGERNAME>CUSTOMER_LEDGER</LEDGERNAME>
              <ISPARTYLEDGER>Yes</ISPARTYLEDGER>
              <ISDEEMEDPOSITIVE>Yes</ISDEEMEDPOSITIVE>
              <AMOUNT>-TOTAL_AMOUNT</AMOUNT>
              <BILLALLOCATIONS.LIST>
                <NAME>INVOICE_NO</NAME>
                <BILLTYPE>New Ref</BILLTYPE>
                <AMOUNT>-TOTAL_AMOUNT</AMOUNT>
                <BILLDATE>YYYYMMDD</BILLDATE>
              </BILLALLOCATIONS.LIST>
            </LEDGERENTRIES.LIST>

            <LEDGERENTRIES.LIST>
              <LEDGERNAME>Output Cgst @ 9 %</LEDGERNAME>
              <ISDEEMEDPOSITIVE>No</ISDEEMEDPOSITIVE>
              <AMOUNT>CGST_AMOUNT</AMOUNT>
            </LEDGERENTRIES.LIST>

            <LEDGERENTRIES.LIST>
              <LEDGERNAME>Output Sgst @ 9 %</LEDGERNAME>
              <ISDEEMEDPOSITIVE>No</ISDEEMEDPOSITIVE>
              <AMOUNT>SGST_AMOUNT</AMOUNT>
            </LEDGERENTRIES.LIST>
          </VOUCHER>
        </TALLYMESSAGE>
      </REQUESTDATA>
    </IMPORTDATA>
  </BODY>
</ENVELOPE>
```

---

## As Voucher — no class (ledger-only)

`OBJVIEW="Accounting Voucher View"` + `ISINVOICE=No`. Customer entry **must come first**.

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
            <ISINVOICE>No</ISINVOICE>
            <PARTYLEDGERNAME>CUSTOMER_LEDGER</PARTYLEDGERNAME>

            <!-- Customer FIRST — drives Day Book Particulars -->
            <ALLLEDGERENTRIES.LIST>
              <LEDGERNAME>CUSTOMER_LEDGER</LEDGERNAME>
              <ISPARTYLEDGER>Yes</ISPARTYLEDGER>
              <ISDEEMEDPOSITIVE>Yes</ISDEEMEDPOSITIVE>
              <AMOUNT>-TOTAL_AMOUNT</AMOUNT>
              <BILLALLOCATIONS.LIST>
                <NAME>INVOICE_NO</NAME>
                <BILLTYPE>New Ref</BILLTYPE>
                <AMOUNT>-TOTAL_AMOUNT</AMOUNT>
                <BILLDATE>YYYYMMDD</BILLDATE>
              </BILLALLOCATIONS.LIST>
            </ALLLEDGERENTRIES.LIST>

            <ALLLEDGERENTRIES.LIST>
              <LEDGERNAME>SALES_LEDGER</LEDGERNAME>
              <ISDEEMEDPOSITIVE>No</ISDEEMEDPOSITIVE>
              <AMOUNT>BASE_AMOUNT</AMOUNT>
            </ALLLEDGERENTRIES.LIST>

            <ALLLEDGERENTRIES.LIST>
              <LEDGERNAME>Output Cgst @ RATE %</LEDGERNAME>
              <ISDEEMEDPOSITIVE>No</ISDEEMEDPOSITIVE>
              <AMOUNT>CGST_AMOUNT</AMOUNT>
            </ALLLEDGERENTRIES.LIST>

            <ALLLEDGERENTRIES.LIST>
              <LEDGERNAME>Output Sgst @ RATE %</LEDGERNAME>
              <ISDEEMEDPOSITIVE>No</ISDEEMEDPOSITIVE>
              <AMOUNT>SGST_AMOUNT</AMOUNT>
            </ALLLEDGERENTRIES.LIST>
          </VOUCHER>
        </TALLYMESSAGE>
      </REQUESTDATA>
    </IMPORTDATA>
  </BODY>
</ENVELOPE>
```
