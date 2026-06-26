## Description: <br>
Query Veeam Backup & Replication and Veeam ONE via MCP server running in Docker. Provides intelligent backup monitoring, job analysis, capacity planning, and infrastructure health checks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[JGM2025](https://clawhub.ai/user/JGM2025) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers, backup administrators, and infrastructure operators use this skill to ask natural-language questions about Veeam Backup & Replication and Veeam ONE status, alerts, job history, repository capacity, and backup health. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill depends on an external beta Veeam MCP server and Docker image for access to backup infrastructure. <br>
Mitigation: Install only after verifying the MCP server package and Docker image came from a trusted Veeam source. <br>
Risk: The skill uses long-lived administrator credentials for Veeam Backup & Replication or Veeam ONE. <br>
Mitigation: Use a dedicated least-privilege account, protect the credential file with restrictive permissions, and rotate credentials regularly. <br>
Risk: The scripts allow self-signed certificate acceptance for HTTPS connections. <br>
Mitigation: Prefer trusted TLS certificates and review any self-signed certificate exception before use. <br>
Risk: The interactive MCP script can expose broad server tool access if run before reviewing available tools and permissions. <br>
Mitigation: Review the MCP server's available tools and configured permissions before using the interactive session. <br>


## Reference(s): <br>
- [ClawHub Veeam MCP Release](https://clawhub.ai/JGM2025/veeam-mcp) <br>
- [Model Context Protocol](https://modelcontextprotocol.io/) <br>
- [Veeam Intelligence Documentation](https://helpcenter.veeam.com/) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Responses depend on the configured Docker MCP server, Veeam Intelligence availability, and the permissions of the local Veeam credentials.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
