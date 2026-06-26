# Inventory Masters — Check & Create

Required when posting Item Invoice vouchers (Purchase or Sales). If a stock item, UOM, or godown referenced in a voucher does not exist in Tally, the import will fail with "Stock Item does not exist."

## Fetch stock item details (unit + HSN + GST rate)

Use this before PDF generation to auto-fill `unit`, `hsn-code`, and `gst-rate` without asking the user.

```xml
<?xml version="1.0" encoding="utf-8"?>
<ENVELOPE>
  <HEADER>
    <VERSION>1</VERSION>
    <TALLYREQUEST>Export</TALLYREQUEST>
    <TYPE>Data</TYPE>
    <ID>StockItemDetailReport</ID>
  </HEADER>
  <BODY>
    <DESC>
      <STATICVARIABLES>
        <SVEXPORTFORMAT>$$SysName:XML</SVEXPORTFORMAT>
        <SVCURRENTCOMPANY>COMPANY_NAME</SVCURRENTCOMPANY>
      </STATICVARIABLES>
      <TDL>
        <TDLMESSAGE>
          <REPORT NAME="StockItemDetailReport">
            <FORMS>StkDetailForm</FORMS>
          </REPORT>
          <FORM NAME="StkDetailForm">
            <PARTS>StkDetailPart</PARTS>
          </FORM>
          <PART NAME="StkDetailPart">
            <LINES>StkDetailLine</LINES>
            <REPEAT>StkDetailLine : StkItemColl</REPEAT>
            <SCROLL>Vertical</SCROLL>
          </PART>
          <LINE NAME="StkDetailLine">
            <FIELDS>FldName, FldBaseUnits, FldGSTRate</FIELDS>
          </LINE>
          <FIELD NAME="FldName">
            <SET>$Name</SET>
          </FIELD>
          <FIELD NAME="FldBaseUnits">
            <SET>$BaseUnits</SET>
          </FIELD>
          <FIELD NAME="FldGSTRate">
            <SET>$$FilteredValue:GSTRateDetails:GSTRate:GSTRateDutyHead:IGST</SET>
          </FIELD>
          <COLLECTION NAME="StkItemColl">
            <TYPE>Stock Item</TYPE>
            <FILTER>ByItemName</FILTER>
          </COLLECTION>
          <SYSTEM TYPE="Formulae" NAME="ByItemName">
            $Name = "ITEM_NAME"
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
| `unit` | `FldBaseUnits` | `Bag` |
| `gst-rate` | `FldGSTRate` (IGST rate = total GST %) | `28` |

**HSN code — parse from item name:** Items commonly follow the naming convention `{Name} {HSN} @ {Rate} %` (e.g., `PPC Cement 2523 @ 28 %`). Extract:
- HSN → digits immediately before ` @ ` in the item name
- GST rate → digits after `@ ` and before ` %` (use this if `FldGSTRate` is empty)
- Unit → last token of `DSPCLQTY` in Stock Summary (e.g., `-56943 Bag` → `Bag`)

If any field is still missing after the name parse, ask the user only for that specific field.

---

## Check if a stock item exists

Fetch `List of Accounts` (same query as in `reference/ledgers.md`) and search for `<NAME>ITEM_NAME</NAME>`. Alternatively, fetch the Stock Summary:

```xml
<?xml version="1.0" encoding="utf-8"?>
<ENVELOPE>
  <HEADER><TALLYREQUEST>Export Data</TALLYREQUEST></HEADER>
  <BODY>
    <EXPORTDATA>
      <REQUESTDESC>
        <REPORTNAME>Stock Summary</REPORTNAME>
        <STATICVARIABLES>
          <SVEXPORTFORMAT>$$SysName:XML</SVEXPORTFORMAT>
          <SVCURRENTCOMPANY>COMPANY_NAME</SVCURRENTCOMPANY>
        </STATICVARIABLES>
      </REQUESTDESC>
    </EXPORTDATA>
  </BODY>
</ENVELOPE>
```

If the item is absent, create in order: Stock Group → UOM → Stock Item.

## Create Stock Group

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
          <STOCKGROUP NAME="GROUP_NAME" ACTION="Create">
            <NAME>GROUP_NAME</NAME>
          </STOCKGROUP>
        </TALLYMESSAGE>
      </REQUESTDATA>
    </IMPORTDATA>
  </BODY>
</ENVELOPE>
```

## Create Unit of Measure (UOM)

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
          <UNIT NAME="UOM_SYMBOL" ACTION="Create">
            <NAME>UOM_SYMBOL</NAME>
            <ISSIMPLEUNIT>Yes</ISSIMPLEUNIT>
            <ORIGINALNAME>UOM_FULL_NAME</ORIGINALNAME>
            <DECIMALPLACES>0</DECIMALPLACES>
          </UNIT>
        </TALLYMESSAGE>
      </REQUESTDATA>
    </IMPORTDATA>
  </BODY>
</ENVELOPE>
```

Common symbols: `Pcs`, `Kg`, `Ltr`, `Box`, `Bag`, `Mtr`, `Nos`.

## Create Stock Item

UOM and Stock Group must exist first.

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
          <STOCKITEM NAME="ITEM_NAME" ACTION="Create">
            <NAME>ITEM_NAME</NAME>
            <PARENT>STOCK_GROUP_NAME</PARENT>
            <BASEUNITS>UOM_SYMBOL</BASEUNITS>
          </STOCKITEM>
        </TALLYMESSAGE>
      </REQUESTDATA>
    </IMPORTDATA>
  </BODY>
</ENVELOPE>
```

## Godown / batch defaults

If godowns/batches are **not** explicitly enabled in the company, use:

- `GODOWNNAME` → `Main Location`
- `BATCHNAME` → `Primary Batch`

If a custom godown is needed, create it first:

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
          <GODOWN NAME="GODOWN_NAME" ACTION="Create">
            <NAME>GODOWN_NAME</NAME>
          </GODOWN>
        </TALLYMESSAGE>
      </REQUESTDATA>
    </IMPORTDATA>
  </BODY>
</ENVELOPE>
```
