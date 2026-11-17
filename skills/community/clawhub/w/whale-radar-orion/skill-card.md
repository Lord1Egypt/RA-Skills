## Description:

Detects large cbBTC whale movements on Base within a four-hour window and summarizes whether activity suggests accumulation, distribution, or neutral market signals.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kokoju007](https://clawhub.ai/user/kokoju007)

### License/Terms of Use:

MIT-0

## Use Case:

External crypto-market users and agent operators use this skill to request high-level cbBTC whale activity summaries on Base and route to Orion ACP for paid detailed transaction data when needed.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Free whale-event classifications may be unreliable as financial signals unless current on-chain data is verified.

Mitigation: Verify live Base cbBTC activity with a trusted on-chain data source before acting on the signal.

Risk: The skill routes users toward paid ACP offerings for external transaction data.

Mitigation: Review the ACP purchase details and expected data before paying for enhanced signals.

## Reference(s):

- [Orion ACP listing](https://app.virtuals.io/virtuals/1809)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown or plain text summary]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include whale-event status, direction hint, one-line summary, example output, and paid ACP offering names.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
