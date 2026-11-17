## Description:

小红书大字图全流程制作技能。当用户需要制作小红书配图（带文字的大图、卖点图）时触发。完整流程：理解需求 → 精炼文案 → 用 AI 生成底图 → 叠加文字 → 通过飞书发出。所有图片存 /workspace/xhs/。

This skill is ready for commercial/non-commercial use.

## Publisher:

[cleanbinggmail](https://clawhub.ai/user/cleanbinggmail)

### License/Terms of Use:

MIT-0

## Use Case:

Content creators and social media operators use this skill to turn short topics into Xiaohongshu-style poster images with concise cover copy, generated visuals, overlaid text, and Feishu delivery.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated user-derived images may contain private, client, unpublished, or business-sensitive material and the workflow sends final images to a fixed Feishu recipient without an explicit confirmation step.

Mitigation: Review prompts and generated images before installation or use; modify the workflow to stop after local image generation and require explicit approval before sending through Feishu when sensitive material may be present.

## Reference(s):

- [小红书大字图 — 详细工作流](references/workflow.md)

## Skill Output:

**Output Type(s):** [text, files, guidance, API calls]

**Output Format:** [Image files plus concise completion text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated images are written under /workspace/xhs/ and final images are sent through Feishu according to the workflow.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
