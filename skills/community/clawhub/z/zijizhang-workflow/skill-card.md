## Description: <br>
Helps an agent operate the ZJZ bookkeeping app for account binding, employee management, payroll, invoices, bank receipts and statements, tax and social security filing, audit tasks, and financial report lookup. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[shootofficial](https://clawhub.ai/user/shootofficial) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and accounting operators use this skill to guide an agent through ZJZ bookkeeping, payroll, invoice, bank, tax, social security, audit, and report workflows. It is intended for account-specific operational tasks where the user reviews sensitive financial actions before execution. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can expose sensitive payroll, tax, invoice, bank, and financial report data. <br>
Mitigation: Use it only in trusted agent sessions, minimize shared chat or log exposure, and redact full ID numbers, bank account numbers, payroll tables, and financial documents where possible. <br>
Risk: The skill can initiate changes to bookkeeping, payroll, invoice, bank, tax, social security, and audit state. <br>
Mitigation: Require explicit user confirmation before every write action, echo the company uid, target object, submitted fields, and field sources, and stop on non-200 CLI responses. <br>
Risk: Broad activation rules may cause the agent to enter the workflow for general bookkeeping, tax, report, or task-handling requests. <br>
Mitigation: Confirm the user intends to operate the ZJZ account and verify the active company context before running account-specific commands. <br>
Risk: Incorrect or invented values could lead to inaccurate filings, payroll, invoice handling, or bank reconciliation. <br>
Mitigation: Use only user-provided values, CLI-returned values, or values explicitly allowed by the workflow, and ask for missing data instead of filling gaps. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/shootofficial/zijizhang-workflow) <br>
- [Workflow and CLI Reference Index](references/README.md) <br>
- [Payroll Workflow](workflow/payroll.md) <br>
- [Bank Receipt and Statement Workflow](workflow/bank.md) <br>
- [Invoice Upload Workflow](workflow/invoice_upload.md) <br>
- [Sales Invoice Workflow](workflow/invoice_sales.md) <br>
- [Income Invoice Workflow](workflow/invoice_income.md) <br>
- [Social Security Workflow](workflow/social_security.md) <br>
- [Individual Tax Workflow](workflow/individual_tax.md) <br>
- [Audit Workflow](workflow/audit.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration instructions] <br>
**Output Format:** [Markdown guidance with inline shell commands and structured tables] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include command sequences, confirmation prompts, and summaries of returned payroll, tax, invoice, bank, audit, and report data.] <br>

## Skill Version(s): <br>
0.0.4 (source: SKILL.md frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
