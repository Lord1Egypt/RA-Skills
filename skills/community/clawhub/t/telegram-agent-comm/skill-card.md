## Description:

规范多角色 Agent 使用统一格式和账号通过 Telegram Bot 向固定用户 ID 发送任务汇报、问题上报和协作消息。

This skill is ready for commercial/non-commercial use.

## Publisher:

[thcjp](https://clawhub.ai/user/thcjp)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent teams use this skill to standardize Telegram progress updates across main, architect, backend, frontend, product, content, crawler, and QA agent roles. It is intended for coordinated task status reporting, completion summaries, and issue escalation to a configured Telegram recipient.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Routine agent updates are routed to fixed Telegram ID 5440561025.

Mitigation: Install only when that ID is the intended recipient, or revise the target routing before use.

Risk: Messages may expose project paths, technical details, or other sensitive status information.

Mitigation: Redact sensitive content before sending Telegram updates and avoid using this channel for confidential data.

Risk: Telegram Bot tokens and account configuration are required for operation.

Mitigation: Keep bot tokens outside committed files, restrict access to configuration files, and rotate tokens if exposure is suspected.

Risk: The artifact declares broad read, exec, write, glob, and grep tool usage.

Mitigation: Remove unnecessary permissions where the agent platform allows it and review generated commands before execution.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/thcjp/skills/telegram-agent-comm)
- [Publisher profile](https://clawhub.ai/user/thcjp)
- [Telegram Bot API endpoint](https://api.telegram.org)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with JSON-like Telegram message call examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Messages are organized by fixed role account identifiers and a fixed Telegram target ID.]

## Skill Version(s):

1.0.1 (source: server release metadata and artifact frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
