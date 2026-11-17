## Description:

获取天气预报和气温信息。使用场景：用户询问天气、温度、降雨、出行建议等。支持通过 wttr.in 查询全球城市天气，无需 API Key。

This skill is ready for commercial/non-commercial use.

## Publisher:

[anmu14641](https://clawhub.ai/user/anmu14641)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to answer current weather, temperature, rain, and travel-planning questions for global cities by querying wttr.in with curl. It is not intended for historical weather data, severe weather alerts, or meteorological analysis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Weather lookups contact wttr.in and disclose the queried location string to that external service.

Mitigation: Avoid exact home addresses or other sensitive locations unless that disclosure is acceptable.

Risk: The skill depends on wttr.in availability, rate limits, and network stability.

Mitigation: Retry transient failures and avoid high-frequency automated requests.

Risk: The skill is not designed for severe weather alerts or meteorological analysis.

Mitigation: Use official meteorological or emergency sources for hazardous-weather decisions.

## Reference(s):

- [wttr.in weather service](https://wttr.in/:help)
- [ClawHub skill page](https://clawhub.ai/anmu14641/skills/tianqi-weather)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown guidance with inline curl commands and wttr.in format examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Weather results depend on wttr.in availability, rate limits, network stability, and the queried location string.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact _meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
