## Description:

Read the user's personal Telegram account in a controlled, read-only way via Telethon/MTProto for listing dialogs, reading recent messages, and searching Telegram messages without relying on the Telegram Bot API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ropl-btc](https://clawhub.ai/user/ropl-btc)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to inspect a user's Telegram dialogs and messages through a local read-only CLI. It is suited to narrow, user-directed read tasks such as finding chats, reviewing recent messages, checking unread conversations, or searching message text.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The install command references mutable remote code.

Mitigation: Review and pin the CLI source to a specific audited commit or signed release before installation.

Risk: Telegram API credentials and the local session config are high-value secrets.

Mitigation: Keep TELEGRAM_API_ID, TELEGRAM_API_HASH, TELEGRAM_SESSION_STRING, and ~/.config/telegram-readonly/config.json out of commits, logs, prompts, and shared tool contexts.

Risk: A reusable Telegram session can continue to access the user's account if exposed.

Mitigation: Use the skill only for narrow read tasks and revoke the Telegram session if the config file or session string may have been exposed.

Risk: Unread preservation is best-effort and can depend on Telegram client behavior.

Mitigation: Test unread-state behavior on a low-risk chat before broader use, and stop if reads unexpectedly mark messages as read.

## Reference(s):

- [Setup and safety](references/setup-and-safety.md)
- [Telegram API development tools](https://my.telegram.org)
- [ClawHub skill page](https://clawhub.ai/ropl-btc/skills/telegram-readonly)
- [ClawHub publisher profile](https://clawhub.ai/user/ropl-btc)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and JSON CLI output expectations]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The referenced CLI emits JSON for dialogs, messages, searches, unread dialogs, authentication status, and help output.]

## Skill Version(s):

0.1.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
