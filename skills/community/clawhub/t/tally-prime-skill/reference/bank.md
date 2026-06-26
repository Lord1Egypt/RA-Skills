# Bank Statement Vouchers — TallyPrime XML Templates

Covers: Payment · Receipt · Contra

## Conventions

- Always set `SVCURRENTCOMPANY` and `GUID`.
- Dates as `YYYYMMDD`. Escape `&` → `&amp;`.
- All three voucher types use `OBJVIEW="Accounting Voucher View"` and `ALLLEDGERENTRIES.LIST`.
- Voucher totals must sum to zero.

## Bank statement → Tally mapping

Bank statements are from the **bank's perspective**. Post from the **business's books**:

| Bank statement | Business books | Voucher type |
|---|---|---|
| Credit (money in) | Bank account debited | **Receipt** |
| Debit (money out) | Bank account credited | **Payment** |
| Internal transfer | Fund moves between accounts | **Contra** |

| Transaction | Voucher | Debit | Credit |
|---|---|---|---|
| NEFT/RTGS/UPI credit from customer | Receipt | Bank | Customer ledger |
| NEFT/RTGS/UPI debit to supplier | Payment | Supplier/Expense | Bank |
| Cash deposit to bank | Contra | Bank | Cash |
| ATM / cash withdrawal | Contra | Cash | Bank |
| Bank A → Bank B transfer | Contra | Destination Bank | Source Bank |
| Interest credit | Receipt | Bank | Interest Income |
| Bank charges | Payment | Bank Charges | Bank |

---

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

            <!-- Bank / Cash — debit (money in) -->
            <ALLLEDGERENTRIES.LIST>
              <LEDGERNAME>BANK_OR_CASH_LEDGER</LEDGERNAME>
              <ISDEEMEDPOSITIVE>Yes</ISDEEMEDPOSITIVE>
              <AMOUNT>-AMOUNT</AMOUNT>
            </ALLLEDGERENTRIES.LIST>

            <!-- Customer — credit -->
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

---

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

            <!-- Payee (vendor / expense) — debit -->
            <ALLLEDGERENTRIES.LIST>
              <LEDGERNAME>VENDOR_OR_EXPENSE_LEDGER</LEDGERNAME>
              <ISPARTYLEDGER>Yes</ISPARTYLEDGER>
              <ISDEEMEDPOSITIVE>Yes</ISDEEMEDPOSITIVE>
              <AMOUNT>-AMOUNT</AMOUNT>
            </ALLLEDGERENTRIES.LIST>

            <!-- Bank / Cash — credit (money out) -->
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

---

## Contra (bank / cash transfers)

Debit the account that **receives** funds; credit the account that **gives** funds.

| Scenario | Debit (`TO_LEDGER`) | Credit (`FROM_LEDGER`) |
|---|---|---|
| Cash deposit to bank | Bank ledger | Cash ledger |
| ATM / cash withdrawal | Cash ledger | Bank ledger |
| Bank A → Bank B | Bank B ledger | Bank A ledger |

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

            <!-- Account receiving funds — debit -->
            <ALLLEDGERENTRIES.LIST>
              <LEDGERNAME>TO_LEDGER</LEDGERNAME>
              <ISDEEMEDPOSITIVE>Yes</ISDEEMEDPOSITIVE>
              <AMOUNT>-AMOUNT</AMOUNT>
            </ALLLEDGERENTRIES.LIST>

            <!-- Account giving funds — credit -->
            <ALLLEDGERENTRIES.LIST>
              <LEDGERNAME>FROM_LEDGER</LEDGERNAME>
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
