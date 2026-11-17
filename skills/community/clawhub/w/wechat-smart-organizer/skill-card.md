## Description:

微信聊天记录智能整理技能。当用户想要读取微信聊天记录、提取关键信息、存储到Obsidian笔记、或创建日历事件时使用此技能。功能包括：查询会话、读取聊天记录、搜索关键词、提取任务/时间/待办事项、智能分类存储到Obsidian、创建日历提醒。

This skill is ready for commercial/non-commercial use.

## Publisher:

[pjpan](https://clawhub.ai/user/pjpan)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to inspect local WeChat conversations, extract tasks, dates, contacts, links, and meeting-related items, and organize the results into Obsidian notes or calendar-ready data.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles private WeChat messages and may expose sensitive conversations through generated notes or calendar data.

Mitigation: Review extracted content before saving or sharing it, and avoid processing conversations that contain sensitive personal, financial, or confidential information unless explicitly needed.

Risk: The skill asks users to install and initialize a third-party WeChat CLI with broad local access, including sudo initialization and macOS Full Disk Access.

Mitigation: Use a pinned and verified CLI package, avoid sudo unless the publisher clearly justifies it, and grant only the narrowest local permissions required for the task.

Risk: Obsidian vaults may sync generated notes to external services or shared workspaces.

Mitigation: Confirm the selected vault and its sync or sharing settings before writing extracted WeChat content.

## Reference(s):

- [Command reference](references/commands.md)
- [ClawHub skill page](https://clawhub.ai/pjpan/skills/wechat-smart-organizer)
- [Project homepage](https://github.com/ppj/wechat-smart-organizer)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell command examples, JSON extraction summaries, Markdown Obsidian notes, and calendar event data]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May read private local WeChat content and write selected extracted content into a user-selected Obsidian vault.]

## Skill Version(s):

1.0.0 (source: frontmatter and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
