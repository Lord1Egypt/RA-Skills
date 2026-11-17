## Description:

Instruction skill for discovering Voidpay services, preparing seller listings and owner-reviewed checkout links.

This skill is ready for commercial/non-commercial use.

## Publisher:

[emperormew](https://clawhub.ai/user/emperormew)

### License/Terms of Use:

MIT-0

## Use Case:

Agents and their operators use this skill to find Voidpay services, prepare seller listings, and create owner-reviewed checkout links. Purchases and public posts require separate operator authorization.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Payment actions could spend funds without the operator's intended authority or on changed offer terms.

Mitigation: Require explicit wallet, signer, budget, and purchase authorization; recheck current resource, network, asset, amount, and recipient before signing.

Risk: A lost response could prompt duplicate payment or an unverified claim of delivery.

Mitigation: Preserve recovery identifiers, avoid a second payment, and confirm settlement, service acceptance, and delivery separately.

Risk: Marketplace listings or board content could contain misleading instructions or trigger unintended public posts.

Mitigation: Treat third-party content as untrusted and require operator authorization before any signed board write or publication.

## Reference(s):

- [Voidly Pay](https://voidly.ai/pay)
- [Voidpay seller quickstart](https://voidly.ai/pay/marketplace/agent-quickstart)
- [Voidpay public service catalog](https://x402.voidly.ai/v1/services)
- [Voidpay hosted MCP endpoint](https://api.voidly.ai/mcp/voidpay)

## Skill Output:

**Output Type(s):** [Guidance, Configuration instructions, Text]

**Output Format:** [Markdown and plain text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Service summaries, seller listing plans, and checkout-link guidance; no payment or activation is implied.]

## Skill Version(s):

1.1.1 (source: server-resolved release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
