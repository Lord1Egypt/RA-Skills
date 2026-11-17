## Description:

Deploy Git repositories, diagnose errors and slow sites, and manage xCloud servers, sites, SSL, backups, billing and teams through nine capability skills.

This skill is ready for commercial/non-commercial use.

## Publisher:

[asif2bd](https://clawhub.ai/user/asif2bd)

### License/Terms of Use:

MIT

## Use Case:

Developers and site operators use this skill to deploy and troubleshoot applications and manage xCloud hosting resources, WordPress, certificates, accounts and billing with an AI agent.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Agent actions could modify or delete live infrastructure, interrupt services, or incur charges.

Mitigation: Review the target and impact, verify permissions, and require explicit confirmation for deployments, deletions, server changes and payments.

Risk: API credentials or sensitive account data could be exposed.

Mitigation: Prefer secure MCP OAuth or least-privilege read-only credentials, use a trusted connection, and keep tokens and sensitive responses out of chat and logs.

Risk: Historical REST examples may be mistaken for permission to make sensitive changes.

Mitigation: Treat non-GET REST examples as documentation; use approved MCP tools or the xCloud dashboard for changes.

## Reference(s):

- [xCloud MCP documentation](https://app.xcloud.host/mcp/docs)
- [xCloud API documentation](https://app.xcloud.host/api/v1/docs)
- [Authentication guidance](plugins/xcloud/reference/auth.md)
- [Capability map](plugins/xcloud/reference/capability-map.md)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration instructions]

**Output Format:** [Markdown with inline commands and configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose actions for connected xCloud tools; actual infrastructure changes require user approval.]

## Skill Version(s):

4.4.2 (source: frontmatter and server-resolved release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
