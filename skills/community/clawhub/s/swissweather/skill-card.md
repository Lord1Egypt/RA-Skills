## Description:

Get current weather measurements from 100+ Swiss MeteoSwiss stations and multi-day Swiss weather forecasts by postal code.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xenofex7](https://clawhub.ai/user/xenofex7)

### License/Terms of Use:


## Use Case:

Developers and agent users use this skill to retrieve Swiss current weather measurements by station and multi-day forecasts by postal code from MeteoSwiss/public Swiss weather endpoints.

### Deployment Geography for Use:

Global for users querying Swiss weather data.

## Known Risks and Mitigations:

Risk: The skill makes outbound requests to MeteoSwiss/public Swiss weather endpoints when weather data is requested.

Mitigation: Use the skill where outbound access to those public endpoints is expected and acceptable.

Risk: The Python scripts depend on the third-party `requests` package.

Mitigation: Install in an isolated Python environment and pin `requests` before use.

Risk: The MeteoSwiss forecast endpoint may be unstable or change.

Mitigation: Fall back to the current weather CSV endpoint or updated MeteoSwiss documentation when forecast requests fail.

## Reference(s):

- [MeteoSwiss API Reference](references/api_info.md)
- [Official MeteoSwiss](https://www.meteoschweiz.admin.ch)
- [Swiss Open Data Platform](https://data.geo.admin.ch)
- [MeteoSwiss Current Weather CSV](https://data.geo.admin.ch/ch.meteoschweiz.messwerte-aktuell/VQHA80.csv)
- [MeteoSwiss Forecast API](https://app-prod-ws.meteoswiss-app.ch/v1/plzDetail?plz={postal_code})
- [Swiss-Weather on ClawHub](https://clawhub.ai/xenofex7/skills/swissweather)

## Skill Output:

**Output Type(s):** [Shell commands, Code, JSON, Text, Guidance]

**Output Format:** [Markdown guidance with inline shell commands; scripts return formatted text tables or JSON.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [No API key is required; weather data freshness and availability depend on MeteoSwiss/public Swiss weather endpoints.]

## Skill Version(s):

1.0.0 (source: release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
