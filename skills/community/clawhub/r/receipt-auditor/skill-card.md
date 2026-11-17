## Description:

Extract, categorize, and audit receipts and bills to generate expense reports and spot discrepancies.

This skill is ready for commercial/non-commercial use.

## Publisher:

[harrylabsj](https://clawhub.ai/user/harrylabsj)

### License/Terms of Use:

MIT-0

## Use Case:

Employees, freelancers, and household finance users use this skill to turn receipt or bill text into categorized reimbursement reports, shared-expense splits, and anomaly checks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Receipt prompts may contain personal or payment details and are written to a local plaintext file.

Mitigation: Use only redacted receipts, avoid sensitive account details, or remove the prompt-saving path before installation.

Risk: Expense classifications, totals, split calculations, and anomaly flags are generated from user-provided receipt text and may be wrong.

Mitigation: Manually verify parsed line items, totals, duplicate flags, and reimbursement decisions before submission or payment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/harrylabsj/skills/receipt-auditor)
- [Expense categories](artifact/references/categories.json)
- [Input schema](artifact/schemas/input.schema.json)
- [Output schema](artifact/schemas/output.schema.json)
- [Report template](artifact/references/templates/report-template.md)
- [AA split template](artifact/references/templates/aa-split-template.md)
- [Audit template](artifact/references/templates/audit-template.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown reports and tables, with JSON-compatible input and output schemas for structured use.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Supports report, aa-split, and audit modes; generated totals, classifications, and anomaly flags should be manually verified.]

## Skill Version(s):

1.0.0 (source: release evidence, frontmatter, skill.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
