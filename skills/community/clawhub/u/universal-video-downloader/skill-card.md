## Description:

Download videos from YouTube, Instagram, TikTok, Twitter/X, and 1000+ other sites using yt-dlp. Supports quality selection and automatic cleanup. Use when a user provides a video link from any platform and wants to download it.

This skill is ready for commercial/non-commercial use.

## Publisher:

[itzsubhadip](https://clawhub.ai/user/itzsubhadip)

### License/Terms of Use:


## Use Case:

Agents use this skill when a user provides a supported video URL and wants available formats inspected, a selected format downloaded, and the resulting file delivered for temporary use.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can fetch arbitrary URLs from the agent environment.

Mitigation: Run it in a sandbox with restricted outbound network access and review links before execution.

Risk: Downloaded files may remain on disk unless the agent explicitly deletes them after delivery.

Mitigation: Use disk quotas and require post-delivery cleanup with an explicit remove command.

Risk: Large downloads or long-running downloads can consume disk, bandwidth, or execution time.

Mitigation: Add or enforce file size limits, timeouts, and storage monitoring before broad deployment.

Risk: Sensitive or private media URLs could be exposed to the downloader runtime.

Mitigation: Avoid sensitive/private media until URL validation and data-handling controls are in place.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/itzsubhadip/skills/universal-video-downloader)
- [yt-dlp](https://github.com/yt-dlp/yt-dlp)
- [FFmpeg](https://ffmpeg.org/)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, files, guidance]

**Output Format:** [Markdown guidance with inline shell commands and JSON command output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces downloaded media files that should be deleted after delivery.]

## Skill Version(s):

1.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
