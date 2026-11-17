## Description:

Operates TencentCloud Oceanus workspaces through a Python CLI for SQL/JAR job lifecycle tasks, configuration publishing, runtime control, dependency resources, folders, metadata browsing, events, and logs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tencent-adm](https://clawhub.ai/user/tencent-adm)

### License/Terms of Use:

Apache-2.0

## Use Case:

Developers and operations engineers use this skill to inspect and manage TencentCloud Oceanus workspace resources, including SQL and JAR jobs, resource dependencies, folders, metadata, events, and logs. It supports both read-only investigation and guarded resource-changing workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can change TencentCloud Oceanus resources, including job creation, job runs, resource uploads, configuration publication, stops, and folder deletion.

Mitigation: Use least-privilege credentials and manually confirm every resource-changing or destructive operation before execution.

Risk: Long-lived TencentCloud credentials, untrusted endpoints, or unchecked COS upload/download URLs could expose cloud access or data.

Mitigation: Prefer short-lived credentials, avoid storing permanent keys in shell profiles, only set custom endpoints when trusted, and validate COS URLs before sharing or using them.

Risk: Publishing job configurations without review can apply unintended SQL, JAR, dependency, or runtime changes.

Mitigation: Preserve the draft review gate and wait for explicit human approval before publishing a new job configuration.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/tencent-adm/skills/tencentcloud-oceanus-ops)
- [Agent Operating Protocol](references/agent-operating-protocol.md)
- [Command Catalog](references/command-catalog.md)
- [Command Map](references/command-map.md)
- [Credential Setup](references/credential-setup.md)
- [Enum Reference](references/enum-reference.md)
- [Error Handling Matrix](references/error-handling.md)
- [Oceanus Product Model](references/oceanus-product-model.md)
- [Playbook: Create SQL Job](references/playbooks/create-sql-job.md)
- [Playbook: Create JAR Job](references/playbooks/create-jar-job.md)
- [Playbook: Modify Job Config](references/playbooks/modify-job-config.md)
- [Playbook: Job Runtime Operations](references/playbooks/job-runtime-ops.md)
- [Playbook: Job Observability](references/playbooks/job-observability.md)
- [Playbook: Dependency Resource Management](references/playbooks/dependency-management.md)
- [TencentCloud CAM API key console](https://console.cloud.tencent.com/cam/capi)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration instructions, Guidance, Text]

**Output Format:** [Markdown with inline bash commands and JSON, table, or text CLI results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Commands require a TencentCloud region; resource-changing operations require confirmation; credentials are read from environment variables.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
