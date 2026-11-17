## Description:

Video Downloader helps agents download videos from yt-dlp-compatible platforms, select a preferred resolution, merge audio and video, and sanitize local filenames.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jingrongx](https://clawhub.ai/user/jingrongx)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to fetch videos from YouTube, Bilibili, Douyin, and other yt-dlp-compatible sites into a local temporary or user-specified directory. It is useful when an agent workflow needs a local media file path for downstream processing or transfer.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill fetches user-provided video URLs and may contact external sites.

Mitigation: Avoid internal, localhost, or otherwise sensitive URLs, and only download from sources the user is authorized to access.

Risk: Downloaded media files are written to a local output directory.

Mitigation: Use a fresh, private output directory for each download and avoid shared or untrusted folders.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jingrongx/skills/video-downloader-skill)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Files]

**Output Format:** [Plain text status messages and a local video file path]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes downloaded media files to a temporary or user-specified local directory; requires yt-dlp and ffmpeg.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
