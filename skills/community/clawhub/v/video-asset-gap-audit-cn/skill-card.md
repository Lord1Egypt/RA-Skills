## Description:

核验已批准镜头与现有素材的内容、画幅、时长和授权覆盖，并输出缺失、规格不符及待确认项。

This skill is ready for commercial/non-commercial use.

## Publisher:

[xxjrq](https://clawhub.ai/user/xxjrq)

### License/Terms of Use:

MIT No Attribution (MIT-0)

## Use Case:

视频制作人员可在开拍或补料前，用它逐项核对已批准镜头与现有素材，识别可用素材、缺口、规格不符和需要补充确认的信息。

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The installation package is unpinned.

Mitigation: Review the package contents and pin the intended version or commit before installing.

Risk: Some code inspection was incomplete, so the benign security verdict has medium confidence.

Mitigation: Review the included scripts before running them.

Risk: An audit logic issue could lead to unreliable production decisions.

Mitigation: Manually verify coverage and authorization decisions before acting on the report.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/xxjrq/skills/video-asset-gap-audit-cn)
- [Project Repository](https://github.com/xxjrq/video-asset-gap-audit-cn)
- [Video Storyboard Reference](https://github.com/agentara/skills/blob/main/skills/aigc/video-storyboard/SKILL.md)

## Skill Output:

**Output Type(s):** [Markdown, Guidance]

**Output Format:** [Markdown tables and actionable checklists]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Per-shot coverage audit for one video, with up to 30 shots and 50 assets.]

## Skill Version(s):

1.0.0 (source: server-resolved release evidence, manifest.yaml)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
