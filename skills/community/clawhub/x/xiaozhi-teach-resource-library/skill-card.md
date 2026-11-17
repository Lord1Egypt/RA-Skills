## Description:

帮助独立教师为讲义、题目、讲评话术和错因案例建立带标签与版权状态的可检索资源库，并支持教师审阅后的检索、改编和复用。

This skill is ready for commercial/non-commercial use.

## Publisher:

[qizhitang](https://clawhub.ai/user/qizhitang)

### License/Terms of Use:

MIT-0

## Use Case:

面向独立教师，用于整理既有教学资源，并按学科、知识点、难度和学段检索候选；教师可记录改编来源与使用效果，供后续复用。面向学生或家长的材料应由教师审阅后再使用。

### Deployment Geography for Use:

China (mainland-specific guidance; confirm applicable local requirements)

## Known Risks and Mitigations:

Risk: Some guidance may extend into tutoring or question generation beyond the stated resource-library role.

Mitigation: Review that broader guidance before use, keep student-facing material under teacher review, and verify AI-generated questions before adding them for reuse.

Risk: Stored student cases, assessment material, or third-party teaching resources may contain sensitive or restricted content.

Mitigation: Remove identifying student details, avoid storing unpublished exam content, and record copyright status before adding resources.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/qizhitang/skills/xiaozhi-teach-resource-library)
- [Resource categorization](references/resource-categorization.md)
- [Resource entry examples](references/resource-entry-examples.md)
- [Copyright annotation template](references/copyright-annotation-template.md)
- [AI-generated item check](shared/ai-item-check.md)
- [Crisis referral protocol](shared/crisis-referral-protocol.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON]

**Output Format:** [Chinese text or Markdown; structured JSON resource records when applicable]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Resource records can include classification, copyright status, teaching level, difficulty, source, and reuse notes; student-facing material requires teacher review.]

## Skill Version(s):

2.12.7 (source: SKILL.md frontmatter, server-resolved release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
