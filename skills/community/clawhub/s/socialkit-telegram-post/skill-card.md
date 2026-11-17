## Description:

Posts a message, photo, video or album to a Telegram channel or group through the official Bot API, as the user's own bot, after the user approves it.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ahmadhussain0335](https://clawhub.ai/user/ahmadhussain0335)

### License/Terms of Use:

MIT-0

## Use Case:

People who manage Telegram channels or groups use this skill to prepare and, after explicit user approval, publish text, photo, video, or album posts through their own bot.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A leaked bot token can let others control the bot.

Mitigation: Keep the token secret, store it in environment variables, grant only the required posting permission, and revoke it with BotFather if it leaks.

Risk: Remote media may change after the post is reviewed.

Mitigation: Confirm the destination, text, and attachments before approval; use local copies when the exact media contents matter.

## Reference(s):

- [Telegram setup](references/setup.md)
- [Telegram Bot API](https://core.telegram.org/bots/api)

## Skill Output:

**Output Type(s):** [Text, JSON, Shell commands, Guidance]

**Output Format:** [Telegram post draft with text and media metadata, plus Markdown guidance and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Text posts support up to 4,096 characters; captions up to 1,024. The skill pauses for the user's approval before publishing.]

## Skill Version(s):

0.3.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
