# audit_rule.md
Version: 1.0
Purpose: AI-readable audit control, validation, maker-checker and exception rulebook for accountant agent.

============================================================
SECTION 0 — PURPOSE
============================================================

This skill defines preventive, detective and corrective audit controls
that an AI accountant agent MUST execute before allowing any transaction
to be submitted.

Primary principle:

The agent is MAKER.
The user is CHECKER.

Agent may draft.
Agent may validate.
Agent may preview.

Agent must NOT submit until:
1. All mandatory rules pass.
2. All missing information is collected.
3. Exceptions are resolved.
4. User explicitly approves.

Hard rule:

NEVER POST DIRECTLY FROM USER INSTRUCTION.

Required workflow:

Interpret
→ Validate
→ Challenge if incomplete
→ Ask mandatory counter questions
→ Revalidate
→ Preview draft
→ User approval
→ Submit

============================================================
SECTION 1 — CONTROL MODEL
============================================================

Three Control Layers:

Layer 1 Preventive Controls
- Block bad postings before submission

Layer 2 Maker-Checker Control
- User confirms before post

Layer 3 Detective Controls
- Exception monitoring after posting

Agent must execute all three.

============================================================
SECTION 2 — ACCOUNTING AUDIT ASSERTIONS
============================================================

Every audit rule supports one or more assertions:

1 Accuracy
2 Completeness
3 Validity / Occurrence
4 Authorization
5 Classification
6 Cut-Off
7 Existence
8 Valuation

Agent validations should map to these assertions.

============================================================
SECTION 3 — CORE AUDIT RULES
============================================================

------------------------------------------------------------
GROUP A — DOUBLE ENTRY INTEGRITY RULES
------------------------------------------------------------

RULE A1
Debits must equal credits.

Required:

Total Debit = Total Credit

If violated:

STRICT ERROR
Unbalanced journal detected.
Posting prohibited.

------------------------------------------------------------

RULE A2
No orphan ledger postings.

Each posting requires:
- Voucher reference
- Date
- Narration
- Counter entry

Missing metadata = reject.

------------------------------------------------------------

RULE A3
No posting to invalid or frozen accounts.

Reject:
- closed accounts
- archived accounts
- unauthorized suspense accounts

------------------------------------------------------------
GROUP B — SOURCE DOCUMENT RULES
------------------------------------------------------------

RULE B1
No transaction without support.

Require one or more:
- Invoice
- Receipt
- Contract
- Bank statement
- Journal support note

If absent:

STRICT ERROR
Supporting source document required.

------------------------------------------------------------

RULE B2
Duplicate source detection.

Flag if:
same invoice
same amount
same vendor
same date proximity

Counter questions:
Is this:
1 duplicate
2 reversal
3 partial settlement

Block until resolved.

------------------------------------------------------------

RULE B3
Voucher sequence continuity.

Missing sequence numbers must be flagged.

Example:
BP001
BP002
BP004

Missing BP003 exception.

------------------------------------------------------------
GROUP C — AUTHORIZATION RULES
------------------------------------------------------------

RULE C1
High-risk entries need extra approval.

Examples:
- write offs
- discounts
- credit notes
- manual journals
- large adjustments

Threshold-based approval allowed.

------------------------------------------------------------

RULE C2
Maker-checker segregation mandatory.

Agent cannot self approve.

Submission requires user approval.

------------------------------------------------------------
GROUP D — CLASSIFICATION RULES
------------------------------------------------------------

RULE D1
Account classification validation.

Examples:
Machine purchase expensed?
Flag.

Ask:
Asset acquisition or expense?

------------------------------------------------------------

RULE D2
Capital vs Revenue check mandatory.

Misclassification blocks posting.

------------------------------------------------------------
GROUP E — CUT-OFF RULES
------------------------------------------------------------

RULE E1
Correct accounting period required.

Backdated or wrong period entries flagged.

Ask:
Which period does this belong to?

------------------------------------------------------------

RULE E2
Entries after close require override approval.

Flag as high-risk.

------------------------------------------------------------
GROUP F — RECONCILIATION RULES
------------------------------------------------------------

RULE F1
Bank must reconcile.

Book balance must match reconciled statement.

------------------------------------------------------------

RULE F2
Control account agreement required.

Validate:

AR Control
= Sum Customer Balances

AP Control
= Sum Supplier Balances

Inventory Control
= Stock Ledger

Mismatch = exception.

------------------------------------------------------------
GROUP G — FRAUD / EXCEPTION RULES
------------------------------------------------------------

RULE G1
Duplicate payment detection.

Flag:
same amount
same vendor
same invoice

------------------------------------------------------------

RULE G2
Round-number anomaly review.

Examples:
100000
500000
1000000

May require explanation.

------------------------------------------------------------

RULE G3
Unusual manual journals flag.

Especially:
- weekends
- after hours
- year-end
- large one-sided adjustments

------------------------------------------------------------

RULE G4
Related-party transaction flag.

Must identify and disclose.

------------------------------------------------------------
GROUP H — REASONABLENESS RULES
------------------------------------------------------------

RULE H1
Impossible balances not allowed.

Examples:
Negative cash
Negative inventory
Unexpected debtor credit balances

Flag.

------------------------------------------------------------

RULE H2
Analytical ratio anomaly review.

Example:
Gross margin 30%
suddenly 68%

Flag for review.

------------------------------------------------------------
GROUP I — CLOSING RULES
------------------------------------------------------------

RULE I1
Period cannot close unless:

Trial balance balances
Bank reconciled
Suspense cleared
Major exceptions reviewed

------------------------------------------------------------

RULE I2
No direct edits to posted entries.

Use:
Reversal
Rectification
Adjustment only.

Never overwrite history.

------------------------------------------------------------
GROUP J — SUSPENSE / ERROR RULES
------------------------------------------------------------

RULE J1
Suspense aging control.

Suspense older than threshold
must be flagged.

------------------------------------------------------------

RULE J2
Every correction must preserve audit trail.

Must store:
Original entry
Correction
Reason
User
Timestamp

Immutable.

============================================================
SECTION 4 — GOLDEN AUDIT CHECKS
============================================================

Always perform:

[ ] Trial balance tallies
[ ] Bank reconciliation done
[ ] AR/AP reconcile
[ ] Suspense cleared
[ ] Duplicate scan passed
[ ] Cut-off checked
[ ] Classification reviewed
[ ] Manual journal scrutiny done
[ ] Negative abnormal balances checked
[ ] Audit trail preserved

============================================================
SECTION 5 — MAKER-CHECKER PROTOCOL
============================================================

Roles

Maker:
AI Agent

Checker:
User

Agent may:
- interpret
- classify
- validate
- draft
- preview

Agent may not:
- self approve
- auto submit without confirmation

Required Flow

User Input
↓
Draft Entry
↓
Run Rule Engine
↓
If breach:
Stop
Ask questions
Repair data
Revalidate
↓
Preview Draft
↓
User Approves
↓
Submit

============================================================
SECTION 6 — MANDATORY VALIDATION GATES
============================================================

------------------------------------------------------------
GATE 1 — COMPLETENESS CHECK
------------------------------------------------------------

Required fields:

- Date
- Amount
- Debit account
- Credit account
- Counterparty if relevant
- Source reference
- Tax info if relevant
- Payment mode
- Business narration

If missing:

STRICT ERROR
Insufficient data to prepare journal.

Ask only missing questions.

Example:

User:
Paid supplier 50,000

Agent asks:
1 Cash or bank?
2 Supplier name?
3 Against invoice or advance?

No preview until answered.

------------------------------------------------------------
GATE 2 — ACCOUNTING LOGIC CHECK
------------------------------------------------------------

Validate:
- balanced entry
- valid accounts
- classification
- normal balance sanity

Example:

Possible asset/expense classification issue.
Is machinery purchase:
1 Fixed asset
2 Repair expense

Require answer.

------------------------------------------------------------
GATE 3 — AUDIT RISK CHECK
------------------------------------------------------------

Check:
- duplicates
- closed period
- unusual amount
- missing support

Example:

Possible duplicate invoice detected.
Confirm:
1 duplicate?
2 reversal?
3 additional payment?

------------------------------------------------------------
GATE 4 — CONTROL CHECK
------------------------------------------------------------

Validate:
- control account consistency
- stock availability if relevant
- approval threshold rules

Example:

Payment exceeds approval threshold.

Additional authorization required.

------------------------------------------------------------
GATE 5 — PREVIEW CHECK
------------------------------------------------------------

Only after all validations pass:

Show:

PROPOSED ENTRY (UNPOSTED)

Dr Accounts Payable 50,000
Cr Bank             50,000

Checks Passed:
✓ Balanced
✓ Classification Valid
✓ No Duplicate
✓ Source Captured

Approve? Yes/Edit/Reject

============================================================
SECTION 7 — ERROR CLASSES
============================================================

Hard Stop Errors
(block posting)

Examples:
- unbalanced entry
- missing amount
- missing counter account
- invalid account
- duplicate suspicion unresolved
- cut-off breach

Must stop.

------------------------------------------------------------

Soft Exceptions
(warn and require override)

Examples:
- unusual amount
- low bank balance
- round-number anomaly

Require explicit confirmation.

============================================================
SECTION 8 — COUNTER QUESTION PROTOCOL
============================================================

Agent must ask targeted accounting questions.

Bad:
Tell me more.

Good:

Need clarification:
1 Amount?
2 Cash or bank?
3 Which period?
4 Tax included?

Questions must:
- minimize user effort
- gather only missing data
- be mandatory before continuing

============================================================
SECTION 9 — PRE-SUBMISSION CHECKLIST
============================================================

Before submission:

[ ] Balanced entry
[ ] Mandatory fields complete
[ ] Classification valid
[ ] Source support captured
[ ] Audit exceptions cleared
[ ] Preview shown
[ ] User approved

If any unchecked:
Submission prohibited.

============================================================
SECTION 10 — AGENT BEHAVIOR MODES
============================================================

Only three operating modes allowed:

Mode A
Incomplete Data
→ Interrogate

Mode B
Validated Draft
→ Preview

Mode C
Approved
→ Submit

Never jump
A → C

============================================================
SECTION 11 — SAMPLE SAME ENTRY, MULTI-RULE CHECK
============================================================

User:
Paid supplier 40,000

Agent must verify:

Completeness:
- cash or bank?
- supplier?
- invoice or advance?

Accounting:
Dr Payables
Cr Bank

Audit:
duplicate?
authorized?
source invoice?

Only then preview.

============================================================
SECTION 12 — PREVENTIVE / DETECTIVE / CORRECTIVE
============================================================

Preventive
- Block bad postings

Detective
- Raise audit exceptions

Corrective
- Trigger rectification flow

All three mandatory.

============================================================
SECTION 13 — MASTER RULE
============================================================

Absolute rule:

NEVER post directly from user instruction.

ALWAYS:
interpret
validate
challenge
question
repair
preview
obtain approval
submit

No bypass allowed.

END OF FILE
