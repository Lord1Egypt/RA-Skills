## Description:

Drafts SuperBooks invoices from customer details or tracked time, creates customers when needed, and sends invoices only after explicit confirmation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[devino](https://clawhub.ai/user/devino)

### License/Terms of Use:

MIT-0

## Use Case:

Business owners and bookkeepers use this skill to prepare SuperBooks invoices from customer requests or tracked time, create missing customers, and send approved invoices after a separate confirmation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can access customer and tracked-time data and create customer records or invoice drafts.

Mitigation: Use an appropriate SuperBooks account and review customer, line items, amounts, and due date before approving a draft.

Risk: Sending an invoice emails the customer.

Mitigation: Require a separate explicit confirmation naming the invoice and recipient before sending.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/devino/skills/superbooks-drafting-invoices)

## Skill Output:

**Output Type(s):** [Text, Guidance]

**Output Format:** [Markdown]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports draft details and invoice status; delivery requires separate confirmation.]

## Skill Version(s):

1.0.1 (source: ClawHub release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
