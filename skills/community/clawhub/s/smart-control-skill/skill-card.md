## Description:

Control smart home devices configured in Smart Plus APP by querying devices and scenes, controlling power, adjusting air conditioners, and triggering smart scenes with an MXCHIP OAuth token.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kagxin](https://clawhub.ai/user/kagxin)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to let an agent operate Smart Plus APP devices and scenes through the MXCHIP MCP service. It is suited for home automation tasks such as checking device status, turning devices on or off, changing air conditioner settings, and running preset scenes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can control real smart-home devices and scenes, including power, HVAC, curtains, sockets, and automation scenes.

Mitigation: Require explicit user confirmation before executing control or scene actions, especially for power, HVAC, curtain, socket, and scene changes.

Risk: The MXCHIP OAuth token can grant broad access to a user's Smart Plus APP devices.

Mitigation: Store MXCHIP_OAUTH_TOKEN only in environment or secret storage, keep it out of chats and logs, and rotate it if exposed.

Risk: Custom service endpoints could redirect requests or token-bearing traffic away from the expected MXCHIP service.

Mitigation: Use the documented MXCHIP MCP endpoint unless a trusted reviewer has approved a different base URL.

## Reference(s):

- [API Reference](references/api_reference.md)
- [MXCHIP Official Website](https://www.mxchip.com/)
- [MXCHIP OAuth Token Page](https://app.api.cloud.mxchip.com:2443/oauth2/mcp/oauth)
- [MXCHIP MCP Endpoint](https://app.api.cloud.mxchip.com:2443/mcp)
- [ClawHub Skill Page](https://clawhub.ai/kagxin/skills/smart-control-skill)

## Skill Output:

**Output Type(s):** [text, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline Python and bash examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires MXCHIP_OAUTH_TOKEN and can initiate real smart-home device or scene actions when used with valid credentials.]

## Skill Version(s):

1.0.2 (source: server release metadata, skill.json, README changelog)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
