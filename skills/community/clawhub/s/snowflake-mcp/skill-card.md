## Description: <br>
Connect to the Snowflake Managed MCP server with Clawdbot or other MCP clients. Use when wiring Snowflake MCP endpoints, validating connectivity, or configuring Cortex AI services. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[vikrambalaaj](https://clawhub.ai/user/vikrambalaaj) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and data platform engineers use this skill to configure Snowflake Managed MCP endpoints, authenticate MCP clients, validate available tools, and adapt Snowflake Cortex service examples for agent workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The MCP client may receive broad Snowflake credentials or high-privilege role access. <br>
Mitigation: Use a dedicated low-privilege role and token for runtime access, and avoid ACCOUNTADMIN outside initial setup. <br>
Risk: SQL execution tools can allow broad or arbitrary database actions when configured without restrictions. <br>
Mitigation: Restrict SQL permissions to read-only where possible and review every enabled tool before connecting it to an agent. <br>
Risk: Configuration files such as mcp.json and Snowflake connection files can expose tokens or passwords. <br>
Mitigation: Keep configuration files secret, do not commit credentials, and rotate exposed tokens immediately. <br>
Risk: Side-effecting tools such as Send_Email can let an agent perform external actions. <br>
Mitigation: Remove side-effecting tools from production configurations unless they are explicitly approved, gated, and monitored. <br>
Risk: The optional local MCP package introduces dependency and supply-chain exposure. <br>
Mitigation: Pin or verify the local MCP package before use. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/vikrambalaaj/snowflake-mcp) <br>
- [Snowflake MCP Server Guide](https://www.snowflake.com/en/developers/guides/getting-started-with-snowflake-mcp-server/) <br>
- [Snowflake Cortex Agents MCP Documentation](https://docs.snowflake.com/en/user-guide/snowflake-cortex/cortex-agents-mcp) <br>
- [Model Context Protocol](https://modelcontextprotocol.io) <br>
- [MCP Client Setup Reference](mcp-client-setup.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with JSON, YAML, SQL, and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires user-supplied Snowflake account values, role choices, tokens, database and schema names, and MCP endpoint names.] <br>

## Skill Version(s): <br>
2.0.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
