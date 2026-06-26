# transaction_language.md

## Purpose
This file defines natural language variations used by humans when referring to accounting transactions.
It helps the agent map user intent → correct voucher type.

---

# 1. SALES INVOICE (SE - Sales Entry)

## Keywords
sales invoice, customer invoice, tax invoice, sales bill, outward invoice, revenue invoice

## Examples
- Create a sales invoice for ₹25,000 to ABC Traders
- Raise an invoice for the goods sold yesterday
- Enter this customer bill as a sales entry
- Post an outward tax invoice for this sale
- Record invoice no SI-1045 for customer payment
- Make a sales bill for 100 bags supplied
- Book revenue against this invoice
- Pass a sales voucher for this order
- Generate an output invoice with GST
- Record a credit sale invoice

---

# 2. PURCHASE INVOICE (PE - Purchase Entry)

## Keywords
purchase bill, supplier invoice, vendor bill, input invoice, inward bill

## Examples
- Enter supplier invoice from Reliance Chemicals
- Record this purchase bill for raw materials
- Post a vendor invoice worth ₹48,000
- Make a purchase entry against invoice no 4567
- Book this inward invoice under purchases
- Record GST input purchase from this bill
- Pass purchase voucher for chemicals bought
- Enter vendor bill received on credit
- Post invoice received from supplier
- Add this bill into purchase register

---

# 3. CASH RECEIPT (CR)

## Keywords
cash received, cash collection, receipt voucher, money received

## Examples
- Record cash received from customer
- Pass a cash receipt for ₹15,000
- Enter receipt voucher for cash payment
- Book cash collection from debtor
- Record cash received toward dues
- Post customer cash payment
- Make CR voucher for rent received
- Enter money received in hand
- Record walk-in customer cash receipt
- Pass receipt entry for cash deposit

---

# 4. BANK RECEIPT (BR)

## Keywords
bank receipt, NEFT received, RTGS received, bank credit, transfer received

## Examples
- Record bank receipt from customer via NEFT
- Post amount received in bank
- Enter BR for ₹50,000 received by RTGS
- Book payment received through bank transfer
- Record customer payment credited in bank
- Pass receipt for cheque realized
- Enter UPI receipt in bank account
- Record wire transfer from client
- Book incoming bank payment
- Make bank receipt entry

---

# 5. CASH PAYMENT (CP)

## Keywords
cash paid, petty cash, cash expense, cash disbursement

## Examples
- Record cash paid for office expenses
- Pass cash payment for transport charges
- Enter petty cash payment of ₹2,000
- Book cash paid to supplier
- Record cash for labor wages
- Make CP voucher for electricity
- Post cash expense paid today
- Enter payment made in cash
- Record reimbursement from cash
- Pass cash settlement entry

---

# 6. BANK PAYMENT (BP)

## Keywords
bank payment, online payment, cheque payment, transfer made

## Examples
- Record bank payment to supplier by NEFT
- Pass BP voucher for vendor payment
- Enter online transfer for raw materials
- Book cheque issued to supplier
- Record bank payment of rent
- Make payment for utility bill via bank
- Post outgoing bank transfer
- Record UPI payment from account
- Enter wire payment to vendor
- Book supplier settlement through bank

---

# 7. SALES RETURN / CREDIT NOTE (SR)

## Keywords
credit note, sales return, customer return, credit memo

## Examples
- Issue credit note for returned goods
- Record sales return from customer
- Pass SR for damaged goods returned
- Enter customer return with adjustment
- Book credit note against invoice
- Reverse sale due to rejection
- Post return voucher
- Make credit memo for excess billing
- Record output return adjustment
- Pass sales return entry

---

# 8. PURCHASE RETURN / DEBIT NOTE (PR)

## Keywords
debit note, purchase return, supplier return

## Examples
- Record purchase return to supplier
- Raise debit note for defective material
- Pass PR voucher for goods returned
- Enter supplier return adjustment
- Book debit note against wrong supply
- Reverse purchase due to damage
- Record vendor return memo
- Post debit adjustment for shortage
- Make purchase return entry
- Pass debit note for rejected materials

---

# 9. CONTRA ENTRY (CN)

## Keywords
contra, cash to bank, bank to cash, internal transfer

## Examples
- Record cash deposited into bank
- Pass contra for bank withdrawal
- Transfer ₹20,000 from cash to bank
- Enter internal fund transfer
- Book cash withdrawn for expenses
- Make CN for bank transfer
- Record transfer between accounts
- Post ATM withdrawal entry
- Enter funds moved internally
- Pass internal transfer voucher

---

# 10. JOURNAL ENTRY (JE)

## Keywords
journal entry, adjustment entry, manual entry, accrual, provision

## Examples
- Pass journal entry for depreciation
- Record adjusting entry for expenses
- Make JE for salary provision
- Post manual journal for reclassification
- Enter adjustment for prepaid rent
- Book write-off entry
- Pass rectification entry
- Record month-end accrual
- Make provision for audit fees
- Post general journal adjustment

---

# 11. OPENING ENTRY (OE)

## Keywords
opening balance, opening entry, brought forward

## Examples
- Enter opening balances
- Pass opening entry for bank balance
- Record opening stock
- Create OE for debtor balances
- Book beginning balances
- Post opening capital
- Enter brought-forward balances
- Set up opening journal
- Record opening vendor balances
- Import opening trial balance

---

# 12. BANK STATEMENT DRIVEN ENTRIES (AUTO / MIXED)

## Keywords
bank reconciliation, statement entry, bank import

## Examples
- Reconcile bank statement transactions
- Record entries from bank statement
- Match this statement line
- Post bank charges from statement
- Book interest credited in bank
- Record cheque bounce
- Enter contra from bank deposit
- Pass journal for bank charges
- Record statement transactions
- Reconcile and create vouchers

---

# COMMON COLLOQUIAL PHRASES (IMPORTANT)

## Indian + Global Usage
- pass entry
- do voucher
- book this transaction
- post this bill
- make receipt
- adjust this
- reverse this entry
- knock off invoice
- settle payment
- journal karo
- contra maaro
- receipt book karo
- bill punch karo

---

# NOTES FOR AGENT

1. Always infer intent from action words:
   - "receive" → CR / BR
   - "pay" → CP / BP
   - "return" → SR / PR
   - "transfer" → CN
   - "adjust" → JE

2. If ambiguity exists:
   - Ask: cash or bank?
   - Ask: sale or purchase?

3. Prefer structured mapping:
   - Sales → SE / SR
   - Purchase → PE / PR
   - Money In → CR / BR
   - Money Out → CP / BP

4. Bank statement inputs may generate:
   - BR / BP / CN / JE depending on nature

---
