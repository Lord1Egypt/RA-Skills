## Description:

Download videos, audio, subtitles, and clean paragraph-style transcripts from YouTube and any other yt-dlp supported site.

This skill is ready for commercial/non-commercial use.

## Publisher:

[steipete](https://clawhub.ai/user/steipete)

### License/Terms of Use:


## Use Case:

External users, developers, and agents use this skill to fetch clean transcripts, subtitles, audio, video files, or format listings from YouTube and other sites supported by yt-dlp.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill exposes unrestricted yt-dlp argument passthrough after `--`, which can give an agent broader local command authority than a normal video downloader needs.

Mitigation: Install only for trusted users and prompts; prefer a future version that removes raw passthrough or replaces it with an allowlist for benign options such as format selection and verbosity.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/steipete/skills/video-transcript-downloader)
- [youtube-transcript-plus package](https://registry.npmjs.org/youtube-transcript-plus/-/youtube-transcript-plus-1.1.1.tgz)

## Skill Output:

**Output Type(s):** [Text, Markdown, Files, Shell commands, Configuration, Guidance]

**Output Format:** [Plain text, file paths, format listings, and Markdown with shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Transcript output defaults to a cleaned single paragraph; downloads and subtitle commands print resolved output paths when successful.]

## Skill Version(s):

1.0.0 (source: evidence.release.version and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
