## Description:

用于安装蚁小二 CLI、同步正式技能并完成基础配置与环境自检。

This skill is ready for commercial/non-commercial use.

## Publisher:

[yixiaoer888](https://clawhub.ai/user/yixiaoer888)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to install the yxer CLI, sync the formal yixiaoer skill, initialize API-key based configuration, and run an environment self-check before using the production publishing workflow.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill defaults to mutable global CLI installation and global skill synchronization.

Mitigation: Install only after trusting the yixiaoer888 publisher, prefer a pinned reviewed version, and use local sync or install options when global availability is not required.

Risk: The setup flow uses an API key during configuration.

Mitigation: Avoid putting real API keys directly in chat or reusable shell history, and provide secrets only through an appropriate local secret-handling process.

Risk: Security evidence marks the release suspicious because it bootstraps a CLI and remote skill sync workflow.

Mitigation: Review the generated shell commands before execution and run the provided environment self-check after installation.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/yixiaoer888/skills/yixiaoer-publish)
- [Publisher profile](https://clawhub.ai/user/yixiaoer888)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs installation, synchronization, configuration, and self-check steps for the yxer CLI; it does not produce publishing payloads.]

## Skill Version(s):

1.6.5 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
