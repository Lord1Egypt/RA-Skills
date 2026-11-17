## Description:

Guides a video workflow that transcribes source media, drafts coarse and highlight edit plans, segments and assembles clips with FFmpeg, and records clip metadata and review scores in Feishu Bitable.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhuchenggong19851114-design](https://clawhub.ai/user/zhuchenggong19851114-design)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and video operations teams use this skill to turn source videos into transcribed, AI-analyzed coarse and fine cuts, then create Feishu-scored custom final editions for review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security summary identifies unsafe execution concerns in the bundled workflow.

Mitigation: Review and harden the Python implementation before use, and run it only on trusted local video paths.

Risk: The security summary identifies secret-logging concerns around Feishu configuration.

Mitigation: Keep Feishu tokens in environment variables, avoid printing them in logs, and rotate credentials if they were exposed.

Risk: The security guidance warns that video content, summaries, and local paths may be written to Feishu.

Mitigation: Confirm exactly what media-derived content and file paths will be uploaded before using the workflow with customer or sensitive videos.

Risk: The security summary identifies under-scoped automation concerns.

Mitigation: Manually review generated edit plans, clip selections, and final versions before publishing or sharing outputs.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/zhuchenggong19851114-design/skills/video-ai-process)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with Python and shell examples; workflow artifacts include transcript text, SRT subtitles, MP4 clips, final MP4 edits, and Feishu Bitable records.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a local video path and video name, plus FFmpeg, faster-whisper, MiniMax integration, and Feishu Bitable tokens.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
