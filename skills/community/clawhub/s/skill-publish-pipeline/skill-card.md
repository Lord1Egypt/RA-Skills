## Description:

帮助代理将本地 Skill 发布到 ClawHub 并同步到 GitHub 托管仓库，涵盖发布前检查、dry-run 验证、登录、发布后核验和已知环境陷阱。

This skill is ready for commercial/non-commercial use.

## Publisher:

[junci003](https://clawhub.ai/user/junci003)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill when preparing a local skill for ClawHub publication and optional GitHub source hosting. It guides pre-publication review, publishing commands, device-flow login, repository setup, and post-publication checks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The bundled device-login helper disables HTTPS certificate verification while handling a read/write ClawHub access token.

Mitigation: Review before installing and do not use the helper until TLS verification is fixed.

Risk: Access tokens or token prefixes may be exposed through logs or screenshots during login troubleshooting.

Mitigation: Treat ClawHub tokens as passwords and avoid printing or sharing token values in logs, screenshots, or transcripts.

Risk: Publishing, GitHub push, hide, or delete actions can change public distribution state or hosted source.

Mitigation: Confirm intent before running commands that publish, push, hide, delete, or otherwise modify public release state.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/junci003/skills/skill-publish-pipeline)
- [Publisher profile](https://clawhub.ai/user/junci003)
- [ClawHub](https://clawhub.ai)
- [SkillHub search API](https://lightmake.site/api/v1/search)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with PowerShell, bash, Python, and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose commands that publish to ClawHub, authenticate to ClawHub, inspect releases, create GitHub repositories, push Git commits, or repair Git upstream references.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
