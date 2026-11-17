## Description:

Send messages, manage chats, handle files, and automate Telegram bot workflows via the Telegram Bot API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hith3sh](https://clawhub.ai/user/hith3sh)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, and operations teams use this skill to send Telegram bot messages, inspect chats, manage bot commands, handle media, and automate notifications through ClawLink-hosted Telegram Bot API tooling.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The setup installs and enables an external ClawLink plugin and hosted service that stores the connected Telegram bot token and proxies Telegram requests.

Mitigation: Install only when the user trusts ClawLink, understands the hosted credential flow, and has reviewed the enabled plugin access.

Risk: Telegram write actions can send, delete, forward, moderate, or create invite-link changes in chats where the bot has permission.

Mitigation: Keep explicit user confirmation in place for write operations and preview the intended action before calling the tool.

## Reference(s):

- [Telegram Bot API Documentation](https://core.telegram.org/bots/api)
- [Telegram Bot Features](https://core.telegram.org/bots/features)
- [BotFather](https://t.me/botfather)
- [ClawLink OpenClaw Docs](https://docs.claw-link.dev/openclaw)
- [ClawHub Skill Page](https://clawhub.ai/hith3sh/skills/telegram-messaging)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration, API calls, markdown]

**Output Format:** [Markdown guidance with inline shell commands and JSON parameters for ClawLink tool calls]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Tool execution depends on the user connecting a Telegram bot through ClawLink; write operations require explicit user confirmation.]

## Skill Version(s):

0.2.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
