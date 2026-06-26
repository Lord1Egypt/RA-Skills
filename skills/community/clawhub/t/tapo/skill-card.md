## Description: <br>
Control TP-Link Tapo smart home devices, including lights, plugs, power strips, hubs, sensors, and cameras, through a Tapo MCP server. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mihai-dinculescu](https://clawhub.ai/user/mihai-dinculescu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to connect OpenClaw to an existing Tapo MCP server, inspect discovered devices, read device state, control supported smart-home devices, and request camera snapshots when configured. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can enable control of physical Tapo smart-home devices if connected to a configured Tapo MCP server. <br>
Mitigation: Install only for intended smart-home control, keep the server on localhost or a trusted private network, and review device-control commands before execution. <br>
Risk: Bearer tokens and local mcporter configuration may expose access to the Tapo MCP server if stored or shared insecurely. <br>
Mitigation: Use a strong TAPO_MCP_API_KEY and protect ~/.mcporter/mcporter.json when it stores an authorization token. <br>
Risk: Camera snapshot credentials can expose still images from private spaces. <br>
Mitigation: Enable camera snapshot credentials only where everyone affected understands the privacy impact. <br>


## Reference(s): <br>
- [ClawHub Tapo skill page](https://clawhub.ai/mihai-dinculescu/tapo) <br>
- [Tapo skill setup](references/setup.md) <br>
- [Tapo MCP server setup](references/tapo-mcp-setup.md) <br>
- [Tapo MCP documentation](https://github.com/mihai-dinculescu/tapo/tree/main/tapo-mcp) <br>
- [Model Context Protocol](https://modelcontextprotocol.io/) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration, API calls] <br>
**Output Format:** [Markdown guidance with bash commands and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires npx, a reachable Tapo MCP server, and sensitive credentials for authenticated access or camera snapshots.] <br>

## Skill Version(s): <br>
0.4.1 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
