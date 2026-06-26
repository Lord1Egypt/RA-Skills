# Purchase Vouchers — TallyPrime XML Templates

Covers: Item Invoice · Accounting Invoice · As Voucher (with and without voucher class).

## Conventions

- Always set `SVCURRENTCOMPANY` and `GUID`.
- Dates as `YYYYMMDD`. Escape `&` → `&amp;`.
- Include `BILLALLOCATIONS.LIST` on the vendor entry. Voucher totals must sum to zero.
- `Invoice Voucher View` → use `LEDGERENTRIES.LIST`
- `Accounting Voucher View` → use `ALLLEDGERENTRIES.LIST`

## Voucher class — decision rules

Run this **every time** before posting.

```
Does the company's Purchase voucher type have a class configured?
│
├─ YES → Exact class name confirmed?
│         ├─ Yes → Use "with class" template. Set CLASSNAME + all 4 GST header fields.
│         └─ No  → STOP. Ask: "What is the exact class name in Tally?"
│
├─ NO  → Use "no class" template.
│
└─ UNKNOWN → STOP. Ask: "Does this company use voucher classes (e.g. Purchase @ 18 %)?"
```

### GST ledger names per class rate

| Class | CGST % | SGST % | Input CGST ledger | Input SGST ledger |
|---|---|---|---|---|
| Purchase @ 5 % | 2.5 | 2.5 | `Input Cgst @ 2.5 %` | `Input Sgst @ 2.5 %` |
| Purchase @ 18 % | 9 | 9 | `Input Cgst @ 9 %` | `Input Sgst @ 9 %` |
| Purchase @ 28 % | 14 | 14 | `Input Cgst @ 14 %` | `Input Sgst @ 14 %` |

Ledger names must match **exactly** as configured in Tally.

### Class mode — required header fields

```xml
<CLASSNAME>Purchase @ 18 %</CLASSNAME>
<CMPGSTIN>COMPANY_GSTIN</CMPGSTIN>
<PARTYGSTIN>VENDOR_GSTIN</PARTYGSTIN>
<GSTREGISTRATIONTYPE>Regular</GSTREGISTRATIONTYPE>
<PLACEOFSUPPLY>STATE_NAME</PLACEOFSUPPLY>
```

## Mode selection

| Mode | `OBJVIEW` | `ISINVOICE` | Use when |
|---|---|---|---|
| Item Invoice | `Invoice Voucher View` | Yes | Stock items with Qty/Rate/Amount |
| Accounting Invoice | `Invoice Voucher View` | Yes | Invoice layout, ledger-only (services/expenses) |
| As Voucher | `Accounting Voucher View` | No | Classic By/To accounting view |

---

## Item Invoice — no class

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

            <!-- Repeat for each stock item -->
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

            <ALLLEDGERENTRIES.LIST>
              <LEDGERNAME>PURCHASE_LEDGER</LEDGERNAME>
              <ISDEEMEDPOSITIVE>Yes</ISDEEMEDPOSITIVE>
              <AMOUNT>-TAXABLE_VALUE</AMOUNT>
            </ALLLEDGERENTRIES.LIST>

            <ALLLEDGERENTRIES.LIST>
              <LEDGERNAME>Input Cgst @ RATE %</LEDGERNAME>
              <ISDEEMEDPOSITIVE>Yes</ISDEEMEDPOSITIVE>
              <AMOUNT>-CGST_AMOUNT</AMOUNT>
            </ALLLEDGERENTRIES.LIST>

            <ALLLEDGERENTRIES.LIST>
              <LEDGERNAME>Input Sgst @ RATE %</LEDGERNAME>
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

---

## Item Invoice — with class (5 / 18 / 28 %)

Replace `Purchase @ 18 %` and GST ledger names per the rate table above.

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

            <CLASSNAME>Purchase @ 18 %</CLASSNAME>
            <CMPGSTIN>COMPANY_GSTIN</CMPGSTIN>
            <PARTYGSTIN>VENDOR_GSTIN</PARTYGSTIN>
            <GSTREGISTRATIONTYPE>Regular</GSTREGISTRATIONTYPE>
            <PLACEOFSUPPLY>STATE_NAME</PLACEOFSUPPLY>

            <!-- LEDGERENTRIES.LIST required in Invoice Voucher View -->
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
                <LEDGERNAME>PURCHASE_LEDGER</LEDGERNAME>
                <ISDEEMEDPOSITIVE>No</ISDEEMEDPOSITIVE>
                <AMOUNT>TAXABLE_VALUE</AMOUNT>
              </ACCOUNTINGALLOCATIONS.LIST>
            </ALLINVENTORYENTRIES.LIST>

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
        </TALLYMESSAGE>
      </REQUESTDATA>
    </IMPORTDATA>
  </BODY>
</ENVELOPE>
```

---

## Accounting Invoice — no class

Invoice layout, no stock items. `LEDGERENTRIES.LIST` required (Invoice Voucher View).
`VCHENTRYMODE` must be set to `Accounting Invoice` — without it Tally defaults to Item Invoice.

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
            <VCHENTRYMODE>Accounting Invoice</VCHENTRYMODE>
            <NARRATION>NARRATION_TEXT</NARRATION>

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

            <LEDGERENTRIES.LIST>
              <LEDGERNAME>PURCHASE_LEDGER</LEDGERNAME>
              <ISDEEMEDPOSITIVE>Yes</ISDEEMEDPOSITIVE>
              <AMOUNT>-TAXABLE_VALUE</AMOUNT>
            </LEDGERENTRIES.LIST>

            <LEDGERENTRIES.LIST>
              <LEDGERNAME>Input Cgst @ RATE %</LEDGERNAME>
              <ISDEEMEDPOSITIVE>Yes</ISDEEMEDPOSITIVE>
              <AMOUNT>-CGST_AMOUNT</AMOUNT>
            </LEDGERENTRIES.LIST>

            <LEDGERENTRIES.LIST>
              <LEDGERNAME>Input Sgst @ RATE %</LEDGERNAME>
              <ISDEEMEDPOSITIVE>Yes</ISDEEMEDPOSITIVE>
              <AMOUNT>-SGST_AMOUNT</AMOUNT>
            </LEDGERENTRIES.LIST>

            <!-- Optional -->
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

---

## Accounting Invoice — with class (5 / 18 / 28 %)

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
            <VCHENTRYMODE>Accounting Invoice</VCHENTRYMODE>
            <NARRATION>NARRATION_TEXT</NARRATION>

            <CLASSNAME>Purchase @ 18 %</CLASSNAME>
            <CMPGSTIN>COMPANY_GSTIN</CMPGSTIN>
            <PARTYGSTIN>VENDOR_GSTIN</PARTYGSTIN>
            <GSTREGISTRATIONTYPE>Regular</GSTREGISTRATIONTYPE>
            <PLACEOFSUPPLY>STATE_NAME</PLACEOFSUPPLY>

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

            <LEDGERENTRIES.LIST>
              <LEDGERNAME>PURCHASE_LEDGER</LEDGERNAME>
              <ISDEEMEDPOSITIVE>Yes</ISDEEMEDPOSITIVE>
              <AMOUNT>-TAXABLE_VALUE</AMOUNT>
            </LEDGERENTRIES.LIST>

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
        </TALLYMESSAGE>
      </REQUESTDATA>
    </IMPORTDATA>
  </BODY>
</ENVELOPE>
```

---

## As Voucher (classic By/To view)

`OBJVIEW="Accounting Voucher View"` + `ISINVOICE=No`. Vendor entry **must come first** so the Day Book Particulars column shows the vendor name.

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

            <!-- Vendor FIRST — drives Day Book Particulars -->
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

            <ALLLEDGERENTRIES.LIST>
              <LEDGERNAME>PURCHASE_LEDGER</LEDGERNAME>
              <ISDEEMEDPOSITIVE>Yes</ISDEEMEDPOSITIVE>
              <AMOUNT>-TAXABLE_VALUE</AMOUNT>
            </ALLLEDGERENTRIES.LIST>

            <ALLLEDGERENTRIES.LIST>
              <LEDGERNAME>Input Cgst @ RATE %</LEDGERNAME>
              <ISDEEMEDPOSITIVE>Yes</ISDEEMEDPOSITIVE>
              <AMOUNT>-CGST_AMOUNT</AMOUNT>
            </ALLLEDGERENTRIES.LIST>

            <ALLLEDGERENTRIES.LIST>
              <LEDGERNAME>Input Sgst @ RATE %</LEDGERNAME>
              <ISDEEMEDPOSITIVE>Yes</ISDEEMEDPOSITIVE>
              <AMOUNT>-SGST_AMOUNT</AMOUNT>
            </ALLLEDGERENTRIES.LIST>

            <!-- Optional -->
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
