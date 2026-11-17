## Description:

从零创建带 AI 能力的微信小程序项目。当用户想创建一个全新的微信小程序（不是已有项目上添加功能）时触发。集成云开发、数据库、登录、支付等能力。需要 Node.js 18+ 和 mp-skills CLI。

This skill is ready for commercial/non-commercial use.

## Publisher:

[binggg](https://clawhub.ai/user/binggg)

### License/Terms of Use:

MIT-0

## Use Case:

Developers use this skill to plan and create a new AI-enabled WeChat Mini Program project, install initial mp-skills capabilities, and receive setup guidance for appid, cloud environment, database, login, payment, and WeChat developer tooling configuration.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill directs agents to run unpinned CLI commands and install mutable remote skill content.

Mitigation: Install only trusted mp-skills packages and referenced TencentCloudBase skills; prefer pinned versions or immutable commits and inspect generated files before using production resources.

Risk: Using the all-skills installation path can add more remote content than the user has reviewed.

Mitigation: Prefer installing only the selected skills and avoid the --all path unless the full repository contents have been reviewed.

Risk: Generated cloud, AppID, payment, or setup changes could affect real credentials or production cloud resources.

Mitigation: Run setup in a clean project environment and review cloud configuration changes before connecting real credentials, AppIDs, payment settings, or production resources.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/binggg/skills/wxa-create-ai-miniprogram)

## Skill Output:

**Output Type(s):** [Markdown, Shell commands, Configuration instructions, Guidance]

**Output Format:** [Markdown with inline bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include project creation commands, recommended skill installation commands, and manual configuration steps for appid, cloud environment ID, and setup.]

## Skill Version(s):

0.2.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
