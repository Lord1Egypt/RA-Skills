## Description:

为独立教师提供试听诊断、最小化需求采集与新学员建档流程，涵盖监护人同意、需求访谈、前测、试讲观察和试听后报名跟进。

This skill is ready for commercial/non-commercial use.

## Publisher:

[qizhitang](https://clawhub.ai/user/qizhitang)

### License/Terms of Use:

MIT

## Use Case:

独立教师可用此技能为新学员准备试听与需求访谈、整理学情观察，并在取得监护人同意后建立精简的学员档案。它也提供试听后报名阶段的跟进建议；排课、课后记录和续费等后续事务交由相应技能处理。

### Deployment Geography for Use:

Global; follow local requirements for tutoring, minors' data, and safeguarding.

## Known Risks and Mitigations:

Risk: The security review notes instructions and write access that may extend beyond intake, and reports incomplete analysis because two referenced paths were missing.

Mitigation: Before installation, review the reported scope mismatches and confirm that any student-profile or course-package ledger write access is needed; keep records limited to consented, pseudonymous learning information.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/qizhitang/skills/xiaozhi-teach-student-intake)
- [Student basic information form](references/student-basic-info-form.md)
- [5W needs interview checklist](references/needs-interview-5w-checklist.md)
- [Trial lesson structure](references/trial-lesson-5-segment-structure.md)
- [Trial observation record](references/trial-observation-record.md)
- [Formal student profile template](references/formal-student-profile-template.md)
- [Trial-to-enrollment follow-up scripts](references/followup-scripts-trial-conversion.md)
- [Crisis referral protocol](shared/crisis-referral-protocol.md)
- [Student workspace schema](shared/solo-teacher-workspace.schema.json)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance, Files]

**Output Format:** [Chinese-language interview prompts, lesson and observation templates, follow-up drafts, and structured student profile data.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Drafts are for teacher review; persistent student profile creation requires guardian consent.]

## Skill Version(s):

2.12.7 (source: frontmatter; server release 2.12.7)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
