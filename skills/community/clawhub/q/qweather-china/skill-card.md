## Description:

Provides localized China weather information through the QWeather API, including current conditions, forecasts, life indices, air quality, and weather alerts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[uni-huang](https://clawhub.ai/user/uni-huang)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to let an agent answer China-focused weather questions, including current weather, forecasts, air quality, life indices, and practical weather guidance. It can also be used from the command line after QWeather credentials and cache settings are configured.

### Deployment Geography for Use:

China

## Known Risks and Mitigations:

Risk: The skill handles a QWeather signing key and reads credential-related configuration paths, which could expose credentials if misconfigured.

Mitigation: Use a dedicated QWeather private key stored under ~/.config/qweather/private.pem with restrictive permissions, and avoid printing credential-related environment values in errors.

Risk: A stale .openclaw private-key path remains in openclaw_config.yaml.

Mitigation: Remove or replace the stale .openclaw key path before installing the skill in a sensitive environment.

Risk: If QWEATHER_API_HOST is not constrained, signed requests could be sent to an unapproved host.

Mitigation: Validate QWEATHER_API_HOST against approved qweatherapi.com hosts before sending JWT-authenticated requests.

Risk: Dependencies may be installed without a pinned lock file.

Mitigation: Install dependencies from a pinned lock file or an isolated virtual environment.

## Reference(s):

- [QWeather China on ClawHub](https://clawhub.ai/uni-huang/skills/qweather-china)
- [QWeather Developer Portal](https://dev.qweather.com/)
- [QWeather Documentation](https://dev.qweather.com/docs/)
- [QWeather City Resources](https://dev.qweather.com/docs/resource/city/)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown-style natural-language weather responses with optional shell commands and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses QWeather API results and local cache when configured.]

## Skill Version(s):

1.2.2 (source: SKILL.md frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
