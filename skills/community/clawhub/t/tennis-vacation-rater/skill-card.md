## Description:

Evaluate tennis vacation destinations with structured scoring across transportation, accommodation, weather, and court facilities.

This skill is ready for commercial/non-commercial use.

## Publisher:

[edam17](https://clawhub.ai/user/edam17)

### License/Terms of Use:

MIT-0

## Use Case:

External users and travel-planning agents use this skill to compare tennis vacation destinations, rate transportation, lodging, weather, and court facilities, and generate concise destination reports with source labels for prices and missing data.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may ask an agent to check or run an unverified local flyai command for flight prices.

Mitigation: Prefer web-search-only use unless the flyai CLI provenance and installed version are verified before execution.

Risk: Travel links may be inaccessible, private, expired, or blocked by platforms, which can lead to unsupported destination assumptions.

Mitigation: Use the stop-and-ask protocol: rely on text provided by the user, request the destination and departure city when access fails, and label missing data.

Risk: Price-monitoring language may imply persistent automatic alerts that the artifact does not actually create.

Mitigation: Present price checks as one-time, on-demand checks during the current conversation and avoid claiming background monitoring.

## Reference(s):

- [Tennis Vacation Rater on ClawHub](https://clawhub.ai/edam17/skills/tennis-vacation-rater)
- [Dimension Details](references/dimension-details.md)
- [Price Monitoring Guide](references/price-monitoring-guide.md)
- [Report Templates](references/report-template.md)
- [Link Handling Guide](references/link-handling-guide.md)
- [Tennis Destinations Database](references/destinations.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown travel-rating report with scoring tables, source labels, optional shell commands, and booking guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports should label flight, hotel, weather, and court data sources and mark unavailable facts instead of inventing them.]

## Skill Version(s):

1.0.5 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
