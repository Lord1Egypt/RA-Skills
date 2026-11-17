## Description:

Telegram CLI for reading, searching, and sending messages. Use when the user asks about Telegram messages, wants to check inbox, search chats, send messages, or look up contacts and groups.

This skill is ready for commercial/non-commercial use.

## Publisher:

[arein](https://clawhub.ai/user/arein)

### License/Terms of Use:

MIT

## Use Case:

Developers and agent users use this skill to inspect Telegram chats, search message history, check unread messages, look up contacts or group information, and send or reply to Telegram messages through a CLI.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requires access to a Telegram account, private messages, contacts, groups, and live messaging capabilities.

Mitigation: Use it only when account access is acceptable, inspect the installed package, prefer a pinned reviewed package version or commit, and remove stored credentials when no longer needed.

Risk: Chat export, reading, search, and send operations can expose or modify sensitive Telegram content.

Mitigation: Limit use to intended chats, review commands before execution, and confirm where credentials and session data are stored.

## Reference(s):

- [Telegram API application setup](https://my.telegram.org/apps)
- [ClawHub skill page](https://clawhub.ai/arein/skills/tg)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands; CLI commands can return JSON, Markdown, or plain text.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Telegram API credentials and local session configuration.]

## Skill Version(s):

0.1.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
