## Description:

Get current weather and short-range forecasts in Chinese for a city or region using wttr.in and Open-Meteo.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jvy](https://clawhub.ai/user/jvy)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use Tianqi to answer Chinese-language questions about current weather, temperature, rain, wind, and short-range forecasts. It is suited for quick travel and daily planning responses where Celsius temperatures and Chinese place names are preferred.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: City names or coordinates may be sent to public weather services.

Mitigation: Use only the location detail needed for the forecast and disclose uncertainty when the location or source is unclear.

Risk: Some wttr.in examples use plain HTTP-style host URLs.

Mitigation: Prefer explicit HTTPS URLs for weather requests, especially on untrusted networks.

## Reference(s):

- [wttr.in help](https://wttr.in/:help)
- [Open-Meteo geocoding API](https://geocoding-api.open-meteo.com/v1/search)
- [Open-Meteo forecast API](https://api.open-meteo.com/v1/forecast)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Text]

**Output Format:** [Markdown with Chinese-language weather summaries and inline bash examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include current conditions, temperature, feels-like temperature, daily high and low, precipitation probability or trend, wind conditions, two- to three-day forecast changes, and data-source notes.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
