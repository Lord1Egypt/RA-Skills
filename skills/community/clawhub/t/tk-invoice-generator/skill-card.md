## Description:

Generate professional invoices from project data, including line items, tax calculation, payment terms, formatted output, outstanding invoice tracking, and payment reminders.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tktk-ai](https://clawhub.ai/user/tktk-ai)

### License/Terms of Use:

MIT-0

## Use Case:

External freelancers, agencies, consultants, and business operators use this skill to draft invoices, calculate totals, set payment terms, identify overdue invoices, and draft reminder emails.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Invoices can contain client addresses, email addresses, payment links, bank details, invoice history, and contract terms.

Mitigation: Treat invoice inputs and outputs as sensitive business data; redact unnecessary details before sharing and avoid retaining account numbers or confidential terms unless retention is intentional.

Risk: Generated invoice totals, tax amounts, due dates, and late-fee language may be inaccurate if the user provides incomplete data or local requirements differ.

Mitigation: Review calculations, payment terms, and tax treatment before sending invoices or reminders.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/tktk-ai/skills/tk-invoice-generator)
- [ClawHub publisher profile](https://clawhub.ai/user/tktk-ai)
- [clawhub.com](https://clawhub.com)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown-style invoice drafts, reports, and reminder email text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include calculated subtotals, tax, discounts, totals, due dates, payment terms, and reminder language based on user-provided billing data.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
