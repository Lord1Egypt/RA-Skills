## Description:

Video to text converter. Downloads videos from Bilibili using bilibili-api, from other sites using yt-dlp, then transcribes audio using faster-whisper. Use when you need to convert video content (B站/YouTube/local files) into text transcripts or subtitles.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lkyyyy320](https://clawhub.ai/user/lkyyyy320)

### License/Terms of Use:


## Use Case:

Developers and agents use this skill to convert online videos or local media files into text transcripts or subtitle-ready text. It is suited for Bilibili, yt-dlp-supported platforms, and local audio/video files.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Bilibili session credentials can be exposed if passed on the command line or hardcoded into the script.

Mitigation: Avoid command-line or hardcoded credentials; use an isolated environment and rotate credentials if they may have been stored in shell or log history.

Risk: The skill downloads media and installs runtime dependencies before transcription.

Mitigation: Review the skill before installation, use a virtual environment with pinned dependencies, and avoid sudo unless required by the host environment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/lkyyyy320/skills/video-to-text-2)

## Skill Output:

**Output Type(s):** [Text, Files, Shell commands, Configuration guidance]

**Output Format:** [Plain text transcripts, optional transcript files, and Markdown guidance with shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May download temporary media files; optional output path saves the transcript to a file.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
