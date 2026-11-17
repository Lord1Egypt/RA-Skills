## Description:

China Weather helps agents answer weather requests for Chinese cities, including current conditions, forecasts, air quality, and life index details with formatted Chinese or English output.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tobewin](https://clawhub.ai/user/tobewin)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to query and format weather information for Chinese cities through wttr.in or configured weather providers. It supports current weather, multi-day forecasts, air quality, and life index reporting.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: City queries and configured weather API keys may be sent to third-party weather services.

Mitigation: Install only where external weather lookups are acceptable, keep API keys low-privilege, and treat queried city names as shared with wttr.in or the configured provider.

Risk: A configured QWeather host could route requests to an untrusted service.

Mitigation: Use only a trusted QWeather host issued by the provider.

Risk: Runtime dependency installation can introduce supply-chain risk.

Mitigation: Prefer isolated environments with pinned dependency versions when installing dependencies.

## Reference(s):

- [QWeather Developer Documentation](https://dev.qweather.com)
- [OpenWeatherMap API](https://openweathermap.org/api)
- [Seniverse](https://www.seniverse.com)
- [ClawHub Skill Page](https://clawhub.ai/tobewin/skills/weather-query-pro)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with Python and shell code blocks plus formatted weather text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires curl and python3; optional weather provider API keys may be configured for richer data.]

## Skill Version(s):

1.0.3 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
