## Description:

Real-time institutional transaction monitoring.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ssidharhubble](https://clawhub.ai/user/ssidharhubble)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to request real-time institutional transaction signals for a supplied asset ticker. It may return market-signal JSON or a payment-required response for premium signals.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill contacts an external API with the requested ticker, and the remote dependency is under-disclosed.

Mitigation: Review the endpoint and network behavior before installing, and use the skill only if the publisher and API are trusted.

Risk: The skill can show a cryptocurrency payment instruction with a fixed wallet address.

Mitigation: Do not allow an agent to act on the payment message automatically; verify the endpoint, wallet recipient, and payment terms manually.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ssidharhubble/skills/whale-scanner)
- [Publisher profile](https://clawhub.ai/user/ssidharhubble)
- [Premium signal pricing](https://ssyopros.zo.space/pricing)
- [Whale signal API endpoint](https://x402-money-machine-api-ssyopros.zocomputer.io/api/whale/{ticker})

## Skill Output:

**Output Type(s):** [JSON, guidance]

**Output Format:** [JSON object from the remote signal API, or a payment-required guidance object]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Input is a single asset ticker; output depends on the remote API response and payment status.]

## Skill Version(s):

1.1.2 (source: server-resolved release metadata; artifact/package.json reports 1.1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
