## Description:

将日语视频转换为中文硬字幕，覆盖 ffmpeg 音频提取、Whisper 日语转录、LLM 日译中、SRT 转 ASS、ffmpeg 硬字幕烧录和验证流程。

This skill is ready for commercial/non-commercial use.

## Publisher:

[xunnv](https://clawhub.ai/user/xunnv)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to batch-process Japanese MP4 videos into Chinese hard-subtitled MP4 outputs with resumable intermediate audio, SRT, and ASS files.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Video transcript text can be sent to the configured QClaw gateway and to MyMemory when fallback translation is used.

Mitigation: Use the skill only with videos whose transcript may be shared with those services, and disable external fallback unless it is explicitly needed.

Risk: The artifact includes a hardcoded bearer token.

Mitigation: Rotate or remove the embedded token and load credentials from a local secret or environment-specific configuration before use.

Risk: Batch processing scans the configured input directory for MP4 files.

Mitigation: Restrict the input directory to the intended videos before running the script.

## Reference(s):

- [Video subtitle workflow](artifact/references/workflow.md)
- [ClawHub skill page](https://clawhub.ai/xunnv/skills/video-japanese-subtitle)

## Skill Output:

**Output Type(s):** [guidance, shell commands, code, configuration]

**Output Format:** [Markdown guidance with shell commands and Python configuration details]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [When the script is run, it creates local WAV, SRT, ASS, and hard-subtitled MP4 files under the configured output directory.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
