## Description:

Stable weather skill for OpenClaw. Designed for reliable same-day weather queries with predictable output, Chinese city support, and automation-friendly plain/json modes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[paceycrognale](https://clawhub.ai/user/paceycrognale)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and automation builders use this skill to retrieve same-day city weather for OpenClaw agents, chatbots, daily summaries, logs, and structured workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: City lookups for non-preset locations are sent to Open-Meteo services.

Mitigation: Document the external data flow and restrict allowed Open-Meteo domains in privacy-sensitive environments.

Risk: Weather output is limited to same-day, single-city results and uses fixed China-oriented language and timezone settings.

Mitigation: Use it only for same-day city checks unless locale, timezone, and multi-day behavior are reviewed or extended.

## Reference(s):

- [Weather Stable ClawHub release](https://clawhub.ai/paceycrognale/skills/weather-stable)
- [Open-Meteo](https://open-meteo.com/)
- [Open-Meteo Geocoding API](https://geocoding-api.open-meteo.com/v1/search)
- [Open-Meteo Forecast API](https://api.open-meteo.com/v1/forecast)

## Skill Output:

**Output Type(s):** [Text, JSON]

**Output Format:** [Plain text, formatted terminal text, or JSON weather output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Single-city same-day weather lookup; requires python3 and outbound access to Open-Meteo]

## Skill Version(s):

1.0.0 (source: server release metadata and RELEASE_NOTES.md)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
