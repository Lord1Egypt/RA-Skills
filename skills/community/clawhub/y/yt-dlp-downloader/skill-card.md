## Description:

Downloads and merges online videos from Bilibili, Douyin, or YouTube when the user provides a complete video URL.

This skill is ready for commercial/non-commercial use.

## Publisher:

[roykingw](https://clawhub.ai/user/roykingw)

### License/Terms of Use:

MIT

## Use Case:

External users and developers can use this skill to ask an agent to download a supported online video URL, merge the media to MP4, and report the script result.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A normal download request can run local commands and automatically install unpinned software on the host.

Mitigation: Install yt-dlp and ffmpeg ahead of time from trusted sources, pin dependency versions where possible, and require approval before any host package or Python environment changes.

Risk: The skill downloads media into the user's Downloads folder.

Mitigation: Run it only with trusted URLs, validate that the URL is intended for download, and execute in a constrained environment when handling unfamiliar links.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/roykingw/skills/yt-dlp-downloader)
- [ClawHub publisher profile](https://clawhub.ai/user/roykingw)

## Skill Output:

**Output Type(s):** [text, shell commands, files]

**Output Format:** [Plain text script output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Downloads are saved as MP4 files in the user's Downloads folder when execution succeeds.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
