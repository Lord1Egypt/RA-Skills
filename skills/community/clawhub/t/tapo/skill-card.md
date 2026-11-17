## Description:

Control TP-Link Tapo smart home devices (plugs, lights, light strips, power strips, hubs and their child devices, cameras) via Tapo MCP.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mihai-dinculescu](https://clawhub.ai/user/mihai-dinculescu)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and smart-home users use the skill to discover Tapo devices, inspect device state and energy data, control supported plugs, lights, switches and child devices, and capture camera snapshots through a configured Tapo MCP server.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup sends a bearer token over plain HTTP, which may expose credentials on an untrusted network path.

Mitigation: Review how the token is protected in transit and only connect over a network path you trust; avoid exposing the service beyond the intended local network.

Risk: Setup uses unpinned packages and a mutable image, which may change after review.

Mitigation: Review and pin package and image versions before deployment.

Risk: The server has network access to smart-home devices, and host-network access may expand its reach.

Mitigation: Assess whether host networking is necessary and limit the server's network access to the devices and hosts it needs.

Risk: Control actions, including test examples, can turn off connected equipment.

Mitigation: Confirm the target device and intended effect before running a control action, especially when equipment depends on continuous power.

## Reference(s):

- [Tapo Skill Setup](references/setup.md)
- [Setting Up the Tapo MCP Server](references/tapo-mcp-setup.md)
- [Tapo MCP project documentation](https://github.com/mihai-dinculescu/tapo/tree/main/tapo-mcp)
- [Model Context Protocol](https://modelcontextprotocol.io/)

## Skill Output:

**Output Type(s):** [Text, JSON, API calls, JPEG images, Shell commands, Configuration guidance]

**Output Format:** [Device information and state as text or JSON, camera snapshots as JPEG, and setup guidance in Markdown with shell examples.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Device-control calls may change smart-home equipment; snapshot links, when provided by the server, are short-lived.]

## Skill Version(s):

0.7.0 (source: frontmatter; release evidence also reports 0.7.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
