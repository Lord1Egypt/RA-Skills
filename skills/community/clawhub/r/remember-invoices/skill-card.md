## Description:

Billing memory that tracks invoices, payment status, and follow-ups so revenue is never lost in a thread.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bluecolumnconsulting-lgtm](https://clawhub.ai/user/bluecolumnconsulting-lgtm)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and business teams configuring billing agents use this skill to record invoices, recall outstanding or overdue balances, and update payment follow-up notes in conversation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends detailed invoice, customer, and payment-status information to BlueColumn's hosted service.

Mitigation: Install only after organizational approval for sending billing records to BlueColumn, and confirm retention, deletion, access controls, and customer-data processing terms before using real billing data.

Risk: Invoice records may include sensitive banking, contract, or customer information beyond what the workflow requires.

Mitigation: Use data minimization: avoid bank details, full contracts, and unnecessary prior messages, and store only the invoice and follow-up fields needed for the billing task.

Risk: API credentials could expose billing-memory operations if overbroad or mishandled.

Mitigation: Use narrowly scoped BlueColumn API keys, keep them out of prompts and logs, and rotate or revoke them when access changes.

## Reference(s):

- [BlueColumn API reference](https://bluecolumn.ai/docs)
- [ClawHub skill page](https://clawhub.ai/bluecolumnconsulting-lgtm/skills/remember-invoices)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown with inline bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires BLUECOLUMN_API_KEY and sends invoice and customer billing records to BlueColumn-hosted API endpoints.]

## Skill Version(s):

1.0.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
