## Description:

帮助独立教师生成周课表、检查师生时间冲突，并跟踪课时包余量、到期提示和补课请假建议。

This skill is ready for commercial/non-commercial use.

## Publisher:

[qizhitang](https://clawhub.ai/user/qizhitang)

### License/Terms of Use:

MIT-0

## Use Case:

独立教师可用此技能规划每周课程、检查时间冲突，并跟踪课时包余额与到期时间。写入课表前由教师确认。

### Deployment Geography for Use:

中国大陆（各地规定可能不同）

## Known Risks and Mitigations:

Risk: The security assessment notes a potential mismatch between the reported instruction to compose parent-facing replies and the skill's stated scope; its analysis was partial.

Mitigation: Keep parent communication in the designated parent-communication skill and have the teacher review it; consider the security assessment incomplete.

## Reference(s):

- [Weekly schedule template](references/weekly-schedule-template.md)
- [Leave, makeup, and rescheduling forms](references/leave-makeup-reschedule-forms.md)
- [Solo teacher workspace schema](shared/solo-teacher-workspace.schema.json)
- [ClawHub release page](https://clawhub.ai/qizhitang/skills/xiaozhi-teach-schedule-manager)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON]

**Output Format:** [Chinese text or Markdown, with structured workspace JSON for confirmed schedule and course package updates]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Schedule writes require teacher confirmation; course package tracking stores lesson counts, not financial amounts.]

## Skill Version(s):

2.12.7 (source: frontmatter, ClawHub release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
