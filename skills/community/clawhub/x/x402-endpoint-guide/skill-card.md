## Description:

Guides developers through building, hosting, and listing a paid x402 API endpoint that accepts per-call USDC payments.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mykel1283nelson-hub](https://clawhub.ai/user/mykel1283nelson-hub)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this guide to create an x402-gated API, plan USDC-per-call pricing and hosting, and make the endpoint discoverable to agents.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A valid payment authorization may be reused for multiple calls without a fresh settled payment.

Mitigation: Require successful settlement before paid work and atomically reject reused payment identifiers or nonces.

Risk: An insufficiently checked facilitator response could grant access for the wrong payment terms.

Mitigation: Validate facilitator responses against the expected recipient, network, asset, and amount before granting access.

Risk: Payment details are shared with the facilitator.

Mitigation: Review or configure the facilitator and document what payment data leaves the system.

## Reference(s):

- [Imported skill source](https://github.com/mykel1283nelson-hub/citruscoastai/tree/main/skills/x402-endpoint-guide)
- [Live reference endpoint](https://citrus-coast-ai-teardown.onrender.com)
- [x402 facilitator endpoint](https://x402.org/facilitator/verify)

## Skill Output:

**Output Type(s):** [Code, Configuration instructions, Guidance]

**Output Format:** [Markdown with Python code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes an illustrative payment gate, hosting and discovery guidance; the sample is not production-ready payment code.]

## Skill Version(s):

0.1.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
