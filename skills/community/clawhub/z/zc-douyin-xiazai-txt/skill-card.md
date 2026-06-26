## Description: <br>
抖音无水印视频下载与文案提取工具，使用本地 ffmpeg 与 Whisper 完成下载、音频提取和文字转写，可选语义分段。 <br>

This skill is for research and development only. <br>

## Publisher: <br>
[openclawzhangchong](https://clawhub.ai/user/openclawzhangchong) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External developers and users can use this skill to resolve Douyin share links or modal IDs, download videos locally, extract audio, and generate Chinese transcript Markdown with optional segmentation. The artifact describes the intended use as personal learning and research rather than commercial use. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill downloads media and writes transcripts to local output directories. <br>
Mitigation: Provide only intended Douyin links or numeric IDs, choose the output directory deliberately, and review or delete downloaded media and transcripts when no longer needed. <br>
Risk: The skill invokes local ffmpeg and Whisper binaries. <br>
Mitigation: Install ffmpeg and Whisper from trusted sources and verify they run as expected before processing media. <br>
Risk: Downloaded or transcribed content may be subject to platform rules or third-party rights. <br>
Mitigation: Use the skill only for authorized content and follow Douyin platform rules and applicable rights restrictions. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/openclawzhangchong/zc-douyin-xiazai-txt) <br>
- [Publisher profile](https://clawhub.ai/user/openclawzhangchong) <br>
- [Douyin service endpoint referenced by artifact](https://aweme.snssdk.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, files] <br>
**Output Format:** [Command-line output plus local MP4/WAV intermediates and transcript.md Markdown files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Node.js, ffmpeg, and local Whisper; default Whisper model is base.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
