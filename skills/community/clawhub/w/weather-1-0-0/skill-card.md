## Description:

Provide current weather and forecasts using wttr.in and Open-Meteo APIs without requiring an API key.

This skill is ready for commercial/non-commercial use.

## Publisher:

[99percentgod](https://clawhub.ai/user/99percentgod)

### License/Terms of Use:


## Use Case:

External users and developers use this skill to request current weather, forecasts, and weather API lookup guidance for city names, airport codes, or coordinates.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Weather lookups disclose the requested city, airport code, or coordinates to wttr.in or Open-Meteo.

Mitigation: Avoid sensitive personal details in query strings and use only locations or coordinates appropriate to share with the selected public weather service.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/99percentgod/skills/weather-1-0-0)
- [wttr.in help](https://wttr.in/:help)
- [Open-Meteo forecast API documentation](https://open-meteo.com/en/docs)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, JSON, Files]

**Output Format:** [Markdown guidance with inline shell commands, plain-text or JSON weather responses, and optional PNG image output.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires curl; no API key is required; weather requests are sent to wttr.in or Open-Meteo.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact _meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
