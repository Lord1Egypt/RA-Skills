## Description:

帮助代理查看当前登录知识星球用户的个人资料、跨星球主题足迹，并在明确确认后提交 NPS 评分和产品建议。

This skill is ready for commercial/non-commercial use.

## Publisher:

[zsxq](https://clawhub.ai/user/zsxq)

### License/Terms of Use:

MIT-0

## Use Case:

External users and their agents use this skill to inspect the active 知识星球 account, review recent cross-star posting footprints, and submit product feedback after confirmation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: NPS feedback is a write operation and may submit user-supplied suggestions to 知识星球 official channels.

Mitigation: Require explicit confirmation of the score and suggestion before execution, and keep the suggestion within the documented 500-character limit.

Risk: Profile and footprint JSON can expose private account information.

Mitigation: Treat returned user IDs, profile fields, account bindings, and posting history as private user data and avoid unnecessary sharing or logging.

Risk: Shell command construction around NPS suggestions can mishandle user-supplied text.

Mitigation: Prefer direct argument-array execution or carefully quoted arguments instead of interpolating suggestions into shell strings.

Risk: A mutable global zsxq-cli install or upgrade can change behavior unexpectedly.

Mitigation: Use a pinned, reviewed zsxq-cli version when deploying the skill in managed environments.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/zsxq/skills/zsxq-user)
- [user +info（查看个人资料）](references/zsxq-user-info.md)
- [user +footprints（查看主题足迹）](references/zsxq-user-footprints.md)
- [user +nps（提交 NPS 反馈）](references/zsxq-user-nps.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, JSON, guidance]

**Output Format:** [Markdown guidance with inline shell commands and optional JSON CLI output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires zsxq-cli and an authenticated 知识星球 account.]

## Skill Version(s):

1.3.1 (source: frontmatter and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
