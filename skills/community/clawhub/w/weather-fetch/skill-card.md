## Description:

Fetches current weather data for supported Chinese cities from weathercn.com using Playwright and returns temperature, humidity, pressure, visibility, wind, sunrise and sunset times, and AQI fields.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wndagg](https://clawhub.ai/user/wndagg)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and end users use this skill to run a command-line lookup for supported Chinese city names and receive current weather details scraped from weathercn.com.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill launches Chromium with the browser sandbox disabled while visiting a remote weather site.

Mitigation: Run it in a contained, low-privilege environment and review browser execution settings before deployment.

Risk: The release describes broad city coverage, but the submitted artifact contains a limited hardcoded city mapping.

Mitigation: Confirm supported cities before relying on the output, and expand or validate the city list for production use.

## Reference(s):

- [ClawHub Weather Fetch listing](https://clawhub.ai/wndagg/skills/weather-fetch)
- [Project homepage](https://github.com/wNDAGG/mimi-scripts)
- [weathercn.com mobile weather source](https://m.weathercn.com)

## Skill Output:

**Output Type(s):** [text, JSON]

**Output Format:** [JSON plus a plain-text weather summary emitted to stdout]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Weather values are scraped at runtime from remote web content and depend on the supported city mapping in the artifact.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
