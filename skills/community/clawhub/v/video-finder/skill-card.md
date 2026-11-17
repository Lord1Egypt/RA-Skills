## Description:

Video Finder helps users search, filter, and download adult videos using stored preferences, proxy configuration, yt-dlp downloads, progress tracking, and feedback.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xiaoka520](https://clawhub.ai/user/xiaoka520)

### License/Terms of Use:

MIT-0

## Use Case:

External users use this OpenClaw agent skill to search adult-video sites, filter results by stored preferences, confirm a selection, and download chosen videos with yt-dlp. Use only where adult-content access and downloading are legal.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill searches and downloads adult content.

Mitigation: Use only in a private environment and only where the requested access and downloads are legal.

Risk: The skill can store sensitive viewing preferences, history, and feedback in local JSON and Markdown files.

Mitigation: Review or delete generated preferences, tracking, and history files after use, and treat them as sensitive records.

Risk: Proxy configuration may contain plaintext credentials.

Mitigation: Avoid storing reusable proxy passwords and redact proxy credentials in logs, examples, and conversation output.

Risk: Background yt-dlp jobs and cleanup commands can touch the selected download directory.

Mitigation: Choose a dedicated download directory and review download paths before approving a download.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/xiaoka520/skills/video-finder)
- [Publisher Profile](https://clawhub.ai/user/xiaoka520)
- [Source Repository](https://github.com/xiaoka520/video-finder)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with shell command examples and generated JSON/Markdown state files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or update local preference, proxy, download-tracking, and history files; may run background yt-dlp download commands.]

## Skill Version(s):

0.1.8 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
