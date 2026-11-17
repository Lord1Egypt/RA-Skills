## Description:

UpdateStock MCP manages A-share DuckDB stock databases over stdio, including database creation, full or incremental data updates, stock-market data queries, and QuantAll-compatible database setup.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mifochen](https://clawhub.ai/user/mifochen)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, quantitative analysts, and agent users use this skill to create and maintain local DuckDB databases for Chinese A-share market data, then query that data or prepare it for QuantAll analysis workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The scanner reports real security and control issues that should be reviewed before installation.

Mitigation: Install and run the skill only in an isolated environment until the issues have been reviewed.

Risk: The Tushare token is stored in a local plaintext file.

Mitigation: Keep the token out of shared folders and backups, and restrict file access to the user running the MCP server.

Risk: The MCP server can expose or modify local DuckDB stock databases.

Mitigation: Use a dedicated database path with least-privilege filesystem access and avoid exposing sensitive DuckDB files through the server.

Risk: Starting QuantAll launches a local HTTP MCP service.

Mitigation: Start QuantAll only when that local service is intended and trusted for the current session.

Risk: Query inputs are not confirmed safe by the scanner guidance.

Mitigation: Treat query inputs as unsafe until SQL construction has been fixed, and avoid connecting the tool to untrusted callers.

Risk: Dependencies are specified with lower bounds rather than pinned versions.

Mitigation: Prefer pinned dependencies in a virtual environment before deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/mifochen/skills/update-stock-mcp)
- [Tushare registration](https://tushare.pro/register)

## Skill Output:

**Output Type(s):** [text, JSON, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with MCP tool calls, JSON snippets, shell commands, and text or JSON tool responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or update local DuckDB databases and JSON configuration files when the MCP tools are executed.]

## Skill Version(s):

2.2.0 (source: server release metadata and release changelog)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
