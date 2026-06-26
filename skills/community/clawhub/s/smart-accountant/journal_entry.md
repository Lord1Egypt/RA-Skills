# journal_entry.md
# Skill Knowledge File: Journal Entry Foundations
# Purpose:
# Teach an Accountant Agent how to interpret business events,
# classify impacted accounts, apply debit-credit logic,
# generate balanced journal entries,
# and translate natural language into accounting records.

---

# 1. CORE DEFINITION

A Journal Entry records a financial event in accounting.

Every valid journal entry must contain:

- Trigger (business event)
- Accounts impacted
- Debit logic
- Credit logic
- Narration
- Validation

Mandatory rule:

Total Debit = Total Credit

Never generate unbalanced entries.

---

# 2. JOURNAL ENTRY ANATOMY

For every transaction analyze in this order:

Step 1
Identify trigger.

Step 2
Identify impacted accounts.

Step 3
Classify accounts using COA:
- Asset
- Liability
- Equity
- Income
- Expense

Step 4
Apply debit/credit rules.

Step 5
Generate journal entry.

Step 6
Add narration.

Step 7
Validate balance.

---

# 3. VOUCHER TYPES

Use only these voucher types:

CR  Cash Receipt
BR  Bank Receipt

CP  Cash Payment
BP  Bank Payment

PE  Purchase Entry
SE  Sales Entry

PR  Purchase Return
SR  Sales Return

CN  Contra

JE  General Journal Entry

OE  Opening Entry

Rule:
Use specialized voucher first.
Use JE only as fallback.

---

# 4. OUTPUT FORMAT

Return entries in this structure:

Date:
Voucher Type:
Trigger:

Journal Entry:

| Ledger | Dr | Cr |
|--------|----|----|

Narration:

Validation:
Debit total:
Credit total:
Balanced: Yes/No

---

# 5. NATURAL LANGUAGE TO ACCOUNTING EXAMPLES

====================================================
CASE 1
Owner invests 1 lakh as capital
====================================================

Human may say:
- I started business with 1 lakh.
- I introduced capital.
- I put ₹100000 into business.

Trigger:
Owner introduced capital.

Voucher Type:
OE (or JE if not opening)

Accounts impacted:
Cash (Asset)
Capital (Equity)

Debit logic:
Cash increased.
Assets increase with debit.

Credit logic:
Capital increased.
Equity increases with credit.

Journal Entry:

Date: Transaction Date

| Ledger           | Dr      | Cr      |
|-----------------|---------|---------|
| Cash            |100000   |         |
| Owner Capital   |         |100000   |

Narration:
Being capital introduced by owner.

Validation:
Debit = 100000
Credit =100000
Balanced Yes

---

====================================================
CASE 2
Owner purchases inventory on credit
====================================================

Human may say:
- Bought stock from supplier on credit.
- Purchased inventory payable later.
- Vendor gave material on credit.

Trigger:
Credit purchase.

Voucher Type:
PE

Accounts impacted:
Inventory (Asset)
Accounts Payable / Vendor (Liability)

Debit logic:
Inventory increased.

Credit logic:
Liability to supplier created.

Sample Amount:
50000

Journal Entry:

| Ledger            | Dr     | Cr     |
|------------------|--------|--------|
| Inventory        |50000   |        |
| Vendor Payable   |        |50000   |

Narration:
Being inventory purchased on credit.

Validation:
Balanced Yes

Note:
If "receivable" was intended, correct term here is payable.
Supplier credit increases payable, not receivable.

---

====================================================
CASE 3
Customer purchases items and pays cash
====================================================

Human may say:
- Customer bought goods and paid cash.
- Cash sale made.
- Sold goods for cash.

Trigger:
Cash sale.

Voucher Type:
SE or CR depending system design.
Default use SE.

Sample selling price:
70000

Accounts impacted:
Cash (Asset)
Sales (Income)

Debit logic:
Cash increased.

Credit logic:
Sales income earned.

Journal Entry:

| Ledger | Dr    | Cr    |
|--------|------|-------|
| Cash   |70000 |       |
| Sales  |      |70000  |

Narration:
Being goods sold for cash.

Validation:
Balanced Yes

---

====================================================
CASE 4
Owner generates profit
====================================================

Important:
Profit is generally result of revenue-expense entries.
Profit is not usually separately "generated" by standalone journal.

Agent rule:
Do not create separate journal merely because profit exists,
unless closing profit to equity.

Derived Example:

Sales 70000
Inventory Cost 50000

Profit:
20000

Optional closing transfer:

Voucher:
JE

| Ledger          | Dr    | Cr    |
|----------------|-------|-------|
| Profit & Loss  |20000  |       |
| Retained Earnings |    |20000  |

Narration:
Being profit transferred to equity.

Validation:
Balanced Yes

Rule:
Profit usually emerges from transactions,
not from separate operational journal.

---

====================================================
CASE 5
Owner pays vendor from bank account
====================================================

Human may say:
- Paid supplier through bank.
- Cleared vendor bill.
- Paid creditor via bank.

Trigger:
Vendor payment.

Voucher Type:
BP

Accounts impacted:
Vendor Payable
Bank

Sample Amount:
50000

Debit logic:
Liability reduced.
Liabilities decrease with debit.

Credit logic:
Bank reduced.
Asset decreases with credit.

Journal Entry:

| Ledger          | Dr    | Cr    |
|----------------|-------|-------|
| Vendor Payable |50000  |       |
| Bank           |       |50000  |

Narration:
Being payment made to supplier through bank.

Validation:
Balanced Yes

---

====================================================
CASE 6
Owner takes profit home (drawings)
====================================================

Human may say:
- Owner withdrew profit.
- Took money for personal use.
- Drew cash from business.

Trigger:
Owner drawings.

Voucher Type:
JE or CP

Accounts impacted:
Drawings (contra equity)
Cash/Bank

Sample:
20000

Debit logic:
Drawings increase on debit.
Reduces owner equity.

Credit logic:
Cash decreases.

Journal Entry:

| Ledger   | Dr    | Cr    |
|---------|-------|-------|
| Drawings|20000  |       |
| Cash    |       |20000  |

Narration:
Being drawings withdrawn by owner.

Validation:
Balanced Yes

Important:
This reduces equity.
It does not directly reduce "original capital account" transaction;
it reduces owner interest via drawings.

---

# 6. TRANSACTION FLOW EXAMPLE
Full business lifecycle:

1 Capital introduced
2 Inventory purchased on credit
3 Goods sold for cash
4 Profit generated
5 Supplier paid
6 Drawings withdrawn

This represents a complete miniature business cycle.

Agent should understand transaction relationships,
not treat entries in isolation.

---

# 7. VALIDATION RULES

For every generated entry check:

- Debit total equals credit total
- Correct voucher selected
- Accounts exist in COA
- Account classifications valid
- Narration present
- Amounts positive
- No imbalance
- No duplicate posting

Reject entry if validation fails.

---

# 8. NATURAL LANGUAGE INTERPRETATION RULES

Users may speak informally.

Examples:

"Put money in business"
=> Capital introduction

"Bought stock on udhar"
=> Credit purchase

"Paid supplier"
=> Vendor payment

"Took money home"
=> Drawings

Interpret business intent, not literal wording.

---

# 9. AGENT OPERATING LOOP

Observe event
→ classify transaction
→ choose voucher
→ identify accounts
→ apply debit/credit logic
→ generate balanced journal
→ narrate
→ validate

Never skip sequence.

---

# 10. SCOPE LIMIT

This file covers:
- Journal entry fundamentals
- Voucher types
- Natural language to journal conversion
- Balanced posting logic

Not covered:
- Trial balance
- Financial statements
- Tax treatment
- Reconciliation

---
End of journal_entry.md
