## Description:

Queries the weather forecast for a specified city and returns weather conditions and a temperature range.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yuancaihua](https://clawhub.ai/user/yuancaihua)

### License/Terms of Use:


## Use Case:

External users and agents use this skill to answer weather questions by parsing a requested city and date, calling a weather API, and returning a concise forecast summary.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: An embedded Weather.com API key may be exposed or misused.

Mitigation: Replace the embedded key with a user-controlled secret or platform-managed credential before use.

Risk: Weather queries are sent to an external Weather.com service.

Mitigation: Document the provider and data flow, and send only city and date data appropriate for that provider.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/yuancaihua/skills/weather-query-ych)

## Skill Output:

**Output Type(s):** [text]

**Output Format:** [Plain text weather summary]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes city, date, weather status, and temperature range when available.]

## Skill Version(s):

1.0.0 (source: server release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
