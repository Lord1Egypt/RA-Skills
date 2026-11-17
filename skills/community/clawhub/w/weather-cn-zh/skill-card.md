## Description:

Gets current weather and forecasts using Moji Weather as the primary source and MSN China Weather as a fallback.

This skill is ready for commercial/non-commercial use.

## Publisher:

[paudyyin](https://clawhub.ai/user/paudyyin)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to answer current weather, temperature, and forecast questions for China-focused locations using Moji Weather or MSN China Weather. It is not intended for historical weather, severe weather alerts, or detailed meteorological analysis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Weather lookups may send location-based queries to Moji Weather or MSN China Weather.

Mitigation: Use this skill only when those weather providers are acceptable for the requested location query, and disclose the data source in responses.

Risk: The skill is not designed for severe weather alerts, historical weather, or detailed meteorological analysis.

Mitigation: Route safety-critical, historical, or specialist meteorology requests to authoritative weather services instead of this skill.

## Reference(s):

- [Moji Weather](https://tianqi.moji.com/)
- [MSN China Weather](https://www.msn.cn/zh-cn/weather/)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown text with sourced weather observations and forecasts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes source attribution and caveats when provider data differs.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
