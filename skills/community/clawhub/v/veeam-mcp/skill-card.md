## Description:

Query Veeam Backup & Replication and Veeam ONE via MCP server running in Docker. Provides intelligent backup monitoring, job analysis, capacity planning, and infrastructure health checks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jgm2025](https://clawhub.ai/user/jgm2025)

### License/Terms of Use:

MIT

## Use Case:

Developers and infrastructure operators use this skill to query Veeam Backup & Replication and Veeam ONE from an agent workflow for backup monitoring, job analysis, alert review, capacity planning, and infrastructure health checks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles powerful Veeam backup-system credentials.

Mitigation: Use a dedicated least-privilege Veeam account and restrict the local credentials file permissions before installation.

Risk: Troubleshooting and command-line use can expose credential material if users print or share local configuration.

Mitigation: Do not print, paste, log, or share the credentials file or command output containing secrets.

Risk: The skill configures HTTPS connections with self-signed certificate acceptance.

Mitigation: Require trusted certificates or certificate pinning for production use.

Risk: The skill depends on a Veeam MCP Docker image obtained outside the skill artifact.

Mitigation: Run only a Veeam MCP Docker image whose source and exact digest have been verified.

## Reference(s):

- [Model Context Protocol](https://modelcontextprotocol.io/)
- [Veeam Intelligence Documentation](https://helpcenter.veeam.com/)
- [OpenClaw Docs](https://docs.openclaw.ai)
- [ClawHub Skill Page](https://clawhub.ai/jgm2025/skills/veeam-mcp)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and JSON configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May relay Veeam MCP query responses when the user provides configured access to Veeam services.]

## Skill Version(s):

1.0.3 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
