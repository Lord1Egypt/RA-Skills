# Reports — Post-Entry Review & Ledger Fetch

Focused on: post-entry voucher review (mandatory after every post) and ledger name fetch (bank statement pre-flight).

## Import response — how to read it

After every `Import Data` POST, Tally returns a statistics block. Always parse it before telling the user the entry is complete.

Key fields to check:

| Field | Meaning |
|---|---|
| `CREATED` | Objects successfully created |
| `ALTERED` | Objects successfully altered |
| `ERRORS` | Import errors — treat any non-zero value as failure |
| `EXCEPTIONS` | Partial/unexpected failures |

**Rule:** if `ERRORS > 0` or `CREATED = 0` (for a Create action), the voucher was **not** posted. Do not tell the user it was posted. Read the error detail, diagnose, and fix before retrying.

---

## Fetch last Sales invoice number (for auto-increment)

Use before PDF generation to determine the next invoice number without asking the user.

```xml
<?xml version="1.0" encoding="utf-8"?>
<ENVELOPE>
  <HEADER><TALLYREQUEST>Export Data</TALLYREQUEST></HEADER>
  <BODY>
    <EXPORTDATA>
      <REQUESTDESC>
        <REPORTNAME>Voucher Register</REPORTNAME>
        <STATICVARIABLES>
          <SVEXPORTFORMAT>$$SysName:XML</SVEXPORTFORMAT>
          <SVCURRENTCOMPANY>COMPANY_NAME</SVCURRENTCOMPANY>
          <SVVOUCHERTYPENAME>Sales</SVVOUCHERTYPENAME>
          <SVFROMDATE>FYSTART_YYYYMMDD</SVFROMDATE>
          <SVTODATE>TODAY_YYYYMMDD</SVTODATE>
        </STATICVARIABLES>
      </REQUESTDESC>
    </EXPORTDATA>
  </BODY>
</ENVELOPE>
```

- `SVFROMDATE`: start of the current financial year (Indian FY starts April 1 — e.g., `20250401`).
- `SVTODATE`: today's date.
- From the response, collect all `<VOUCHERNUMBER>` values, extract the numeric part from the last/highest one, and add 1.
- If no Sales vouchers exist yet this FY, start from `1`.

---

## Post-entry review (mandatory after every Create)

After every voucher post, fetch it back from Tally and verify before telling the user it is done.

### Step 1 — Fetch via Voucher Register (preferred)

Filter by voucher type and the exact voucher date:

```xml
<?xml version="1.0" encoding="utf-8"?>
<ENVELOPE>
  <HEADER><TALLYREQUEST>Export Data</TALLYREQUEST></HEADER>
  <BODY>
    <EXPORTDATA>
      <REQUESTDESC>
        <REPORTNAME>Voucher Register</REPORTNAME>
        <STATICVARIABLES>
          <SVEXPORTFORMAT>$$SysName:XML</SVEXPORTFORMAT>
          <SVCURRENTCOMPANY>COMPANY_NAME</SVCURRENTCOMPANY>
          <SVVOUCHERTYPENAME>VOUCHER_TYPE</SVVOUCHERTYPENAME>
          <SVFROMDATE>VOUCHER_YYYYMMDD</SVFROMDATE>
          <SVTODATE>VOUCHER_YYYYMMDD</SVTODATE>
        </STATICVARIABLES>
      </REQUESTDESC>
    </EXPORTDATA>
  </BODY>
</ENVELOPE>
```

`SVVOUCHERTYPENAME` values: `Purchase` · `Sales` · `Payment` · `Receipt` · `Contra`

### Step 2 — Fallback: Day Book

Use when Voucher Register does not return enough detail:

```xml
<?xml version="1.0" encoding="utf-8"?>
<ENVELOPE>
  <HEADER><TALLYREQUEST>Export Data</TALLYREQUEST></HEADER>
  <BODY>
    <EXPORTDATA>
      <REQUESTDESC>
        <REPORTNAME>Day Book</REPORTNAME>
        <STATICVARIABLES>
          <SVEXPORTFORMAT>$$SysName:XML</SVEXPORTFORMAT>
          <SVCURRENTCOMPANY>COMPANY_NAME</SVCURRENTCOMPANY>
          <SVFROMDATE>VOUCHER_YYYYMMDD</SVFROMDATE>
          <SVTODATE>VOUCHER_YYYYMMDD</SVTODATE>
        </STATICVARIABLES>
      </REQUESTDESC>
    </EXPORTDATA>
  </BODY>
</ENVELOPE>
```

### Step 3 — Fallback: Ledger Vouchers

Use when you need to confirm a specific party or bank ledger entry:

```xml
<?xml version="1.0" encoding="utf-8"?>
<ENVELOPE>
  <HEADER><TALLYREQUEST>Export Data</TALLYREQUEST></HEADER>
  <BODY>
    <EXPORTDATA>
      <REQUESTDESC>
        <REPORTNAME>Ledger Vouchers</REPORTNAME>
        <STATICVARIABLES>
          <SVEXPORTFORMAT>$$SysName:XML</SVEXPORTFORMAT>
          <SVCURRENTCOMPANY>COMPANY_NAME</SVCURRENTCOMPANY>
          <SVLEDGERNAME>LEDGER_NAME</SVLEDGERNAME>
          <SVFROMDATE>FROM_YYYYMMDD</SVFROMDATE>
          <SVTODATE>TO_YYYYMMDD</SVTODATE>
        </STATICVARIABLES>
      </REQUESTDESC>
    </EXPORTDATA>
  </BODY>
</ENVELOPE>
```

### Review checklist

Locate the voucher by GUID first; if GUID is not in the export, match by voucher type + number + date + party + amount.

- Company and voucher type
- Voucher number/reference and date
- Party ledger and all debit/credit ledger names
- Debit/credit direction and total amount
- GST ledgers, taxable value, tax split, round-off
- Bill-wise allocations and narration

If anything does not match, do **not** confirm to the user. Explain the mismatch in business terms and ask how to proceed.

---

## Ledger Names — fetch all (bank statement pre-flight)

Before posting bank statement transactions, fetch all ledger names and confirm the mapping with the user once before posting.

```xml
<?xml version="1.0" encoding="utf-8"?>
<ENVELOPE>
  <HEADER>
    <VERSION>1</VERSION>
    <TALLYREQUEST>Export</TALLYREQUEST>
    <TYPE>Data</TYPE>
    <ID>LedgerListReport</ID>
  </HEADER>
  <BODY>
    <DESC>
      <STATICVARIABLES>
        <SVEXPORTFORMAT>$$SysName:XML</SVEXPORTFORMAT>
        <SVCURRENTCOMPANY>COMPANY_NAME</SVCURRENTCOMPANY>
      </STATICVARIABLES>
      <TDL>
        <TDLMESSAGE>
          <REPORT NAME="LedgerListReport">
            <FORMS>LedgerListForm</FORMS>
          </REPORT>
          <FORM NAME="LedgerListForm">
            <PARTS>LedgerListPart</PARTS>
          </FORM>
          <PART NAME="LedgerListPart">
            <LINES>LedgerListLine</LINES>
            <REPEAT>LedgerListLine : LedgerCollection</REPEAT>
            <SCROLL>Vertical</SCROLL>
          </PART>
          <LINE NAME="LedgerListLine">
            <FIELDS>LedgerNameField</FIELDS>
          </LINE>
          <FIELD NAME="LedgerNameField">
            <SET>$Name</SET>
          </FIELD>
          <COLLECTION NAME="LedgerCollection">
            <TYPE>Ledger</TYPE>
          </COLLECTION>
        </TDLMESSAGE>
      </TDL>
    </DESC>
  </BODY>
</ENVELOPE>
```

Present the relevant ledgers to the user as: "These are the ledgers I will use for the bank entries: [bank ledger], [party ledgers]. Confirm to proceed." Do not post until confirmed.
