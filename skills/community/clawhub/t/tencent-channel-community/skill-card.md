## Description:

腾讯频道(QQ频道)社区管理 skill（CLI 版），用于频道创建、设置、搜索、成员管理、发帖、评论、通知、私信、内容巡检和问答自动回复等任务。

This skill is ready for commercial/non-commercial use.

## Publisher:

[tencent-adm](https://clawhub.ai/user/tencent-adm)

### License/Terms of Use:

MIT-0

## Use Case:

External users and community managers use this skill to operate QQ/Tencent channels through the Tencent channel CLI, including channel administration, member actions, content publishing, notifications, private messages, moderation review, and assisted Q&A workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill relies on a globally installed Tencent channel CLI that may change outside the skill package.

Mitigation: Use a pinned and verified CLI version before granting account access or executing management commands.

Risk: The skill can perform public posting, deletions, member kicks, mutes, approvals, DMs, and notification actions.

Mitigation: Require explicit user confirmation before destructive, permission-changing, private-message, or public-posting operations.

Risk: Some workflows use command strings returned at runtime, including login and notification setup flows.

Mitigation: Review returned commands before execution and avoid blindly running command strings.

Risk: The skill may fetch or transform user-provided URLs for posting workflows.

Mitigation: Avoid automatic URL fetching unless the URL is clearly safe and relevant to the user's requested post.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/tencent-adm/skills/tencent-channel-community)
- [Tencent Connect AI](https://connect.qq.com/ai)
- [频道管理（manage-guild）](artifact/references/manage-guild.md)
- [成员管理（manage-member）](artifact/references/manage-member.md)
- [内容管理（feed）](artifact/references/feed-reference.md)
- [频道消息通知参考](artifact/references/notification-reference.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with Tencent channel CLI commands and JSON command inputs when needed]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include confirmation prompts for destructive actions, QR-code login guidance, notification setup steps, and summarized command results.]

## Skill Version(s):

1.1.5 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
