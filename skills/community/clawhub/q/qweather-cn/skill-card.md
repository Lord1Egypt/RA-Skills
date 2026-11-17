## Description:

Qweather helps agents call the QWeather API for current weather, forecasts, weather alerts, and lifestyle indices using city codes or location values.

This skill is ready for commercial/non-commercial use.

## Publisher:

[k176060444-lgtm](https://clawhub.ai/user/k176060444-lgtm)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill when they need QWeather-based weather lookups, including current conditions, short-range forecasts, warnings, and lifestyle indices for supported locations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The release evidence reports a real-looking API key embedded in documentation and source code.

Mitigation: Review before installing, rotate or replace the key, and prefer a user-provided secret such as an environment variable.

Risk: The security guidance notes Chinese-only output, missing air-quality support, and limited location handling.

Mitigation: Confirm language, endpoint coverage, and location behavior meet the deployment use case before relying on the skill.

## Reference(s):

- [QWeather Geo API documentation](https://dev.qweather.com/docs/api/geo/)
- [ClawHub Qweather skill page](https://clawhub.ai/k176060444-lgtm/skills/qweather-cn)

## Skill Output:

**Output Type(s):** [text, shell commands, guidance]

**Output Format:** [Markdown with command examples and plain-text weather summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Chinese-language weather output; QWeather attribution may be required by the upstream service.]

## Skill Version(s):

1.0.0 (source: server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
