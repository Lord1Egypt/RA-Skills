## Description:

面向初高中学生的数学解题教练，通过分级追问帮助学生理解单题、订正错误并练习同类题，也支持学生明确提出时的考前梳理。

This skill is ready for commercial/non-commercial use.

## Publisher:

[qizhitang](https://clawhub.ai/user/qizhitang)

### License/Terms of Use:

MIT-0

## Use Case:

初中和高中学生可用它拆解单道数学题、订正错误、练习同类题，或在明确提出时进行考前梳理。默认只在当前会话引导；读取档案、归档和提醒须由学生当轮明确开启。

### Deployment Geography for Use:

China (mainland curriculum defaults)

## Known Risks and Mitigations:

Risk: Optional cross-session record reads and handoffs can involve student learning data.

Mitigation: Keep use session-only by default; require the documented current-session consent before record reads, writes, or sharing, and honor the pause and sharing controls.

Risk: The security assessment is partial and medium confidence, with scope and language-choice issues and an unresolved local reference.

Mitigation: Review the reported issues and verify the missing reference for the intended use; treat the benign verdict as an assessment of available evidence, not a guarantee.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/qizhitang/skills/xiaozhi-math-problem-solving-coach)
- [Hint ladder](artifact/shared/hint-ladder.md)
- [AI-generated problem checks](artifact/shared/ai-item-check.md)
- [Four-step problem-solving workflow](artifact/references/photo-4step-statemachine.md)
- [Socratic question guide](artifact/references/math-socrates-guide.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Guidance]

**Output Format:** [Chinese tutoring dialogue, mathematical notation, structured study outlines, practice questions, and consent-based JSON handoff entries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses graduated hints and similar-problem practice; generated questions are checked before presentation.]

## Skill Version(s):

2.12.7 (source: release evidence and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
