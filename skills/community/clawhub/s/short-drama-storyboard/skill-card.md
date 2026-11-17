## Description:

把短剧剧本和视觉设定写成切镜有据、前后接戏清晰并带首帧提示词的分镜 Markdown。

This skill is ready for commercial/non-commercial use.

## Publisher:

[worldwonderer](https://clawhub.ai/user/worldwonderer)

### License/Terms of Use:

MIT

## Use Case:

编剧、导演和分镜创作者可用此技能把定稿剧本与视觉设定拆成连续、可执行的镜头表，并编写每镜首帧及必要的尾帧提示词。

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security review was partial because the referenced short-drama.json file was missing; project-specific prompt-language or production-profile settings may therefore be unavailable.

Mitigation: Check whether short-drama.json is expected for the project and supply the relevant language or timing settings when they matter; otherwise use the skill's documented defaults.

## Reference(s):

- [短剧分镜 ClawHub 页面](https://clawhub.ai/worldwonderer/skills/short-drama-storyboard)
- [镜头设计方法](artifact/references/shot-craft.md)
- [场面调度手册](artifact/references/blocking-playbooks.md)
- [首尾帧构图与写法](artifact/references/keyframe-craft.md)
- [打戏与动作分镜](artifact/references/fight-craft.md)
- [阶段规则](artifact/references/stage-contract.md)
- [剧本到首帧完整示例](artifact/references/screenplay-to-keyframe-example.md)

## Skill Output:

**Output Type(s):** [Markdown, Guidance]

**Output Format:** [Markdown shot list with first-frame prompts and optional last-frame prompts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes shot timing, camera and blocking notes, continuity details, and sound cues; does not generate media.]

## Skill Version(s):

1.0.21 (source: server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
