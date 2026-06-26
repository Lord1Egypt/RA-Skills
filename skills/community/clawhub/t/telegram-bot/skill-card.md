## Description: <br>
Build and manage Telegram bots via the Telegram Bot API. Create bots, send messages, handle webhooks, manage groups and channels. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Sebastian-Buitrag0](https://clawhub.ai/user/Sebastian-Buitrag0) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and operators use this skill to configure and operate Telegram bots, including bot setup, messaging, updates, webhooks, and group or channel management. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: A Telegram bot token grants the agent access to operate the configured bot. <br>
Mitigation: Use a dedicated bot token and keep it out of chats, logs, screenshots, and repositories. <br>
Risk: Commands can send messages or perform moderation actions against the wrong chat, user, or message ID. <br>
Mitigation: Test commands in a private chat first and verify chat, user, and message IDs before write or moderation actions. <br>
Risk: Webhook configuration can expose bot updates to an unintended endpoint. <br>
Mitigation: Configure webhooks only to HTTPS endpoints you control. <br>


## Reference(s): <br>
- [Telegram Bot API Documentation](https://core.telegram.org/bots/api) <br>
- [BotFather Commands](https://core.telegram.org/bots#botfather) <br>
- [Telegram Bot API Changelog](https://core.telegram.org/bots/api-changelog) <br>
- [ClawHub Skill Page](https://clawhub.ai/Sebastian-Buitrag0/telegram-bot) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline shell commands and JSON payload examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires curl, jq, and TELEGRAM_BOT_TOKEN for command execution.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
