## Description:

Command-line weather checker tool with global city support, temperature, precipitation, and probability display with emoji formatting.

This skill is ready for commercial/non-commercial use.

## Publisher:

[luckisnow](https://clawhub.ai/user/luckisnow)

### License/Terms of Use:

MIT

## Use Case:

External users and developers use this skill to query current and forecast weather for global cities from the command line, with readable text output or structured JSON for downstream use.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Installation instructions download mutable remote code.

Mitigation: Use the bundled reviewed script or a pinned, checksummed release before installation.

Risk: Optional system-wide installation uses sudo.

Mitigation: Prefer a virtual environment and a user-local command path.

Risk: City searches and coordinates are sent to Open-Meteo APIs.

Mitigation: Disclose this data flow to users and avoid submitting sensitive location queries.

## Reference(s):

- [Weather Checker on ClawHub](https://clawhub.ai/luckisnow/skills/weather-checker)
- [Open-Meteo API](https://open-meteo.com/)
- [Open-Meteo Geocoding API](https://geocoding-api.open-meteo.com/v1/search)
- [Open-Meteo Forecast API](https://api.open-meteo.com/v1/forecast)

## Skill Output:

**Output Type(s):** [Text, JSON, Shell commands, Guidance]

**Output Format:** [CLI text, single-line summaries, JSON objects, and Markdown usage examples with shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Weather requests may send city names and coordinates to Open-Meteo APIs.]

## Skill Version(s):

1.0.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
