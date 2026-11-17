## Description:

Voice communication via Telegram. Automatically transcribes incoming voice messages using faster-whisper and replies with TTS voice. Use for all voice-related interactions on Telegram.

This skill is ready for commercial/non-commercial use.

## Publisher:

[polityang](https://clawhub.ai/user/polityang)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and Telegram bot operators use this skill to support voice-based conversations by transcribing incoming Telegram voice messages and sending synthesized voice replies.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Telegram voice messages are transcribed automatically and may contain sensitive information.

Mitigation: Use the skill only where automatic transcription is acceptable, and review how OpenClaw stores, transmits, and retains audio files and transcripts.

Risk: The artifact installs faster-whisper without a pinned version.

Mitigation: Pin and review the faster-whisper version in an isolated environment before deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/polityang/skills/telegram-voice)

## Skill Output:

**Output Type(s):** [Text, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with Python, JSON, and shell command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces Telegram voice transcription and TTS reply guidance; no standalone files.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
