## Description:

Get the weather for a specific location or coordinates.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mangonob](https://clawhub.ai/user/mangonob)

### License/Terms of Use:


## Use Case:

Developers and external users use this skill to retrieve real-time weather, daily forecasts, or hourly forecasts for a location or coordinates through QWeather.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The documentation includes realistic QWeather authentication material in its example configuration.

Mitigation: Do not reuse the example credentials, do not commit private keys, and store QWeather credentials in a protected local config or secret manager.

Risk: The installation flow asks users to globally install package code.

Mitigation: Install only a pinned version from a trusted package source after reviewing the package contents.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/mangonob/skills/skills-weather)
- [QWeather developer documentation](https://dev.qweather.com)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Configuration]

**Output Format:** [Plain text responses with command-line options and JSON configuration examples.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires either a location or coordinates; forecast duration can be daily or hourly, but not both in the same request.]

## Skill Version(s):

1.0.3 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
