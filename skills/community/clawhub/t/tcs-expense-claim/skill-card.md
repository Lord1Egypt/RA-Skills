## Description:

End-to-end business travel expense claim processor that organizes uploaded receipts, categorizes expenses, generates claim PDFs and XLSX summaries, and prepares tables for reimbursement entry.

This skill is ready for commercial/non-commercial use.

## Publisher:

[insanelyqurious](https://clawhub.ai/user/insanelyqurious)

### License/Terms of Use:

MIT-0

## Use Case:

Employees and business travelers use this skill to turn receipt images and PDFs into reimbursement-ready claim packages. It is especially tailored for TCS-style expense categories, currency conversion notes, and manual portal entry tables.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Helper scripts may read or write broader local paths than intended when given manifests or output paths.

Mitigation: Review manifests and output paths before execution, and use only receipts intended for reimbursement until path containment and filename sanitization are added.

Risk: Generated claim PDFs and spreadsheets can contain sensitive reimbursement information.

Mitigation: Inspect generated files before submission or sharing, and run the skill only for receipts the user intends to package for reimbursement.

Risk: Externally supplied expense text may be carried into spreadsheet outputs.

Mitigation: Avoid untrusted expense text until spreadsheet text escaping is added, and review XLSX contents before distributing the workbook.

## Reference(s):

- [TCS Expense Categories](artifact/tcs_categories.md)
- [Standard FX Rates Reference](artifact/fx_rates.md)
- [ClawHub Skill Page](https://clawhub.ai/insanelyqurious/skills/tcs-expense-claim)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, files]

**Output Format:** [Markdown guidance with generated PDF and XLSX files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generates per-day per-category PDF claim packages, an expense_claim.xlsx workbook, and summary tables for manual reimbursement entry.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
