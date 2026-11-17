## Description:

Bundle entry for TencentDB PostgreSQL skills that routes Tencent Cloud PostgreSQL management, extension-service, inspection, and slow-SQL requests into bounded scenario workflows with read-only preflight and confirmation gates for ambiguous or high-risk changes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tencent-adm](https://clawhub.ai/user/tencent-adm)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, database operators, and cloud administrators use this skill to inspect and manage TencentDB for PostgreSQL instances, including instance status, backup and access checks, mem0 and REST service operations, routine metric inspection, and slow-SQL lookup.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requires Tencent Cloud credentials that may carry broad PostgreSQL administration authority.

Mitigation: Use a least-privilege CAM sub-account, prefer short-lived or session credentials, and provide secrets only through the runtime environment.

Risk: Persistent shell, launchctl, or Windows user-variable setup can leave cloud secrets available beyond the immediate session.

Mitigation: Avoid persistent storage for production secrets; inject credentials only for the active host process when possible and rotate any exposed keys.

Risk: Endpoint override behavior for signed API calls can redirect privileged requests if used with production credentials.

Mitigation: Do not use endpoint override variables with production credentials unless the target endpoint is strictly controlled and reviewed.

Risk: Write, fee-impacting, or public-exposure changes can alter database service state or increase attack surface.

Mitigation: Rely on the documented read-only preflight and explicit confirmation gates before write actions, public REST exposure, security-group replacement, recovery, backup download, or other high-risk follow-up operations.

## Reference(s):

- [TencentDB PostgreSQL Skill on ClawHub](https://clawhub.ai/tencent-adm/skills/tencentdb-postgresql-skill)
- [Tencent Cloud API Key Management](https://console.cloud.tencent.com/cam/capi)
- [Tencent Cloud PostgreSQL Console](https://console.cloud.tencent.com/postgres)
- [Tencent Cloud Python SDK Documentation](https://cloud.tencent.com/document/sdk/Python)
- [Tencent Cloud API Documentation](https://cloud.tencent.com/document/api)
- [Tencent Cloud PostgreSQL API Endpoint](https://postgres.tencentcloudapi.com)
- [Management scenario](references/tencent-pg-management/SKILL.md)
- [mem0 deployment scenario](references/tencent-pg-mem0-deploy/SKILL.md)
- [REST deployment and troubleshooting scenario](references/tencent-pg-rest-deploy/SKILL.md)
- [PostgreSQL inspection scenario](references/tencent-pg-inspection/SKILL.md)
- [Slow SQL lookup scenario](references/tencent-pg-slowquery-diagnosis/SKILL.md)
- [Common region normalization rules](references/common/region_normalization.md)
- [Common error handling templates](references/common/error_handling.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown and structured text with inline shell commands, status summaries, API facts, and next-step guidance.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include Tencent Cloud OpenAPI facts, TaskId values, service status, metric summaries, slow-SQL rows, and confirmation prompts for risky follow-up actions.]

## Skill Version(s):

1.0.3 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
