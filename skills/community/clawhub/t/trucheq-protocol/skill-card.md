## Description:

Interact with TruCheq P2P commerce protocol - browse verified marketplace listings, chat with sellers via XMTP, pay via x402 on Base.

This skill is ready for commercial/non-commercial use.

## Publisher:

[vduda](https://clawhub.ai/user/vduda)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, and marketplace agents use this skill to browse P2P listings, inspect seller trust indicators, create listings, exchange XMTP messages, and prepare x402 payments through the configured TruCheq API.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Identity proofs, images, messages, wallet addresses, and payment data are routed through the configured TruCheq API endpoint.

Mitigation: Use only a trusted HTTPS TRUCHEQ_API_URL and confirm where sensitive identity, listing, messaging, wallet, and payment data will be sent before using the skill.

Risk: Marketplace purchases involve direct seller payments without escrow.

Mitigation: Independently verify listing details, seller address, chain, token, amount, and refund expectations before paying.

Risk: The skill is configured for Base Sepolia and XMTP dev environment behavior.

Mitigation: Confirm that testnet and development messaging settings match the intended transaction environment before executing marketplace flows.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/vduda/skills/trucheq-protocol)
- [Publisher Profile](https://clawhub.ai/user/vduda)

## Skill Output:

**Output Type(s):** [Guidance, API Calls, Shell commands, Configuration]

**Output Format:** [Markdown with HTTP examples, JSON snippets, and curl-oriented instructions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires curl plus TRUCHEQ_API_URL and XMTP_ENV configuration.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
