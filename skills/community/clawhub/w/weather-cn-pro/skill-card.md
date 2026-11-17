## Description:

weather-cn-pro queries China Weather for Chinese city current weather, hourly forecasts, seven-day forecasts, and lifestyle indexes without requiring an API key.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ziqi-jin](https://clawhub.ai/user/ziqi-jin)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to run a local Bash weather lookup for supported Chinese city names and receive formatted current conditions, hourly forecasts, seven-day forecasts, and lifestyle indexes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The script uses eval on data parsed from a remote weather page, which could allow command execution if that page or connection is compromised.

Mitigation: Review and modify the script to parse weather fields without eval before installing or running it in a trusted environment.

Risk: The artifact includes an AQI function that is not part of the documented normal weather lookup flow.

Mitigation: Document, remove, or review the AQI function before broader use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ziqi-jin/skills/weather-cn-pro)
- [China Weather data source](https://www.weather.com.cn/)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Guidance]

**Output Format:** [Terminal text with formatted weather sections]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires curl and grep; accepts a supported Chinese city name as input.]

## Skill Version(s):

1.0.0 (source: server release metadata and script header)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
