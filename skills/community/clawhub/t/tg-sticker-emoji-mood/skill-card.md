## Description:

Automatically adds mood-matched Telegram stickers and emojis during Telegram conversations, including proactive sticker-first reactions in casual exchanges.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dandysuper](https://clawhub.ai/user/dandysuper)

### License/Terms of Use:


## Use Case:

Agents connected to Telegram use this skill to add mood-matched stickers and light emoji to casual chats, celebrations, greetings, and supportive replies. It is intended for informal conversation contexts and should be skipped for serious, formal, sensitive, or user-opted-out chats.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can automatically post stickers into Telegram chats through a bot.

Mitigation: Use a dedicated low-privilege bot token, restrict where the bot is present, and avoid enabling the skill in formal or sensitive chats.

Risk: The security evidence identifies a helper-script input handling flaw in the --emoji path.

Mitigation: Fix or avoid the --emoji helper path until input is passed safely to Python.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/dandysuper/skills/tg-sticker-emoji-mood)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with bash command examples; helper-script actions may return Telegram Bot API JSON or sticker-set listings.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires TELEGRAM_BOT_TOKEN and a Telegram chat id; can send Telegram sticker messages through the configured bot.]

## Skill Version(s):

3.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
