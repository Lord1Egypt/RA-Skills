# general_ledger.md
# Skill Knowledge File: General Ledger Foundations
# Purpose:
# Teach an Accountant Agent how ledgers are structured,
# how journal entries post into ledgers,
# how balances accumulate,
# and how ledger groups organize postable ledgers.

---

# 1. CORE DEFINITIONS

## Ledger Group

Definition:
A Ledger Group is a classification folder used to organize ledgers.

Examples:
- Assets
- Liabilities
- Equity
- Income
- Expenses

Nested examples:
- Current Assets
- Bank Accounts
- Sundry Creditors

Rules:
- Ledger Groups can contain child groups.
- Ledger Groups can contain Ledgers.
- Ledger Groups do not accept postings.
- Ledger Groups only organize and aggregate.

Hard Rule:

Postings are never made to Ledger Groups.

---

## Ledger

Definition:
A Ledger is a postable account where journal entries are recorded.

Examples:
- Cash
- Bank
- Inventory
- Vendor Payable
- Sales
- Capital
- Drawings

Rules:
- Entries post only to Ledgers.
- Ledgers maintain balances.
- Ledgers can be debited or credited.
- Opening balances belong at Ledger level only.

Hard Rule:

Transactions happen only in Ledgers.

---

# 2. HIERARCHY

Chart of Accounts
  -> Ledger Groups
      -> Ledgers

Example:

Assets
  Current Assets
      Cash
      Bank
      Inventory

Liabilities
  Creditors
      Vendor Payable

---

# 3. RELATIONSHIP

Accounting flow:

Business Event
→ Journal Entry
→ Ledger Posting
→ Running Balances
→ Trial Balance

Journal records events chronologically.

Ledger groups postings account-wise.

---

# 4. LEDGER FORMAT

Use running balance format:

| Date | Voucher | Particulars | Dr | Cr | Balance |

Balance should follow normal account nature.

For Assets/Expenses:
normal balance generally debit.

For Liabilities/Equity/Income:
normal balance generally credit.

---

# 5. POSTING RULE

Every journal entry posts to each impacted ledger separately.

One journal entry creates at least two ledger postings.

Example:

Journal:

Cash Dr 100000
 To Capital 100000

Posts to:

Cash Ledger
Capital Ledger

separately.

---

# 6. PREVIOUS BUSINESS CYCLE EXAMPLES

Using previous journal_entry.md scenarios.

==================================================
CASE 1
Owner invests capital 100000
==================================================

Journal:

Cash Dr 100000
 To Capital 100000

--------------------------------
Cash Ledger
--------------------------------

| Date | Voucher | Particulars | Dr | Cr | Balance |
|------|---------|-------------|----|----|---------|
|1 Jan | OE      | Capital     |100000| |100000 Dr|

--------------------------------
Capital Ledger
--------------------------------

| Date | Voucher | Particulars | Dr | Cr | Balance |
|------|---------|-------------|----|----|---------|
|1 Jan | OE      | Cash        | |100000|100000 Cr|

---

==================================================
CASE 2
Inventory purchased on credit 50000
==================================================

Journal:

Inventory Dr 50000
 To Vendor Payable 50000

--------------------------------
Inventory Ledger
--------------------------------

| Date |Voucher|Particulars|Dr|Cr|Balance|
|-----|------|-----------|--|--|-------|
|2 Jan|PE|Vendor Payable|50000||50000 Dr|

--------------------------------
Vendor Payable Ledger
--------------------------------

|Date|Voucher|Particulars|Dr|Cr|Balance|
|----|------|-----------|--|--|-------|
|2 Jan|PE|Inventory||50000|50000 Cr|

---

==================================================
CASE 3
Cash sale 70000
==================================================

Journal:

Cash Dr 70000
 To Sales 70000

--------------------------------
Cash Ledger
--------------------------------

Opening from Case 1:
100000 Dr

|Date|Voucher|Particulars|Dr|Cr|Balance|
|----|------|-----------|--|--|-------|
|1 Jan|OE|Capital|100000||100000 Dr|
|3 Jan|SE|Sales|70000||170000 Dr|

--------------------------------
Sales Ledger
--------------------------------

|Date|Voucher|Particulars|Dr|Cr|Balance|
|----|------|-----------|--|--|-------|
|3 Jan|SE|Cash||70000|70000 Cr|

---

==================================================
CASE 4
Profit generated
==================================================

Profit:
Sales 70000
Cost 50000
Profit 20000

Optional transfer:

Profit & Loss Dr 20000
 To Retained Earnings 20000

--------------------------------
Retained Earnings Ledger
--------------------------------

|Date|Voucher|Particulars|Dr|Cr|Balance|
|----|------|-----------|--|--|-------|
|4 Jan|JE|Profit Transfer||20000|20000 Cr|

Note:
Profit often emerges from balances and may not require separate daily ledger posting.

---

==================================================
CASE 5
Supplier paid through bank 50000
==================================================

Journal:

Vendor Payable Dr 50000
 To Bank 50000

--------------------------------
Vendor Payable Ledger
--------------------------------

|Date|Voucher|Particulars|Dr|Cr|Balance|
|----|------|-----------|--|--|-------|
|2 Jan|PE|Inventory||50000|50000 Cr|
|5 Jan|BP|Bank|50000||0|

Vendor payable settled.

--------------------------------
Bank Ledger
--------------------------------

|Date|Voucher|Particulars|Dr|Cr|Balance|
|----|------|-----------|--|--|-------|
|5 Jan|BP|Vendor Payable||50000|50000 Cr*

*Assumes no prior funding in bank.
Actual running balance depends on prior entries.

---

==================================================
CASE 6
Owner withdraws profit 20000
==================================================

Journal:

Drawings Dr 20000
 To Cash 20000

--------------------------------
Drawings Ledger
--------------------------------

|Date|Voucher|Particulars|Dr|Cr|Balance|
|----|------|-----------|--|--|-------|
|6 Jan|JE|Cash|20000||20000 Dr|

--------------------------------
Cash Ledger
--------------------------------

Prior balance:
170000 Dr

|Date|Voucher|Particulars|Dr|Cr|Balance|
|----|------|-----------|--|--|-------|
|1 Jan|OE|Capital|100000||100000 Dr|
|3 Jan|SE|Sales|70000||170000 Dr|
|6 Jan|JE|Drawings||20000|150000 Dr|

---

# 7. AGENT POSTING LOGIC

For each journal entry:

For every debit line:
post debit into that ledger.

For every credit line:
post credit into that ledger.

Update running balance.

Never post to ledger groups.

---

# 8. LEDGER OPENING RULE

When user says:

"Open Cash ledger"

Return only transactions posted to Cash ledger.

Do not show unrelated ledger entries.

Support separate viewing per ledger.

Examples:
- Open Bank ledger
- Show Vendor ledger
- Show Sales ledger

---

# 9. VALIDATION RULES

Validate:

- Entries post only to ledgers
- Ledger groups cannot receive postings
- Every journal affects at least two ledgers
- Running balances update after every posting
- Ledger balance must reconcile with journal postings

Reject invalid posting.

---

# 10. LEDGER OBJECT MODEL

Ledger Group:
Name
Parent Group
Postable = No

Ledger:
Name
Parent Group
Account Type
Normal Balance
Opening Balance
Running Balance
Postable = Yes

---

# 11. PRINCIPLE

Ledger Groups classify.

Ledgers transact.

Journal records.

Ledger accumulates.

Trial balance summarizes.

---

# 12. SCOPE LIMIT

This file covers:
- Ledger groups
- Ledgers
- Posting logic
- Running balances

Not covered:
- Trial balance
- Reconciliation
- Financial statements

---
End of general_ledger.md
