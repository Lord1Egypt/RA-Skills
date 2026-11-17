## Description:

Get current weather and today or tomorrow's forecast with rule-based Spidey outdoor-planning guidance. Defaults to Los Angeles; supports a city supplied in the request.

This skill is ready for commercial/non-commercial use.

## Publisher:

[caballeroaldo](https://clawhub.ai/user/caballeroaldo)

### License/Terms of Use:

MIT-0

## Use Case:

People use this skill to retrieve current conditions or today's or tomorrow's forecast for Los Angeles or a requested city, then receive concise, rule-based planning guidance for outdoor activities.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security review is partial and notes a possible mismatch between the described city support and the behavior it could inspect.

Mitigation: Review the complete package before installation and verify location handling for the cities you plan to request.

Risk: Weather forecasts and the skill's outdoor-planning categories do not establish that an activity is safe; official alerts and some conditions are not included.

Mitigation: Treat the planning take as general guidance, check official local advisories, and consult current conditions relevant to the activity.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/caballeroaldo/skills/spidey-weather)
- [Open-Meteo forecast documentation](https://open-meteo.com/en/docs)
- [Open-Meteo geocoding documentation](https://open-meteo.com/en/docs/geocoding-api)
- [OpenClaw Agent Skills documentation](https://docs.openclaw.ai/tools/skills)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Guidance]

**Output Format:** [Markdown weather report, or JSON containing status, report, and weather data when requested]

**Output Parameters:** [Location, optional country code, and today or tomorrow; defaults to Los Angeles and today]

**Other Properties Related to Output:** [Includes current conditions when applicable, forecast values in Fahrenheit and mph, local date/timezone, provider attribution, and deterministic planning guidance.]

## Skill Version(s):

1.0.0 (source: skill frontmatter and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
