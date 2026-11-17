## Description:

Uses the QWeather API to answer weather, forecast, precipitation, wind, alert, and air quality questions for locations in China.

This skill is ready for commercial/non-commercial use.

## Publisher:

[royalmetoo](https://clawhub.ai/user/royalmetoo)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agent builders use this skill to retrieve and format QWeather data for Chinese cities, including current conditions, hourly and daily forecasts, air quality, and weather alerts.

### Deployment Geography for Use:

China

## Known Risks and Mitigations:

Risk: A configured QWeather API key is stored locally and can be exposed through committed files, broad filesystem access, or shared command output.

Mitigation: Keep the real key out of version control, restrict access to qweather_config.json, and avoid sharing logs or full request URLs that include the key.

Risk: Weather responses may be incomplete or unavailable if QWeather returns errors or omits fields.

Mitigation: Follow the skill behavior of omitting missing fields, stopping on failed city lookup, and citing QWeather as the data source.

## Reference(s):

- [QWeather API Reference](artifact/references/api_reference.md)
- [QWeather Developer Console](https://console.qweather.com)
- [ClawHub Skill Page](https://clawhub.ai/royalmetoo/skills/qweather-query)

## Skill Output:

**Output Type(s):** [Markdown, API Calls, Configuration instructions, Guidance]

**Output Format:** [Markdown]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs cite QWeather as the data source, omit missing fields, and only support cities in China.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
