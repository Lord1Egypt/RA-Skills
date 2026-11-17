## Description:

Create interactive Telegram messages with inline buttons using OpenClaw CLI for selections, confirmations, workflow menus, quick actions, callback handling, and message editing.

This skill is ready for commercial/non-commercial use.

## Publisher:

[netanelrotem](https://clawhub.ai/user/netanelrotem)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and automation builders use this skill to create Telegram bot messages with inline buttons, validate button JSON, and edit messages after callbacks to keep chat workflows clear.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Telegram bot tokens can grant message access for chats where the bot is installed if they are exposed through config files, shell history, or logs.

Mitigation: Store the token in environment variables or secure configuration, keep it out of committed files and logs, and rotate tokens if exposure is suspected.

Risk: Commands can send or edit messages in the wrong Telegram chat if placeholder chat IDs or targets are not replaced carefully.

Mitigation: Use only bots and chats you control, verify the `telegram:CHAT_ID` target before running examples, and keep separate bots for development and production.

Risk: Malformed or oversized button JSON can fail at send time or produce poor mobile usability.

Mitigation: Validate button JSON before sending, keep standard menus to one to three buttons per row, and respect Telegram's documented eight-per-row and 100-total button limits.

Risk: The backup/delete example describes a simulated message flow and could be mistaken for proof that file operations happened.

Mitigation: Treat example confirmation messages as Telegram interaction demos, and implement and verify any real file operation outside this skill before claiming completion.

## Reference(s):

- [Telegram Interactive Buttons ClawHub page](https://clawhub.ai/netanelrotem/skills/telegram-interactive-buttons)
- [Complete reference](references/REFERENCE.md)
- [Setup guide](SETUP.md)
- [OpenClaw documentation](https://docs.openclaw.ai)
- [Telegram Bot API](https://core.telegram.org/bots/api)
- [BotFather](https://t.me/BotFather)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands, JSON button examples, and helper-script guidance.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces Telegram inline-button layouts and OpenClaw command patterns; requires OpenClaw, bash, Telegram bot configuration, and optional Python validation.]

## Skill Version(s):

1.1.2 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
