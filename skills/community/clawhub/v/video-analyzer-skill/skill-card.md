## Description:

Download, transcribe, and analyze videos from YouTube, X/Twitter, and TikTok with local Whisper processing for TL;DRs, timestamps, and actionable insights.

This skill is ready for commercial/non-commercial use.

## Publisher:

[minilozio](https://clawhub.ai/user/minilozio)

### License/Terms of Use:

MIT

## Use Case:

External users and developers use this skill to extract transcripts, summaries, key moments, and downloadable media from video URLs across common social and video platforms.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The bundled script has a command-injection flaw in shell command construction, especially around language values.

Mitigation: Review before installing; avoid untrusted prompts or unusual language values until the script replaces shell=True with argument arrays and validates language codes.

Risk: The skill contacts video platforms, writes temporary transcripts, can save media to Desktop, and may download Whisper models on first use.

Mitigation: Use it only where those network calls, downloads, and local file writes are acceptable, and confirm content permissions before processing third-party media.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/minilozio/skills/video-analyzer-skill)
- [Declared project homepage](https://github.com/minilozio/video-analyzer-skill)
- [Whisper.cpp model download source](https://huggingface.co/ggerganov/whisper.cpp/resolve/main/)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, files, guidance]

**Output Format:** [Markdown summaries and timestamped transcript or download file paths]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create transcript files under /tmp, save downloaded media to Desktop, and download Whisper models on first use.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
