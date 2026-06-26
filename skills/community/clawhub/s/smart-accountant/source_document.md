# source_document.md
# Skill Knowledge File: Source Document Foundations
# Purpose:
# Teach an Accountant Agent that accounting starts from evidence.
# Every transaction should originate from a source document,
# which drives voucher selection, journal entry creation,
# and ledger posting.

---

# 1. CORE PRINCIPLE

Primary Rule:

Document first.
Entry second.

No accounting entry should normally exist without supporting evidence.

A Source Document is the original proof that a business event occurred.

Source documents trigger transactions.

Transactions trigger journal entries.

Journal entries post into ledgers.

Flow:

Source Document
→ Voucher Type
→ Journal Entry
→ Ledger Posting

---

# 2. WHAT A SOURCE DOCUMENT DOES

Every source document serves three purposes:

1. Evidence
Proof transaction occurred.

2. Trigger
Creates accounting event.

3. Control
Supports validation, audit, and verification.

---

# 3. SOURCE DOCUMENT TYPES

Use these core document types only.

--------------------------------
A. Sales Invoice
--------------------------------

Purpose:
Proof goods/services sold.

Usually triggers:
SE Sales Entry

Typical ledgers:
- Customer Ledger or Cash Ledger
- Sales Ledger

Examples user may say:
- I sold goods.
- Made invoice for customer.
- Customer bought products.

Possible journal:

Credit Sale

Customer Dr
 To Sales

Cash Sale

Cash Dr
 To Sales

---

--------------------------------
B. Purchase Invoice
--------------------------------

Purpose:
Proof goods/services purchased.

Usually triggers:
PE Purchase Entry

Typical ledgers:
- Inventory/Purchase Ledger
- Vendor Ledger

Examples:
- Bought material from supplier.
- Received vendor bill.
- Purchased stock on credit.

Typical journal:

Inventory Dr
 To Vendor

---

--------------------------------
C. Receipt
--------------------------------

Purpose:
Proof money received.

Usually triggers:
CR or BR

Types:
Cash receipt
Bank receipt

Typical ledgers:
- Cash or Bank
- Related ledger

Examples:
- Customer paid us.
- Received advance.
- Payment received.

Example journal:

Cash Dr
 To Customer

---

--------------------------------
D. Payment Voucher
--------------------------------

Purpose:
Proof payment made.

Usually triggers:
CP or BP

Types:
Cash payment
Bank payment

Typical ledgers:
- Expense or Payable
- Cash or Bank

Examples:
- Paid supplier.
- Paid rent.
- Bank transfer made.

Example:

Vendor Dr
 To Bank

---

--------------------------------
E. Credit Note / Debit Note
--------------------------------

Purpose:
Document reductions, returns or adjustments.

May trigger:
SR
PR
or JE in exceptions

Examples:
- Customer returned goods.
- Returned goods to supplier.
- Price adjustment.

---

--------------------------------
F. Bank Statement
--------------------------------

Purpose:
External evidence from bank.

Can support:
BR
BP
CN
JE in bank charges/interest cases

Examples:
- Bank charged fees.
- Interest credited.
- Transfer reflected.

Important:
Bank statement is supporting evidence,
not itself a voucher.

---

# 4. SOURCE DOCUMENT METADATA

Capture this information when available:

Document Type
Document Number
Date
Related Ledger(s)
Amount
Remarks

Example:

Document Type:
Purchase Invoice

Document Number:
PI-1034

Date:
2026-04-29

Related Ledgers:
Inventory
Vendor Payable

Amount:
50000

Remarks:
Raw material purchase.

---

# 5. RELATED LEDGERS RULE

Do not use "counterparty" concept.

Use Related Ledger(s).

Everything affected is represented through ledgers.

Examples:

Sales Invoice:
Customer Ledger
Sales Ledger

Payment Voucher:
Vendor Ledger
Bank Ledger

One document may impact multiple ledgers.

---

# 6. SOURCE DOCUMENT VS VOUCHER

Important distinction:

Source Document
is evidence.

Voucher Type
is transaction classification.

Never confuse them.

Example:

Sales Invoice
(Source Document)

SE
(Voucher Type)

They are not the same.

---

# 7. DOCUMENT TO VOUCHER MAPPING

Default mapping:

Sales Invoice
→ SE

Purchase Invoice
→ PE

Receipt
→ CR or BR

Payment Voucher
→ CP or BP

Credit/Debit Note
→ PR or SR

Bank Statement
→ BR / BP / CN / JE depending event

---

# 8. JE SPECIAL RULE

General Journal Entry (JE)
is exception voucher.

Use specialized vouchers first.

Use JE only when no dedicated voucher fits.

Allowed JE scenarios:

- Depreciation
- Accruals
- Prepaids
- Provisions
- Rectification entries
- Reclassifications
- Drawings/Owner adjustments
- Closing adjustments

Rule:

Operational events
→ specialized vouchers

Accounting adjustments
→ JE

JE should be treated as restricted exception.

---

# 9. NATURAL LANGUAGE INTERPRETATION

Users may describe documents informally.

Examples:

"I have supplier bill"
→ Purchase Invoice

"Customer paid cash"
→ Receipt

"Paid vendor from bank"
→ Payment Voucher

Interpret business intent.

If document details missing,
ask for clarification.

---

# 10. VALIDATION RULES

For each document verify:

- Document exists
- Document type identified
- Related ledgers identified
- Amount matches entry
- Voucher type matches document
- Date valid
- Duplicate document number not found

Flag exceptions if mismatch.

---

# 11. MISSING DOCUMENT RULE

If no source document exists:

Ask:
What evidence supports this transaction?

Do not blindly post unsupported routine entries.

Exception:
Allowed JE adjustment scenarios may arise without external documents.

---

# 12. AGENT OPERATING LOOP

When receiving transaction request:

Identify source document
→ identify related ledgers
→ determine voucher type
→ generate journal entry
→ validate against document
→ post to ledgers

Do not skip sequence.

---

# 13. PRINCIPLES

Document creates transaction.

Transaction creates journal.

Journal creates ledger posting.

Evidence precedes accounting.

---

# 14. SCOPE LIMIT

This file covers:
- Source documents
- Document-voucher relationship
- Evidence validation
- JE exception routing

Does not cover:
- Full journal mechanics
- Ledger posting details
- Reporting

See:
journal_entry.md
general_ledger.md

---
End of source_document.md
