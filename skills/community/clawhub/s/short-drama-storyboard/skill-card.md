## Description:

支持将短剧剧本和视觉设定拆解为分镜与首尾帧提示词，也可快速草拟单场镜头；不生成媒体或进行独立连戏审查。

This skill is ready for commercial/non-commercial use.

## Publisher:

[worldwonderer](https://clawhub.ai/user/worldwonderer)

### License/Terms of Use:

MIT

## Use Case:

短剧编剧、导演与分镜创作者可用它将定稿剧本和视觉设定拆为正式分镜并编写逐镜首帧或尾帧提示词，也可快速起草单场镜头方案。

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The expected local short-drama.json reference was not included in the bundled artifact, so its contents could not be assessed; project-specific timing or prompt-language settings may be unavailable.

Mitigation: Review and provide that project configuration when its settings are needed; otherwise use the documented fallback behavior for timing and prompt language.

## Reference(s):

- [ClawHub release](https://clawhub.ai/worldwonderer/skills/short-drama-storyboard)
- [镜头设计方法](artifact/references/shot-craft.md)
- [分镜文档格式规范](artifact/references/format-spec.md)
- [场面调度手册](artifact/references/blocking-playbooks.md)
- [打戏与动作分镜](artifact/references/fight-craft.md)
- [首尾帧构图与写法](artifact/references/keyframe-craft.md)
- [阶段规则](artifact/references/stage-contract.md)
- [剧本到首帧完整示例](artifact/references/screenplay-to-keyframe-example.md)

## Skill Output:

**Output Type(s):** [Markdown, Text, Guidance]

**Output Format:** [Markdown shot tables and copyable first-frame or last-frame prompts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May describe shot timing, camera, staging, action, and sound. Does not generate media.]

## Skill Version(s):

1.0.25 (source: server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
