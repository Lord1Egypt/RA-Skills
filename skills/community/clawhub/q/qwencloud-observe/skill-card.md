## Description:

Reports the health, performance, resource status, and actual billed cost of an application deployed by qwencloud-deploy to Alibaba Cloud International in plain language without opening the console.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cuixiaoyang123](https://clawhub.ai/user/cuixiaoyang123)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to observe qwencloud-deployed applications on Alibaba Cloud International. It summarizes application reachability, ECS and optional RDS health, network exposure, resilience signals, unknowns, and actual billed USD cost.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requires Alibaba Cloud permissions that can run commands on ECS instances and install the CloudMonitor agent.

Mitigation: Use a tightly scoped, temporary RAM role, remove or separate cms:InstallMonitoringAgent and broad ecs:RunCommand where possible, and review command content before execution.

Risk: A malicious or incorrect .qwencloud-deploy file could point observations at unintended resources.

Mitigation: Run the skill only in trusted project directories and verify the resolved region and resource IDs before cloud queries.

Risk: Cloud logs, state files, command output, or slow SQL records can expose credentials or sensitive values if handled carelessly.

Mitigation: Do not read .qwencloud-deploy.local, do not print AccessKeys or tokens, and redact passwords, connection strings, cookies, signed URLs, and SQL literals from outputs.

## Reference(s):

- [Observe Workflow](references/workflow.md)
- [Observe Application](references/observe_application.md)
- [Observe ECS](references/observe_ecs.md)
- [Observe RDS](references/observe_rds.md)
- [Observe Network](references/observe_network.md)
- [Observe Resilience](references/observe_resilience.md)
- [Observe Cost](references/observe_cost.md)
- [RAM Policies](references/ram_policies.md)
- [Aliyun CLI Install and Credential Check](references/cli_installation_guide.md)
- [Aliyun CLI Gotchas](references/api_gotchas.md)
- [Alibaba Cloud Billing API Documentation](https://help.aliyun.com/en/user-center/developer-reference/call-api-operations-to-manage-resources-and-costs)
- [Alibaba Cloud RDS Performance Parameters](https://help.aliyun.com/en/rds/developer-reference/performance-parameters)
- [Alibaba Cloud RDS DescribeSlowLogRecords API](https://help.aliyun.com/zh/rds/developer-reference/api-rds-2014-08-15-describeslowlogrecords)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, JSON, Files, Guidance]

**Output Format:** [Plain-language text or Markdown summaries, optional Markdown/HTML report files, and structured JSON handoff or timeline records.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes health score, grade, layer evidence, data timestamp, unknowns, risks, and actual billed USD cost; cost is not estimated.]

## Skill Version(s):

1.0.3 (source: server release metadata; artifact frontmatter says 1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
