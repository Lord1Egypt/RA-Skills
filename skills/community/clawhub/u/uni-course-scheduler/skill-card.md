## Description:

Plans university courses from course catalogs, recommends courses, builds weekly schedules with enrollment priorities, and exports Excel workbooks and ICS calendars.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ez-hq](https://clawhub.ai/user/ez-hq)

### License/Terms of Use:

MIT

## Use Case:

University students use this skill to plan semesters from official course-catalog information, evaluate course recommendations and scheduling priorities, and export schedules. It supports free local planning for an individual student and optional paid cloud processing for batch or institutional needs, with confirmation before submission.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Automated checks cannot guarantee accurate schedules, prerequisites, or degree recommendations.

Mitigation: Verify class times, prerequisites, and degree requirements against official university sources; treat recommendations as planning assistance.

Risk: Optional cloud processing sends student and course information to an external provider and incurs a per-run fee.

Mitigation: Before each cloud submission, review the provider, fields sent, and fee; obtain explicit consent and minimize shared student information. Use local mode to avoid the optional cloud transfer.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/ez-hq/skills/uni-course-scheduler)
- [Course catalog collection guidance](artifact/references/catalog-collection.md)
- [Local validation guidance](artifact/references/local-validation.md)
- [Cloud output format](artifact/references/cloud-output-format.md)

## Skill Output:

**Output Type(s):** [Guidance, Analysis, Files]

**Output Format:** [Course recommendations and schedules, Excel (.xlsx) workbooks, ICS (.ics) calendars, and text or Markdown summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Local personal mode or optional paid cloud mode; validate schedules and academic requirements against official university sources.]

## Skill Version(s):

2.7.14 (source: SKILL.md frontmatter, skill.json, server release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
