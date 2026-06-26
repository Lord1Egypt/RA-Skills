# rectification.md
# Skill Knowledge File: Transaction Rectification & Posting Controls
# Purpose:
# Teach an Accountant Agent how to prevent errors,
# detect mistakes,
# correct posted transactions,
# and enforce confirmation before ledger posting.

---

# 1. CORE PRINCIPLE

Primary philosophy:

Prevent errors if possible.
Correct errors if necessary.

Preferred sequence:

Validate
→ Preview
→ Confirm
→ Post

Do not post first and fix later when avoidable.

---

# 2. TWO-STAGE POSTING MODEL

Transactions exist in two states:

A. Draft / Unposted

B. Posted / Finalized

Rules:

Draft transactions:
- May be edited
- May be deleted
- May be corrected directly
- No rectification entry required

Posted transactions:
- Should not be silently edited
- Should not be silently deleted
- Must be corrected through accounting entries

Important Principle:

Before posting:
edit is allowed.

After posting:
rectify through entries.

---

# 3. MANDATORY PREVIEW CONFIRMATION

Hard Rule:

Never auto-post financial entries directly into ledgers.

Always generate preview first.

Show user:

- Voucher type
- Journal entry
- Impacted ledgers
- Debit/Credit amounts
- Ledger impact preview (if available)
- Validation result

Then ask:

Are you sure of this entry?

Only commit after explicit confirmation.

Accepted confirmation examples:
- Confirm
- Yes post
- Approve
- Proceed

Until confirmed:
Remain draft.

---

# 4. POSTING STATES

Use these transaction states:

Draft
Previewed
Confirmed
Posted

Optional transitions:

Draft
→ Previewed
→ Confirmed
→ Posted

Do not skip confirmation.

---

# 5. WRONG ACCOUNT POSTED

Example:

Wrong:

Rent Expense Dr 5000
 To Cash 5000

Should have been:

Repairs Expense

--------------------------------
If Draft
--------------------------------

Edit account directly.

No rectification needed.

---

--------------------------------
If Posted
--------------------------------

Do not delete original entry.

Reason:
- preserves audit trail
- prevents hidden history changes
- keeps reports reproducible

Use rectification entry:

Repairs Expense Dr 5000
 To Rent Expense 5000

Result:
Wrong classification corrected.

---

# 6. WRONG AMOUNT POSTED

Example:

Posted:
1000

Should be:
10000

Difference:
9000

--------------------------------
If Draft
--------------------------------

Edit amount.

---

--------------------------------
If Posted
--------------------------------

Post adjustment for difference only.

Correction:

Expense Dr 9000
 To Cash 9000

Rule:
Adjust delta.
Do not overwrite posted history.

---

# 7. DUPLICATE POSTING

Example:
Same entry accidentally entered twice.

--------------------------------
Prevent Before Posting
--------------------------------

Agent must detect potential duplicates before commit.

Check possible duplicate using:

- Same date
- Same voucher type
- Same Ledger 1
- Same Ledger 2
- Same amount
- Similar narration (optional)
- Same source document number (if available)

If potential duplicate found:

Pause posting.

Ask user:

Possible duplicate detected.
Post anyway?

Require confirmation.

---

--------------------------------
If Duplicate Already Posted
--------------------------------

Reverse one duplicate.

Example reversal:

Original duplicate:
Expense Dr 5000
 To Cash 5000

Reverse:
Cash Dr 5000
 To Expense 5000

---

# 8. PREVENTIVE CONTROLS

Rectification begins with prevention.

Use controls before posting:

- Balance validation
- Duplicate detection
- Ledger existence checks
- Voucher-type checks
- Amount validation
- Preview confirmation

Goal:
Prevent errors before they reach ledgers.

---

# 9. RECTIFICATION METHODS

Use one of three methods:

1 Edit
For draft transactions only.

2 Adjustment Entry
Correct difference or classification.

3 Reversal Entry
Reverse wrong or duplicate posted entry.

---

# 10. ALLOWED REVERSAL / CORRECTION USE CASES

Use reversal/rectification for:

- Wrong ledger used
- Wrong amount
- Duplicate posting
- Wrong debit/credit side
- Missing part of compound entry
- Reclassification errors

---

# 11. JE USAGE FOR RECTIFICATION

Rectification generally uses:

JE General Journal Entry

Use JE for:
- correction entries
- reversal entries
- reclassifications

Operational vouchers should not normally be used for corrections.

---

# 12. NEVER SILENTLY ALTER POSTED BOOKS

Hard Rule:

Do not:
- overwrite posted entries
- silently modify posted books
- delete posted history without trace

Corrections must remain traceable.

History must remain auditable.

---

# 13. EXAMPLES

--------------------------------
Example A
Wrong account correction
--------------------------------

Wrong:
Rent Dr 5000
 To Cash

Correction:

Repairs Dr 5000
 To Rent 5000

---

--------------------------------
Example B
Amount correction
--------------------------------

Posted 1000 instead of 10000

Adjustment:

Expense Dr 9000
 To Cash 9000

---

--------------------------------
Example C
Duplicate reversal
--------------------------------

Reverse duplicate:

Cash Dr 5000
 To Expense 5000

---

# 14. AGENT ERROR HANDLING LOGIC

If transaction still Draft:

Prefer edit.

Else if Posted and wrong:
Use rectification.

Else if duplicate risk detected:
Warn before posting.

Decision logic:

if draft:
 edit

elif duplicate suspected:
 warn and confirm

elif posted error:
 create JE rectification

---

# 15. PREVIEW TEMPLATE

Use preview like:

Preview Entry

Voucher:
BP

Journal:
Vendor Payable Dr 50,000
 To Bank 50,000

Impact:
Vendor balance becomes zero.
Bank reduces by 50,000.

Balanced:
Yes

Are you sure of this entry?

Only post after confirmation.

---

# 16. AGENT OPERATING PHILOSOPHY

Prevent
Detect
Correct

not merely

Post
Fix later

This is preferred control model.

---

# 17. RELATION TO OTHER FILES

Uses:
coa.md
journal_entry.md
general_ledger.md
source_document.md

Rectification happens only after transaction logic exists.

---

# 18. SCOPE LIMIT

This file covers:
- Posting controls
- Preview confirmation
- Rectification logic
- Reversal logic
- Duplicate prevention

Does not cover:
- Fraud detection
- Audit procedures
- Financial reporting adjustments

---

# 19. FOUNDATIONAL PRINCIPLES

Before posting:
Preview and confirm.

After posting:
Correct through entries.

Prevent if possible.
Correct if necessary.

Never auto-post without asking:

Are you sure of this entry?

---

End of rectification.md
