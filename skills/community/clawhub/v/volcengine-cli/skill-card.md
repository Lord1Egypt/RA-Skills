## Description:

Create and manage Volcengine cloud resources using the Volcengine CLI (`ve`), including OpenAPI calls, TOS object operations, and Ark CLI workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[volc-sdk-team](https://clawhub.ai/user/volc-sdk-team)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and cloud operators use this skill to authenticate with Volcengine, discover services and actions, run `ve` commands, troubleshoot errors, and manage cloud resources across compute, networking, load balancing, databases, storage, TOS, and Ark workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Installer and update flows can change local tools or skills and introduce supply-chain exposure.

Mitigation: Prefer the npm/package-manager path or a pinned, verified local installer; avoid pipe-to-shell installation and set VOLCENGINE_CLI_SKIP_SKILLS=1 unless a skill update is intended.

Risk: Custom API hosts or endpoints may receive signed requests or temporary session tokens.

Mitigation: Use only trusted Volcengine endpoints and avoid custom API hosts unless the endpoint is fully trusted.

Risk: The skill can help perform broad credential-bearing cloud operations.

Mitigation: Review generated commands before execution, confirm the intended account and region, and use DryRun or read-only discovery paths when available before making changes.

## Reference(s):

- [Volcengine CLI Skill Guide](artifact/SKILL.md)
- [Common Error Handling](artifact/references/common-errors.md)
- [Console Login Procedure](artifact/references/console-login.md)
- [Extended APIs](artifact/references/extend-apis.md)
- [Cloud Control API Service Notes](artifact/references/cloudcontrol.md)
- [ECS Service Notes](artifact/references/ecs.md)
- [VPC Service Notes](artifact/references/vpc.md)
- [RDS Service Notes](artifact/references/rds.md)
- [Redis Service Notes](artifact/references/redis.md)
- [Storage Service Notes](artifact/references/storage.md)
- [Volcengine CLI Releases](https://github.com/volcengine/volcengine-cli/releases)
- [Ark CLI Skills Repository](https://github.com/volcengine/ark-cli/tree/main/skills)
- [ClawHub Skill Page](https://clawhub.ai/volc-sdk-team/skills/volcengine-cli)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, API calls, Guidance]

**Output Format:** [Markdown with inline shell commands, configuration notes, and JSON-oriented API response guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs may guide authenticated cloud operations and should preserve required Volcengine caller metadata on every command.]

## Skill Version(s):

1.1.4 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
