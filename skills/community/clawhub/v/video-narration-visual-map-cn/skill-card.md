## Description:

输入已批准旁白、编号既有镜头或素材说明、目标观看收益与必须展示的证据，输出逐句旁白到镜头编号和可见证据的对应表，并列出有声无画、画不支撑话与需补素材项。

This skill is ready for commercial/non-commercial use.

## Publisher:

[xxjrq](https://clawhub.ai/user/xxjrq)

### License/Terms of Use:

MIT No Attribution

## Use Case:

Video editors and content reviewers use this skill before finalizing a video to check whether existing shots visibly support each approved narration line and to identify missing evidence or footage.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The documented install command uses an unpinned CLI, and the security review reports that inspection was incomplete.

Mitigation: Verify the CLI version and source revision before installing; review the skill files before use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/xxjrq/skills/video-narration-visual-map-cn)
- [Project repository (listed in release manifest)](https://github.com/xxjrq/video-narration-visual-map-cn)
- [Related video storyboard reference](https://github.com/agentara/skills/blob/main/skills/aigc/video-storyboard/SKILL.md)

## Skill Output:

**Output Type(s):** [Markdown, Guidance]

**Output Format:** [Markdown table mapping narration to shot IDs and visible evidence, followed by missing-material recommendations; requests missing input when narration or shot descriptions are absent.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [One video per request; supports up to 30 narration units and 30 candidate shots.]

## Skill Version(s):

1.0.0 (source: release evidence and manifest)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
