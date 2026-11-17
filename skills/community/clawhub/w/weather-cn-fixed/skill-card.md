## Description:

Chinese weather query tool that uses China Weather Network to fetch real-time weather without an API key or model dependency.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ziqi-jin](https://clawhub.ai/user/ziqi-jin)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers can use this skill to look up current Chinese weather, temperature ranges, and lifestyle indices for supported cities through a shell script.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The shell script evaluates parsed weather data, so manipulated network content could run commands as the user.

Mitigation: Remove eval before routine use and parse returned key-value data without shell evaluation.

Risk: Weather lookup depends on network access to www.weather.com.cn and may return delayed or unavailable data.

Mitigation: Review results before acting on them and keep documented fallback weather sources available.

Risk: The optional shell alias modifies the user's persistent shell startup configuration.

Mitigation: Add the alias only when persistent convenience behavior is desired and review the target shell profile first.

## Reference(s):

- [China Weather Network](https://www.weather.com.cn/)
- [ClawHub skill page](https://clawhub.ai/ziqi-jin/skills/weather-cn-fixed)

## Skill Output:

**Output Type(s):** [text, shell commands, guidance]

**Output Format:** [Formatted terminal text with Chinese weather fields and usage guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires curl and grep; fetches network data from www.weather.com.cn.]

## Skill Version(s):

1.0.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
