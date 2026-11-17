## Description:

Get current weather and forecasts with no API key required.

This skill is ready for commercial/non-commercial use.

## Publisher:

[litiao1224](https://clawhub.ai/user/litiao1224)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to retrieve current weather or forecasts through wttr.in, with Open-Meteo as a JSON fallback for programmatic weather data.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Weather lookups contact third-party services and can disclose the queried location plus normal request metadata such as IP address.

Mitigation: Avoid querying sensitive private locations when that disclosure is not acceptable, and review requests before execution.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/litiao1224/skills/weather-litiao)
- [wttr.in help](https://wttr.in/:help)
- [Open-Meteo documentation](https://open-meteo.com/en/docs)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Guidance]

**Output Format:** [Markdown with inline bash commands and weather API examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires curl for the wttr.in command examples; Open-Meteo fallback returns JSON.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact/_meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
