## Description:

Reviews unpaid and overdue SuperBooks invoices, summarizes outstanding balances by customer, and drafts a reminder for the user to send.

This skill is ready for commercial/non-commercial use.

## Publisher:

[devino](https://clawhub.ai/user/devino)

### License/Terms of Use:

MIT-0

## Use Case:

Business owners and accounts-receivable staff use this skill to identify unpaid and overdue invoices, prioritize customers with outstanding balances, and draft reminders for their own review and sending.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Invoice and customer details are sensitive business information.

Mitigation: Connect SuperBooks only when invoice analysis is needed and share results only with authorized users.

Risk: An inaccurate reminder could misstate an amount or due date.

Mitigation: Check invoice details and review the drafted reminder before sending it yourself.

## Reference(s):

- [Chasing Unpaid Invoices on ClawHub](https://clawhub.ai/devino/skills/superbooks-chasing-unpaid-invoices)

## Skill Output:

**Output Type(s):** [Analysis, Text, Markdown]

**Output Format:** [Markdown invoice table, balance summary, and optional reminder draft]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses SuperBooks invoice, customer, and currency data; does not send reminders or modify invoices.]

## Skill Version(s):

1.0.1 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
