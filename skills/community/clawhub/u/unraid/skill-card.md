## Description: <br>
Query and monitor Unraid servers via the GraphQL API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jmagar](https://clawhub.ai/user/jmagar) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users, developers, and infrastructure operators use this skill to query Unraid 7.2+ GraphQL endpoints for server status, disk health, storage shares, logs, Docker containers, virtual machines, notifications, and fleet dashboard reporting. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill handles sensitive Unraid server inventory, share, container, VM, and syslog data. <br>
Mitigation: Use only a Viewer-role Unraid API key and review generated dashboard, debug, and memory files before sharing or retaining them. <br>
Risk: API keys can be exposed if passed directly on command lines or stored carelessly. <br>
Mitigation: Prefer environment variables or protected local configuration files with restricted permissions, and rotate keys if exposure is suspected. <br>
Risk: The helper script disables TLS certificate verification by default for curl requests. <br>
Mitigation: Change curl usage to verify certificates unless the operator explicitly accepts the self-signed certificate risk for a trusted local server. <br>


## Reference(s): <br>
- [Unraid API Reference](references/api-reference.md) <br>
- [Unraid API Endpoints Reference](references/endpoints.md) <br>
- [Unraid API Quick Reference](references/quick-reference.md) <br>
- [Unraid API Troubleshooting Guide](references/troubleshooting.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration] <br>
**Output Format:** [Markdown guidance with bash commands and JSON GraphQL responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May read Unraid GraphQL responses and may generate local dashboard or debug files when helper scripts are run.] <br>

## Skill Version(s): <br>
1.0.1 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
