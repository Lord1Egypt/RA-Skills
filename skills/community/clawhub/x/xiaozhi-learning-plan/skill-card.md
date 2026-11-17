## Description:

将学习目标拆解为可执行的30天学习方案（小学高段采用周计划），并在学生启用后跟进执行偏差。

This skill is ready for commercial/non-commercial use.

## Publisher:

[qizhitang](https://clawhub.ai/user/qizhitang)

### License/Terms of Use:

MIT-0

## Use Case:

学生可用此技能把考试准备或学习目标转成按学科、日期和可用时间安排的学习计划。经单独同意后，它也可使用有限的学习档案摘要跟进进度，生成家长看板，或交接提醒任务。

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: ClawScan reports unresolved privacy and scope conflicts involving access to and sharing of learning-profile data, including broader learning metrics and schema-allowed profile writeback.

Mitigation: Before use, review the profile-data consent and sharing rules, confirm the requested metrics and writeback scope are acceptable, and enable each profile or sharing action only with explicit consent.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/qizhitang/skills/xiaozhi-learning-plan)
- [Plan templates](artifact/references/plan-templates.md)
- [Grade-band guidance](artifact/shared/grade-bands.md)
- [Crisis referral protocol](artifact/shared/crisis-referral-protocol.md)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, JSON]

**Output Format:** [中文文本和Markdown学习计划、进度简报或家庭看板；需要提醒时可附带结构化JSON交接]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [内容会按学段、学习目标、可用时间和学生选择调整。]

## Skill Version(s):

2.12.7 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
