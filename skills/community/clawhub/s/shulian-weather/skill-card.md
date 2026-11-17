## Description:

Gets current weather conditions and forecasts through WeatherAPI.com after the user configures their own API key.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jianmo1997](https://clawhub.ai/user/jianmo1997)

### License/Terms of Use:

MIT

## Use Case:

External users and developers use this skill to answer weather, temperature, and forecast questions for worldwide locations through WeatherAPI.com.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requires a WeatherAPI key, which could be exposed through configuration files, shell history, logs, or shared command output.

Mitigation: Use OpenClaw UI or a protected secret store when available, restrict permissions on files containing the key, redact logs and commands before sharing, and rotate the key if exposure is suspected.

## Reference(s):

- [WeatherAPI.com](https://www.weatherapi.com/)
- [ClawHub skill page](https://clawhub.ai/jianmo1997/skills/shulian-weather)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline JSON and bash examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires curl and a user-provided WEATHER_API_KEY; WeatherAPI responses are JSON.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
