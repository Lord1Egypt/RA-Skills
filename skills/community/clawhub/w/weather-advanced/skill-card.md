## Description:

Provides Chinese-language city weather lookup with current conditions, a 7-day forecast, air quality, UV information, clothing suggestions, and cold-risk guidance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dreamximu](https://clawhub.ai/user/dreamximu)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and end users can use this skill to query weather for Chinese cities and receive a concise forecast with practical life-index guidance. It is suited for agent workflows that need human-readable weather status rather than raw meteorological data.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: City names are sent to the third-party api.vvhan.com weather service.

Mitigation: Use only when sharing the queried city with that external service is acceptable.

Risk: Weather responses depend on availability and accuracy of the third-party API.

Mitigation: Treat results as informational and retry or verify through another source when weather accuracy is important.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/dreamximu/skills/weather-advanced)
- [Weather API endpoint](https://api.vvhan.com/api/weather)

## Skill Output:

**Output Type(s):** [text, guidance]

**Output Format:** [Plain text with formatted Chinese weather sections]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Returns current weather, forecast, air quality, UV, clothing advice, wind details, and error messages when a city is missing or unsupported.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
