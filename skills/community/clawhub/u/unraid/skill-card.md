## Description:

Query and monitor Unraid servers via the GraphQL API. Use when the user asks to 'check Unraid', 'monitor Unraid', 'Unraid API', 'get Unraid status', 'check disk temperatures', 'read Unraid logs', 'list Unraid shares', 'Unraid array status', 'Unraid containers', 'Unraid VMs', or mentions Unraid system monitoring, disk health, parity checks, or server status.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jmagar](https://clawhub.ai/user/jmagar)

### License/Terms of Use:


## Use Case:

Developers, operators, and homelab administrators use this skill to query Unraid 7.2+ GraphQL endpoints for server health, storage status, logs, containers, virtual machines, notifications, and related monitoring tasks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill uses an Unraid API key and can expose infrastructure details through API responses, reports, or logs.

Mitigation: Use a dedicated Viewer API key, scope access to the minimum needed, and treat generated output as sensitive.

Risk: Dashboard behavior can persist inventory and debug output to local files.

Mitigation: Review the dashboard script before running it and only keep generated files in locations appropriate for sensitive operational data.

Risk: Using insecure or self-signed HTTPS options can reduce confidence in the server connection.

Mitigation: Prefer verified HTTPS for remote access and review any use of insecure curl options before deployment.

## Reference(s):

- [Unraid API - Complete Reference Guide](references/api-reference.md)
- [Unraid API Endpoints Reference](references/endpoints.md)
- [Unraid API Quick Reference](references/quick-reference.md)
- [Unraid API Troubleshooting Guide](references/troubleshooting.md)
- [ClawHub Skill Page](https://clawhub.ai/jmagar/skills/unraid)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with bash and GraphQL snippets, JSON API responses, and optional generated reports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include sensitive infrastructure status, log content, API responses, and dashboard files.]

## Skill Version(s):

1.0.1 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
