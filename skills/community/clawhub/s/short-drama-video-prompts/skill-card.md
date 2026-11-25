## Description:

把短剧分镜和首帧写成可直接复制的视频提示词，也可独立起草视频动作或成片配乐/主题曲提示词。用于文生/图生视频动作、人物表演、运镜、口型、环境动态、镜头时长与配乐提示词编写；不调生成接口、不写歌词、不改分镜起止状态。

This skill is ready for commercial/non-commercial use.

## Publisher:

[worldwonderer](https://clawhub.ai/user/worldwonderer)

### License/Terms of Use:

MIT

## Use Case:

短剧编剧、分镜师和视频制作人员可用此技能，把已定稿的分镜和首帧整理成可复制的视频生成提示词，也可起草独立的视频动作或成片配乐提示词。

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The prompt guidance includes English or Chinese language requirements that may not fit every user's workflow.

Mitigation: Check the language requirements against the project's intended prompt language before adopting the guidance.

Risk: Security scan coverage was partial because a local path-like reference in SKILL.md could not be matched to a bundled artifact.

Mitigation: Review the referenced local material and complete coverage checks for the full release package before relying on the scan assessment.

## Reference(s):

- [视频提示词格式规范](references/format-spec.md)
- [阶段职责与规则](references/stage-contract.md)
- [视频提示词写作指南](references/video-prompt-guide.md)
- [目标模型与交付配置指南](references/model-and-delivery-profiles.md)
- [表演弧线与动作计时](references/performance-action-timing.md)
- [运镜、现场声与跨镜连戏](references/camera-audio-continuity.md)
- [Seedance 2.0 提示词写法](references/seedance-2.0.md)
- [Seedance 2.5 提示词写法](references/seedance-2.5.md)
- [Wan 3.0 提示词写法](references/wan-3.0.md)
- [MiniMax H3 提示词写法](references/minimax-h3.md)
- [Seedance 视频生成 API](https://docs.volcengine.com/docs/82379/1520757)
- [Seedance 提示词指南](https://docs.volcengine.com/docs/82379/2607689)
- [Wan 3.0 视频生成 API](https://help.aliyun.com/zh/model-studio/wan3-video-generation-api-reference)
- [Wan 3.0 视频生成指南](https://platform.qianwenai.com/docs/developer-guides/video-generation/wan30-video)
- [MiniMax H3 Base 提示词指南](https://github.com/MiniMax-AI/MiniMax-H3/blob/main/skills/h3-prompt-writing/references/base-en.txt)
- [MiniMax H3 Full-reference 指南](https://github.com/MiniMax-AI/MiniMax-H3/blob/main/skills/h3-prompt-writing/references/ref-en.txt)
- [MiniMax 视频生成 API](https://platform.minimax.io/docs/api-reference/video-generation-v2-create)
- [MiniMax H3 Context-IR API](https://platform.minimax.io/docs/api-reference/video-generation-v2-h3-context-ir)
- [Skill 发布页](https://clawhub.ai/worldwonderer/skills/short-drama-video-prompts)
- [Publisher profile](https://clawhub.ai/user/worldwonderer)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Standalone video or music prompts, or Markdown project files with structured MOTION, GROUP, and MUSIC entries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Prompt drafting only; it does not call generation services, write lyrics, or change approved shot start and end states.]

## Skill Version(s):

1.0.25 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
