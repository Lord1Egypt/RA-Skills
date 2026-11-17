## Description:

Transcribes Telegram voice messages and audio notes into plain-text transcripts using OpenAI Whisper API or local Whisper.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dreadterror](https://clawhub.ai/user/dreadterror)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to let an OpenClaw agent read Telegram voice notes, transcribe them, and respond to the spoken content as if it had been typed.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Voice recordings may contain sensitive content and can be sent to OpenAI by default when local mode is not explicitly used.

Mitigation: Use local Whisper mode for sensitive audio or disclose and approve external transcription before processing recordings.

Risk: URL mode can fetch arbitrary audio URLs without strong scoping.

Mitigation: Avoid URL mode unless the URL source is trusted, or run the skill in a network-restricted sandbox.

Risk: A persistent Telegram hook can automatically process user audio.

Mitigation: Make Telegram users aware that voice notes may be transcribed automatically and limit hook deployment to intended chats.

## Reference(s):

- [Setup Guide](references/setup.md)
- [Telegram Bot API](https://api.telegram.org)
- [ClawHub skill page](https://clawhub.ai/dreadterror/skills/telegram-voice-transcribe)

## Skill Output:

**Output Type(s):** [text, JSON, shell commands, configuration, guidance]

**Output Format:** [JSON transcript object and human-readable guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces transcript, language, and duration fields on success, or an error field on failure.]

## Skill Version(s):

1.3.1 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
