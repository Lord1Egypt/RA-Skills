## Description:

Despite the QuickBooks-themed release name, the artifact content describes a CreditClaw payment skill that lets an agent shop online with guardrailed wallets, multiple payment methods, and owner approval.

This skill is ready for commercial/non-commercial use.

## Publisher:

[triplehippo](https://clawhub.ai/user/triplehippo)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers would use this skill to let an agent register and operate a CreditClaw wallet, check spending permissions, request owner approvals, make purchases, and create checkout or payment links. It is appropriate only where real-money payment authority and related buyer or card data handling are explicitly approved by the owner.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill gives an agent broad real-money payment and card-handling authority.

Mitigation: Use only in an isolated payment environment with restricted network and filesystem access, and require explicit owner control for purchases, invoices, public shop publishing, and webhook fulfillment.

Risk: The security evidence reports reliance on mutable remote instructions and locally executed remote-delivered code.

Mitigation: Pin and review artifact content before use, and avoid executing mutable server-delivered scripts or natural-language tasks without validation.

Risk: Leaking CREDITCLAW_API_KEY could enable unauthorized spending or wallet access.

Mitigation: Store the key only in a secure secrets manager and send it only to creditclaw.com endpoints required by the reviewed artifact.

Risk: Checkout, invoice, buyer, shipping, and webhook flows can affect privacy and fulfillment outcomes.

Mitigation: Apply owner approval, data-minimization, and reconciliation checks before sending invoices, publishing shops, storing buyer data, or fulfilling webhook-triggered actions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/triplehippo/skills/qb)
- [CreditClaw main skill documentation](https://creditclaw.com/creditcard/skill.md)
- [CreditClaw package metadata](https://creditclaw.com/creditcard/skill.json)
- [CreditClaw checkout guide](https://creditclaw.com/creditcard/checkout.md)
- [CreditClaw encrypted card guide](https://creditclaw.com/creditcard/encrypted-card.md)
- [CreditClaw wallet management guide](https://creditclaw.com/creditcard/management.md)
- [CreditClaw spending permissions guide](https://creditclaw.com/creditcard/spending.md)
- [CreditClaw heartbeat guide](https://creditclaw.com/creditcard/heartbeat.md)
- [CreditClaw Crossmint wallet guide](https://creditclaw.com/creditcard/crossmint-wallet.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance, API calls]

**Output Format:** [Markdown guidance with curl commands, JSON examples, and configuration instructions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires CREDITCLAW_API_KEY and network access to creditclaw.com; no fixed token or file output contract.]

## Skill Version(s):

1.0.6 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
