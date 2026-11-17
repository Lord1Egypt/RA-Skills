## Description:

Converts video or audio files from URLs into text transcripts or SRT subtitles using Whisper-based transcription services.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sxliuyu](https://clawhub.ai/user/sxliuyu)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to transcribe user-provided video or audio URLs into plain text or subtitle output. It is suited for extracting speech content from supported media formats when external transcription services are acceptable.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Unsafe shell-string execution may allow command injection.

Mitigation: Remove shell-string execution and pass command arguments through a safe argument array before installation or use.

Risk: Network-fetch behavior may expose private recordings, signed URLs, internal service URLs, or confidential meeting audio.

Mitigation: Use only non-confidential media, restrict allowed URL targets, and require explicit consent before sending media to third-party transcription providers.

Risk: Downloads and temporary files can exceed expected limits or remain after failures.

Mitigation: Enforce download limits during streaming and clean temporary files on all failure paths.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/sxliuyu/skills/video-transcribe-pro)
- [Publisher profile](https://clawhub.ai/user/sxliuyu)
- [MyShell Whisper transcription endpoint](https://api.myshell.ai/v1/audio/transcriptions)
- [OpenAI audio transcription endpoint](https://api.openai.com/v1/audio/transcriptions)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Plain text transcript or SRT subtitle text, returned in tool output and command-line logs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Supports URL, language, and text-or-SRT output format parameters; documented maximum media size is 25MB.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
