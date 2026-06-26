# report_manual.md
Version: 1.0
Purpose: AI-readable domain skill document for accounting reporting layer built on accountant-transaction-layer.

============================================================
SECTION 0 — OVERVIEW
============================================================

This manual defines the accounting reporting layer generated from the transaction layer.

Transaction Layer:
- Journal Entry (JE)
- Adjusting Entry (AE)
- Cash Receipt (CR)
- Bank Receipt (BR)
- Cash Payment (CP)
- Bank Payment (BP)

Flow:

Transactions
→ General Ledger
→ Control / Subsidiary Reports
→ Financial Statements
→ Management / Audit Reporting

Core 12 Reports:
1. Trial Balance
2. Profit & Loss
3. Balance Sheet
4. Cash Flow Statement
5. General Ledger
6. Accounts Receivable Aging
7. Accounts Payable Aging
8. Cash / Bank Book
9. Sales Register
10. Purchase Register
11. Bank Reconciliation
12. Audit / Rectification Report

For each report this manual defines:
- What it is
- How generated
- Why it matters
- When used
- Example layout
- Relation to other reports

============================================================
SECTION 1 — REPORT DEPENDENCY MAP
============================================================

Hierarchy:

Level 1 Source Reports
- General Ledger
- Cash Book
- Sales Register
- Purchase Register

Level 2 Control Reports
- AR Aging
- AP Aging
- Bank Reconciliation
- Rectification Report

Level 3 Financial Statements
- Trial Balance
- P&L
- Balance Sheet
- Cash Flow

Dependency Flow:

Vouchers
 ↓
General Ledger
 ↓
Trial Balance
 ├── Profit & Loss
 ├── Balance Sheet
 └── Cash Flow (with additional movement analysis)

============================================================
SECTION 2 — REPORT DEFINITIONS
============================================================

------------------------------------------------------------
1. TRIAL BALANCE
------------------------------------------------------------

WHAT
Summary of all account balances proving:

Total Debits = Total Credits

Bridge between ledger and financial statements.

HOW GENERATED
From all posted ledger balances:

Opening Balance
+ Debit Movements
- Credit Movements
= Closing Balance

Grouped by:
- Assets
- Liabilities
- Equity
- Income
- Expenses

WHY IT MATTERS
- Validates posting integrity
- Detects classification issues
- Basis for financial statements

WHEN USED
- Daily internal review
- Month close
- Year close
- Audit

EXAMPLE

TRIAL BALANCE
------------------------------------------------
Cash                   50,000
Bank                  120,000
Inventory              70,000
Rent Expense           10,000
Salary Expense         20,000

Sales                              220,000
Capital                             50,000
------------------------------------------------
Debit                270,000
Credit               270,000

RELATION
Feeds:
- P&L
- Balance Sheet
- Cash Flow

Built from:
- General Ledger

------------------------------------------------------------
2. PROFIT & LOSS
------------------------------------------------------------

WHAT
Measures profitability.

Net Profit = Revenue – Expenses

HOW GENERATED
Income and expense accounts extracted from Trial Balance.

WHY
Shows:
- Gross profit
- Net profit
- Operating performance

WHEN
- Monthly
- Quarterly
- Year-end

EXAMPLE

Sales Revenue        220,000
COGS                (140,000)
Gross Profit          80,000

Expenses
Rent                  10,000
Salary                20,000
Utilities              5,000

Net Profit            45,000

RELATION
Uses:
- Trial Balance

Feeds:
- Equity in Balance Sheet

------------------------------------------------------------
3. BALANCE SHEET
------------------------------------------------------------

WHAT
Financial position statement.

Assets = Liabilities + Equity

HOW GENERATED
From:
- Asset accounts
- Liability accounts
- Capital
- Current profit/loss

WHY
Shows:
- Net worth
- Liquidity
- Solvency

WHEN
- Monthly
- Year-end
- Audit
- Financing

EXAMPLE

Assets
Cash              50,000
Inventory         70,000
Receivables       30,000
Total Assets     150,000

Liabilities
Payables          40,000

Equity
Capital           90,000
Profit            20,000

Liab + Equity    150,000

RELATION
Uses:
- Trial Balance
- P&L

------------------------------------------------------------
4. CASH FLOW STATEMENT
------------------------------------------------------------

WHAT
Tracks cash movement.

Sections:
- Operating
- Investing
- Financing

HOW GENERATED
Using:
- Cash/Bank ledgers
- Balance sheet changes
- P&L adjustments

WHY
Profit != Cash

WHEN
- Monthly
- Cash planning
- Year-end

EXAMPLE

Operating Cash
Receipts         150,000
Payments         (90,000)

Net Operating     60,000

Investing        (20,000)

Financing         40,000

Net Increase      80,000

RELATION
Uses:
- Cash Book
- Balance Sheet
- P&L

------------------------------------------------------------
5. GENERAL LEDGER
------------------------------------------------------------

WHAT
Detailed account-wise transaction history.

HOW
Every voucher updates ledger.

Example:
Dr Rent
Cr Cash

WHY
Primary drill-down.

WHEN
Daily, audit, reconciliation.

EXAMPLE

BANK LEDGER
Date     Voucher  Dr      Cr    Balance
1-Apr    BR001   25,000         25,000
4-Apr    BP003           5,000  20,000

RELATION
Foundation for nearly all reports.

------------------------------------------------------------
6. AR AGING
------------------------------------------------------------

WHAT
Outstanding customer receivables by age.

HOW
Open invoices bucketed:
0-30
31-60
61-90
90+

WHY
Collection risk control.

WHEN
Weekly / Monthly

EXAMPLE

Customer    Current 30d 60d Total
ABC         10,000          10,000
XYZ          5,000 7,000    12,000

RELATION
Derived from:
- Sales Register
- Customer Ledger

------------------------------------------------------------
7. AP AGING
------------------------------------------------------------

WHAT
Supplier obligations by due age.

HOW
Supplier open balances bucketed.

WHY
Payment planning.

WHEN
Weekly / Monthly

EXAMPLE

Supplier   Current 30d Total
RawChem    8,000  2,000 10,000

------------------------------------------------------------
8. CASH/BANK BOOK
------------------------------------------------------------

WHAT
Chronological cash and bank movement book.

Generated from:
CR
BR
CP
BP

EXAMPLE

Date   Voucher Receipt Payment
1-Apr CR001   20,000
2-Apr CP004            5,000

------------------------------------------------------------
9. SALES REGISTER
------------------------------------------------------------

WHAT
List of all sales invoices.

EXAMPLE

Inv   Customer Amount Tax Total
S001  ABC      10,000 1800 11800

Feeds:
- Revenue
- AR
- Tax

------------------------------------------------------------
10. PURCHASE REGISTER
------------------------------------------------------------

WHAT
List of purchase invoices.

EXAMPLE

Bill Vendor Amount Tax Total
P001 ABC   12,000 2160 14160

Feeds:
- Expenses
- AP
- Inventory

------------------------------------------------------------
11. BANK RECONCILIATION
------------------------------------------------------------

WHAT
Book vs bank matching.

EXAMPLE

Book Balance           50,000
Add Transit             5,000
Less Outstanding       (3,000)
Adjusted               52,000

Statement Balance      52,000

------------------------------------------------------------
12. AUDIT / RECTIFICATION REPORT
------------------------------------------------------------

WHAT
Exception and correction activity.

EXAMPLE

Date Voucher Issue         Correction
5-Apr JE004 Wrong account  Reclass JE009

WHY
Internal control layer.

============================================================
SECTION 3 — LOSS TREATMENT RULE
============================================================

Loss does NOT become liability.

Loss reduces equity.

Correct:

Capital          500,000
Less Loss        (15,000)
Net Equity       485,000

Rule:
Profit increases equity.
Loss reduces equity.

============================================================
SECTION 4 — MAIN 4 REPORTS USING 6 TRANSACTION USE CASE
============================================================

Use Case Transactions

1 Capital Introduced
Dr Bank 500000
Cr Capital 500000

2 Inventory on Credit
Dr Inventory 120000
Cr Payables 120000

3 Cash Sale
Dr Cash 50000
Cr Sales 50000

4 Record Cost
Dr COGS 30000
Cr Inventory 30000

5 Rent Paid
Dr Rent 10000
Cr Cash 10000

6 Supplier Payment
Dr Payables 40000
Cr Bank 40000

------------------------------------------------------------
Derived Ledger Balances
------------------------------------------------------------

Bank 480000
Cash 40000
Inventory 90000
Payables 80000
Capital 500000
Sales 50000
COGS 30000
Rent 10000

------------------------------------------------------------
A. TRIAL BALANCE
------------------------------------------------------------

Bank          480000
Cash           40000
Inventory      90000
COGS           30000
Rent           10000

Payables                 80000
Capital                 500000
Sales                    50000

Debits 650000
Credits650000

------------------------------------------------------------
B. P&L
------------------------------------------------------------

Sales          50000
COGS          (30000)

Gross Profit    20000

Rent           (10000)

Net Profit      10000

------------------------------------------------------------
C. CASH FLOW
------------------------------------------------------------

Operating:
Customer Cash     50000
Rent            (10000)
Supplier Pay    (40000)

Operating Net         0

Financing:
Capital 500000

Net Increase 500000

------------------------------------------------------------
D. BALANCE SHEET
------------------------------------------------------------

Assets
Bank         480000
Cash          40000
Inventory     90000
Total        610000

Liabilities
Payables      80000

Equity
Capital      500000
Profit        10000
Total Equity 510000

Liab+Eq      610000

============================================================
SECTION 5 — REPORT PERSPECTIVES ON SAME ENTRY
============================================================

Example:
Pay supplier 40,000

Dr Payables
Cr Bank

Effects:

Trial Balance
- Bank down
- Payables down

P&L
- No effect

Cash Flow
- Operating outflow

Balance Sheet
- Asset down
- Liability down

One transaction.
Four report perspectives.

============================================================
SECTION 6 — FREQUENCY MATRIX
============================================================

Report                    Daily Month Year Audit
Trial Balance               Y     Y    Y    Y
P&L                         N     Y    Y    Y
Balance Sheet               N     Y    Y    Y
Cash Flow                   N     Y    Y    Y
General Ledger              Y     Y    Y    Y
AR Aging                    N     Y    Y    Y
AP Aging                    N     Y    Y    Y
Cash Book                   Y     Y    Y    Y
Sales Register              Y     Y    Y    Y
Purchase Register           Y     Y    Y    Y
Bank Reconciliation         N     Y    Y    Y
Rectification Report        Y     Y    Y    Y

============================================================
SECTION 7 — AI AGENT RULES
============================================================

Before producing any report:
1 Validate all vouchers posted.
2 Ensure trial balance balances.
3 Generate reports from ledger, not raw vouchers directly unless drill-down requested.
4 For loss:
- reduce equity
- never classify as liability.

Report drill-down order:
Financial Statement
→ Trial Balance line
→ Ledger
→ Voucher
→ Source Transaction

This preserves explainability.

END OF MANUAL
