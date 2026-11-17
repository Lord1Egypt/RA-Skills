## Description:

抖音无水印视频下载与文案提取工具，使用本地 ffmpeg 与 Whisper 完成下载、音频提取和文字转写，可选语义分段。

This skill is for research and development only.

## Publisher:

[openclawzhangchong](https://clawhub.ai/user/openclawzhangchong)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and creators use this skill to inspect Douyin share links or modal IDs, download video files, extract audio locally, and produce Chinese transcripts for personal study or research workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can make unvalidated network requests to arbitrary URLs before confirming they are Douyin links.

Mitigation: Use only trusted Douyin share links or modal IDs; a safer release should validate Douyin hosts, block private and loopback addresses, limit redirects, and run dependencies in an isolated environment.

Risk: Downloaded media and generated transcripts may include third-party content subject to platform rules or rights restrictions.

Mitigation: Use the skill only for personal study or research workflows and review outputs before storing, sharing, or reusing them.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/openclawzhangchong/skills/zc-douyin-xiazai-txt)
- [Publisher profile](https://clawhub.ai/user/openclawzhangchong)
- [Douyin service endpoint referenced by the skill](https://aweme.snssdk.com)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown transcript files and terminal text output from Node.js commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires local Node.js, ffmpeg, and Whisper; default Whisper model is base.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
