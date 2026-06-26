## Description: <br>
Send messages, manage chats, handle files, and automate Telegram bot workflows via the Telegram Bot API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hith3sh](https://clawhub.ai/user/hith3sh) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, operators, and other OpenClaw users use this skill to work with Telegram bots through ClawLink, including sending messages, reading chat metadata, managing chat workflows, and handling files or media. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Telegram bot tokens are sensitive credentials handled through ClawLink. <br>
Mitigation: Install only if ClawLink is trusted for the connected bot token, and reconnect or revoke the Telegram bot token if access should change. <br>
Risk: Write actions can send, delete, forward, or modify Telegram content and chat settings. <br>
Mitigation: Review each preview carefully and approve execution only when the target chat, content, and action match the user's intent. <br>
Risk: Admin-scoped actions can affect groups or channels where the bot has elevated rights. <br>
Mitigation: Limit bot admin permissions to the minimum needed and double-check invite-link, deletion, moderation, and command changes before confirmation. <br>


## Reference(s): <br>
- [ClawHub Telegram Skill Page](https://clawhub.ai/hith3sh/telegram-messaging) <br>
- [Telegram Bot API Documentation](https://core.telegram.org/bots/api) <br>
- [Telegram Bot Features](https://core.telegram.org/bots/features) <br>
- [BotFather](https://t.me/botfather) <br>
- [ClawLink OpenClaw Docs](https://docs.claw-link.dev/openclaw) <br>
- [ClawLink Verification](https://claw-link.dev/verify) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and JSON tool parameters] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Guides live Telegram tool discovery and uses previews before write actions.] <br>

## Skill Version(s): <br>
0.2.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
