## Description:

Universal video downloader supporting multiple platforms (Douyin, Bilibili, YouTube, TikTok, etc.). Can download videos by URL or search by keyword (Douyin supported). Use when users need to download videos from video platforms.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wwkgit](https://clawhub.ai/user/wwkgit)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to download videos from supported platforms by URL, batch URL list, or Douyin keyword search, with metadata saved alongside downloaded media.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Browser-download mode uses authenticated browser automation on third-party video pages and disables Chromium sandboxing.

Mitigation: Review before installing, run only in an isolated environment or disposable browser profile, avoid administrator or root execution, and keep Chromium and DrissionPage updated.

Risk: Browser mode may use logged-in cookies while accessing video platforms.

Mitigation: Use a dedicated browser profile without sensitive accounts or cookies when downloading from third-party pages.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wwkgit/skills/video-downloader-tool)

## Skill Output:

**Output Type(s):** [text, shell commands, files, JSON metadata, guidance]

**Output Format:** [Markdown guidance with shell commands; downloaded MP4 files and JSON metadata when the script is run.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Browser mode may use authenticated cookies and visit third-party video pages; downloaded media use sanitized filenames.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
