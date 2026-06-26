# Inventory (Stock Groups / Items / UOM) + Item Invoices

This file covers inventory masters and itemized voucher patterns for trading/manufacturing clients.

## Conventions

- Inventory masters also use `REPORTNAME=All Masters`.
- For item invoices, prefer **Invoice Voucher View** and include `ALLINVENTORYENTRIES.LIST`.
- If a tag/value is unclear, create one sample in Tally UI and export the voucher/master to XML; then replicate.

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
          <STOCKGROUP NAME="Electronics" ACTION="Create">
            <NAME>Electronics</NAME>
          </STOCKGROUP>
        </TALLYMESSAGE>
      </REQUESTDATA>
    </IMPORTDATA>
  </BODY>
</ENVELOPE>
```

## Create Unit of Measure (UOM) — simple

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
          <UNIT NAME="Pcs" ACTION="Create">
            <NAME>Pcs</NAME>
            <ISSIMPLEUNIT>Yes</ISSIMPLEUNIT>
            <ORIGINALNAME>Pieces</ORIGINALNAME>
            <DECIMALPLACES>0</DECIMALPLACES>
          </UNIT>
        </TALLYMESSAGE>
      </REQUESTDATA>
    </IMPORTDATA>
  </BODY>
</ENVELOPE>
```

## Create Stock Item (minimal)

UOM is commonly required.

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
            <BASEUNITS>UOM_NAME</BASEUNITS>
          </STOCKITEM>
        </TALLYMESSAGE>
      </REQUESTDATA>
    </IMPORTDATA>
  </BODY>
</ENVELOPE>
```

## Create Godown / Location

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
          <GODOWN NAME="Factory" ACTION="Create">
            <NAME>Factory</NAME>
          </GODOWN>
        </TALLYMESSAGE>
      </REQUESTDATA>
    </IMPORTDATA>
  </BODY>
</ENVELOPE>
```

## Sales (Item Invoice) — inventory entries

This is a template for an item invoice with one item line. Expand by repeating `ALLINVENTORYENTRIES.LIST` blocks.

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
            <GUID>UNIQUE_GUID</GUID>
            <DATE>YYYYMMDD</DATE>
            <VOUCHERTYPENAME>Sales</VOUCHERTYPENAME>
            <VOUCHERNUMBER>INVOICE_NO</VOUCHERNUMBER>
            <ISINVOICE>Yes</ISINVOICE>
            <PERSISTEDVIEW>Invoice Voucher View</PERSISTEDVIEW>
            <PARTYLEDGERNAME>CUSTOMER_LEDGER</PARTYLEDGERNAME>

            <!-- Party ledger -->
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

            <!-- Item line -->
            <ALLINVENTORYENTRIES.LIST>
              <STOCKITEMNAME>ITEM_NAME</STOCKITEMNAME>
              <ISDEEMEDPOSITIVE>No</ISDEEMEDPOSITIVE>
              <ACTUALQTY>1 Pcs</ACTUALQTY>
              <BILLEDQTY>1 Pcs</BILLEDQTY>
              <RATE>1000.00/Pcs</RATE>
              <AMOUNT>1000.00</AMOUNT>

              <BATCHALLOCATIONS.LIST>
                <GODOWNNAME>Main Location</GODOWNNAME>
                <BATCHNAME>Primary Batch</BATCHNAME>
                <AMOUNT>1000.00</AMOUNT>
                <ACTUALQTY>1 Pcs</ACTUALQTY>
                <BILLEDQTY>1 Pcs</BILLEDQTY>
              </BATCHALLOCATIONS.LIST>

              <ACCOUNTINGALLOCATIONS.LIST>
                <LEDGERNAME>SALES_LEDGER</LEDGERNAME>
                <ISDEEMEDPOSITIVE>No</ISDEEMEDPOSITIVE>
                <AMOUNT>1000.00</AMOUNT>
              </ACCOUNTINGALLOCATIONS.LIST>
            </ALLINVENTORYENTRIES.LIST>
          </VOUCHER>
        </TALLYMESSAGE>
      </REQUESTDATA>
    </IMPORTDATA>
  </BODY>
</ENVELOPE>
```

## Notes

- If godowns/batches are not enabled, `GODOWNNAME` is typically `Main Location` and `BATCHNAME` is `Primary Batch`.
- For services-only invoices, prefer accounting-only sales voucher templates (see `reference/vouchers.md`).

