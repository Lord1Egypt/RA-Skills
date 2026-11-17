## Description:

智护运维平台 AIOps 集成技能，提供资产中心、CMDB 资产发现、监控告警、展示中心、VictoriaMetrics、Categraf SNMP 指标、操作系统监控添加和纳管设备智能巡检相关 API 参考与工作流。

This skill is ready for commercial/non-commercial use.

## Publisher:

[luckypig1209](https://clawhub.ai/user/luckypig1209)

### License/Terms of Use:

MIT-0

## Use Case:

Operations teams and developers use this skill to query Zhihu AIOps assets, alarms, CMDB discovery data, VictoriaMetrics metrics, and SNMP device metrics, and to follow workflows for managed-device inspection and operating-system monitoring onboarding.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can guide state-changing AIOps platform actions such as create, update, delete, import, export, and scan task operations.

Mitigation: Use least-privilege platform accounts and require explicit operator confirmation before running state-changing requests.

Risk: The skill handles platform tokens and host passwords and includes non-HTTPS local or internal endpoint defaults.

Mitigation: Use HTTPS for non-local endpoints, keep secrets in environment variables, avoid reusable host passwords where possible, and redact tokens and passwords from logs.

## Reference(s):

- [资产中心 API 详细参数](references/api_asset.md)
- [CMDB 扫描 API 详细参数](references/api_cmdb.md)
- [展示中心 API 详细参数](references/api_dashboard.md)
- [监控中心 API 详细参数](references/api_monitor.md)
- [VictoriaMetrics API 参考](references/api_victoriametrics.md)
- [Categraf SNMP 指标 API 参考](references/api_snmp_metrics.md)
- [纳管设备巡检 Skill](references/inspection-run.md)
- [操作系统监控添加工作流](references/add-os-monitor.md)
- [ClawHub skill page](https://clawhub.ai/luckypig1209/skills/zhihu-aiops-skill)
- [ClawHub publisher profile](https://clawhub.ai/user/luckypig1209)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration instructions, API calls]

**Output Format:** [Markdown with inline bash, JSON, and PromQL examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses environment variables for platform API, credentials, and VictoriaMetrics endpoint.]

## Skill Version(s):

2.1.0 (source: server release metadata; artifact frontmatter reports 1.0.1)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
