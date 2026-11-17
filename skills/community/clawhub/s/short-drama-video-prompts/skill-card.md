## Description:

把短剧分镜和首帧写成可直接复制的视频提示词 Markdown，也可按用户要求写成片配乐或主题曲提示词。

This skill is ready for commercial/non-commercial use.

## Publisher:

[worldwonderer](https://clawhub.ai/user/worldwonderer)

### License/Terms of Use:

MIT

## Use Case:

Short-drama creators use this skill to turn finalized storyboards and opening frames into copy-ready, shot-by-shot video prompts covering action, performance, camera movement, sound, and continuity. It can also draft soundtrack or theme-music prompts when requested.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Model-specific workflows may impose prompt-language requirements that do not fit every project.

Mitigation: Check the selected model and project language settings before using the generated prompts.

Risk: Prompts or reference media copied into external video services may expose sensitive project material.

Mitigation: Review the service's privacy terms and avoid submitting confidential material unless its use is permitted.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/worldwonderer/skills/short-drama-video-prompts)
- [Video prompt writing guide](artifact/references/video-prompt-guide.md)
- [Model and delivery profiles](artifact/references/model-and-delivery-profiles.md)
- [Performance and action timing](artifact/references/performance-action-timing.md)
- [Camera, audio, and continuity](artifact/references/camera-audio-continuity.md)
- [Stage contract](artifact/references/stage-contract.md)
- [Seedance 2.0 guide](artifact/references/seedance-2.0.md)
- [Seedance 2.5 guide](artifact/references/seedance-2.5.md)
- [MiniMax H3 guide](artifact/references/minimax-h3.md)
- [Wan 3.0 guide](artifact/references/wan-3.0.md)
- [Volcengine video generation API](https://docs.volcengine.com/docs/82379/1520757)
- [Seedance prompt guide](https://docs.volcengine.com/docs/82379/2607689)
- [Wan 3.0 video generation API](https://help.aliyun.com/zh/model-studio/wan3-video-generation-api-reference)
- [MiniMax video generation API](https://platform.minimax.io/docs/api-reference/video-generation-v2-create)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown with copy-ready video prompts and optional soundtrack or theme-music prompts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Prompts preserve finalized storyboard timing and start/end states; the skill does not call generation interfaces or invent lyrics.]

## Skill Version(s):

1.0.21 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
