## Description:

Fetch Telegram chat message history via MTProto user API (Telethon). Use when needing to read old messages from any Telegram chat, group, or forum topic that the bot API can't access. Supports fetching by chat ID, forum topic/thread, message count, pagination, and JSON output. Requires one-time user login with phone number + 2FA.

This skill is ready for commercial/non-commercial use.

## Publisher:

[rhlsthrm](https://clawhub.ai/user/rhlsthrm)

### License/Terms of Use:


## Use Case:

Developers and agent operators use this skill to retrieve account-accessible Telegram chat, group, or forum-topic history when Telegram Bot API history access is insufficient. It supports bounded history retrieval, pagination, sender metadata, and JSON output for downstream analysis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can read and print private Telegram message history available to the logged-in user account.

Mitigation: Use a dedicated Telegram account with access only to the required chats, limit requested chats and message counts, and review retrieved history before sharing or storing it.

Risk: Telegram API credentials, session files, verification codes, or 2FA passwords could expose account access if handled insecurely.

Mitigation: Protect or relocate api_credentials.json and session files, avoid passing 2FA passwords on the command line, and delete or revoke the Telegram session when work is complete.

## Reference(s):

- [Telegram API app credentials](https://my.telegram.org/apps)
- [ClawHub skill page](https://clawhub.ai/rhlsthrm/skills/telegram-history)

## Skill Output:

**Output Type(s):** [Text, JSON, Shell commands, Configuration instructions]

**Output Format:** [Plain text or JSON message history, with Markdown setup and usage commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can include message IDs, timestamps, sender identifiers, sender names, usernames, reply targets, and message text.]

## Skill Version(s):

1.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
