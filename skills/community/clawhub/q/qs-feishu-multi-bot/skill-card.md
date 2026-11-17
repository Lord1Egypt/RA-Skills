## Description:

Guides developers through configuring multiple Feishu bots on one OpenClaw Gateway, with each bot routed to a separate OpenClaw agent with isolated workspaces, sessions, auth profiles, and optional models.

This skill is ready for commercial/non-commercial use.

## Publisher:

[qushengswaych](https://clawhub.ai/user/qushengswaych)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to configure one OpenClaw Gateway instance for multiple Feishu bot accounts and route each account, user, or group to the intended OpenClaw agent.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Open Feishu access settings could let unintended users reach configured agents.

Mitigation: Keep pairing or explicit allowlists enabled for direct messages and groups unless public access is intentionally required.

Risk: Public-facing agents may expose tools, files, credentials, logs, or rate limits beyond the intended audience.

Mitigation: Restrict tools, file access, credentials, logging, and rate limits for any agent reachable through Feishu.

Risk: The OpenClaw configuration contains Feishu application secrets.

Mitigation: Protect the configuration file and do not commit it to source control.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/qushengswaych/skills/qs-feishu-multi-bot)
- [Feishu Open Platform](https://open.feishu.cn/app)

## Skill Output:

**Output Type(s):** [markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with JSON5 and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Provides setup steps, routing examples, verification commands, and security notes for OpenClaw and Feishu configuration.]

## Skill Version(s):

1.0.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
