## Description:

Get current weather and forecasts (no API key required).

This skill is ready for commercial/non-commercial use.

## Publisher:

[asterisk622](https://clawhub.ai/user/asterisk622)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to retrieve current weather, compact forecasts, and programmatic weather data for requested locations, airport codes, or coordinates.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Location, airport code, or coordinate queries are sent to public weather services.

Mitigation: Avoid submitting sensitive or precise private locations unless that disclosure is acceptable for the use case.

Risk: Weather responses depend on external public services and may be unavailable, delayed, or inaccurate.

Mitigation: Check returned data before using it in high-impact decisions and fall back to Open-Meteo when wttr.in is unsuitable.

## Reference(s):

- [wttr.in help](https://wttr.in/:help)
- [Open-Meteo forecast API example](https://api.open-meteo.com/v1/forecast?latitude=51.5&longitude=-0.12&current_weather=true)
- [Open-Meteo documentation](https://open-meteo.com/en/docs)
- [ClawHub skill page](https://clawhub.ai/asterisk622/skills/xiaoding-weather)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline bash commands and API URLs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce plain-text weather summaries, JSON weather responses, or PNG weather output depending on the requested service and URL options.]

## Skill Version(s):

1.0.3 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
