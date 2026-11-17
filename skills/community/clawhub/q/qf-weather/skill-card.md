## Description:

Provides real-time weather, hourly forecasts, and seven-day forecasts by city name, coordinates, or IP-derived location using public wttr.in and Open-Meteo weather services.

This skill is ready for commercial/non-commercial use.

## Publisher:

[371166758-qq](https://clawhub.ai/user/371166758-qq)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and end users can ask an agent for current conditions and short-range forecasts for a city, coordinates, or the current network-derived location without configuring a weather API key.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Weather queries may disclose city names, coordinates, or IP-derived location data to public weather services.

Mitigation: Avoid querying sensitive locations unless disclosure to public weather services is acceptable.

Risk: Public weather services can be slow or unavailable, and forecast precision can vary by location input.

Mitigation: Treat weather responses as advisory and retry or cross-check when availability or accuracy matters.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/371166758-qq/skills/qf-weather)
- [wttr.in weather service](https://wttr.in)
- [Open-Meteo weather service](https://open-meteo.com)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown or plain text with optional inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Weather results may depend on public service availability and location lookup precision.]

## Skill Version(s):

1.0.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
