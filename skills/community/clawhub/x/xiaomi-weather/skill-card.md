## Description:

Looks up Chinese city weather using Xiaomi Weather data, including city-name or city-code queries, current conditions, multi-day forecasts, air quality, precipitation probability, and sunrise/sunset details.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tonyhuya](https://clawhub.ai/user/tonyhuya)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to ask an agent for current and forecast weather for Chinese cities. It can return human-readable weather summaries or raw JSON for scripting workflows.

### Deployment Geography for Use:

Global, with functionality focused on Chinese city weather data.

## Known Risks and Mitigations:

Risk: The skill makes external requests to Xiaomi Weather and may query a GitHub-hosted city-code database for unknown city names.

Mitigation: Review the external lookup behavior before use and avoid sending sensitive or private location queries through the tool.

Risk: The city-code database is cached in a shared temporary path and is not pinned or verified.

Mitigation: Avoid running the skill as root and prefer a future version that uses a user-private cache directory with pinned or verified city database content.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/tonyhuya/skills/xiaomi-weather)
- [Xiaomi Weather API notes](https://github.com/huanghui0906/API/blob/master/XiaomiWeather.md)
- [Bundled city code reference](references/cities.tsv)
- [Upstream city database](https://github.com/huanghui0906/API/blob/master/xiaomi_weather.db)
- [Xiaomi Weather API endpoint](https://weatherapi.market.xiaomi.com/wtr-v3/weather/all)

## Skill Output:

**Output Type(s):** [text, JSON, shell commands]

**Output Format:** [Plain text weather summaries or raw JSON, invoked through shell commands.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires curl and python3; default output is a five-day forecast and the requested forecast length is capped at 15 days.]

## Skill Version(s):

1.0.4 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
