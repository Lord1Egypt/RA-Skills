## Description:

Complete guide to connecting OpenClaw with Telegram. Set up bot, configure channels, handle groups/topics, voice messages, inline buttons, media, and troubleshoot common issues. Use when setting up a new Telegram bot for OpenClaw or debugging connection problems.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mosoonpi-ai](https://clawhub.ai/user/mosoonpi-ai)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to set up, secure, and troubleshoot Telegram connectivity for OpenClaw agents, including bot creation, allowed chat configuration, group topics, media handling, and optional voice transcription.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A Telegram bot can be used by unintended users if access controls are not configured.

Mitigation: Keep allowedChatIds and rejectUnknown enabled before using the bot beyond initial testing.

Risk: Bot tokens grant access to the Telegram bot and can be abused if exposed.

Mitigation: Treat the bot token as a secret and avoid storing it in source control, chats, or shared logs.

Risk: Bots added to groups may see group messages depending on Telegram and bot privacy settings.

Mitigation: Add the bot only to groups where participants understand message visibility, and prefer mention- or command-based responses in groups.

Risk: Optional voice transcription setup introduces additional dependencies.

Mitigation: Use pinned or reviewed dependency versions when enabling faster-whisper voice transcription.

## Reference(s):

- [Skill README](README.md)
- [ClawHub skill page](https://clawhub.ai/mosoonpi-ai/skills/telegram-agent-setup)

## Skill Output:

**Output Type(s):** [guidance, markdown, code, shell commands, configuration]

**Output Format:** [Markdown guidance with inline shell commands, JSON configuration examples, and a Python transcription helper snippet]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces setup and troubleshooting instructions for configuring OpenClaw with Telegram; it does not perform the connection itself.]

## Skill Version(s):

1.0.1 (source: server release metadata and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
