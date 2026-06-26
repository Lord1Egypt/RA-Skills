## Description: <br>
一键分析小红书视频链接，提取文案、转录语音并深度总结视频内容。当用户提供小红书链接并要求“总结、分析、提取视频”时触发此技能。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[songxianqun](https://clawhub.ai/user/songxianqun) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and content analysts use this skill to process Xiaohongshu video links, extract metadata and speech transcripts, and produce a structured summary of the video content. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill downloads media from user-provided Xiaohongshu links and processes it with local command-line tools. <br>
Mitigation: Use trusted links, run the skill from a dedicated working directory, and review generated metadata and transcript files before relying on the summary. <br>
Risk: Temporary video, audio, metadata, and transcript files may contain user-provided or sensitive content. <br>
Mitigation: Delete xhs_temp.mp4, xhs_temp.mp3, xhs_temp.txt, and xhs_meta.json after the agent has read the outputs. <br>
Risk: The workflow depends on a separate xiaohongshu-extract skill and external binaries. <br>
Mitigation: Install xiaohongshu-extract, curl, ffmpeg, Whisper, and Python from trusted sources before use. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/songxianqun/xhs-video-summary) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, JSON, Shell commands] <br>
**Output Format:** [Structured Markdown summary with supporting JSON metadata and plain-text transcript files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires curl, ffmpeg, Whisper, Python, and the xiaohongshu-extract dependency; temporary media, transcript, and metadata files should be deleted after use.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
