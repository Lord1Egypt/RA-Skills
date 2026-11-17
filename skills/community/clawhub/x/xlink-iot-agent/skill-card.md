## Description:

XLink IoT Agent helps agents query XLink IoT devices, monitor events and alerts, retrieve device attributes, and invoke device-control services through the XLink Gateway API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xlink-iot](https://clawhub.ai/user/xlink-iot)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and IoT operators use this skill to inspect XLink device status, query event and alert data, fetch latest or historical attributes, and issue reviewed XLink device-control commands.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can send live IoT device-control commands.

Mitigation: Require human review before any device-control command is run, especially commands that change device state.

Risk: The skill signs requests to a configurable gateway host.

Mitigation: Keep XLINK_BASE_URL pinned to the official HTTPS gateway or a trusted internal gateway.

Risk: Credentials and command payloads may be sensitive.

Mitigation: Use least-privilege XLink credentials, protect XLINK_APP_SECRET, and avoid debug logs when sensitive command payloads are present.

## Reference(s):

- [XLink IoT Agent release page](https://clawhub.ai/xlink-iot/skills/xlink-iot-agent)
- [CLI reference](references/cli-reference.md)
- [Gateway authentication](references/api-auth.md)
- [API documentation](references/api-doc.md)
- [Response schemas](references/response-schema.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell command examples, Python snippets, and optional JSON API responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include live XLink API response data when commands are executed with valid credentials.]

## Skill Version(s):

0.1.0 (source: SKILL.md frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
