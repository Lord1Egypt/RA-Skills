## Description:

Wire one site-scoped read-only MCP sidecar to a local Campus Copilot snapshot.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xiaojiou176](https://clawhub.ai/user/xiaojiou176)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to connect a local MCP-capable runtime to one site's read-only Campus Copilot snapshot. It helps inspect snapshot-scoped assignments, messages, or events without live browser interaction or write-capable actions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Using the wrong snapshot path or site can ground the local MCP consumer in unintended records.

Mitigation: Confirm the snapshot path and selected site before launching the sidecar or adding it to a persistent MCP client configuration.

Risk: A reusable MCP config example may not match every local runtime's expected server configuration shape.

Mitigation: Review the actual MCP config file before reuse, and use the direct sidecar command when the consumer does not support the same mcpServers shape.

Risk: The skill is intended for read-only, snapshot-scoped access and does not support live browser control or posting actions.

Mitigation: Keep agent claims and actions limited to snapshot data, and do not use it for posting, replying, submitting, or live browser takeover.

## Reference(s):

- [Codex MCP integration example](examples/integrations/codex-mcp.example.json)
- [Claude Code MCP integration example](examples/integrations/claude-code-mcp.example.json)
- [Claude Desktop MCP example](examples/mcp/claude-desktop.example.json)
- [Codex repo-root MCP example](examples/mcp/codex-repo-root.example.json)
- [Claude Desktop repo-root MCP example](examples/mcp/claude-desktop-repo-root.example.json)
- [OpenClaw read-only guidance](examples/openclaw-readonly.md)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration]

**Output Format:** [Markdown guidance with inline shell commands and JSON configuration references]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read-only, snapshot-scoped setup guidance; no bundled executable code.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
