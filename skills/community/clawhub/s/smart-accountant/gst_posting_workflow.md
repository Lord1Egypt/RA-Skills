# GST Posting Workflow
Version: 1.0
Layer: Workflow Skill

Purpose:
Define mandatory posting sequence.

---

## Workflow

Step 1
Read source document.

Extract:
- Party
- Taxable value
- Rate
- Supply type
- Place of supply
- GST relevance

---

Step 2
Resolve party tax treatment.

---

Step 3
Run GST applicability checks.

Questions:

- GST applicable?
- Exempt?
- Reverse charge?
- ITC eligible?
- Missing GST risk?

---

Step 4
Generate proposed tax lines.

Auto build journal.

---

Step 5
Run Missed GST rules.

Check all detection triggers.

---

Step 6
Show posting preview.

Display:

Tax Preview
Journal Preview
Risk Flags

Example:

Purchases Dr ...
Input CGST Dr ...
Input SGST Dr ...
To Vendor ...

---

Step 7
Require user confirmation.

Only then:

Commit posting.

---

## Workflow Pseudocode

on_transaction():

validate_source()

resolve_tax()

build_tax_entry()

run_missed_gst_detection()

preview()

if user_confirms:
 post()
else:
 stop()

---

## Forbidden Workflow

Never:

Receive invoice
→ post immediately
→ fix GST later

Forbidden.

---

## Exception Handling

Rectification entries:
Allowed only through review.

Never bypass workflow.

---

## Skill Interaction Priority

Workflow order:

gst_guard
then
missed_gst_rules
then
posting

Not reverse.

---

## Golden Rule

No GST-sensitive transaction posts
without:
- determination
- validation
- preview
- approval