## Description:

Super MCP Integration connects OpenClaw agents to configured Model Context Protocol servers so they can discover available tools and call them through a unified mcp interface.

This skill is ready for commercial/non-commercial use.

## Publisher:

[subaru0573](https://clawhub.ai/user/subaru0573)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw administrators use this skill to configure agent access to trusted MCP servers, inspect available remote tools, validate tool parameters, and execute supported tools for workflows such as legal search, database queries, and weather lookups.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A single approved mcp tool can invoke many externally supplied tools from connected MCP servers.

Mitigation: Restrict the mcp tool to trusted or administrative agents and require review or confirmation before using state-changing, account, messaging, filesystem, database, or similar tools.

Risk: Untrusted or misconfigured MCP server endpoints can expose agents to unsafe or misleading external capabilities.

Mitigation: Connect only to MCP servers you control or trust, prefer HTTPS endpoints, and install the skill only in trusted workspaces.

Risk: Configuration, URLs, or diagnostic reports may expose credentials or sensitive environment details.

Mitigation: Avoid URL-embedded credentials and manually redact configuration and logs before sharing diagnostic reports.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/subaru0573/skills/super-mcp-integration-1-0-0)
- [README](README.md)
- [API Reference](docs/API.md)
- [Configuration Guide](docs/CONFIGURATION.md)
- [Usage Examples](docs/EXAMPLES.md)
- [Real Working Example: kr-legal-search](docs/REAL_EXAMPLE_KR_LEGAL.md)
- [Troubleshooting Guide](docs/TROUBLESHOOTING.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown guidance with JSON examples, shell commands, and tool-call patterns]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The skill guides use of a unified mcp tool with list and call actions; actual remote tool outputs depend on the connected MCP servers.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
