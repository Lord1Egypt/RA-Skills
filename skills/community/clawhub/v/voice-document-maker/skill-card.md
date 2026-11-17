## Description:

制作有声视频文档技能 - 将文字自动转为 TTS 语音，并配上 AI 生成的精美背景图，合成 MP4 视频文件。适用于微信视频卡片交付。

This skill is ready for commercial/non-commercial use.

## Publisher:

[interccy-stack](https://clawhub.ai/user/interccy-stack)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and WeChat bot operators use this skill to turn text into video-card messages with spoken Chinese audio and a generated visual background. It is intended for cases where an MP4 video card is easier for recipients to play than standalone voice files.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: User text and background prompts may be sent to external TTS and image-generation providers.

Mitigation: Avoid sensitive text or private prompts unless disclosure to those providers is acceptable.

Risk: Output handling can overwrite files outside the intended output folder.

Mitigation: Run with a simple .mp4 filename from an unprivileged account, and prefer a hardened version that confines output to its own folder and uses per-run temporary files.

Risk: The security verdict is suspicious despite a coherent video-generation purpose.

Mitigation: Review before installing, scan the skill before deployment, and confirm the script behavior matches the intended environment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/interccy-stack/skills/voice-document-maker)
- [Pollinations image generation endpoint](https://image.pollinations.ai/prompt/{encoded_prompt}?width=720&height=1280&nologo=true)

## Skill Output:

**Output Type(s):** [text, code, shell commands, configuration, files]

**Output Format:** [Markdown guidance with shell commands; generated artifact is an MP4 video file.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Creates TTS audio, a generated background image, and a vertical MP4 video; user text and background prompts may be sent to external providers.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
