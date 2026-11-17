## Description:

Get current weather and forecasts (no API key required).

This skill is ready for commercial/non-commercial use.

## Publisher:

[tongguanghai](https://clawhub.ai/user/tongguanghai)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, and agents use this skill to look up current weather and forecasts for a requested place. It provides curl-based commands for quick human-readable results from wttr.in and JSON weather data from Open-Meteo.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Weather queries may send requested locations or coordinates to public weather services.

Mitigation: Use only locations or coordinates that are acceptable to disclose to wttr.in or Open-Meteo; avoid sensitive addresses or private coordinates.

## Reference(s):

- [Weather Test on ClawHub](https://clawhub.ai/tongguanghai/skills/weather-test1)
- [wttr.in help](https://wttr.in/:help)
- [Open-Meteo Forecast API documentation](https://open-meteo.com/en/docs)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown with inline bash code blocks and optional JSON API responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires curl for command examples; no API key is requested.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact _meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
