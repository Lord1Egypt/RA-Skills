## Description:

Tiny and short Python CLI tool to control Home Assistant devices and automations via the REST API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xwings](https://clawhub.ai/user/xwings)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and smart-home operators use this skill to let an agent inspect and control Home Assistant entities, automations, notifications, templates, history, and related device services through a Python command-line tool.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can exercise broad Home Assistant authority, including sensitive services such as locks, alarms, garage doors, presence, device trackers, templates, and location-related commands.

Mitigation: Use a dedicated least-privilege Home Assistant token, require explicit user intent for sensitive actions, and review commands before execution.

Risk: Home Assistant tokens and alarm codes may be exposed if passed directly on the command line or used over an unprotected connection.

Mitigation: Prefer secure environment-based secret handling, avoid passing tokens or alarm codes in visible command arguments, and use HTTPS for the Home Assistant endpoint.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/xwings/skills/py-homeassistant-cli)
- [xwings publisher profile](https://clawhub.ai/user/xwings)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Plain text with shell command examples and JSON command output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires HA_URL and HA_TOKEN or equivalent command-line arguments to reach a Home Assistant instance.]

## Skill Version(s):

1.0.10 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
