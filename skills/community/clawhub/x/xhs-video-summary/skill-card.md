## Description:

Analyzes Xiaohongshu video links by extracting metadata, transcribing speech, and producing a structured deep summary.

This skill is ready for commercial/non-commercial use.

## Publisher:

[songxianqun](https://clawhub.ai/user/songxianqun)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to summarize Xiaohongshu videos from a link, including video information, theme, detailed content breakdown, practical value, and highlight quotes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill executes a separately installed local xiaohongshu-extract helper script.

Mitigation: Review and verify the helper skill source before use, and run the workflow in a sandbox or dedicated workspace.

Risk: The skill downloads Xiaohongshu media and processes remote files locally with curl, ffmpeg, and Whisper.

Mitigation: Use it only on trusted links, keep media-processing tools updated, and avoid running it in sensitive working directories.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/songxianqun/skills/xhs-video-summary)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance, files]

**Output Format:** [Markdown summary with generated metadata and transcript files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses local curl, ffmpeg, Whisper, Python, and a separately installed xiaohongshu-extract helper skill.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
