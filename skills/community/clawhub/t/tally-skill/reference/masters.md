# Masters (Ledgers / Groups) — TallyPrime XML

This file contains templates to create and alter accounting masters that CAs routinely need: groups and ledgers (including address/GST fields where relevant).

## Conventions

- Master operations use `TALLYREQUEST=Import Data` and `REPORTNAME=All Masters`.
- Always include `SVCURRENTCOMPANY`.
- Create dependent masters first (e.g., group before ledger).

## Create Group

Example: create `North Zone Debtors` under `Sundry Debtors`.

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
          <GROUP NAME="North Zone Debtors" ACTION="Create">
            <NAME>North Zone Debtors</NAME>
            <PARENT>Sundry Debtors</PARENT>
          </GROUP>
        </TALLYMESSAGE>
      </REQUESTDATA>
    </IMPORTDATA>
  </BODY>
</ENVELOPE>
```

## Create Ledger (minimal)

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

## Create Party Ledger (Customer / Vendor)

Before creating, collect all required fields from the user:

| Field | Description | Example |
|---|---|---|
| `LEDGER_NAME` | Full legal name of the party | `Sample Suppliers Pvt Ltd` |
| `PARENT` | `Sundry Debtors` (customer) or `Sundry Creditors` (vendor/supplier) | `Sundry Creditors` |
| `PARTYGSTIN` | 15-digit GSTIN of the party | `24AAAAA0000A1Z5` |
| `GSTREGISTRATIONTYPE` | GST registration type | `Regular` / `Unregistered` / `Consumer` / `Composition` |
| `STATE` | State of the party's registered address | `Maharashtra` |
| `PLACEOFSUPPLY` | Usually same as state | `Maharashtra` |
| `ADDRESS` (lines) | Street address (one `<ADDRESS>` tag per line) | `123 Main Road`, `Industrial Area` |
| `MAILINGNAME` | Name to print on invoices (usually same as ledger name) | `Sample Suppliers Pvt Ltd` |
| `OPENINGBALANCE` | Opening balance amount (0 if none; positive = credit, negative = debit) | `10000.00` |
| `APPLICABLEFROM` | GST registration effective date in `YYYYMMDD` | `20170701` |

**Ask the user for every field above before posting. Do not guess GSTIN, state, or opening balance.**

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
            <PARENT>Sundry Creditors</PARENT><!-- or Sundry Debtors -->
            <TAXTYPE>Others</TAXTYPE>
            <GSTREGISTRATIONTYPE>Regular</GSTREGISTRATIONTYPE>
            <PARTYGSTIN>PARTY_GSTIN</PARTYGSTIN>
            <COUNTRYOFRESIDENCE>India</COUNTRYOFRESIDENCE>
            <LEDGERCOUNTRYISDCODE>+91</LEDGERCOUNTRYISDCODE>
            <ISBILLWISEON>No</ISBILLWISEON>
            <ISCOSTCENTRESON>No</ISCOSTCENTRESON>
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

            <CONTACTDETAILS.LIST>
              <NAME>Primary Mobile No.</NAME>
              <COUNTRYISDCODE>+91</COUNTRYISDCODE>
              <ISDEFAULTWHATSAPPNUM>Yes</ISDEFAULTWHATSAPPNUM>
            </CONTACTDETAILS.LIST>

          </LEDGER>
        </TALLYMESSAGE>
      </REQUESTDATA>
    </IMPORTDATA>
  </BODY>
</ENVELOPE>
```

> **Note**: For unregistered parties, omit `<PARTYGSTIN>` and set `<GSTREGISTRATIONTYPE>Unregistered</GSTREGISTRATIONTYPE>` in both the ledger header and `LEDGSTREGDETAILS.LIST`.

## Create Ledger (with address / contact fields)

Field availability depends on enabled features. Safest workflow: create a sample ledger in UI and export it to XML, then copy required tags.

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

            <MAILINGNAME.LIST TYPE="String">
              <MAILINGNAME>MAILING_NAME</MAILINGNAME>
            </MAILINGNAME.LIST>

            <ADDRESS.LIST TYPE="String">
              <ADDRESS>ADDRESS_LINE_1</ADDRESS>
              <ADDRESS>ADDRESS_LINE_2</ADDRESS>
              <ADDRESS>CITY</ADDRESS>
            </ADDRESS.LIST>

            <PINCODE>PIN</PINCODE>
            <COUNTRYNAME>India</COUNTRYNAME>
            <STATENAME>STATE_NAME</STATENAME>
            <EMAIL>EMAIL</EMAIL>
            <MOBILE>MOBILE</MOBILE>
            <LEDGERPHONE>PHONE</LEDGERPHONE>
          </LEDGER>
        </TALLYMESSAGE>
      </REQUESTDATA>
    </IMPORTDATA>
  </BODY>
</ENVELOPE>
```

## Ledger alteration (update existing ledger)

Set `ACTION="Alter"` and send the desired fields.

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
          <LEDGER NAME="LEDGER_NAME" ACTION="Alter">
            <NAME>LEDGER_NAME</NAME>
            <PARENT>NEW_PARENT_GROUP</PARENT>
          </LEDGER>
        </TALLYMESSAGE>
      </REQUESTDATA>
    </IMPORTDATA>
  </BODY>
</ENVELOPE>
```

## Ledger group reference (common CA mapping)

| Ledger Type | Parent Group |
|---|---|
| Customer (debtor) | `Sundry Debtors` |
| Vendor (creditor) | `Sundry Creditors` |
| Sales income | `Sales Accounts` |
| Purchases | `Purchase Accounts` |
| Direct costs | `Direct Expenses` |
| Indirect expenses | `Indirect Expenses` |
| Bank account | `Bank Accounts` |
| Cash | `Cash-in-Hand` |
| GST ledgers | `Duties & Taxes` |

## New Company Setup — Standard GST Ledgers

When a new company is created, run all seven blocks below (in order) to set up the minimum GST ledger set. Substitute `COMPANY_NAME` with the exact company name.

### 1. Input SGST @ 9 %

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
          <LEDGER NAME="Input Sgst @ 9 %" ACTION="Create">
            <NAME>Input Sgst @ 9 %</NAME>
            <PARENT>Duties &amp; Taxes</PARENT>
            <TAXTYPE>GST</TAXTYPE>
            <GSTDUTYHEAD>SGST/UTGST</GSTDUTYHEAD>
            <RATEOFTAXCALCULATION>9</RATEOFTAXCALCULATION>
            <ROUNDINGMETHOD>&#4; Not Applicable</ROUNDINGMETHOD>
            <ISGSTDUTYLEDGER>Yes</ISGSTDUTYLEDGER>
          </LEDGER>
        </TALLYMESSAGE>
      </REQUESTDATA>
    </IMPORTDATA>
  </BODY>
</ENVELOPE>
```

### 2. Input CGST @ 9 %

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
            <ROUNDINGMETHOD>&#4; Not Applicable</ROUNDINGMETHOD>
            <ISGSTDUTYLEDGER>Yes</ISGSTDUTYLEDGER>
          </LEDGER>
        </TALLYMESSAGE>
      </REQUESTDATA>
    </IMPORTDATA>
  </BODY>
</ENVELOPE>
```

### 3. Input IGST @ 18 %

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
          <LEDGER NAME="Input IGST @ 18 %" ACTION="Create">
            <NAME>Input IGST @ 18 %</NAME>
            <PARENT>Duties &amp; Taxes</PARENT>
            <TAXTYPE>GST</TAXTYPE>
            <GSTDUTYHEAD>IGST</GSTDUTYHEAD>
            <RATEOFTAXCALCULATION>18</RATEOFTAXCALCULATION>
            <ROUNDINGMETHOD>&#4; Not Applicable</ROUNDINGMETHOD>
            <ISGSTDUTYLEDGER>Yes</ISGSTDUTYLEDGER>
          </LEDGER>
        </TALLYMESSAGE>
      </REQUESTDATA>
    </IMPORTDATA>
  </BODY>
</ENVELOPE>
```

### 4. Purchase @ 18 % (with GST rate details)

Purchase ledger under `Purchase Accounts` with embedded GST rate splits (CGST 9% + SGST 9% + IGST 18%) for local taxable goods.

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
          <LEDGER NAME="Purchase @ 18 %" ACTION="Create">
            <NAME>Purchase @ 18 %</NAME>
            <PARENT>Purchase Accounts</PARENT>

            <GSTAPPLICABLE>&#4; Applicable</GSTAPPLICABLE>
            <GSTTYPEOFSUPPLY>Goods</GSTTYPEOFSUPPLY>
            <TAXTYPE>Others</TAXTYPE>
            <VATAPPLICABLE>&#4; Applicable</VATAPPLICABLE>

            <ISBILLWISEON>No</ISBILLWISEON>
            <ISCOSTCENTRESON>Yes</ISCOSTCENTRESON>
            <ISREVENUE>Yes</ISREVENUE>
            <ISDEEMEDPOSITIVE>Yes</ISDEEMEDPOSITIVE>

            <GSTDETAILS.LIST>
              <APPLICABLEFROM>20170701</APPLICABLEFROM>
              <TAXABILITY>Taxable</TAXABILITY>
              <GSTNATUREOFTRANSACTION>Local Purchase - Taxable</GSTNATUREOFTRANSACTION>
              <SRCOFGSTDETAILS>Specify Details Here</SRCOFGSTDETAILS>
              <GSTTYPEOFSUPPLY>Goods</GSTTYPEOFSUPPLY>

              <STATEWISEDETAILS.LIST>
                <STATENAME>&#4; Any</STATENAME>

                <RATEDETAILS.LIST>
                  <GSTRATEDUTYHEAD>CGST</GSTRATEDUTYHEAD>
                  <GSTRATEVALUATIONTYPE>Based on Value</GSTRATEVALUATIONTYPE>
                  <GSTRATE>9</GSTRATE>
                  <GSTRATEPERUNIT>0</GSTRATEPERUNIT>
                </RATEDETAILS.LIST>

                <RATEDETAILS.LIST>
                  <GSTRATEDUTYHEAD>SGST/UTGST</GSTRATEDUTYHEAD>
                  <GSTRATEVALUATIONTYPE>Based on Value</GSTRATEVALUATIONTYPE>
                  <GSTRATE>9</GSTRATE>
                  <GSTRATEPERUNIT>0</GSTRATEPERUNIT>
                </RATEDETAILS.LIST>

                <RATEDETAILS.LIST>
                  <GSTRATEDUTYHEAD>IGST</GSTRATEDUTYHEAD>
                  <GSTRATEVALUATIONTYPE>Based on Value</GSTRATEVALUATIONTYPE>
                  <GSTRATE>18</GSTRATE>
                  <GSTRATEPERUNIT>0</GSTRATEPERUNIT>
                </RATEDETAILS.LIST>

              </STATEWISEDETAILS.LIST>
            </GSTDETAILS.LIST>

            <HSNDETAILS.LIST>
              <APPLICABLEFROM>20210401</APPLICABLEFROM>
              <HSNCODE></HSNCODE>
              <SRCOFHSNDETAILS>As per Company/Group</SRCOFHSNDETAILS>
            </HSNDETAILS.LIST>

            <LANGUAGENAME.LIST>
              <NAME.LIST TYPE="String">
                <NAME>Purchase @ 18 %</NAME>
                <NAME>18</NAME>
              </NAME.LIST>
              <LANGUAGEID>1033</LANGUAGEID>
            </LANGUAGENAME.LIST>

          </LEDGER>
        </TALLYMESSAGE>
      </REQUESTDATA>
    </IMPORTDATA>
  </BODY>
</ENVELOPE>
```

> **Note**: Adjust the rate (9 %, 5 %, 12 %, 28 %, etc.) and nature of transaction (e.g., `Interstate Purchase - Taxable`) to match the company's actual tax slabs and supply type.

### 5. Round Off

Used to absorb invoice rounding differences. Place this in every new company setup.

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
          <LEDGER NAME="Round Off" ACTION="Create">
            <NAME>Round Off</NAME>
            <PARENT>Indirect Expenses</PARENT>
            <TAXTYPE>Others</TAXTYPE>
            <TDSAPPLICABLE>&#4; Not Applicable</TDSAPPLICABLE>
            <GSTAPPLICABLE>&#4; Not Applicable</GSTAPPLICABLE>
            <VATAPPLICABLE>&#4; Not Applicable</VATAPPLICABLE>
            <VATDEALERNATURE>Invoice Rounding</VATDEALERNATURE>
            <ROUNDINGMETHOD>Normal Rounding</ROUNDINGMETHOD>
            <ROUNDINGLIMIT>1</ROUNDINGLIMIT>
            <ISBILLWISEON>No</ISBILLWISEON>
            <ISCOSTCENTRESON>Yes</ISCOSTCENTRESON>
            <ISREVENUE>Yes</ISREVENUE>
            <ISDEEMEDPOSITIVE>No</ISDEEMEDPOSITIVE>
            <LANGUAGENAME.LIST>
              <NAME.LIST TYPE="String">
                <NAME>Round Off</NAME>
                <NAME>3</NAME>
              </NAME.LIST>
              <LANGUAGEID>1033</LANGUAGEID>
            </LANGUAGENAME.LIST>
          </LEDGER>
        </TALLYMESSAGE>
      </REQUESTDATA>
    </IMPORTDATA>
  </BODY>
</ENVELOPE>
```

### 6. Output SGST @ 9 %

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
          <LEDGER NAME="Output Sgst @ 9 %" ACTION="Create">
            <NAME>Output Sgst @ 9 %</NAME>
            <PARENT>Duties &amp; Taxes</PARENT>
            <TAXTYPE>GST</TAXTYPE>
            <GSTDUTYHEAD>SGST/UTGST</GSTDUTYHEAD>
            <RATEOFTAXCALCULATION>9</RATEOFTAXCALCULATION>
            <ROUNDINGMETHOD>&#4; Not Applicable</ROUNDINGMETHOD>
            <ISGSTDUTYLEDGER>Yes</ISGSTDUTYLEDGER>
          </LEDGER>
        </TALLYMESSAGE>
      </REQUESTDATA>
    </IMPORTDATA>
  </BODY>
</ENVELOPE>
```

### 7. Output CGST @ 9 %

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
          <LEDGER NAME="Output Cgst @ 9 %" ACTION="Create">
            <NAME>Output Cgst @ 9 %</NAME>
            <PARENT>Duties &amp; Taxes</PARENT>
            <TAXTYPE>GST</TAXTYPE>
            <GSTDUTYHEAD>CGST</GSTDUTYHEAD>
            <RATEOFTAXCALCULATION>9</RATEOFTAXCALCULATION>
            <ROUNDINGMETHOD>&#4; Not Applicable</ROUNDINGMETHOD>
            <ISGSTDUTYLEDGER>Yes</ISGSTDUTYLEDGER>
          </LEDGER>
        </TALLYMESSAGE>
      </REQUESTDATA>
    </IMPORTDATA>
  </BODY>
</ENVELOPE>
```

## Check if a ledger exists (export list and search)

Use `List of Accounts` report to fetch masters in the company and confirm existence.

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

Then search the response for `<NAME>LEDGER_NAME</NAME>`.

