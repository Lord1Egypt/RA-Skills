## Description: <br>
通用视频下载工具，支持 YouTube、B站、抖音等主流平台。使用 yt-dlp 下载视频，自动选择分辨率、合并音视频、清理文件名。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jingrongx](https://clawhub.ai/user/jingrongx) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and end users use this skill to download videos from yt-dlp-compatible platforms, choose a target resolution, merge separated audio and video streams, and receive a local file path. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill downloads remote media using user-provided URLs. <br>
Mitigation: Use trusted URLs only and follow the ClawScan guidance for yt-dlp and ffmpeg usage. <br>
Risk: Downloaded videos can be large and a custom output directory may write outside the current workspace. <br>
Mitigation: Choose an output folder with enough disk space and verify the output path before running the download. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/jingrongx/video-downloader-skill) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Files, Shell commands] <br>
**Output Format:** [Plain text status messages and a local downloaded video file path] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires yt-dlp and ffmpeg; accepts a video URL, optional resolution, and optional output directory.] <br>

## Skill Version(s): <br>
1.0.1 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
