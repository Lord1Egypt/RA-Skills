## Description:

Queries WittIoT weather stations for device lists, real-time sensor readings, historical trends, and public shortcode weather data.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wittiot](https://clawhub.ai/user/wittiot)

### License/Terms of Use:

MIT-0

## Use Case:

WittIoT weather station users and agents use this skill to inspect bound devices, fetch current temperature, humidity, pressure, light, wind, and rainfall readings, analyze 24-hour, 7-day, or 30-day history, and query public stations by shortcode.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill uses a WittIoT account API key for private device, realtime, and history queries.

Mitigation: Set WITTIOT_API_KEY through a trusted secret mechanism and avoid sharing API keys in chat, command-line arguments, or project-local config files.

Risk: A project-local config.json containing a real API key could be exposed through file sharing or weak file permissions.

Mitigation: Prefer environment-based secret injection; if config.json is used, keep it out of shared artifacts and restrict local file access.

## Reference(s):

- [WittIoT API Specification](references/api-spec.md)
- [WittIoT API Key Page](https://wittiot.com/index/apikey)
- [WittIoT Dashboard](https://wittiot.com/index/dashboard)
- [ClawHub Skill Page](https://clawhub.ai/wittiot/skills/wittiot-device-skill)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with shell command examples and JSON script results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires WITTIOT_API_KEY for private device, realtime, and history queries; public shortcode queries do not require an API key.]

## Skill Version(s):

1.0.0 (source: release evidence and artifact metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
