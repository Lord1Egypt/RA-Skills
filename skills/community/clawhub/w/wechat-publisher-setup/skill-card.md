## Description:

部署微信公众号发布 Agent 团队（画境视觉设计和数澜运营发布），支持封面设计、排版美化、API 发布和数据分析。

This skill is ready for commercial/non-commercial use.

## Publisher:

[little-ke](https://clawhub.ai/user/little-ke)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and WeChat account operators use this skill to deploy a two-agent publishing team that prepares visual assets, formats articles, creates drafts, publishes after confirmation, and reports engagement data.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill stores WeChat publishing credentials locally and may use an unexpected credential file.

Mitigation: Review before installing, use dedicated low-privilege WeChat credentials, confirm the WECHAT_ENV_FILE path, set restrictive file permissions, and rotate credentials if they were already stored.

Risk: Setup behavior may run unsafe shell commands or be influenced by untrusted environment variables.

Mitigation: Run setup only in a controlled environment, review commands before execution, and avoid untrusted environment variables during installation.

Risk: Publication commands can affect the connected WeChat account.

Mitigation: Confirm the target account and require explicit operator approval before creating drafts or publishing.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/little-ke/skills/wechat-publisher-setup)
- [WeChat public platform API base](https://api.weixin.qq.com)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands, Node.js scripts, configuration files, and generated agent workspace files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Node.js and an OpenClaw environment with the content-creation team already deployed.]

## Skill Version(s):

1.0.0 (source: server release evidence and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
