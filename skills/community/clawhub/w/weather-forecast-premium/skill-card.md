## Description:

Provides current weather, multi-day forecasts, air quality, UV index, and severe weather alerts for a requested location through a curl-accessible weather API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[splint3r](https://clawhub.ai/user/splint3r)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to fetch and format weather conditions, forecasts, air quality, UV index, and alert information for user-provided locations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Untrusted location text may be substituted directly into shell command examples, creating command injection risk.

Mitigation: Encode or otherwise safely pass the location value as data before running curl commands, and do not execute commands built from adversarial location strings.

Risk: Weather lookups depend on an unofficial api.openmeteo-api.com wrapper and upstream weather services.

Mitigation: Use the skill only where that third-party wrapper is trusted, and verify important weather results against upstream sources when accuracy matters.

## Reference(s):

- [Weather Forecast Premium on ClawHub](https://clawhub.ai/splint3r/skills/weather-forecast-premium)
- [Weather Forecast Plus API Reference](references/api.md)
- [OpenMeteo API Wrapper Homepage](https://openmeteo-api.com)
- [Open-Meteo](https://open-meteo.com)
- [wttr.in](https://wttr.in)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown with inline shell commands and weather API JSON summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires curl; responses depend on the third-party wrapper and upstream weather services.]

## Skill Version(s):

1.0.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
