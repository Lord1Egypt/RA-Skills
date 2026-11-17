## Description:

Telegram bot that transcribes voice messages with Whisper and replies in Chinese using Microsoft Edge text-to-speech.

This skill is ready for commercial/non-commercial use.

## Publisher:

[polityang](https://clawhub.ai/user/polityang)

### License/Terms of Use:

MIT-0

## Use Case:

Developers use this skill to configure and run a Telegram bot that receives voice messages, transcribes them, and replies with text or synthesized Chinese speech.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Private voice messages and generated replies may be processed by Telegram and Microsoft Edge TTS.

Mitigation: Disclose this processing to bot users, avoid sensitive audio, and use a dedicated Telegram bot token.

Risk: Dependency mismatch around the Whisper package can create supply-chain or installation risk.

Mitigation: Replace the dependency with the intended reviewed package and pin dependencies or use a lock file.

Risk: Transcript logging may expose user voice content in runtime logs.

Mitigation: Disable or remove full transcript logging and run the bot under a low-privilege account.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/polityang/skills/telegram-voice-bot)
- [Telegram BotFather](https://t.me/BotFather)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands, Python code references, and environment variable configuration]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires TELEGRAM_BOT_TOKEN; VOICE_REPLY controls whether replies are sent as synthesized voice.]

## Skill Version(s):

2.0.0 (source: server release metadata and artifact changelog)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
