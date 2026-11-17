## Description:

Download videos from YouTube, Bilibili, Twitter, and thousands of other sites using yt-dlp.

This skill is ready for commercial/non-commercial use.

## Publisher:

[apollo1234](https://clawhub.ai/user/apollo1234)

### License/Terms of Use:


## Use Case:

Developers, employees, and external users use this skill to construct and run yt-dlp commands for downloading videos, extracting MP3 audio, downloading subtitles, selecting quality, and troubleshooting common download errors.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Cookie-based downloads may expose browser session cookies to a local command.

Mitigation: Prefer anonymous downloads first and require explicit user approval before any command uses browser cookies.

Risk: Broad shell and network permissions can allow more access than the download task requires.

Mitigation: Review the generated command before execution and use the narrowest available permissions for shell, network, and filesystem access.

Risk: Downloaded media and metadata are written to local disk.

Mitigation: Confirm the output path before execution and report the final file location to the user.

Risk: Unpinned dependency installation can introduce supply-chain uncertainty.

Mitigation: Install yt-dlp and ffmpeg from trusted, pinned, or managed environments.

## Reference(s):

- [yt-dlp Supported Sites](https://github.com/yt-dlp/yt-dlp/blob/master/supportedsites.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance, files]

**Output Format:** [Markdown with shell command examples and concise status reporting]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce local video, audio, subtitle, and thumbnail files when commands are executed.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
