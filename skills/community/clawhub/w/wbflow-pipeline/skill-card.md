## Description:

流水线总控——按顺序串联 story→script→storyboard→(定妆char)→prompt→image→video→assemble 八个环节，只调度与校验，不产出任何内容。用于一句话驱动整套 AI 漫剧/短视频生产。（WBFlow 由 9 个 skill 组成：本总控 + story/script/storyboard/prompt/char/image/video/assemble 八环，须全套配套安装，单独安装无法运行。）

This skill is ready for commercial/non-commercial use.

## Publisher:

[junci003](https://clawhub.ai/user/junci003)

### License/Terms of Use:

MIT-0

## Use Case:

开发者使用该总控调度 AI 漫剧或短视频制作流程，校验各阶段的产物、引用和一致性，并汇总交付状态。

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workflow depends on all eight companion skills and a referenced verification script, whose availability is not established by this release evidence.

Mitigation: Install and review the companion skills, and confirm the verification script is available before starting the workflow.

Risk: Image or video generation may incur external-model costs, and companion-skill behavior is outside this review.

Mitigation: Review companion behavior, agree on generation costs, and obtain user authorization before invoking external models.

## Reference(s):

- [WBFlow Pipeline on ClawHub](https://clawhub.ai/junci003/skills/wbflow-pipeline)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Validation results]

**Output Format:** [Text guidance and a Markdown delivery checklist/table]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Coordinates and validates workflow stages; does not create story, script, prompts, images, video, or other production content.]

## Skill Version(s):

1.0.1 (source: server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
