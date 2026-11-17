## Description:

Downloads YouTube video audio as MP3 and prepares it for Feishu cloud upload and messaging in an OpenClaw workflow.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yanghuicode](https://clawhub.ai/user/yanghuicode)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to download audio from a YouTube URL, convert it to MP3, and hand the file off for Feishu cloud storage or message delivery. Review the Feishu upload behavior before relying on it as an end-to-end uploader.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The released code may not complete the promised Feishu upload and message flow.

Mitigation: Treat the current release as a local YouTube audio downloader until Feishu upload and send success are implemented and reported only after completion.

Risk: URL handling is broad and may accept inputs outside the intended YouTube-only use case.

Mitigation: Parse and allowlist supported YouTube URL forms before invoking yt-dlp.

Risk: Temporary MP3 files may remain on disk after use.

Mitigation: Use per-run temporary directories and deterministic cleanup after confirmed upload or failure.

Risk: Runtime environment and dependency handling may expose more variables or variability than needed.

Mitigation: Pass only required environment variables and pin runtime dependencies before deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/yanghuicode/skills/youtube-to-feishu)
- [ClawHub publisher profile](https://clawhub.ai/user/yanghuicode)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with progress text and JSON command results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce local MP3 files and Feishu upload or messaging guidance; Feishu actions require OpenClaw integration and authorization.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
