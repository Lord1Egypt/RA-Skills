## Description:

智能助理核心技能，支持 20 轮对话上下文、情感识别、主动提醒、日程管理，集成飞书/钉钉/企业微信。

This skill is ready for commercial/non-commercial use.

## Publisher:

[pengong101](https://clawhub.ai/user/pengong101)

### License/Terms of Use:

MIT-0

## Use Case:

Employees and developers use this skill to support assistant workflows that interpret intent, retain conversation context, adapt responses to emotion, and propose reminder or schedule actions across workplace messaging platforms.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security review says the artifact promises live calendar, reminder, and platform actions that the reviewed code does not implement or safely scope.

Mitigation: Treat action confirmations as proposals until verified integrations exist, and require explicit user confirmation before real meetings, reminders, notifications, or calendar changes are made.

Risk: The artifact asks for Feishu, DingTalk, and WeChat Work bot tokens and includes plaintext configuration examples.

Mitigation: Store tokens in a secret manager or protected environment variables, avoid plaintext config files, use least-privilege bot permissions, and rotate credentials regularly.

Risk: Memory, habit learning, calendar updates, and message sending can expose private workplace or personal data.

Mitigation: Enable these capabilities only with clear privacy controls, data-retention limits, and user-visible approval for sensitive actions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/pengong101/skills/secretary-core)
- [README](artifact/README.md)
- [Context manager notes](artifact/CONTEXT_MANAGER.md)
- [Intent understanding notes](artifact/INTENT_UNDERSTANDING.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with Python and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May require messaging bot tokens; review outputs before enabling calendar, reminder, or message actions.]

## Skill Version(s):

4.0.0 (source: server release evidence and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
