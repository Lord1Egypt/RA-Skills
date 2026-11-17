## Description:

Scans a Solana public wallet address for estimated reclaimable SOL from dormant token accounts and program buffer accounts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nedim1511](https://clawhub.ai/user/nedim1511)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to check a Solana public wallet address for estimated reclaimable SOL and explain the result. The skill requires consent before sending the public address to the Unclaimed SOL API.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The scan sends a public Solana wallet address to unclaimedsol.com and directs users toward a third-party wallet-connection flow.

Mitigation: Disclose the API call, obtain consent before scanning, and avoid encouraging wallet connection or transaction signing unless the user independently trusts the service.

Risk: The skill depends on the Unclaimed SOL API response for claimable SOL estimates and fee-adjusted totals.

Mitigation: Present scan results as estimates, preserve the returned precision, disclose that totals are net of fees, and reference the published fee schedule.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/nedim1511/skills/unclaimed-sol-scanner)
- [Unclaimed SOL](https://unclaimedsol.com)
- [Unclaimed SOL privacy policy](https://blog.unclaimedsol.com/privacy-policy/)
- [Unclaimed SOL fee schedule](https://unclaimedsol.com/fees/)

## Skill Output:

**Output Type(s):** [text, markdown, JSON, shell commands, guidance]

**Output Format:** [Markdown summary with JSON scan results and inline shell command usage]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a Solana public key and user consent before the external API call.]

## Skill Version(s):

1.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
