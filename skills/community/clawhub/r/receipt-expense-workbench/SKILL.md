---
name: receipt-expense-workbench
description: Normalize receipts, reimbursement slips, and invoices into a clean expense
  ledger with category mapping and anomaly flags.
version: 1.1.0
metadata:
  openclaw:
    requires:
      bins:
      - python3
    emoji: 🧰
---

# Receipt Expense Workbench

## Purpose

Normalize receipts, reimbursement slips, and invoices into a clean expense ledger with category mapping and anomaly flags.

## Trigger phrases

- 整理发票
- 报销单汇总
- receipt to expense sheet
- 做费用台账
- expense ledger

## Ask for these inputs

- receipt text or OCR output
- currency
- reimbursement policy if available
- project code
- merchant names

## Workflow

1. Extract vendor, date, amount, tax, and payment method.
2. Map each line item to the bundled category list.
3. Flag duplicates, suspicious totals, missing tax IDs, and missing attachments.
4. Generate a ledger CSV and a reimbursement-ready summary.
5. Keep uncertain fields clearly marked instead of guessing.

## Output contract

- expense ledger CSV
- category summary
- anomaly report
- reimbursement packet checklist

## Files in this skill

- Script: `{baseDir}/scripts/expense_ledger.py`
- Resource: `{baseDir}/resources/expense_categories.csv`

## Operating rules

- Be concrete and action-oriented.
- Prefer preview / draft / simulation mode before destructive changes.
- If information is missing, ask only for the minimum needed to proceed.
- Never fabricate metrics, legal certainty, receipts, credentials, or evidence.
- Keep assumptions explicit.

## Suggested prompts

- 整理发票
- 报销单汇总
- receipt to expense sheet

## Use of script and resources

Use the bundled script when it helps the user produce a structured file, manifest, CSV, or first-pass draft.
Use the resource file as the default schema, checklist, or preset when the user does not provide one.

## Boundaries

- This skill supports planning, structuring, and first-pass artifacts.
- It should not claim that files were modified, messages were sent, or legal/financial decisions were finalized unless the user actually performed those actions.


## Compatibility notes

- Directory-based AgentSkills/OpenClaw skill.
- Runtime dependency declared through `metadata.openclaw.requires`.
- Helper script is local and auditable: `scripts/expense_ledger.py`.
- Bundled resource is local and referenced by the instructions: `resources/expense_categories.csv`.
