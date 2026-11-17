## Description:

Manage Razorpay customers, orders, invoices, payment links, refunds, payouts, and payment operations via the Razorpay API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hith3sh](https://clawhub.ai/user/hith3sh)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to inspect and manage Razorpay payment data, create orders and invoices, issue refunds, manage payment links, and automate payout-related workflows through ClawLink tools.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill relies on a third-party plugin to handle Razorpay credentials and payment data.

Mitigation: Install only after verifying the publisher and version, reviewing granted Razorpay scopes, and confirming how to revoke the connection and remove the plugin.

Risk: Write, refund, payout, invoice, and payment-link actions can affect real money or customer records.

Mitigation: Confirm the target resource, amount, customer details, and intended effect before every write or money-affecting action.

Risk: Server-resolved GitHub import provenance is unavailable for this version.

Mitigation: Do not infer source provenance from the skill text; review the ClawHub publisher, release version, and artifact contents before deployment.

## Reference(s):

- [Razorpay API Documentation](https://razorpay.com/docs/api/)
- [Razorpay Orders API](https://razorpay.com/docs/api/payments/orders/)
- [Razorpay Invoices API](https://razorpay.com/docs/api/invoices/)
- [ClawLink OpenClaw Docs](https://docs.claw-link.dev/openclaw)
- [ClawLink Verification](https://claw-link.dev/verify)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with shell command examples and JSON tool parameters]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Tool execution should use the live Razorpay tool catalog and explicit confirmation for write or money-affecting actions.]

## Skill Version(s):

1.0.6 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
