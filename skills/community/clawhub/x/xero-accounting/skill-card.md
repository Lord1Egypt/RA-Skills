## Description:

Manage invoices, contacts, bills, payments, and accounting records in Xero via the Xero API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hith3sh](https://clawhub.ai/user/hith3sh)

### License/Terms of Use:

MIT-0

## Use Case:

External users and accounting operators use this skill to manage Xero invoices, contacts, bills, payments, and accounting records from an agent chat after connecting their Xero organization through OAuth.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can read and change financial records in the connected Xero organization.

Mitigation: Install only when the user intends to connect ClawLink to Xero, and review write previews before approving invoices, bills, payments, deletes, voids, journals, or account changes.

Risk: Accounting changes can affect tax, currency, and financial reporting outcomes.

Mitigation: Verify important tax, currency, and reporting effects in Xero before relying on or approving changes.

## Reference(s):

- [ClawHub Xero Skill](https://clawhub.ai/hith3sh/skills/xero-accounting)
- [Xero API Documentation](https://developer.xero.com/documentation/)
- [Xero API Overview](https://developer.xero.com/documentation/api/overview)
- [Xero OAuth Guide](https://developer.xero.com/documentation/auth-and-reporting/xero-oauth2)
- [ClawLink OpenClaw Docs](https://docs.claw-link.dev/openclaw)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and tool-call guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include previews and confirmation requests before write operations that affect accounting records.]

## Skill Version(s):

1.0.6 (source: server evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
