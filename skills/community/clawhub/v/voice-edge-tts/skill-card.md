## Description:

Voice (Edge TTS) converts text to speech using Microsoft Edge TTS with saved audio, direct playback, streaming playback, and voice listing actions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhaov1976](https://clawhub.ai/user/zhaov1976)

### License/Terms of Use:

MIT

## Use Case:

Developers and agent users can use this skill to turn text into spoken audio, generate MP3 media files, play speech locally, stream generated speech, and inspect available voices. It is intended for voice output workflows that can tolerate review before installation because the server scan reports unsafe local command and file-operation risks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The server security scan reports that normal inputs can reach unsafe local command and file operations.

Mitigation: Review before installing, replace shell command strings with spawn or execFile argument arrays everywhere, validate all caller options, and restrict output and cleanup to a private skill-owned directory.

Risk: The skill includes runtime dependency installation and sends text to an external TTS service.

Mitigation: Remove or tightly gate runtime installation behavior and clearly warn users before sending text to the external service.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/zhaov1976/skills/voice-edge-tts)
- [Publisher profile](https://clawhub.ai/user/zhaov1976)
- [Windows ffmpeg build referenced by the artifact](https://github.com/GyanD/codexffmpeg/releases)

## Skill Output:

**Output Type(s):** [Text, Files, Audio]

**Output Format:** [JSON-like execution results with status messages, media file paths, voice lists, and streamed or saved audio]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Streaming playback requires ffmpeg or ffplay and local audio support; input text is sent to an external TTS service.]

## Skill Version(s):

1.10.0 (source: server release metadata; artifact changelog uses v1.10; package.json reports 1.1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
