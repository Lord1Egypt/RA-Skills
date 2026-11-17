## Description:

Fetch historical or forecast weather by location or coordinates via Open-Meteo. No API key needed.

This skill is ready for commercial/non-commercial use.

## Publisher:

[minshi-veyt](https://clawhub.ai/user/minshi-veyt)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, analysts, and agents use this skill to fetch recent historical observations or upcoming forecasts by place name or coordinates. It returns daily weather, precipitation, ET0, evaporation, and cumulative water-balance data for planning workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Location names or coordinates provided to the skill may be sent to Open-Meteo services.

Mitigation: Avoid submitting sensitive or unnecessarily precise locations, and disclose the third-party weather service when using the output in user-facing workflows.

Risk: Python dependencies are not fully pinned in the artifact requirements.

Mitigation: Install in an isolated Python environment and pin dependencies or add a lockfile before repeatable deployment.

Risk: The artifact performs live HTTP requests and the security guidance notes that request timeouts should be added for automation.

Mitigation: Add explicit request timeouts before running the scripts in scheduled jobs, long-running agents, or production automation.

## Reference(s):

- [Weather loader ClawHub page](https://clawhub.ai/minshi-veyt/skills/weather-loader)
- [Open-Meteo](https://open-meteo.com/)
- [Open-Meteo Forecast API](https://api.open-meteo.com/v1/forecast?latitude={lat})
- [Open-Meteo Historical Weather API](https://archive-api.open-meteo.com/v1/archive?latitude={lat})
- [Open-Meteo Geocoding API](https://geocoding-api.open-meteo.com/v1/search)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration]

**Output Format:** [CSV or JSON printed to stdout, with concise Markdown command guidance when needed]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [No API key required; historical results default to 10 days with a 30-day maximum, and forecasts default to 7 days with a 15-day maximum.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
