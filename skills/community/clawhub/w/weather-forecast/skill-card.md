## Description:

This skill should be used when users ask about weather forecasts, temperature information, or need to retrieve weather data for specific locations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[alex098929](https://clawhub.ai/user/alex098929)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to answer weather and temperature forecast questions for named locations or coordinates. It retrieves hourly forecast data from Open-Meteo and presents concise natural-language summaries.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Weather requests send the requested coordinates and selected weather fields to Open-Meteo.

Mitigation: Avoid submitting precise personal coordinates when the user does not want that location shared with the weather API.

Risk: Forecast answers may be inaccurate if a named place is mapped to the wrong coordinates.

Mitigation: Confirm ambiguous locations or ask for coordinates before fetching and summarizing forecast data.

## Reference(s):

- [Open-Meteo Forecast API](https://api.open-meteo.com/v1/forecast)
- [Open-Meteo API Response Format](references/api_response_format.md)
- [ClawHub Skill Page](https://clawhub.ai/alex098929/skills/weather-forecast)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, JSON]

**Output Format:** [Markdown or plain text summaries with optional raw JSON weather data]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses latitude and longitude, plus optional hourly weather fields, to request Open-Meteo forecast data.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
