## Description: <br>
Searches, aggregates, and investigates centralized logs in VMware Aria Operations for Logs, formerly vRealize Log Insight, through read-only MCP and CLI queries. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zw008](https://clawhub.ai/user/zw008) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and infrastructure engineers use this skill to search VMware/vSphere log events, identify volume spikes, inspect fields and alert history, and support incident investigation without modifying the Log Insight appliance. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Local credential handling can expose Log Insight passwords if the .env file is readable or long-lived on disk. <br>
Mitigation: Keep ~/.vmware-log-insight/.env chmod 600 and prefer injecting VMWARE_LOG_INSIGHT_<TARGET>_PASSWORD from a secret manager at process start. <br>
Risk: Returned log events can contain sensitive operational data. <br>
Mitigation: Limit use to authorized users, prefer narrow time windows and filters, and redact sensitive log content before sharing outputs. <br>
Risk: Using an account with broader privileges than needed increases impact if credentials are mishandled. <br>
Mitigation: Use a read-only Log Insight service account because the skill only needs event, aggregation, field, version, and alert-query access. <br>
Risk: Disabling TLS verification for self-signed lab appliances can weaken transport protection. <br>
Mitigation: Keep TLS verification enabled by default and disable it only for controlled lab appliances where the connection path is trusted. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/zw008/skills/vmware-log-insight) <br>
- [Capabilities](artifact/references/capabilities.md) <br>
- [CLI Reference](artifact/references/cli-reference.md) <br>
- [Setup Guide](artifact/references/setup-guide.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with CLI commands and JSON query results] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Read-only log search, aggregation, field, version, and alert-query outputs may include sensitive operational log data.] <br>

## Skill Version(s): <br>
1.6.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
