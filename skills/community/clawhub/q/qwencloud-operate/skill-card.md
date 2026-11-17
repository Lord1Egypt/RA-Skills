## Description:

Diagnoses unavailable or slow applications deployed by qwencloud-deploy on Alibaba Cloud International, runs minimal read-only checks, and performs one explicitly confirmed recovery action followed by verification.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cuixiaoyang123](https://clawhub.ai/user/cuixiaoyang123)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and cloud operators use this skill to diagnose and recover qwencloud-deploy applications on Alibaba Cloud International. It supports read-only fault isolation and confirmed recovery for ECS, Nginx, RDS-related app symptoms, EIP binding, certificate, security-group, and disk-space conditions.

### Deployment Geography for Use:

Global for Alibaba Cloud International regions; excludes Aliyun China.

## Known Risks and Mitigations:

Risk: The skill can require broad Alibaba Cloud permissions for diagnosis and recovery.

Mitigation: Use a dedicated, short-lived, least-privilege Alibaba Cloud role scoped to the intended regions and resources; avoid using the wildcard RAM policy as written.

Risk: Cloud Assistant commands and log retrieval can expose sensitive data or affect running services.

Mitigation: Inspect .qwencloud-deploy before use, never read local credential files, redact secrets from evidence and audit records, and require explicit approval before log retrieval or cloud mutation.

Risk: Recovery actions can cause downtime, increase cost, or change public exposure.

Mitigation: Present the target, impact, cost, and verification plan before each action; perform one action at a time, stop on unexpected states, and verify before proposing another change.

Risk: The Aliyun CLI and credentials are part of the execution trust boundary.

Mitigation: Pin and verify the Aliyun CLI installation and use configured credentials without printing or collecting AccessKey, SecretKey, STS token, or full connection strings.

## Reference(s):

- [Operate workflow](references/workflow.md)
- [Minimal diagnosis](references/diagnose.md)
- [RAM policies](references/ram_policies.md)
- [Aliyun CLI install and credential check](references/cli_installation_guide.md)
- [Aliyun CLI gotchas](references/api_gotchas.md)
- [Recover: start a stopped ECS](references/recover_ecs.md)
- [Recover: reboot a hung ECS](references/recover_reboot.md)
- [Recover: restart the app service](references/recover_app.md)
- [Recover: Nginx](references/recover_nginx.md)
- [Recover: re-bind the EIP](references/recover_eip.md)
- [Recover: allow security-group ingress](references/recover_securitygroup.md)
- [Recover: RDS-related handling](references/recover_rds.md)
- [Recover: re-issue the certificate](references/recover_cert.md)
- [Recover: reclaim disk space](references/recover_disk.md)
- [Alibaba Cloud CLI documentation](https://help.aliyun.com/zh/cli/)
- [Alibaba Cloud AccessKey management](https://ram.console.aliyun.com/manage/ak)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown or plain text with inline Aliyun CLI shell commands and JSON audit records]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Recovery actions are proposed one at a time, gated by explicit user confirmation, verified after execution, and recorded with secrets redacted.]

## Skill Version(s):

1.0.3 (source: server release evidence; artifact frontmatter lists 1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
