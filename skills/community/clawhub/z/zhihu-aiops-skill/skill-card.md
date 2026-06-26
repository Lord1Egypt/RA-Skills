## Description: <br>
智护运维平台 AIOps 集成技能，提供资产中心、CMDB 资产发现、监控告警、展示中心、VictoriaMetrics、Categraf SNMP 指标、操作系统监控添加和纳管设备智能巡检相关 API 参考与工作流。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[luckypig1209](https://clawhub.ai/user/luckypig1209) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
IT operations engineers and platform operators use this skill to ask an agent for Zhihu AIOps API guidance, monitoring queries, alarm summaries, asset discovery workflows, managed-device inspection steps, and operating-system monitor onboarding support. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill handles Zhihu platform credentials, VictoriaMetrics endpoints, and SSH or WinRM connection details. <br>
Mitigation: Configure credentials through environment variables or a secret manager, avoid pasting production secrets into chat, and prefer temporary or least-privilege accounts. <br>
Risk: Some documented workflows can create, update, delete, restart, or otherwise change monitored assets and scan tasks. <br>
Mitigation: Review proposed API calls and request bodies before execution, especially write actions and actions against production monitoring environments. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/luckypig1209/zhihu-aiops-skill) <br>
- [Asset Center API reference](artifact/references/api_asset.md) <br>
- [CMDB and asset discovery API reference](artifact/references/api_cmdb.md) <br>
- [Dashboard API reference](artifact/references/api_dashboard.md) <br>
- [Monitor API reference](artifact/references/api_monitor.md) <br>
- [VictoriaMetrics API reference](artifact/references/api_victoriametrics.md) <br>
- [Categraf SNMP metrics reference](artifact/references/api_snmp_metrics.md) <br>
- [Managed-device inspection workflow](artifact/references/inspection-run.md) <br>
- [Operating-system monitor onboarding workflow](artifact/references/add-os-monitor.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline JSON and bash examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include API request examples, PromQL queries, environment variable guidance, and operational checklists.] <br>

## Skill Version(s): <br>
2.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
