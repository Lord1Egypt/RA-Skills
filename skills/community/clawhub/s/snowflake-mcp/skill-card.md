## Description:

Connect to the Snowflake Managed MCP server with Clawdbot or other MCP clients. Use when wiring Snowflake MCP endpoints, validating connectivity, or configuring Cortex AI services.

This skill is ready for commercial/non-commercial use.

## Publisher:

[vikrambalaaj](https://clawhub.ai/user/vikrambalaaj)

### License/Terms of Use:


## Use Case:

Developers and data engineers use this skill to configure Snowflake Managed MCP endpoints, authenticate MCP clients, validate available tools, and optionally prepare local Snowflake MCP configuration.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The setup guidance can encourage highly privileged Snowflake access and broad SQL execution tools.

Mitigation: Use a dedicated least-privilege Snowflake role instead of ACCOUNTADMIN and expose only the SQL operations required for the intended workflow.

Risk: PATs, passwords, and key passphrases may be copied into project files or command arguments during setup.

Mitigation: Store credentials in a secret manager or protected environment mechanism, and avoid committing MCP configuration files that contain secrets.

Risk: Write, destructive, administrative, or email-sending tools can cause unintended data or business actions when exposed through MCP.

Mitigation: Require explicit human approval for sensitive tool calls and disable write, destructive, administrative, or outbound communication actions unless they are necessary.

Risk: Local MCP setup examples can install a moving package version.

Mitigation: Pin local MCP package versions before use and review updates before deploying them.

## Reference(s):

- [Snowflake MCP Server Guide](https://www.snowflake.com/en/developers/guides/getting-started-with-snowflake-mcp-server/)
- [Snowflake MCP Documentation](https://docs.snowflake.com/en/user-guide/snowflake-cortex/cortex-agents-mcp)
- [Model Context Protocol](https://modelcontextprotocol.io)
- [MCP Client Setup Reference](artifact/mcp-client-setup.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JSON, YAML, SQL, and shell command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces setup and validation guidance; it does not directly execute Snowflake actions.]

## Skill Version(s):

2.0.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
