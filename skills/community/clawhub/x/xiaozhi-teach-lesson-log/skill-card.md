## Description:

把独立教师的课后记忆整理为结构化教学档案，记录课堂内容、掌握度、课堂反应、进步和后续调整。

This skill is ready for commercial/non-commercial use.

## Publisher:

[qizhitang](https://clawhub.ai/user/qizhitang)

### License/Terms of Use:

MIT

## Use Case:

Independent teachers use this skill after one-to-one or small-group lessons to create pseudonymous lesson records, review learning progress, and prepare next-lesson notes. Records and lesson-credit entries are shown to the teacher for confirmation before saving.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Release security evidence reports that schema validation may allow lesson-credit balance changes beyond the declared write scope.

Mitigation: Keep usedUnits and remainingUnits changes behind explicit, immediate teacher confirmation, and verify proposed changes against the declared write scope before saving.

## Reference(s):

- [ClawHub release](https://clawhub.ai/qizhitang/skills/xiaozhi-teach-lesson-log)
- [Publisher profile](https://clawhub.ai/user/qizhitang)

## Skill Output:

**Output Type(s):** [Text, JSON, Guidance]

**Output Format:** [Structured lesson records and concise teacher-facing summaries in text or Markdown]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses student aliases; lesson records are previewed for teacher confirmation, and lesson-credit balances change only after explicit confirmation.]

## Skill Version(s):

2.12.7 (source: release evidence and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
