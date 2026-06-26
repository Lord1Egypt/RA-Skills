---
slug: reconcile-broker-commission-statement
name: Reconcile Broker Commission Statement
version: 1.2.0
status: ready_to_publish
owner: revenue-ops
---

# Reconcile Broker Commission Statement

## Summary
Use this skill when a broker, lender, or internal stakeholder provides a commission statement and needs it checked against expected loan-level payouts. The skill extracts statement rows, normalizes loan identifiers, compares amounts to expected commissions, flags discrepancies, and produces a concise reconciliation summary with follow-up actions.

## When to use
- Monthly or ad hoc broker commission statement review
- Pre-payment verification before approving payout
- Investigating short-paid, duplicate, or missing commission items
- Validating clawbacks, split commissions, or post-close adjustments

## Inputs
Provide as many of the following as available:
- Broker commission statement (PDF, spreadsheet, CSV, or pasted table)
- Expected commission export from LOS/CRM/payments system
- Broker name and statement period
- Compensation plan details if nonstandard
- Known exceptions or prior unresolved items

## Required tools
- File reading/parsing
- Spreadsheet/table manipulation
- Basic arithmetic and row-level comparison
- Ability to produce a structured summary

## Output
Deliver:
1. A reconciled table with one row per statement item
2. Status for each row: `match`, `underpaid`, `overpaid`, `missing_expected`, `unexpected_statement_item`, `needs_review`
3. Variance amount and likely reason
4. Totals summary:
   - total statement amount
   - total expected amount
   - net variance
   - count by status
5. Recommended next actions

## Procedure

### 1) Gather context
Confirm:
- statement period covered
- broker/payee name
- gross vs net commission basis
- whether amounts include processing/admin fees, lender-paid adjustments, or tax withholdings
- expected matching key priority:
  1. loan number
  2. borrower + close/fund date
  3. property address + amount

If the source does not clearly state gross vs net, mark affected rows `needs_review` instead of forcing a match.

### 2) Parse and normalize data
For both statement data and expected data:
- Trim whitespace from all text fields
- Normalize loan numbers by removing spaces/dashes while preserving leading zeros where possible
- Standardize dates to ISO format
- Convert currency strings to numeric values
- Keep original raw values in notes if transformation was required
- Normalize borrower names conservatively; do not merge clearly different borrowers

Expected core fields:
- loan_id
- borrower_name
- property_address
- fund_or_close_date
- commission_expected
- split_percent
- expected_basis_notes

Statement core fields:
- statement_loan_id
- borrower_name
- statement_date
- commission_paid
- fee_adjustment
- clawback_amount
- net_paid
- statement_notes

### 3) Match rows
Match in this order:
1. Exact normalized loan ID
2. Same borrower and close/fund date within 7 days
3. Same property address and commission amount within small tolerance

Rules:
- If multiple expected rows could match one statement row, mark `needs_review`
- If one expected loan appears split across multiple statement rows, aggregate only if notes clearly support split payout
- Tolerance for rounding-only differences: 0.01
- Do not auto-match rows with reversed sign unless statement explicitly indicates clawback/reversal

### 4) Compute reconciliation status
Use:
- `match`: statement net aligns to expected within tolerance
- `underpaid`: expected > statement by more than tolerance
- `overpaid`: statement > expected by more than tolerance
- `missing_expected`: expected item not present on statement
- `unexpected_statement_item`: statement item has no supported expected match
- `needs_review`: ambiguous mapping, missing key fields, unclear fee treatment, or unusual adjustments

Variance formula:
`variance = net_paid - commission_expected`

When clawbacks or fees are separately listed:
- Prefer comparing net economic result if plan pays net
- Prefer gross comparison if payout ops approves gross basis
- If basis is unclear, surface both gross and net in notes and mark `needs_review`

### 5) Produce concise findings
Include:
- largest variances first
- any repeated pattern (e.g., all loans from one branch short by fixed bps)
- any likely data issue (duplicate loan IDs, missing loans, date mismatch, split mismatch)
- explicit asks needed to resolve open items

## Guardrails
- Never assume compensation plan terms not supplied in the source material
- Never hide ambiguous matches; mark them
- Preserve an audit trail in notes for manual adjustments
- If OCR quality is poor, state that confidence is limited
- If totals on the statement do not foot to row-level sums, call this out explicitly

## Suggested output format

### Reconciled Rows
| statement_loan_id | loan_id | borrower_name | statement_date | expected_date | net_paid | commission_expected | variance | status | notes |
|---|---|---|---|---|---:|---:|---:|---|---|

### Summary
- Broker:
- Statement period:
- Statement total:
- Expected total:
- Net variance:
- Status counts:
- Key findings:
- Next actions:

## Edge cases
- Negative rows may be reversals or clawbacks; require note support
- Combined statements may include prior-period true-ups
- Split commissions may need allocation before comparison
- Broker statements sometimes show funded date while expected export uses closing date
- A missing loan on the statement may still be pending investor purchase; mention timing risk if relevant

## Publishing instructions
- Publish under slug: `reconcile-broker-commission-statement`
- Category: Finance Operations
- Add tags: `commissions`, `reconciliation`, `mortgage`, `broker-payments`
- Mark as customer-safe: yes
- Do not reference internal system brand names in the public description
- Include a one-line SEO description: `Reconcile broker commission statements against expected loan-level payouts and flag variances fast.`

## Changelog
### 1.2.0
- Clarified gross vs net comparison rules
- Added matching priority and ambiguity handling
- Added publishing metadata and SEO description

### 1.1.0
- Added support for clawbacks, fees, and split commissions
- Improved output schema with status categories

### 1.0.0
- Initial version