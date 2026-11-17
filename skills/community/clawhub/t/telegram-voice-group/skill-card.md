## Description:

Sends text-to-speech voice messages to specified Telegram groups and group topics.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sanwecn](https://clawhub.ai/user/sanwecn)

### License/Terms of Use:

MIT

## Use Case:

Developers and operators use this skill to generate Chinese text-to-speech audio, convert it to Telegram-compatible voice-message format, and send it to a configured Telegram group or topic. It supports topic-level routing for communities and teams that organize discussions through Telegram topics.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Voice text is sent to a Telegram group and may be processed by text-to-speech tooling.

Mitigation: Use only non-sensitive text that is intended for the target Telegram group or topic.

Risk: Setup guidance requests broad Telegram bot administration capabilities.

Mitigation: Grant only the permissions needed to send messages and media unless a separate review approves additional moderation powers.

Risk: Current JavaScript and shell entry points construct commands from user-provided text and options.

Mitigation: Review and harden command construction before running the skill with untrusted input.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/sanwecn/skills/telegram-voice-group)
- [README](artifact/README.md)
- [Features](artifact/FEATURES.md)
- [Dependencies](artifact/DEPENDENCIES.md)
- [Telegram Topics](artifact/TELEGRAM_TOPICS.md)
- [Use Cases](artifact/USE_CASES.md)

## Skill Output:

**Output Type(s):** [Audio, Telegram messages, Shell commands, Guidance]

**Output Format:** [OGG Opus voice message plus Markdown, JavaScript, and shell usage examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Linux, edge-tts, ffmpeg, and Telegram bot permission to send messages and media.]

## Skill Version(s):

0.1.5 (source: server release metadata; artifact package.json reports 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
