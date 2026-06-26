# GST Guard Skill
Version: 1.0
Layer: Transaction Control Skill
Priority: High
Purpose:
Prevent GST omission, wrong tax treatment, incorrect journal construction,
and unsafe posting by enforcing GST reasoning before voucher commit.

---

## Core Principle

GST must be derived at source-entry time.

Never:
- Post taxable transactions first and fix GST later.
- Allow manual tax treatment without validation.
- Allow GST-sensitive transactions to bypass review.

Always:

Source Document
→ GST Validation
→ Tax Determination
→ Journal Preview
→ User Confirmation
→ Commit Posting

---

## Skill Objective

The agent must:

1. Detect whether GST applies.
2. Determine correct GST treatment.
3. Generate tax lines automatically.
4. Detect missed GST situations.
5. Prevent wrong postings before commit.

GST should be derived, not manually authored.

---

## Trigger Conditions

Activate this skill whenever transaction includes:

- Sales invoice
- Purchase invoice
- Expense bill
- Debit note
- Credit note
- Vendor bill
- Customer invoice
- Interstate supply
- Import / export
- Reverse charge transaction
- Manual journal touching GST ledgers

---

## Required Ledger Tax Metadata

Each party ledger should carry:

- GSTIN
- State Code
- Registration Type
- Default Tax Category
- Reverse Charge Flag
- ITC Eligibility Defaults
- GST Ledger Mapping Rules

Example:

Party Ledger
Tax Profile:
- gstin: 24ABCDE1234F1Z5
- state: Gujarat
- registration: regular
- default_supply_type: taxable
- rcm: false

---

## GST Determination Rules

Determine tax using:

function determine_gst(
 company_state,
 party_state,
 registration_type,
 place_of_supply,
 supply_type,
 tax_rate,
 item_tax_class,
 reverse_charge_flag
)

Do NOT use simplistic rule:

if gstin_matches...

That is insufficient.

---

## Supply Rules

If same state:
Use:
- CGST
- SGST

If different state:
Use:
- IGST

State comparison is derived from:
- Place of Supply
- Party State Code
- Company State

---

## Auto Tax Entry Rule

User should enter:
- taxable amount
- rate
- party

Agent should generate tax journal lines.

Never require user to manually construct:

Input CGST Dr ...
Input SGST Dr ...

Agent derives these.

---

## Mandatory Pre-Post GST Review

Before posting, always preview:

- Taxable value
- GST type
- Tax amount
- Input credit status
- GST ledgers impacted
- Risk flags
- Proposed journal entry

Posting requires confirmation.

No blind posting.

---

## Hard Stop Rules

Stop posting if:

- Vendor invoice has missing GST possibility
- GST rate absent for taxable supply
- Wrong tax split suspected
- Interstate using CGST/SGST
- Intrastate using IGST
- Manual journal directly manipulates GST ledgers without review
- GSTIN missing and treatment unresolved

Raise:

Potential Missed GST Detected

---

## Manual Journal Restriction

Journal entries should not bypass GST controls.

If JE touches:
- Input CGST
- Input SGST
- Input IGST
- Output CGST
- Output SGST
- Output IGST

Force secondary review.

---

## Skill Priority

If GST logic conflicts with generic posting logic:

GST Guard overrides posting flow.