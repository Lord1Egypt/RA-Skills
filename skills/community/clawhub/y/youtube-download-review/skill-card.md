## Description:

Helps an agent handle YouTube download requests by preparing yt-dlp and ffmpeg workflows for MP4 video, thumbnails, optional burned-in subtitles, and a short music-media review.

This skill is ready for commercial/non-commercial use.

## Publisher:

[copfee](https://clawhub.ai/user/copfee)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agent operators use this skill when they provide YouTube links and want downloadable video assets, subtitle handling, cover art, and a concise music-oriented interpretation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Untrusted YouTube URLs and title-derived filenames may be placed into shell commands and local output paths.

Mitigation: Use trusted links, pass URLs and filenames as process arguments where possible, sanitize title-derived paths, and review output paths before running commands.

Risk: The skill can download media into the current workspace and burn translated subtitles into video files.

Mitigation: Install only when this behavior is expected, work in an appropriate directory, and require explicit user confirmation before burning subtitles.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/copfee/skills/youtube-download-review)
- [Publisher profile](https://clawhub.ai/user/copfee)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Files, Guidance]

**Output Format:** [Markdown and terminal-facing text with inline shell commands and generated media file paths]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces per-video output directories containing MP4 files, a JPG thumbnail, optional SRT subtitles, and a recommendation markdown file when executed by an agent with yt-dlp and ffmpeg available.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
