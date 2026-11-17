## Description:

qweather helps agents query QWeather for real-time weather, daily forecasts, life indices, and city lookup.

This skill is ready for commercial/non-commercial use.

## Publisher:

[deusyu](https://clawhub.ai/user/deusyu)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use qweather to resolve city names or coordinates and answer weather questions with current conditions, 3- or 7-day forecasts, and life index guidance such as UV, clothing, and car-wash indices.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The QWeather API key can be exposed through request URLs in error output or logs.

Mitigation: Avoid running the skill where stderr is broadly logged and prefer a patched version that redacts key= values from errors.

Risk: A misconfigured QWEATHER_API_HOST can send the API key and city or coordinate queries to an unintended host.

Mitigation: Set QWEATHER_API_HOST only to the official QWeather host assigned for the account and validate the host before use.

## Reference(s):

- [Command Map](references/command-map.md)
- [QWeather Console](https://console.qweather.com)
- [QWeather API Host Settings](https://console.qweather.com/setting)
- [ClawHub Skill Page](https://clawhub.ai/deusyu/skills/rainman-qweather)

## Skill Output:

**Output Type(s):** [text, JSON, shell commands, configuration guidance]

**Output Format:** [JSON from the CLI, typically summarized by the agent as concise natural-language text.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires QWEATHER_API_KEY and QWEATHER_API_HOST; city or coordinate queries are sent to the configured QWeather host.]

## Skill Version(s):

1.0.0 (source: SKILL.md frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
