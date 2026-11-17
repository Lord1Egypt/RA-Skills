## Description:

Query QWeather city codes and real-time weather with bundled executable scripts for resolving city names to QWeather location IDs or adcodes and fetching current conditions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[richliao1112](https://clawhub.ai/user/richliao1112)

### License/Terms of Use:


## Use Case:

Developers and agents use this skill to resolve city names into QWeather identifiers and fetch current weather through the bundled Python script using a configured QWeather API host and key.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The configured QWeather API key can be sent to any HTTPS host supplied as QWEATHER_API_HOST or --api-host.

Mitigation: Use a trusted official QWeather API host and review the host value before running the skill.

Risk: Passing the QWeather API key on the command line can expose it through shell history or logs.

Mitigation: Prefer protected environment or secret-manager injection and rotate the key if exposure is suspected.

## Reference(s):

- [QWeather HTTP API Contract](artifact/references/qweather-http-contract.md)
- [ClawHub Skill Page](https://clawhub.ai/richliao1112/skills/qweather-city-weather)

## Skill Output:

**Output Type(s):** [text, code, shell commands, configuration, guidance]

**Output Format:** [JSON results with Markdown guidance and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Returns success or failure JSON payloads and requires QWEATHER_API_KEY plus QWEATHER_API_HOST.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
