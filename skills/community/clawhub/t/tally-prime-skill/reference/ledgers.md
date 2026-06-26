# Ledgers — Check & Create

Covers: ledger existence check · party ledger creation (customer/vendor) · minimal ledger creation.

## Fetch party GSTIN, place of supply, and address

Use this before PDF generation to auto-fill `customer-gstin`, `place-of-supply`, and address from the party ledger already in Tally.

```xml
<?xml version="1.0" encoding="utf-8"?>
<ENVELOPE>
  <HEADER>
    <VERSION>1</VERSION>
    <TALLYREQUEST>Export</TALLYREQUEST>
    <TYPE>Data</TYPE>
    <ID>PartyDetailReport</ID>
  </HEADER>
  <BODY>
    <DESC>
      <STATICVARIABLES>
        <SVEXPORTFORMAT>$$SysName:XML</SVEXPORTFORMAT>
        <SVCURRENTCOMPANY>COMPANY_NAME</SVCURRENTCOMPANY>
      </STATICVARIABLES>
      <TDL>
        <TDLMESSAGE>
          <REPORT NAME="PartyDetailReport">
            <FORMS>PartyDetailForm</FORMS>
          </REPORT>
          <FORM NAME="PartyDetailForm">
            <PARTS>PartyDetailPart</PARTS>
          </FORM>
          <PART NAME="PartyDetailPart">
            <LINES>PartyDetailLine</LINES>
            <REPEAT>PartyDetailLine : PartyLedgerColl</REPEAT>
            <SCROLL>Vertical</SCROLL>
          </PART>
          <LINE NAME="PartyDetailLine">
            <FIELDS>FldName, FldGSTIN, FldPlaceOfSupply, FldRegType, FldAddr1</FIELDS>
          </LINE>
          <FIELD NAME="FldName">
            <SET>$Name</SET>
          </FIELD>
          <FIELD NAME="FldGSTIN">
            <SET>$PARTYGSTIN</SET>
          </FIELD>
          <FIELD NAME="FldPlaceOfSupply">
            <SET>$PriorStateName</SET>
          </FIELD>
          <FIELD NAME="FldRegType">
            <SET>$GSTRegistrationType</SET>
          </FIELD>
          <FIELD NAME="FldAddr1">
            <SET>$Address</SET>
          </FIELD>
          <COLLECTION NAME="PartyLedgerColl">
            <TYPE>Ledger</TYPE>
            <FILTER>ByLedgerName</FILTER>
          </COLLECTION>
          <SYSTEM TYPE="Formulae" NAME="ByLedgerName">
            $Name = "PARTY_LEDGER_NAME"
          </SYSTEM>
        </TDLMESSAGE>
      </TDL>
    </DESC>
  </BODY>
</ENVELOPE>
```

**Parse the response:**

| Field needed | XML path | Example |
|---|---|---|
| `customer-gstin` | `FldGSTIN` → maps to `$PARTYGSTIN` | `24AFTPD8403N1Z3` |
| `place-of-supply` | `FldPlaceOfSupply` → maps to `$PriorStateName` | `Gujarat` |
| Registration type | `FldRegType` → maps to `$GSTRegistrationType` | `Regular` / `Unregistered` |
| Address line 1 | `FldAddr1` → maps to `$Address` | `C/1, Amarnath Tenament` |

**Full address** — the Day Book / Voucher Register export for any voucher involving this party includes the complete `ADDRESS.LIST` with all lines. Parse it from there when you need more than line 1.

**Place of supply decision:**
- If `FldPlaceOfSupply` == company's state → intra-state → CGST + SGST apply
- If different → inter-state → IGST applies
- If `FldPlaceOfSupply` is empty (unregistered party) → default to company's state

**If `FldGSTIN` is empty:** party is unregistered — omit `--customer-gstin` flag; do not use `--b2b`.

---

## Fetch company address (for PDF `--company-address`)

Use this to auto-fill the seller address on the invoice.

```xml
<?xml version="1.0" encoding="utf-8"?>
<ENVELOPE>
  <HEADER>
    <VERSION>1</VERSION>
    <TALLYREQUEST>Export</TALLYREQUEST>
    <TYPE>Data</TYPE>
    <ID>CompanyAddrReport</ID>
  </HEADER>
  <BODY>
    <DESC>
      <STATICVARIABLES>
        <SVEXPORTFORMAT>$$SysName:XML</SVEXPORTFORMAT>
        <SVCURRENTCOMPANY>COMPANY_NAME</SVCURRENTCOMPANY>
      </STATICVARIABLES>
      <TDL>
        <TDLMESSAGE>
          <REPORT NAME="CompanyAddrReport">
            <FORMS>CmpAddrForm</FORMS>
          </REPORT>
          <FORM NAME="CmpAddrForm">
            <PARTS>CmpAddrPart</PARTS>
          </FORM>
          <PART NAME="CmpAddrPart">
            <LINES>CmpAddrLine</LINES>
            <REPEAT>CmpAddrLine : CmpColl</REPEAT>
            <SCROLL>Vertical</SCROLL>
          </PART>
          <LINE NAME="CmpAddrLine">
            <FIELDS>FldAddr, FldPin, FldState</FIELDS>
          </LINE>
          <FIELD NAME="FldAddr">
            <SET>$Address</SET>
          </FIELD>
          <FIELD NAME="FldPin">
            <SET>$PinCode</SET>
          </FIELD>
          <FIELD NAME="FldState">
            <SET>$StateName</SET>
          </FIELD>
          <COLLECTION NAME="CmpColl">
            <TYPE>Company</TYPE>
          </COLLECTION>
        </TDLMESSAGE>
      </TDL>
    </DESC>
  </BODY>
</ENVELOPE>
```

**Parse the response** and build the `--company-address` string:

| Field | XML tag | Example |
|---|---|---|
| Address line 1 | `FldAddr` | `Shop No 6, Rajendra Shopping Center` |
| Pincode | `FldPin` | `380008` |
| State | `FldState` | `Gujarat` |

Combine as: `"<FldAddr>, <FldState> <FldPin>"`. For the remaining address lines (stored in Tally but not returned by `$Address`), append them from known company data or ask the user once to confirm.

**Company GSTIN** — not available via Company TDL fields. Read `<CMPGSTIN>` from any recent Day Book sales voucher export.

---

## Check if a ledger exists

Fetch the List of Accounts and search the response for the ledger name before posting any voucher.

```xml
<?xml version="1.0" encoding="utf-8"?>
<ENVELOPE>
  <HEADER><TALLYREQUEST>Export Data</TALLYREQUEST></HEADER>
  <BODY>
    <EXPORTDATA>
      <REQUESTDESC>
        <REPORTNAME>List of Accounts</REPORTNAME>
        <STATICVARIABLES>
          <SVEXPORTFORMAT>$$SysName:XML</SVEXPORTFORMAT>
          <SVCURRENTCOMPANY>COMPANY_NAME</SVCURRENTCOMPANY>
        </STATICVARIABLES>
      </REQUESTDESC>
    </EXPORTDATA>
  </BODY>
</ENVELOPE>
```

Search the response XML for `<NAME>LEDGER_NAME</NAME>`. If absent, create the ledger before posting.

## Create party ledger (customer or vendor)

Collect all fields below from the user before creating. Do **not** guess GSTIN, state, or opening balance.

| Field | Description |
|---|---|
| `LEDGER_NAME` | Full legal name |
| `PARENT` | `Sundry Debtors` (customer) or `Sundry Creditors` (vendor) |
| `PARTYGSTIN` | 15-digit GSTIN (omit if unregistered) |
| `GSTREGISTRATIONTYPE` | `Regular` / `Unregistered` / `Consumer` / `Composition` |
| `STATE_NAME` | State of registered address |
| `APPLICABLEFROM` | GST effective date `YYYYMMDD` |
| `ADDRESS_LINE_1/2` | Street address lines |
| `OPENINGBALANCE` | 0 if none; positive = credit, negative = debit |

```xml
<?xml version="1.0" encoding="utf-8"?>
<ENVELOPE>
  <HEADER><TALLYREQUEST>Import Data</TALLYREQUEST></HEADER>
  <BODY>
    <IMPORTDATA>
      <REQUESTDESC>
        <REPORTNAME>All Masters</REPORTNAME>
        <STATICVARIABLES>
          <SVCURRENTCOMPANY>COMPANY_NAME</SVCURRENTCOMPANY>
        </STATICVARIABLES>
      </REQUESTDESC>
      <REQUESTDATA>
        <TALLYMESSAGE xmlns:UDF="TallyUDF">
          <LEDGER NAME="LEDGER_NAME" ACTION="Create">
            <NAME>LEDGER_NAME</NAME>
            <PARENT>Sundry Creditors</PARENT>
            <TAXTYPE>Others</TAXTYPE>
            <GSTREGISTRATIONTYPE>Regular</GSTREGISTRATIONTYPE>
            <PARTYGSTIN>PARTY_GSTIN</PARTYGSTIN>
            <COUNTRYOFRESIDENCE>India</COUNTRYOFRESIDENCE>
            <ISBILLWISEON>No</ISBILLWISEON>
            <OPENINGBALANCE>0</OPENINGBALANCE>

            <LANGUAGENAME.LIST>
              <NAME.LIST TYPE="String">
                <NAME>LEDGER_NAME</NAME>
                <NAME>2</NAME>
              </NAME.LIST>
              <LANGUAGEID>1033</LANGUAGEID>
            </LANGUAGENAME.LIST>

            <LEDGSTREGDETAILS.LIST>
              <APPLICABLEFROM>YYYYMMDD</APPLICABLEFROM>
              <GSTREGISTRATIONTYPE>Regular</GSTREGISTRATIONTYPE>
              <STATE>STATE_NAME</STATE>
              <PLACEOFSUPPLY>STATE_NAME</PLACEOFSUPPLY>
              <GSTIN>PARTY_GSTIN</GSTIN>
              <ISOTHTERRITORYASSESSEE>No</ISOTHTERRITORYASSESSEE>
              <CONSIDERPURCHASEFOREXPORT>No</CONSIDERPURCHASEFOREXPORT>
              <ISTRANSPORTER>No</ISTRANSPORTER>
              <ISCOMMONPARTY>No</ISCOMMONPARTY>
            </LEDGSTREGDETAILS.LIST>

            <LEDMAILINGDETAILS.LIST>
              <ADDRESS.LIST TYPE="String">
                <ADDRESS>ADDRESS_LINE_1</ADDRESS>
                <ADDRESS>ADDRESS_LINE_2</ADDRESS>
              </ADDRESS.LIST>
              <APPLICABLEFROM>YYYYMMDD</APPLICABLEFROM>
              <MAILINGNAME>LEDGER_NAME</MAILINGNAME>
              <STATE>STATE_NAME</STATE>
              <COUNTRY>India</COUNTRY>
            </LEDMAILINGDETAILS.LIST>
          </LEDGER>
        </TALLYMESSAGE>
      </REQUESTDATA>
    </IMPORTDATA>
  </BODY>
</ENVELOPE>
```

For **unregistered** parties: omit `<PARTYGSTIN>` and set `<GSTREGISTRATIONTYPE>Unregistered</GSTREGISTRATIONTYPE>` in both the header and `LEDGSTREGDETAILS.LIST`.

## Create minimal ledger (GST / bank / expense ledgers)

Use for non-party ledgers (GST duty heads, bank accounts, expense accounts).

```xml
<?xml version="1.0" encoding="utf-8"?>
<ENVELOPE>
  <HEADER><TALLYREQUEST>Import Data</TALLYREQUEST></HEADER>
  <BODY>
    <IMPORTDATA>
      <REQUESTDESC>
        <REPORTNAME>All Masters</REPORTNAME>
        <STATICVARIABLES>
          <SVCURRENTCOMPANY>COMPANY_NAME</SVCURRENTCOMPANY>
        </STATICVARIABLES>
      </REQUESTDESC>
      <REQUESTDATA>
        <TALLYMESSAGE xmlns:UDF="TallyUDF">
          <LEDGER NAME="LEDGER_NAME" ACTION="Create">
            <NAME>LEDGER_NAME</NAME>
            <PARENT>PARENT_GROUP</PARENT>
          </LEDGER>
        </TALLYMESSAGE>
      </REQUESTDATA>
    </IMPORTDATA>
  </BODY>
</ENVELOPE>
```

## Ledger group reference

| Ledger type | Parent group |
|---|---|
| Customer (debtor) | `Sundry Debtors` |
| Vendor (creditor) | `Sundry Creditors` |
| Sales income | `Sales Accounts` |
| Purchases | `Purchase Accounts` |
| Direct costs | `Direct Expenses` |
| Indirect expenses | `Indirect Expenses` |
| Bank account | `Bank Accounts` |
| Cash | `Cash-in-Hand` |
| GST ledgers | `Duties &amp; Taxes` |

## GST duty ledger creation (Input / Output CGST / SGST)

Use when a GST ledger is missing. Repeat for each rate slab (substitute rate and duty head).

```xml
<?xml version="1.0" encoding="utf-8"?>
<ENVELOPE>
  <HEADER><TALLYREQUEST>Import Data</TALLYREQUEST></HEADER>
  <BODY>
    <IMPORTDATA>
      <REQUESTDESC>
        <REPORTNAME>All Masters</REPORTNAME>
        <STATICVARIABLES>
          <SVCURRENTCOMPANY>COMPANY_NAME</SVCURRENTCOMPANY>
        </STATICVARIABLES>
      </REQUESTDESC>
      <REQUESTDATA>
        <TALLYMESSAGE xmlns:UDF="TallyUDF">
          <LEDGER NAME="Input Cgst @ 9 %" ACTION="Create">
            <NAME>Input Cgst @ 9 %</NAME>
            <PARENT>Duties &amp; Taxes</PARENT>
            <TAXTYPE>GST</TAXTYPE>
            <GSTDUTYHEAD>CGST</GSTDUTYHEAD>
            <RATEOFTAXCALCULATION>9</RATEOFTAXCALCULATION>
            <ISGSTDUTYLEDGER>Yes</ISGSTDUTYLEDGER>
          </LEDGER>
        </TALLYMESSAGE>
      </REQUESTDATA>
    </IMPORTDATA>
  </BODY>
</ENVELOPE>
```

| `GSTDUTYHEAD` value | Use for |
|---|---|
| `CGST` | Input/Output CGST ledgers |
| `SGST/UTGST` | Input/Output SGST ledgers |
| `IGST` | Input/Output IGST ledgers |
