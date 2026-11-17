## Description:

Processes voice conversations in Picoclaw's native Telegram channel without webhooks by transcribing received audio and generating spoken replies.

This skill is ready for commercial/non-commercial use.

## Publisher:

[titara](https://clawhub.ai/user/titara)

### License/Terms of Use:

MIT-0

## Use Case:

External Picoclaw users and developers use this skill to run a local semi-automatic workflow for Telegram voice messages: receive audio, transcribe it with Groq Whisper, prepare a reply, and generate a spoken response for the existing Telegram channel.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The watcher can process local files from shared directories and send voice content to external speech services.

Mitigation: Run the skill as an unprivileged account, avoid shared /tmp inputs, reject symlinks, set file-size and retention limits, and disclose Groq and Edge TTS data handling to users.

Risk: Voice data, generated audio, metadata, or API keys may be exposed if inputs and secrets are handled loosely.

Mitigation: Use environment-based secrets, avoid passing API keys on command lines, and enforce cleanup for audio and JSON state files.

## Reference(s):

- [Implementation Plan](references/implementation-plan.md)
- [ClawHub Skill Page](https://clawhub.ai/titara/skills/telegram-picoclaw)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Configuration, Files]

**Output Format:** [Markdown guidance with shell commands; runtime scripts emit transcription text, JSON metadata, and MP3 audio files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires GROQ_API_KEY and access to Groq Whisper and Edge TTS services.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
