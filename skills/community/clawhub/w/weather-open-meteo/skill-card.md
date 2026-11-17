## Description:

Get current weather and forecasts via open-meteo.com with optional fallback to wttr.in if available. No API key required.

This skill is ready for commercial/non-commercial use.

## Publisher:

[vdiogov](https://clawhub.ai/user/vdiogov)

### License/Terms of Use:


## Use Case:

External users, developers, and agents use this skill to answer current weather, forecast, temperature, and rain-probability requests for a provided location. It uses Open-Meteo as the primary public weather source and wttr.in as an optional fallback.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Weather lookups send searched locations to external weather services.

Mitigation: Avoid using private or sensitive locations unless external API sharing is acceptable.

Risk: The wttr.in fallback examples include plaintext HTTP or scheme-less URLs.

Mitigation: Prefer the HTTPS Open-Meteo examples and change wttr.in fallback URLs to explicit https:// before use.

## Reference(s):

- [Weather Open-Meteo Skill Page](https://clawhub.ai/vdiogov/skills/weather-open-meteo)
- [vdiogov Publisher Profile](https://clawhub.ai/user/vdiogov)
- [Open-Meteo](https://open-meteo.com/)
- [Open-Meteo API Documentation](https://open-meteo.com/en/docs)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown guidance with inline bash commands and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires curl and jq; no API key required.]

## Skill Version(s):

0.1.5 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
