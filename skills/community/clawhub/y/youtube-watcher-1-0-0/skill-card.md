## Description:

Fetch and read transcripts from YouTube videos. Use when you need to summarize a video, answer questions about its content, or extract information from it.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xvolica](https://clawhub.ai/user/xvolica)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to retrieve YouTube video transcript text so they can summarize videos, answer questions about video content, or extract specific information from captions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill invokes a broad network-capable downloader on user-supplied URLs without URL restriction.

Mitigation: Use it only for YouTube URLs and add URL allowlisting before relying on it in higher-trust environments.

Risk: The skill depends on an external yt-dlp executable available in PATH.

Mitigation: Install yt-dlp from a trusted source, prefer a pinned version, and review updates before deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/xvolica/skills/youtube-watcher-1-0-0)
- [Publisher profile](https://clawhub.ai/user/xvolica)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Guidance]

**Output Format:** [Plain text transcript output with Markdown usage guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires yt-dlp in PATH and works only when closed captions or auto-generated subtitles are available.]

## Skill Version(s):

1.0.0 (source: frontmatter, release evidence, artifact metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
