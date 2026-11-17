## Description:

Get weather data from wttr.in free service. Triggers on: weather, forecast, temperature, rain, UV, humidity, wind. Free, no API key required. Python 3.6+, no pip packages. Works on Windows/macOS/Linux.

This skill is ready for commercial/non-commercial use.

## Publisher:

[etmnb](https://clawhub.ai/user/etmnb)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to retrieve current weather and short-term forecasts for explicit locations, coordinates, or an IP-inferred location without configuring an API key.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Weather queries are sent to wttr.in, and omitting a location allows the service to infer location from the requesting IP address.

Mitigation: Use an explicit city or coordinate location when IP-based location inference is not desired.

Risk: Forecast results depend on the availability and accuracy of the external wttr.in service.

Mitigation: Review returned weather information before relying on it for user-facing or operational decisions.

## Reference(s):

- [wttr.in](https://wttr.in)
- [ClawHub Skill Page](https://clawhub.ai/etmnb/skills/weather-wttr-in)
- [Publisher Profile](https://clawhub.ai/user/etmnb)

## Skill Output:

**Output Type(s):** [Text, JSON, Shell commands, Guidance]

**Output Format:** [Plain text forecast summaries or JSON weather data]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses Python 3.6+ standard library only; returns exit code 0 on success and 1 on failure.]

## Skill Version(s):

1.1.1 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
