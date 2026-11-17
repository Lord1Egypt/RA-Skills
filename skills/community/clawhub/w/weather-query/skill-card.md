## Description:

Use when users ask about weather conditions, forecasts, or climate information for locations in China.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jaceymarvin99](https://clawhub.ai/user/jaceymarvin99)

### License/Terms of Use:


## Use Case:

External users and agents use this skill to retrieve current weather conditions, air quality, alerts, daily life indices, and short-term forecasts for cities and districts in China.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: City or district names are sent to an external weather API.

Mitigation: Avoid unusually precise or sensitive location details when location privacy matters.

Risk: Weather results can be stale or unavailable for specific districts.

Mitigation: Check the returned update timestamp and fall back to the main city name when a district is not found.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jaceymarvin99/skills/weather-query)
- [Current weather API endpoint](https://60s.viki.moe/v2/weather)
- [Forecast weather API endpoint](https://60s.viki.moe/v2/weather/forecast)

## Skill Output:

**Output Type(s):** [text, markdown, JSON, shell commands, guidance]

**Output Format:** [Text, Markdown, or JSON returned by shell commands that call an external weather API.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Forecast queries accept 0-8 days; location queries should use Chinese place names.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
