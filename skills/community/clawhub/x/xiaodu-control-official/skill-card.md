## Description:

Connects, configures, verifies, troubleshoots, and controls Xiaodu smart displays and Xiaodu IoT devices through mcporter, including device discovery, speech, photo capture, media push, household device control, and scene triggering.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dueros-mcp](https://clawhub.ai/user/dueros-mcp)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to configure Xiaodu MCP access from authorization text, verify connected devices, and issue Xiaodu smart display or IoT commands through provided mcporter wrappers.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A Xiaodu AccessToken is written into mcporter home configuration and can control real devices.

Mitigation: Use only a trusted Xiaodu account and protect ~/.mcporter/mcporter.json as a secret store; do not echo or commit tokens.

Risk: Camera capture, media playback, door-lock, scene, or broad household control actions can affect privacy, safety, or property.

Mitigation: Require explicit user confirmation before these actions and verify the target device or scene before execution.

Risk: Changing the MCP base URL or running an unvetted dueros-iot-mcp package could route credentials or device commands to an unintended endpoint.

Mitigation: Avoid --base-url unless the endpoint is certain, and prefer a pinned or locally vetted dueros-iot-mcp package.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/dueros-mcp/skills/xiaodu-control-official)
- [Clawdis Homepage](https://github.com/dueros-mcp/xiaodu-control)
- [用户安装指南](references/install-for-users.md)
- [音像与 IoT 能力边界](references/capability-boundaries.md)
- [命令模板](references/command-patterns.md)
- [排障说明](references/troubleshooting.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance, JSON]

**Output Format:** [Markdown guidance with bash commands and JSON snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May call mcporter and write Xiaodu credentials to the mcporter home configuration when the user provides an AccessToken.]

## Skill Version(s):

1.0.9 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
