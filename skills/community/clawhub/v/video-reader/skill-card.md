## Description: <br>
Tool-driven video question answering with frame extraction, sub-agent analysis, and audio transcription. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[qiankemeng](https://clawhub.ai/user/qiankemeng) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and end users use this skill to answer questions about local or remote videos by combining downloaded video metadata, extracted frame grids, audio transcription, and sub-agent analysis. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can download remote videos and process media from external sources. <br>
Mitigation: Review video sources and proxy settings before use, and run the diagnostic command before analyzing untrusted or region-restricted content. <br>
Risk: Audio transcripts, extracted frames, logs, downloads, and memory files can remain on disk after analysis. <br>
Mitigation: Avoid sensitive videos unless retention is acceptable, and use the cleanup tool to remove cached downloads, frame images, memory, and logs. <br>
Risk: Configured transcription or vision services may receive media-derived data. <br>
Mitigation: Review WHISPER_API_KEY, WHISPER_BASE_URL, VISION_* settings, and prefer local transcription where possible for sensitive content. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/qiankemeng/video-reader) <br>
- [VideoARM Research Paper](https://arxiv.org/abs/2512.12360) <br>
- [VideoARM Project Website](https://milvlg.github.io/videoarm/) <br>
- [VideoARM Skill Repository](https://github.com/qiankemeng/VideoARM-skill) <br>
- [OpenClaw](https://github.com/openclaw/openclaw) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, JSON, Files, Guidance] <br>
**Output Format:** [Markdown responses with inline shell commands and JSON tool outputs] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create local downloads, frame images, transcripts, logs, and memory files during video analysis.] <br>

## Skill Version(s): <br>
4.1.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
