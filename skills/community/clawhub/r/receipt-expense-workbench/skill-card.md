## Description:

Normalize receipts, reimbursement slips, and invoices into a clean expense ledger with category mapping and anomaly flags.

This skill is ready for commercial/non-commercial use.

## Publisher:

[52yuanchangxing](https://clawhub.ai/user/52yuanchangxing)

### License/Terms of Use:

MIT-0

## Use Case:

Employees and finance-facing teams use this skill to turn receipt text or OCR output into expense ledgers, category summaries, anomaly reports, and reimbursement packet checklists.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated CSV ledgers may carry spreadsheet formulas from untrusted receipt or invoice text.

Mitigation: Sanitize cell values before opening generated ledgers in spreadsheet software and keep formula execution disabled for untrusted inputs.

Risk: Receipt and reimbursement materials may contain personal, financial, or policy-sensitive details.

Mitigation: Redact unnecessary details, use explicit input and output paths, and process only materials the user has intentionally provided.

Risk: Expense categories, totals, tax fields, or reimbursement readiness may be incomplete or incorrect when source data is missing or ambiguous.

Mitigation: Use preview outputs, keep uncertain fields marked, and review results against the applicable reimbursement policy before submission.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/52yuanchangxing/skills/receipt-expense-workbench)
- [Artifact README](artifact/README.md)
- [Expense ledger helper script](artifact/scripts/expense_ledger.py)
- [Expense category resource](artifact/resources/expense_categories.csv)

## Skill Output:

**Output Type(s):** [Text, Markdown, CSV files, Shell commands, Guidance]

**Output Format:** [Markdown guidance with optional CSV files and shell command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses explicit input and output paths; uncertain receipt fields should remain marked for review.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact CHANGELOG; artifact SKILL.md frontmatter says 1.1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
