## Description:

Manages a Telegram userbot autopilot that responds to private messages as the user with AI, including contact allowlists, response style configuration, owner notifications, and Telegram paid-media workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[shor73](https://clawhub.ai/user/shor73)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to set up an AI-assisted Telegram userbot that replies to approved private contacts, manages response tone and contact settings, and sends Telegram paid media through channels.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can use a reusable Telegram session to read private chats and send messages as the account owner.

Mitigation: Use a dedicated or low-risk Telegram account, tightly limit the contact allowlist, and protect .session files like passwords.

Risk: Setup handles Telegram API credentials, phone login, optional 2FA, and AI provider API keys.

Mitigation: Avoid command-line or plaintext-file 2FA handling where possible, keep config.json private, and never commit generated secrets or sessions.

Risk: Owner notifications can forward private messages and generated replies through a Telegram bot.

Mitigation: Enable notifications only when needed and only with a bot token and chat ID controlled by the account owner.

Risk: Paid-media helpers can post paid content to channels and send invite links to recipients.

Mitigation: Review every paid-media target, file, price, and message before running the action.

## Reference(s):

- [Telegram Authentication Flow](references/telegram-auth.md)
- [Telegram API Authentication](https://core.telegram.org/api/auth)
- [Telegram Paid Media API](https://core.telegram.org/api/paid-media)
- [Telegram API Development Tools](https://my.telegram.org)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance, files]

**Output Format:** [Markdown guidance with inline JSON configuration examples and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce local configuration, Telegram session, code-entry, and conversation-history files when the user runs the scripts.]

## Skill Version(s):

1.1.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
