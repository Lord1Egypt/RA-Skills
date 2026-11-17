## Description:

Get current weather conditions and forecasts for any location worldwide.

This skill is ready for commercial/non-commercial use.

## Publisher:

[pjtf93](https://clawhub.ai/user/pjtf93)

### License/Terms of Use:


## Use Case:

Developers and agent users use this skill to retrieve current weather, forecasts, and location details for activity planning, travel planning, and weather-aware responses.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Installation instructions may fetch and run an unpinned third-party executable.

Mitigation: Review the upstream project before installing and prefer a pinned, reviewed version with checksum or signature verification.

Risk: Weather and location lookup can disclose sensitive exact locations.

Mitigation: Avoid submitting exact addresses unless needed; use city, region, or otherwise less precise locations when sufficient.

## Reference(s):

- [ClawHub Weathercli Skill Page](https://clawhub.ai/pjtf93/skills/weathercli)
- [weathercli Releases](https://github.com/pjtf93/weathercli/releases)

## Skill Output:

**Output Type(s):** [Shell commands, Text, JSON, Guidance]

**Output Format:** [Markdown guidance with inline shell commands and JSON output examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Weather data requires network access and may include location lookup results.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
