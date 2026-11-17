## Description:

pushplus lets agents send PushPlus notifications across WeChat, email, SMS, enterprise WeChat, DingTalk, Feishu, webhooks, app, voice, and ClawBot channels, and query or manage related PushPlus resources.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lei-mu](https://clawhub.ai/user/lei-mu)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operations teams use this skill to send monitoring alerts, scheduled task results, business exception notifications, and everyday reminders through PushPlus. They can also configure notification channels, inspect delivery results, and manage PushPlus groups or message tokens when account-management credentials are available.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can perform broad PushPlus account-management operations, including creating, changing, deleting, or redirecting tokens, groups, channel configuration, defaults, friends, and preprocessing settings.

Mitigation: Require explicit user confirmation before OpenAPI operations that create, change, delete, or redirect account configuration, and expose OpenAPI credentials only for workflows that need account management.

Risk: Verbose mode may expose real tokens or private notification content in logs.

Mitigation: Avoid verbose mode when using real credentials or sensitive message content, and redact tokens before sharing logs.

Risk: Using broad user tokens for simple notifications expands the impact of credential exposure or unintended operations.

Mitigation: Use least-privileged message tokens where possible, and reserve PUSHPLUS_USER_TOKEN plus PUSHPLUS_SECRET_KEY for confirmed management tasks.

## Reference(s):

- [PushPlus API Reference](artifact/references/api.md)
- [PushPlus Documentation](https://www.pushplus.plus/doc/)
- [PushPlus Apifox API Documentation](https://pushplus.apifox.cn/)
- [PushPlus Token Management](https://www.pushplus.plus/uc-dev.html)
- [PushPlus Website](https://www.pushplus.plus)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with Python and shell command examples; PushPlus API calls return JSON-like dictionaries.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires PushPlus tokens or OpenAPI credentials for live API operations.]

## Skill Version(s):

1.1.0 (source: server release evidence and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
