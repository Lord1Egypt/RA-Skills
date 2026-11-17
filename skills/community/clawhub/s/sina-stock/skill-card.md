## Description:

Sina Stock helps agents retrieve real-time China A-share index and stock quote data from the Sina Finance API without an API key.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sunnyfo](https://clawhub.ai/user/sunnyfo)

### License/Terms of Use:

MIT

## Use Case:

Developers, analysts, and external users can use this skill to query China A-share market indices or individual stock quotes and receive current price, change, volume, turnover, and related quote fields. It is useful for quick market checks, watchlist monitoring, and simple data collection through a CLI workflow.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Queried A-share stock codes are sent to Sina Finance over the network.

Mitigation: Use the skill only where outbound requests to Sina Finance are approved, and avoid it in restricted, regulated, or air-gapped environments unless that egress is authorized.

Risk: Market quote data may be delayed, unavailable outside trading hours, or unsuitable as investment advice.

Mitigation: Treat results as informational quote data, verify important decisions against authoritative financial sources, and do not rely on the skill for investment recommendations.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/sunnyfo/skills/sina-stock)
- [Sina Finance](https://finance.sina.com.cn/)

## Skill Output:

**Output Type(s):** [text, json, shell commands, guidance]

**Output Format:** [Plain text, JSON, or simplified text from CLI commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires outbound network access to Sina Finance; no API key is required.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
