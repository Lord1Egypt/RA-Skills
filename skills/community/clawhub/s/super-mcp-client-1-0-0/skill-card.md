## Description:

Super Mcp Client 1.0.3 helps agents connect to Model Context Protocol servers to discover tools, invoke remote capabilities, list resources, read resources, and access prompt templates.

This skill is ready for commercial/non-commercial use.

## Publisher:

[subaru0573](https://clawhub.ai/user/subaru0573)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent builders use this skill to connect an agent to trusted MCP servers, inspect available tools and resources, call MCP tools, and read server-exposed resources.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Connecting to untrusted MCP servers can expose users to unsafe remote tools, resources, or prompts.

Mitigation: Install and use the skill only with MCP servers you control or trust, and review available tools and resources before invoking them.

Risk: Sensitive values may be exposed if they are passed in tool arguments, resource URIs, or long-lived command-line API keys.

Mitigation: Prefer HTTPS for non-local servers, avoid sensitive values in tool arguments and resource URIs, and avoid putting long-lived API keys directly on the command line.

## Reference(s):

- [Model Context Protocol](https://modelcontextprotocol.io)
- [ClawHub Skill Page](https://clawhub.ai/subaru0573/skills/super-mcp-client-1-0-0)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with Python examples, command examples, and JSON responses from MCP endpoints]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Network and resource access depend on the configured MCP server and user-provided credentials.]

## Skill Version(s):

1.0.0 (source: server release metadata and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
