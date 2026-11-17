## Description:

Send images to Telegram via direct Bot API using curl. Works around OpenClaw's broken image delivery pipeline (issue #63137).

This skill is ready for commercial/non-commercial use.

## Publisher:

[niccoreyes](https://clawhub.ai/user/niccoreyes)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to configure Telegram bot credentials and produce curl commands that send images, documents, or messages to a specified Telegram chat.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Sourcing a skill-local .env file from shell startup files can persistently execute shell code.

Mitigation: Use temporary exports or a proper secret manager instead of sourcing a skill-local .env file, and do not add the provided auto-load block to shell startup files.

Risk: A Telegram bot token can authorize sends to configured chats if it is exposed or reused too broadly.

Mitigation: Keep the Telegram bot token narrowly scoped to the send command and avoid committing or sharing the token.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/niccoreyes/skills/telegram-direct-send)
- [Telegram BotFather](https://t.me/BotFather)
- [Telegram userinfobot](https://t.me/userinfobot)
- [Telegram RawDataBot](https://t.me/RawDataBot)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces curl examples for Telegram Bot API endpoints and environment variable setup guidance.]

## Skill Version(s):

1.0.0 (source: server release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
