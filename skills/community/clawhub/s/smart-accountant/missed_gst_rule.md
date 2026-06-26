# Missed GST Detection Rules
Version: 1.0
Layer: Control Skill
Purpose:
Detect omitted, incorrect, underposted or bypassed GST situations.

---

## Definition

Missed GST means:

- GST omitted when applicable
- Wrong GST type used
- Input credit missed
- Output tax missed
- GST embedded incorrectly in expense
- GST not aligned to source document

---

## Detection Rules

Rule 1

IF:
Vendor expense exists
AND no GST component found

Flag:
Possible Missed GST

---

Rule 2

IF:
Taxable sales
AND no output GST

Flag:
Output GST Missing

---

Rule 3

IF:
Expense gross amount includes tax
AND no separate input GST ledger

Flag:
Possible missed ITC

---

Rule 4

IF:
Interstate transaction
AND CGST/SGST used

Flag:
Wrong tax jurisdiction

---

Rule 5

IF:
Intrastate transaction
AND IGST used

Flag:
Wrong tax jurisdiction

---

Rule 6

IF:
GSTIN absent
AND party likely registered

Flag:
GST master incomplete

---

Rule 7

IF:
Manual JE touches GST ledgers

Flag:
Review required

---

Rule 8

IF:
RCM applicable
AND liability side missing
OR credit side missing

Flag:
Incomplete reverse charge posting

---

Rule 9

IF:
Invoice likely eligible for ITC
AND GST booked to expense

Flag:
Input credit may be missed

---

Rule 10

If GST amount mathematically inconsistent:

Taxable Value × Rate ≠ Tax

Flag:
Tax mismatch

---

## Severity

Warning:
Potential issue.

Error:
Wrong posting.

Hard Stop:
Do not post.

---

## Correction Principle

Never silently auto-fix.

Always:
- flag
- explain
- propose corrected entry
- seek confirmation

---

## Agent Message Template

Potential Missed GST Detected:

Reason:
Suggested correction:
Revised entry preview:
Post corrected version? (Y/N)

---

## Core Philosophy

Detect omission before filing problem occurs.