## Description:

Telegram voice-to-voice for macOS Apple Silicon: transcribe inbound .ogg voice notes with yap (Speech.framework) and reply with Telegram voice notes via say+ffmpeg.

This skill is ready for commercial/non-commercial use.

## Publisher:

[fiberian1981](https://clawhub.ai/user/fiberian1981)

### License/Terms of Use:


## Use Case:

External users and developers use this skill to handle Telegram voice-note conversations on macOS Apple Silicon by transcribing incoming OGG/Opus audio locally, generating a reply, and returning either a Telegram voice note or a text response.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The pathless transcription fallback may transcribe the newest stored Telegram voice file rather than audio tied to the current chat, which could expose another user's audio.

Mitigation: Prefer an attachment path from the current Telegram message and avoid the fallback in shared or multi-user environments.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/fiberian1981/skills/telegram-voice-to-voice-macos)
- [Publisher profile](https://clawhub.ai/user/fiberian1981)
- [yap Speech.framework transcription CLI](https://github.com/finnvoor/yap)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell command invocations and generated OGG voice-note file paths]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires macOS on Apple Silicon with yap, ffmpeg, say, and defaults available locally.]

## Skill Version(s):

0.1.3 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
