## Description: <br>
Download videos from YouTube, Reddit, Twitter/X, TikTok, Instagram, and 1000+ other sites using yt-dlp. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dimitryvin](https://clawhub.ai/user/dimitryvin) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and developers use this skill to download a provided video URL to local storage, optionally extract audio, limit resolution, or prepare a compressed Telegram-size copy. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The downloader performs network requests and writes media files locally, which can retrieve unintended content or place files in sensitive folders. <br>
Mitigation: Run it only on URLs you intend to download and choose a non-sensitive output directory with the --output option when needed. <br>
Risk: The compression helper can continue as a CPU-intensive background job until ffmpeg finishes. <br>
Mitigation: Start background compression only when long-running local processing is acceptable, and monitor the nohup log or stop the process if circumstances change. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/dimitryvin/video-dl) <br>
- [yt-dlp supported sites](https://github.com/yt-dlp/yt-dlp/blob/master/supportedsites.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, files, guidance] <br>
**Output Format:** [Markdown with inline bash commands, local file paths, and status text from shell scripts] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Downloads media to a local output directory; the compression helper writes a Telegram-sized MP4 when successful.] <br>

## Skill Version(s): <br>
1.1.0 (source: server evidence release.version) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
