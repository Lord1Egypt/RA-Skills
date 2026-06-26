# closing.md
Version: 1.0
Purpose: AI-readable closing process skill for periodic accounting close controls.

============================================================
SECTION 0 — PURPOSE
============================================================

This skill defines accounting closing procedures that the agent must
understand and enforce for:

1 Monthly Close
2 Quarterly Close
3 Financial Year-End Close

Core Principle:

Transactions record the period.
Closing certifies the period.

Closing is not merely generating reports.

Closing means:
- verify completeness
- reconcile balances
- post adjustments
- review financial integrity
- lock the period

============================================================
SECTION 1 — CLOSING FRAMEWORK
============================================================

Universal close framework:

1 Capture
2 Reconcile
3 Adjust
4 Review
5 Close / Lock

Expanded form:

Post
→ Reconcile
→ Adjust
→ Review
→ Report
→ Lock

Applies at:
- Month-end
- Quarter-end
- Year-end

============================================================
SECTION 2 — MONTH-END CLOSING PROCESS
============================================================

------------------------------------------------------------
STEP 1 — PERIOD CUT-OFF
------------------------------------------------------------

Define cut-off date.

All transactions belonging to the month
must be posted before close.

Example:
All April transactions recorded before April close.

Cut-off breaches must be flagged.

------------------------------------------------------------
STEP 2 — TRANSACTION COMPLETENESS
------------------------------------------------------------

Verify all postings completed:

Required checks:

- Sales invoices posted
- Purchase invoices posted
- Receipts posted
- Payments posted
- Journal entries posted
- Bank transactions recorded
- Source documents captured

No material pending transactions allowed.

------------------------------------------------------------
STEP 3 — RECONCILIATIONS
------------------------------------------------------------

Mandatory:

A Bank Reconciliation

Book balance
must agree to
reconciled bank balance.

------------------------------------------------------------

B Accounts Receivable Reconciliation

AR Control Account
=
Customer Subledger Total

------------------------------------------------------------

C Accounts Payable Reconciliation

AP Control Account
=
Supplier Subledger Total

------------------------------------------------------------

D Inventory Reconciliation

Inventory GL
=
Stock records / physical records

------------------------------------------------------------
STEP 4 — MONTH-END ADJUSTMENTS
------------------------------------------------------------

Post adjusting entries as needed.

Examples:

Accrued expenses

Dr Salary Expense
Cr Salary Payable

------------------------------------------------------------

Prepaid allocation

Dr Insurance Expense
Cr Prepaid Insurance

------------------------------------------------------------

Depreciation

Dr Depreciation Expense
Cr Accumulated Depreciation

------------------------------------------------------------

Other adjustments:
- accruals
- provisions
- amortization
- correcting adjustments

------------------------------------------------------------
STEP 5 — TRIAL BALANCE REVIEW
------------------------------------------------------------

Review for:

- unusual balances
- suspense balances
- abnormal movements
- margin reasonableness
- classification issues

Trial balance must balance.

------------------------------------------------------------
STEP 6 — REPORT GENERATION
------------------------------------------------------------

Issue:

- Trial Balance
- P&L
- Balance Sheet
- Cash Flow

------------------------------------------------------------
STEP 7 — PERIOD LOCK
------------------------------------------------------------

Lock period after close.

No backdated changes
without controlled override.

------------------------------------------------------------
MONTH-END CHECKLIST
------------------------------------------------------------

Required:

[ ] Transactions complete
[ ] Bank reconciled
[ ] AR reconciled
[ ] AP reconciled
[ ] Inventory reconciled
[ ] Adjustments posted
[ ] Depreciation booked
[ ] Trial balance reviewed
[ ] Reports issued
[ ] Month locked

All must pass before close.

============================================================
SECTION 3 — QUARTER-END CLOSE
============================================================

Quarter close includes everything in month-end close
plus deeper review controls.

------------------------------------------------------------
ADDITIONAL QUARTER PROCEDURES
------------------------------------------------------------

Analytical Review:
- compare prior quarter
- compare budget vs actual
- margin analysis
- ratio analysis

------------------------------------------------------------

Provision Review:
- doubtful debts
- inventory obsolescence
- contingencies

------------------------------------------------------------

Tax Reviews:
- indirect tax reconciliations
- withholding tax review
- advance tax estimation

------------------------------------------------------------

Management Reporting Pack:
- financial package
- variance explanations
- KPI review

------------------------------------------------------------
Quarter Close Focus
------------------------------------------------------------

Monthly close:
operational integrity

Quarter close:
analytical integrity

============================================================
SECTION 4 — YEAR-END CLOSE
============================================================

Year-end close is statutory close.

Includes everything above plus:

------------------------------------------------------------
STEP A — FINAL RECONCILIATIONS
------------------------------------------------------------

Complete full reconciliations:

- all banks
- customer confirmations
- supplier confirmations
- inventory counts
- fixed asset register

------------------------------------------------------------
STEP B — YEAR-END ADJUSTMENTS
------------------------------------------------------------

Post:

- accruals
- depreciation
- amortization
- provisions
- tax provisions
- valuation adjustments

------------------------------------------------------------
STEP C — TRUE CLOSING ENTRIES
------------------------------------------------------------

IMPORTANT:

Not every ledger gets closed.

Only temporary / nominal accounts close.

Temporary accounts:
- revenues
- expenses
- drawings if applicable

Permanent accounts do not close:
- assets
- liabilities
- equity

------------------------------------------------------------
Revenue Closing Example
------------------------------------------------------------

Dr Sales
Cr Profit and Loss

------------------------------------------------------------
Expense Closing Example
------------------------------------------------------------

Dr Profit and Loss
Cr Salary Expense
Cr Rent Expense

------------------------------------------------------------
Profit Transfer
------------------------------------------------------------

Profit:

Dr Profit and Loss
Cr Retained Earnings

Loss:

Dr Retained Earnings
Cr Profit and Loss

Loss reduces equity.
Loss does not become liability.

------------------------------------------------------------
Temporary Account Rule
------------------------------------------------------------

Temporary accounts close.
Permanent accounts carry forward.

This is mandatory accounting rule.

------------------------------------------------------------
STEP D — TAX PROVISION
------------------------------------------------------------

Dr Tax Expense
Cr Tax Payable

------------------------------------------------------------
STEP E — AUDIT PREPARATION
------------------------------------------------------------

Prepare:
- schedules
- support ledgers
- audit working papers
- reconciliations
- supporting evidence

------------------------------------------------------------
STEP F — FINAL STATEMENTS
------------------------------------------------------------

Issue:
- Final P&L
- Final Balance Sheet
- Final Cash Flow
- Notes and schedules

------------------------------------------------------------
STEP G — YEAR LOCK
------------------------------------------------------------

Close fiscal year.

Carry forward:
Assets
Liabilities
Equity balances

Revenue/expense reset.

============================================================
SECTION 5 — OPENING BALANCES VS CLOSING
============================================================

Monthly close does NOT normally create opening journal entries
for next month.

Balances carry forward automatically.

Monthly:
close period
carry balances

No monthly opening journal.

------------------------------------------------------------

Opening entries generally apply:
- initial books setup
- new fiscal year opening

------------------------------------------------------------
Accounting Cycle
------------------------------------------------------------

Opening balances
↓
Transactions
↓
Adjustments
↓
Closing entries
↓
New opening balances

============================================================
SECTION 6 — MONTH / QUARTER / YEAR COMPARISON
============================================================

Monthly:
- operational close

Quarterly:
- enhanced analytical close

Yearly:
- statutory close

------------------------------------------------------------

Activity                  M   Q   Y
Transaction completeness  Y   Y   Y
Reconciliations           Y   Y   Y
Adjustments               Y   Y   Y
Analytical review         L   H   H
Provisions                B   R   F
Tax review                B   M   F
Audit prep                N   L   H
Closing entries           N   N   Y
Period lock               Y   Y   Y

Legend
L Light
H Heavy
B Basic
R Review
F Full

============================================================
SECTION 7 — AGENT CLOSING HARD STOPS
============================================================

Agent must prohibit close if any exist:

Hard blocks:

- Trial balance mismatch
- Unreconciled bank
- Control account mismatch
- Suspense unresolved
- Material adjustments missing
- Pending exceptions unresolved

Close must fail.

Example:

STRICT ERROR
Period close prohibited.

Reasons:
- Bank unreconciled
- Suspense pending

Resolve before close.

============================================================
SECTION 8 — PERIOD LOCK RULES
============================================================

After close:
period should be locked.

Post-close postings:
not permitted without controlled override.

Backdated postings after close:
must trigger exception.

============================================================
SECTION 9 — CLOSE CHECKLIST MASTER
============================================================

Close may proceed only if:

[ ] Posting complete
[ ] Reconciliations complete
[ ] Adjustments complete
[ ] Trial balance reviewed
[ ] Reports generated
[ ] Exceptions cleared
[ ] Approval complete
[ ] Period lock executed

============================================================
SECTION 10 — CLOSE IS NOT JUST REPORTING
============================================================

Incorrect:
Run P&L = close complete

Correct:
Closing certifies books.

Reports are only one output of close.

============================================================
SECTION 11 — AGENT CLOSING PROTOCOL
============================================================

Agent close sequence:

Validate completeness
→ Reconcile
→ Adjust
→ Review
→ Generate reports
→ Run close checks
→ Lock period

No shortcuts.

============================================================
SECTION 12 — MASTER CLOSING RULE
============================================================

Closing cannot occur
until books are:

complete
reconciled
adjusted
reviewed
approved

Only then:
close and lock.

END OF FILE
