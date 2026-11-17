## Description:

Controls Xiaodu smart speakers and IoT devices, including device discovery, status checks, voice commands, broadcasts, smart-home device actions, and scene triggers.

This skill is ready for commercial/non-commercial use.

## Publisher:

[vividlife](https://clawhub.ai/user/vividlife)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to configure Xiaodu MCP access, discover authorized Xiaodu devices, send voice or broadcast commands, control supported smart-home devices, and trigger configured scenes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can control real smart-home devices and trigger scenes.

Mitigation: Use it only with Xiaodu devices the user is authorized to control, and review commands before execution, especially batch operations and scene triggers.

Risk: The skill depends on a Xiaodu access token that can authorize device control.

Mitigation: Store the token outside shared prompts or logs, rotate it regularly, and replace placeholder credentials only in the intended local configuration.

Risk: The IoT MCP configuration uses an unpinned `npx -y` server command with the access token in its environment.

Mitigation: Review and pin the MCP package before using a real token, or install a trusted version through a controlled package workflow.

Risk: The device update script may persist household device state in workspace files and MEMORY.md.

Mitigation: Disable or remove the MEMORY.md update and limit retained device inventory files unless persistent household state is explicitly desired.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/vividlife/skills/xiaodu-iot)
- [Xiaodu Speaker MCP Configuration Guide](references/xiaodu_mcp.md)
- [IoT Device Control API Guide](references/iot_api.md)
- [Xiaodu DuerOS MCP Endpoint](https://xiaodu.baidu.com/dueros_mcp_server/mcp/)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands, JSON configuration snippets, and script examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May invoke mcporter commands against configured Xiaodu MCP servers and may write device lists or logs in the user's OpenClaw workspace.]

## Skill Version(s):

1.0.0 (source: server release evidence and config_template.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
