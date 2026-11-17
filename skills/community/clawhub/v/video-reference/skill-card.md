## Description:

按需分析已完成的视频，提炼可复用的剪辑、声音与叙事参考，并导出制作参考 JSON。

This skill is ready for commercial/non-commercial use.

## Publisher:

[worldwonderer](https://clawhub.ai/user/worldwonderer)

### License/Terms of Use:

MIT

## Use Case:

视频编辑与解说制作人员可用此技能分析已完成的视频，整理镜头节奏、声音分工和叙事结构，并导出 production_reference.json 供后续制作参考。

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: An exported reference may retain source names, dialogue, or timestamps if source checks are incomplete or a nested timestamp target is used.

Mitigation: Review exported material before reuse and check that source details and timestamps have been removed.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/worldwonderer/skills/video-reference)
- [Reference schema](references/reference-schema.md)

## Skill Output:

**Output Type(s):** [Analysis, JSON, Guidance]

**Output Format:** [production_reference.json with measured video and audio metrics, structure, and reusable methods]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Local analysis of a finished video; exports reusable production guidance.]

## Skill Version(s):

1.0.7 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
