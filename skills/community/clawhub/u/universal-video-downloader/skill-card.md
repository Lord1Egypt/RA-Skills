## Description: <br>
Download videos from YouTube, Instagram, TikTok, Twitter/X, and 1000+ other sites using yt-dlp. Supports quality selection and automatic cleanup. Use when a user provides a video link from any platform and wants to download it. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ItzSubhadip](https://clawhub.ai/user/ItzSubhadip) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and agents use this skill to inspect available video qualities for a user-provided URL, download the selected format, deliver the resulting media file, and clean up temporary local storage afterward. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Review before execution as proposals could introduce incorrect or misleading guidance into skills. <br>
Mitigation: Review and scan skill before deployment. <br>

## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ItzSubhadip/universal-video-downloader) <br>
- [Required binary: yt-dlp](https://github.com/yt-dlp/yt-dlp) <br>
- [Required binary: ffmpeg](https://ffmpeg.org/) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, code, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON script output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces local MP4 media files through yt-dlp and ffmpeg; agents should delete downloaded files after successful delivery and consider site terms and local law for user-provided URLs.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
