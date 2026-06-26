## Description: <br>
MCP Client connects agents to external Model Context Protocol servers over stdio or SSE for tool calls, resource reads, prompt retrieval, permission control, auditing, and connection management. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yuyonghao-123](https://clawhub.ai/user/yuyonghao-123) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent builders use this skill to configure and operate MCP server connections, inspect available tools and resources, call MCP tools, and review audit logs. It is intended for workflows that need a reusable JavaScript MCP client or CLI wrapper around filesystem, GitHub, database, or other MCP servers. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The release includes an embedded GitHub token. <br>
Mitigation: Revoke the token, remove it from configuration, and require users to provide least-privilege credentials through environment variables or a secret manager. <br>
Risk: Advertised approval controls may not block sensitive tool or resource access. <br>
Mitigation: Verify approval enforcement with security tests before use, keep auto-approval disabled, and connect only to MCP servers whose capabilities are understood. <br>
Risk: Filesystem MCP access can expose or modify local files when roots are too broad. <br>
Mitigation: Restrict filesystem server roots to the minimum required directories and avoid connecting sensitive workspaces until access boundaries are confirmed. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/yuyonghao-123/yuyonghao-mcp-client) <br>
- [Model Context Protocol specification](https://modelcontextprotocol.io/specification) <br>
- [Model Context Protocol TypeScript SDK](https://github.com/modelcontextprotocol/typescript-sdk) <br>
- [MCP server registry](https://registry.mcp.run) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown and JavaScript or shell snippets, plus JSON MCP server configuration] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs may include MCP tool results, resource content, prompt data, connection status, and audit-log entries depending on the connected server.] <br>

## Skill Version(s): <br>
0.1.1 (source: server release evidence and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
