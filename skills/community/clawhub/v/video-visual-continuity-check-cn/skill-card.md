## Description:

输入已写好的镜头表以及人物、场景参考说明，逐镜核对角色外观、道具状态、光线方向与空间方位的衔接，交付按严重度排序的问题清单和不改写故事的最小修订建议。适用于单次章节、场景或短片方案（最多100行）；资料缺少时明确列出缺项并停止臆测。

This skill is ready for commercial/non-commercial use.

## Publisher:

[xxjrq](https://clawhub.ai/user/xxjrq)

### License/Terms of Use:

MIT No Attribution

## Use Case:

分镜作者和视频制作团队可在拍摄或生成视频前，提交已有镜头表及人物、场景参考，检查相邻镜头中的角色、道具、光线和空间连续性，并获得带证据的分级问题清单与最小修改建议。

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security assessment flags an unpinned CLI installer in the installation instructions.

Mitigation: Confirm the package and release identity before installing; pin a version when your workflow supports it.

Risk: The security assessment reports a possible mismatch between promotional image generation and the stated continuity-review purpose, with some checks incomplete.

Mitigation: Review the image-generation script and expected outputs before running the skill; treat the suspicious verdict as a reason to inspect, not as proof of malicious intent.

## Reference(s):

- [ClawHub release](https://clawhub.ai/xxjrq/skills/video-visual-continuity-check-cn)
- [Project repository listed in manifest](https://github.com/xxjrq/video-visual-continuity-check-cn)

## Skill Output:

**Output Type(s):** [JSON, Markdown tables]

**Output Format:** [JSON or a Markdown table with severity-ranked findings, evidence shot IDs, and minimal-change suggestions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Checks text descriptions only; supports up to 100 shots per submission and reports missing references instead of guessing. Ambiguous wording may need human review.]

## Skill Version(s):

1.0.0 (source: manifest.yaml, server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
