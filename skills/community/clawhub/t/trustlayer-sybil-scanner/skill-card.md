## Description:

Feedback forensics for ERC-8004 agents. Detects Sybil rings, fake reviews, rating manipulation, and reputation laundering across 20 chains. No API key needed.

This skill is ready for commercial/non-commercial use.

## Publisher:

[goatgaucho](https://clawhub.ai/user/goatgaucho)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to check ERC-8004 agent reputation, Sybil risk, rating manipulation signals, cross-chain reputation divergence, and reviewer quality before payments, escrow, hiring, or delegation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: TrustLayer API calls disclose chain IDs, agent IDs, and possibly wallet addresses to an external service.

Mitigation: Use the skill only with data appropriate to send to TrustLayer, and avoid submitting sensitive wallet or operator information without user approval.

Risk: Some endpoints are described as paid x402 endpoints and may trigger micropayment flows.

Mitigation: Confirm payment behavior before using paid endpoints, especially in environments that can automatically satisfy HTTP 402 payment requests.

Risk: Reputation and Sybil signals can be incomplete or change over time.

Mitigation: Present API results as risk guidance, include confidence and anomaly flags when available, and avoid treating one score as a definitive safety guarantee.

## Reference(s):

- [TrustLayer Homepage](https://thetrustlayer.xyz)
- [TrustLayer API Base](https://api.thetrustlayer.xyz)
- [ClawHub Skill Page](https://clawhub.ai/goatgaucho/skills/trustlayer-sybil-scanner)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown with inline shell commands and JSON API output summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May call TrustLayer external API endpoints with chain, agent ID, and wallet address inputs; no API key required for beta trust checks.]

## Skill Version(s):

4.1.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
