## Description:

Helps personal-agent users choose an SCVD signed good, obtain a free quote, approve any wallet funding and purchase, and verify delivery.

This skill is ready for commercial/non-commercial use.

## Publisher:

[seancrecord](https://clawhub.ai/user/seancrecord)

### License/Terms of Use:

MIT-0

## Use Case:

Personal-agent users can compare current SCVD offerings, rehearse a purchase without spending, or authorize a specific x402 purchase and verify its receipt.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A payment or wallet funding could spend funds beyond the user's intent.

Mitigation: Obtain separate funding and purchase approvals for a specific current quote, verify its network and amount, and cap spending at the approved amount.

Risk: Wallet secrets or recovery credentials could be exposed in chat.

Mitigation: Use the provider's secure authentication flow; never request or paste seed phrases, private keys, recovery tokens or API credentials.

Risk: An untrusted wallet integration or incompatible client could mishandle payment.

Mitigation: Install only a trusted release, inspect the referenced wallet skill, and confirm the client's x402 scheme, network and asset against the fresh quote before signing.

Risk: Retrying after an uncertain paid response could result in a duplicate charge.

Mitigation: Preserve the original request and idempotency key, check payment or recovery status, and do not initiate a fresh charge solely because the response was lost.

## Reference(s):

- [SCVD store](https://scvd.store)
- [SCVD current menu](https://scvd.store/menu.json)
- [Host connection and rehearsal guidance](references/hosts.md)
- [Wallet compatibility and setup](references/wallet.md)
- [Coinbase Agentic Wallet x402 payment guide](https://docs.cdp.coinbase.com/agentic-wallet/cli/skills/pay-for-service)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Shell commands]

**Output Format:** [Markdown text with purchase plans, quote details, optional setup commands and receipt summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May report an unsigned quote or no-spend plan; a paid receipt requires separate user approval and a compatible payment client.]

## Skill Version(s):

1.0.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
