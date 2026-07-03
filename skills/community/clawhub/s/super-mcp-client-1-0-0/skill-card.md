## Description: <br>
Super Mcp Client 1.0.3 helps agents connect to Model Context Protocol servers to discover tools and resources, invoke remote tools, read resources, and list prompt templates. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[subaru0573](https://clawhub.ai/user/subaru0573) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent builders use this skill to connect an agent to trusted MCP servers, inspect exposed tools and resources, call tools with JSON arguments, and read selected resources. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Connecting to untrusted MCP servers can expose the agent to unsafe tools, misleading resources, or unintended remote behavior. <br>
Mitigation: Use only MCP servers you control or trust, and review the server's listed tools and resources before invoking tools or reading resources. <br>
Risk: API keys and file:// resource requests can expose sensitive access paths if used with an untrusted server. <br>
Mitigation: Limit API keys to the intended server, avoid file:// resource reads unless required, and treat file resource access as trusted-server-only. <br>


## Reference(s): <br>
- [Model Context Protocol](https://modelcontextprotocol.io) <br>
- [ClawHub skill page](https://clawhub.ai/subaru0573/skills/super-mcp-client-1-0-0) <br>
- [Publisher profile](https://clawhub.ai/user/subaru0573) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with command examples and Python code that returns JSON responses from MCP endpoints.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Python and the requests package; connects to user-specified MCP server URLs.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
