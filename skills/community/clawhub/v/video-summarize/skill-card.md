## Description:

Processes public video links by retrieving subtitles when available or transcribing audio with Whisper, then asks the agent to summarize the transcript.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yilsonyan](https://clawhub.ai/user/yilsonyan)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to summarize public videos from supported platforms by producing or reusing a transcript and then generating a Markdown summary.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The setup flow may install Homebrew packages, modify the shell profile, and download unpinned dependencies.

Mitigation: Review the scripts before installation and prefer manually installing pinned, verified versions of Homebrew packages, Python dependencies, and model files.

Risk: YouTube processing can allow yt-dlp to read Chrome browser cookies.

Mitigation: Remove automatic browser-cookie use unless it is required, and avoid running the skill with browser profiles that contain sensitive sessions.

Risk: Downloaded transcripts and summaries are stored locally and may include sensitive video content.

Mitigation: Use the skill only with content you are allowed to process, and clean the cache and summary directories according to local data-handling requirements.

## Reference(s):

- [Whisper.cpp base model download](https://huggingface.co/ggerganov/whisper.cpp/resolve/main/ggml-base.bin)
- [ClawHub skill page](https://clawhub.ai/yilsonyan/skills/video-summarize)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, files, guidance]

**Output Format:** [Markdown summary and local transcript files, with shell command guidance for video processing.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Caches transcripts and summaries under per-video local output directories.]

## Skill Version(s):

1.0.2026050302 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
