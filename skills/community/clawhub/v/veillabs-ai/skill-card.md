## Description:

Interact with the Veillabs privacy-focused DEX API for cross-chain swaps, private seed distributions, and transaction tracking.

This skill is ready for commercial/non-commercial use.

## Publisher:

[veillabsapp](https://clawhub.ai/user/veillabsapp)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users use this skill to query Veillabs token data, prepare cross-chain swaps or multi-destination seed distributions, and track transaction status through the Veillabs API.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can create cryptocurrency swap or distribution orders.

Mitigation: Require explicit user confirmation before any POST request that creates a swap or distribution, and verify destination addresses and amounts before submission.

Risk: A configurable API endpoint can send wallet and transaction details to an unintended host.

Mitigation: Use the official HTTPS Veillabs API endpoint unless intentionally developing locally, and review VEILLABS_BASE_URL before use.

Risk: Users may provide secrets that the Veillabs API skill does not require.

Mitigation: Do not provide private keys, seed phrases, or wallet credentials to this skill.

## Reference(s):

- [Veillabs API Reference](references/api-reference.md)
- [Veillabs Homepage](https://trade.veillabs.app)
- [ClawHub Skill Listing](https://clawhub.ai/veillabsapp/skills/veillabs-ai)

## Skill Output:

**Output Type(s):** [guidance, markdown, shell commands, configuration, JSON]

**Output Format:** [Markdown guidance with JSON request examples and optional shell commands.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires VEILLABS_BASE_URL and veillabs.enabled when configured.]

## Skill Version(s):

1.0.1 (source: server release metadata; artifact metadata.openclaw.version is 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
