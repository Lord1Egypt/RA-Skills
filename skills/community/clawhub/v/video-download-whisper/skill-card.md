## Description:

下载无法直接访问的视频网站内容（如B站、YouTube等），提取音频后用Whisper转录成文字，适用于需要获取视频完整文字稿进行分析的场景。

This skill is ready for commercial/non-commercial use.

## Publisher:

[haohanyang92](https://clawhub.ai/user/haohanyang92)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, and analysts use this skill to download video content, extract audio, and create Whisper transcripts for review or deeper analysis when direct access to the page content is limited.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill runs video downloader and transcription commands that make outbound requests and write media, audio, and transcript files locally.

Mitigation: Run it in an isolated workspace, review requested URLs and output paths before execution, and inspect downloaded files before using their contents.

Risk: Cookie files or browser cookies can expose account credentials when used for member-only or authenticated content.

Mitigation: Prefer public URLs. If cookies are necessary, treat them as secrets, scope them explicitly, and remove them from the workspace after use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/haohanyang92/skills/video-download-whisper)
- [ClawHub publisher profile](https://clawhub.ai/user/haohanyang92)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with shell command examples and generated transcript text files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires yt-dlp, ffmpeg, and Whisper; scripts write downloaded media, extracted audio, and transcript files to local output directories.]

## Skill Version(s):

1.0.0 (source: release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
