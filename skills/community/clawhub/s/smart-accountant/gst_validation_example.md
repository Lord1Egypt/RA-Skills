# GST Validation Examples
Version: 1.0

Purpose:
Teach the agent examples of correct vs incorrect treatment.

---

## Example 1
Purchase Intrastate

Input:
Purchase 100000
GST 18%
Same state

Expected:

Purchases Dr 100000
Input CGST Dr 9000
Input SGST Dr 9000
To Vendor 118000

Pass

---

## Example 2
Wrong Gross Expense Booking

Input:

Repairs Expense Dr 118000
To Vendor 118000

Detect:
Missed input GST

Suggested:

Repairs Expense Dr 100000
Input GST Dr 18000
To Vendor 118000

Flag warning

---

## Example 3
Interstate Wrong Tax Split

Input:
Vendor state different
CGST booked

Flag:
Error

Correct:
Use IGST

---

## Example 4
Sales Without GST

Customer Dr 100000
To Sales 100000

Taxable supply.

Flag:
Output GST Missing

---

## Example 5
Manual JE touching GST

Input GST Dr ...
To Suspense

Force review.

---

## Example 6
RCM Incomplete

Only liability booked.

Flag:
Missing dual impact.

---

## Example 7
Missing GSTIN

Vendor invoice posted.
No GSTIN.

Prompt:
Registered vendor?
Unregistered?
RCM?

Do not assume.

---

## Example Rule

Examples act as reasoning patterns,
not rigid templates.
Use analogous reasoning.