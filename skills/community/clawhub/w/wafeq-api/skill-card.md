## Description:

Wafeq API Reference helps agents answer and draft integration guidance for Wafeq accounting and e-invoicing API workflows across invoices, contacts, accounts, payments, reports, and related resources.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yordilorenzo](https://clawhub.ai/user/yordilorenzo)

### License/Terms of Use:


## Use Case:

Developers and finance-system integrators use this skill to work with the Wafeq REST API, including authentication, idempotency, CRUD endpoints, financial documents, payments, reports, tax-authority reporting, and entity management.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can guide high-impact financial, payment, payroll, tax-reporting, and bulk email actions.

Mitigation: Use a least-privilege Wafeq API key, start in a sandbox or test organization, and require explicit human review before write, delete, payment, payroll, bulk email, or tax-authority requests.

Risk: Incorrect recipients, amounts, record IDs, or tax details could create inaccurate accounting or reporting outcomes.

Mitigation: Review all recipients, amounts, record IDs, invoice details, tax fields, and generated request bodies before execution.

Risk: API credentials could be exposed if copied into code, prompts, or skill files.

Mitigation: Store credentials only in WAFEQ_API_KEY or the configured skill entry, and avoid hardcoding secrets in generated code or documentation.

## Reference(s):

- [Wafeq Homepage](https://wafeq.com)
- [Wafeq App](https://app.wafeq.com)
- [Wafeq API Keys](https://app.wafeq.com/c/api-keys)
- [Wafeq API Base URL](https://api.wafeq.com/v1/)
- [Core Concepts and Guides](references/core-concepts.md)
- [Enum Types Reference](references/enums.md)
- [Invoices API Reference](references/invoices.md)
- [Accounts, Banking, and Contacts API Reference](references/accounts-banking-contacts.md)
- [Bills, Expenses, Credit Notes, and Debit Notes API Reference](references/bills-expenses-notes.md)
- [Quotes, Payments, Payslips, Items, Files, Journals, Reports, and Entity Management API Reference](references/quotes-payments-remaining.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline code, JSON examples, and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Documentation-only guidance; no direct API calls are executed by the skill.]

## Skill Version(s):

1.1.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
