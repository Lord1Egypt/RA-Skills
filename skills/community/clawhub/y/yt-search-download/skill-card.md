## Description:

多站点视频搜索、下载和字幕提取工具，支持 YouTube 和 B站（Bilibili）等平台，并结合 YouTube Data API v3 与 yt-dlp 完成搜索、频道浏览、视频下载、MP3 音频提取、中英字幕下载和视频信息查询.

This skill is ready for commercial/non-commercial use.

## Publisher:

[joppyao-bit](https://clawhub.ai/user/joppyao-bit)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill from Claude Code or OpenClaw to search YouTube-style video sources, inspect channel updates, download videos or MP3 audio, and extract SRT plus TXT subtitle files for review or summarization.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can write downloaded video, audio, subtitle, and transcript files to local directories.

Mitigation: Run downloads only for trusted URLs, choose an explicit output directory, and review generated files before sharing or reusing them.

Risk: The download workflow may use browser login cookies through yt-dlp for restricted media.

Mitigation: Use a dedicated low-privilege browser profile or explicit cookie file only when authenticated downloads are necessary, and remove automatic browser-cookie behavior if it is not required.

Risk: The security summary says the documentation may overstate supported features.

Mitigation: Validate platform support and required dependencies in the target environment before relying on the skill for production workflows.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/joppyao-bit/skills/yt-search-download)
- [Publisher profile](https://clawhub.ai/user/joppyao-bit)
- [YouTube Data API v3 endpoint](https://www.googleapis.com/youtube/v3)
- [Google Cloud Console](https://console.cloud.google.com/)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown tables, JSON search results, shell commands, downloaded media files, SRT subtitle files, and timestamped TXT transcript files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Search requires a YouTube API key in YT_BROWSE_API_KEY or YOUTUBE_API_KEY; download and subtitle workflows require yt-dlp and write files to a local download directory.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
