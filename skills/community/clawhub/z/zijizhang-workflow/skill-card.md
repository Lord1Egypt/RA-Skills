## Description:

ZJZ Workflow helps agents guide users of the 自记账 app through accounting, payroll, tax, invoice, banking, social security, audit-task, and report-query workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[shootofficial](https://clawhub.ai/user/shootofficial)

### License/Terms of Use:

MIT-0

## Use Case:

External users and their agents use this skill to operate 自记账 accounting workflows, including company context selection, payroll, employee records, bank receipts, invoices, taxes, social security filings, audit todos, and financial reports.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can handle payroll, tax, invoice, banking, and account authorization data.

Mitigation: Use it only with the intended 自记账 account and avoid exposing full ID numbers, bank numbers, auth links, payroll data, or invoice data in shell history, logs, screenshots, or chat unless necessary.

Risk: The security evidence flags broad activation and sensitive write-capable workflows.

Mitigation: Confirm every write action with the user, echo the target company, operation object, submitted fields, and field sources, then check command results before continuing.

Risk: The security evidence flags unsafe shell-style command templates and unverified install/update guidance.

Mitigation: Review the publisher and CLI package before installation, pin and verify the zijizhang-cli version, and avoid server-provided skill ZIP updates unless independently verified.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/shootofficial/skills/zijizhang-workflow)
- [CLI Reference Index](references/README.md)
- [Payroll Workflow](workflow/payroll.md)
- [Bank Workflow](workflow/bank.md)
- [Income Invoice Workflow](workflow/invoice_income.md)
- [Sales Invoice Workflow](workflow/invoice_sales.md)
- [Invoice Upload Workflow](workflow/invoice_upload.md)
- [Social Security Workflow](workflow/social_security.md)
- [Individual Tax Workflow](workflow/individual_tax.md)
- [Audit Workflow](workflow/audit.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and structured tables]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs should preserve user confirmation gates for write actions and avoid exposing sensitive accounting, payroll, tax, invoice, bank, authorization, or identity data unless necessary.]

## Skill Version(s):

0.0.4 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
