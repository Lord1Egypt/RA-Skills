## Description:

MCP Client connects OpenClaw to external MCP servers and supports stdio or SSE transports, tool calls, resource reads, prompt retrieval, permission controls, auditing, and error handling.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yuyonghao-123](https://clawhub.ai/user/yuyonghao-123)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to connect an OpenClaw agent to configured MCP servers, inspect their tools/resources/prompts, and invoke them with approval and audit controls.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Packaged credentials could allow unintended GitHub account access if reused.

Mitigation: Remove the packaged GitHub token, revoke it if controlled by the publisher, and require users to supply their own scoped token through local configuration or environment variables.

Risk: Wildcard auto-approval can let connected MCP tools act without the user control described by the documentation.

Mitigation: Disable wildcard auto-approval by default, keep approvals fail-closed, and require explicit approval for write, delete, account, or network actions.

Risk: Unpinned MCP server packages can change behavior between installs.

Mitigation: Pin MCP server package versions and review server release notes before upgrading.

Risk: Passing the full process environment to child MCP servers can expose secrets to privileged server processes.

Mitigation: Pass only the environment variables each server requires and treat every configured MCP server as privileged code.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/yuyonghao-123/skills/yuyonghao-mcp-client)
- [Model Context Protocol specification](https://modelcontextprotocol.io/specification)
- [Model Context Protocol TypeScript SDK](https://github.com/modelcontextprotocol/typescript-sdk)
- [MCP server registry](https://registry.mcp.run)
- [Filesystem MCP server source](https://github.com/modelcontextprotocol/servers/tree/main/src/filesystem)
- [GitHub MCP server source](https://github.com/modelcontextprotocol/servers/tree/main/src/github)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with JavaScript snippets, shell commands, and JSON configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include MCP server setup details, tool/resource/prompt operation examples, approval decisions, and audit-log guidance.]

## Skill Version(s):

0.1.1 (source: release evidence and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
