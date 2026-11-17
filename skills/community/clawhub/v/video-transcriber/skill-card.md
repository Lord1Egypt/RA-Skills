## Description:

Video Transcriber helps an agent retrieve Bilibili or YouTube captions when available, translate subtitles when needed, or download audio and transcribe it with whisper.cpp when captions are unavailable.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xing2xian](https://clawhub.ai/user/xing2xian)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to help an agent summarize videos, retrieve subtitles, or create transcripts for Bilibili and YouTube content.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The documented workflow uses unsafe download command patterns for user-supplied video URLs.

Mitigation: Review video URLs before execution, allowlist supported platforms, avoid shell string interpolation, and run downloads in isolated temporary directories.

Risk: The workflow disables certificate verification in download commands.

Mitigation: Remove --no-check-certificate unless a reviewer approves a specific exception.

Risk: Downloaded audio and generated transcript files may be retained locally.

Mitigation: Make retention behavior clear to users and clean temporary audio/subtitle files after use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/xing2xian/skills/video-transcriber)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown with shell command examples and transcript or summary text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce subtitle text, translated captions, audio transcription output, or video summaries depending on caption availability.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
