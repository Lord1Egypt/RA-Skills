## Description:

Build and manage Telegram bots via the Telegram Bot API, including bot creation, message sending, webhook handling, and group or channel management.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sebastian-buitrag0](https://clawhub.ai/user/sebastian-buitrag0)

### License/Terms of Use:


## Use Case:

Developers and bot operators use this skill to configure Telegram bots and run Telegram Bot API commands for messages, media, webhooks, updates, group administration, and callback interactions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Bot-token access lets the agent operate the Telegram bot associated with TELEGRAM_BOT_TOKEN.

Mitigation: Install only when that access is intended, keep the token private, and confirm bot actions before execution.

Risk: Commands can send messages, media, files, locations, and moderation actions to selected chats or users.

Mitigation: Confirm chat IDs, user IDs, file paths, locations, and moderation commands before running generated curl commands.

Risk: Telegram messages may include secrets or unnecessary personal data.

Mitigation: Avoid sending secrets or unneeded personal data through Telegram.

Risk: The echo-bot sample is useful starter code but is not production-hardened.

Mitigation: Harden input handling, permissions, logging, and deployment controls before using the sample in production.

## Reference(s):

- [Telegram Bot API Documentation](https://core.telegram.org/bots/api)
- [BotFather Commands](https://core.telegram.org/bots#botfather)
- [Telegram Bot API Changelog](https://core.telegram.org/bots/api-changelog)
- [ClawHub Skill Page](https://clawhub.ai/sebastian-buitrag0/skills/telegram-bot)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline bash, JSON, and HTML code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Commands require curl, jq, and TELEGRAM_BOT_TOKEN; examples call the Telegram Bot API over the network.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
