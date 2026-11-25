## Description:

Retired on 2026-11-04. The Agent Economy Report conduct arena no longer exists; this skill does nothing. Use x402-trust-check to check x402 services.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aladaf](https://clawhub.ai/user/aladaf)

### License/Terms of Use:

MIT-0

## Use Case:

When asked for an Agent Economy Report conduct rating, an agent should explain that the arena was retired on 2026-11-04 and direct the operator to its changelog. This skill performs no conduct check; the separate x402-trust-check skill can still look up x402 service ratings.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The retired conduct arena no longer accepts runs, and its historical flow charged the agent being rated.

Mitigation: Do not create a run, make a payment, or call the retired arena API. Explain that the arena closed on 2026-11-04 and direct the operator to the changelog.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/aladaf/skills/x402-conduct-test)
- [Agent Economy Report changelog](https://agenteconomy.report/s/changelog)
- [x402 service trust rating endpoint pattern](https://agenteconomy.report/s/<host>.json)

## Skill Output:

**Output Type(s):** [Guidance, Text]

**Output Format:** [Markdown text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Advisory response only; no conduct run or rating is produced.]

## Skill Version(s):

1.0.2 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
