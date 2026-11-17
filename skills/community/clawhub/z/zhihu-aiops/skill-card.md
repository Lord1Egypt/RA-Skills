## Description:

Use this skill when working with the Zhihu AIOps / Zhihu operations platform, including asset management, CMDB discovery, monitoring, alarm dashboards, VictoriaMetrics and Categraf SNMP metrics, managed asset inspection reports, and adding OS monitoring assets.

This skill is ready for commercial/non-commercial use.

## Publisher:

[luckypig1209](https://clawhub.ai/user/luckypig1209)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operations engineers use this skill to work with Zhihu AIOps assets, CMDB scan tasks, monitoring and alarm views, VictoriaMetrics queries, Categraf SNMP metrics, managed asset inspection reports, and OS monitoring setup. It provides reference-guided workflows and API examples rather than a production CLI wrapper.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can handle platform API, admin, and SSH credentials.

Mitigation: Use least-privilege accounts over HTTPS, keep secrets in environment variables, and do not paste real passwords into chat or generated scripts.

Risk: The skill can guide state-changing platform actions such as create, delete, restart, export, and monitor setup operations.

Mitigation: Require explicit user confirmation before state-changing actions and review generated commands before execution.

Risk: Example admin/default credentials and local or HTTP endpoints may be inappropriate for production environments.

Mitigation: Replace examples with approved environment-specific values, avoid default admin accounts, and verify how the platform stores SSH credentials used for monitoring.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/luckypig1209/skills/zhihu-aiops)
- [Asset Center API](references/api_asset.md)
- [CMDB Scan API](references/api_cmdb.md)
- [Dashboard and Alarm Summary API](references/api_dashboard.md)
- [Monitor Center API](references/api_monitor.md)
- [VictoriaMetrics API](references/api_victoriametrics.md)
- [Categraf SNMP Metrics API](references/api_snmp_metrics.md)
- [Add OS Monitoring Workflow](references/add-os-monitor.md)
- [Managed Asset Inspection Workflow](references/inspection-run.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with JSON, PromQL, and bash examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include authenticated API request examples and operational checklists; generated secrets should be omitted or redacted.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
