## Description:

Downloads videos from YouTube, Reddit, Twitter/X, TikTok, Instagram, and 1000+ other sites using yt-dlp.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dimitryvin](https://clawhub.ai/user/dimitryvin)

### License/Terms of Use:


## Use Case:

External users, developers, and agents use this skill when a user provides a video URL and wants a local media download or audio extraction, with optional compression for Telegram-sized sharing.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Downloaded videos are saved locally under ~/Downloads/videos/ by default.

Mitigation: Confirm the destination before running the skill or use the documented --output option for a deliberate directory.

Risk: The optional Telegram compression workflow can be run in the background and the documented example writes logs to /tmp/compress.log.

Mitigation: Use a private log path on shared machines and keep track of any background compression jobs that are started.

Risk: The Telegram section is a manual compression helper, not a secure sending workflow.

Mitigation: Review the compressed output before sending it through any messaging channel.

## Reference(s):

- [yt-dlp supported sites](https://github.com/yt-dlp/yt-dlp/blob/master/supportedsites.md)

## Skill Output:

**Output Type(s):** [shell commands, files, guidance]

**Output Format:** [Markdown with bash commands and file path output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Downloads default to ~/Downloads/videos/ and may emit a MEDIA:<path> status line on success.]

## Skill Version(s):

1.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
