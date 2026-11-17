## Description:

Transcribe audio and video files using OpenAI Whisper API. Use when user wants to transcribe audio/video files, extract speech from media, or get text from recordings. Automatically handles audio extraction from video files.

This skill is ready for commercial/non-commercial use.

## Publisher:

[djismgaming](https://clawhub.ai/user/djismgaming)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users can use this skill to turn audio or video recordings into transcripts, captions, timestamped text, or structured transcription results.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Potentially sensitive recordings are uploaded to a hardcoded private-network HTTP service without encryption or clear consent controls.

Mitigation: Use only when the endpoint, network path, retention policy, and transport security are acceptable; avoid sensitive recordings unless those conditions are verified.

Risk: The transcription endpoint is hardcoded to 192.168.0.11:8080, which may be unavailable or inappropriate in another environment.

Mitigation: Prefer a version that allows the endpoint to be configured and supports HTTPS or a loopback endpoint.

Risk: Video transcription creates temporary extracted audio files.

Mitigation: Use secure temporary-file handling and review local storage behavior before processing sensitive media.

## Reference(s):

- [Transcription Guide](artifact/references/transcription_guide.md)
- [ClawHub Skill Page](https://clawhub.ai/djismgaming/skills/transcription)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown, plain text transcripts, JSON transcription results, SRT subtitles, VTT captions, and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May upload source media to a configured Whisper-compatible endpoint and may extract audio from video with ffmpeg before transcription.]

## Skill Version(s):

1.0.1 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
