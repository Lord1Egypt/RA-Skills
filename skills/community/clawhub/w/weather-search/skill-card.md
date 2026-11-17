## Description:

Query real-time weather information using Amap (Gaode Maps) Weather API for weather, temperature, wind, and humidity in Chinese cities.

This skill is ready for commercial/non-commercial use.

## Publisher:

[george-china](https://clawhub.ai/user/george-china)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to look up current Amap weather data for Chinese cities by city name or city code. It is useful for answering user questions about conditions such as temperature, wind, humidity, and weather status.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Weather queries and optional coordinate lookups share city or location data with Amap.

Mitigation: Use the skill only when Amap is an acceptable weather provider and avoid precise coordinates unless they are needed for the task.

Risk: The Amap API key may appear in command-line arguments, logs, or monitoring output.

Mitigation: Use a restricted, low-quota AMAP_API_KEY and rotate it if logs or monitoring systems may have captured it.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/george-china/skills/weather-search)
- [Amap Weather API Documentation](https://lbs.amap.com/api/javascript-api/guide/services/weather)
- [Amap Developer Console](https://console.amap.com/)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration]

**Output Format:** [Markdown guidance with shell commands and JSON weather API responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires curl and an AMAP_API_KEY environment variable; optional pretty and human-readable script output may use jq when available.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
