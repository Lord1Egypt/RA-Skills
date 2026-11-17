## Description:

Provides QWeather-powered lookups for current weather, forecasts, geolocation, precipitation, lifestyle indices, warnings, air quality, sunrise and sunset, moon phase, and solar angle by city, location ID, or coordinates.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yinguobing](https://clawhub.ai/user/yinguobing)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users can use this skill to configure and run QWeather CLI queries for weather, geolocation, forecast, air quality, astronomy, and related environmental data. It is useful when an agent needs concrete shell commands and credential setup guidance for weather lookups.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requires installing an external Cargo binary before use.

Mitigation: Install only trusted or reviewed versions of the qweather package or repository, and prefer a pinned version where possible.

Risk: The skill requires QWeather credentials, including QWEATHER_PRIVATE_KEY.

Mitigation: Limit QWeather environment variables to the runtime environment where the CLI runs and avoid exposing private key material in prompts, logs, or shared shells.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/yinguobing/skills/qweather-skill)
- [qweather-skill homepage](https://github.com/yinguobing/qweather-skill)
- [QWeather Console](https://console.qweather.com/project)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline shell commands and environment variable examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires QWeather credentials and the qw CLI installed from the qweather Cargo package or repository.]

## Skill Version(s):

0.5.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
