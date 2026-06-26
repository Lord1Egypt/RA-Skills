## Description: <br>
Complete Wafeq accounting and e-invoicing API reference for the Middle East, including invoices, contacts, accounts, bills, expenses, notes, payments, payroll, quotes, reports, and related Wafeq REST API tasks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[YordiLorenzo](https://clawhub.ai/user/YordiLorenzo) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and integration engineers use this skill to reference Wafeq API authentication, schemas, endpoint patterns, and workflows for accounting, e-invoicing, reporting, payroll, and payment integrations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can guide actions against sensitive accounting, payroll, payment, and tax-reporting APIs. <br>
Mitigation: Manually review write, delete, bulk-send, payment, payroll, and tax-reporting actions before execution, and use the narrowest available API scopes. <br>
Risk: Wafeq API keys and OAuth tokens can grant access to financial-system data. <br>
Mitigation: Store credentials in a protected secret store or OpenClaw configuration, never hardcode them, and avoid logging credential values. <br>


## Reference(s): <br>
- [Wafeq homepage](https://wafeq.com) <br>
- [ClawHub skill page](https://clawhub.ai/YordiLorenzo/wafeq-api) <br>
- [Core concepts](references/core-concepts.md) <br>
- [Enum types](references/enums.md) <br>
- [Invoices](references/invoices.md) <br>
- [Accounts, banking, and contacts](references/accounts-banking-contacts.md) <br>
- [Bills, expenses, credit notes, and debit notes](references/bills-expenses-notes.md) <br>
- [Quotes, payments, payslips, items, files, journals, and reports](references/quotes-payments-remaining.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with endpoint references, JSON examples, and inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Documentation-only guidance; API calls require user-provided Wafeq credentials.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
