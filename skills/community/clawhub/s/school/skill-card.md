## Description:

AI-powered education for K-12 students with parental controls, adaptive learning by age, homework help, exam prep, and progress tracking.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ivangdavila](https://clawhub.ai/user/ivangdavila)

### License/Terms of Use:


## Use Case:

Parents and students use this skill to organize K-12 learning support, age-adapted tutoring, homework help, exam preparation, curriculum alignment, progress tracking, and parent-visible controls.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may retain sensitive child learning records locally while claiming protections that the artifacts do not implement.

Mitigation: Review before installing, minimize retained child data, and rely only on security controls provided by the hosting application.

Risk: School names, detailed session history, emotional disclosures, or other sensitive child data could be stored by default.

Mitigation: Avoid storing these data types unless explicitly needed, consented to, and protected by the deployment environment.

Risk: Parent-only access and encryption are described in the artifacts but are not implemented by the skill files themselves.

Mitigation: Confirm that the host app enforces access control, deletion, and encryption before using the skill with real children.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ivangdavila/skills/school)
- [Publisher profile](https://clawhub.ai/user/ivangdavila)
- [Age-specific approaches](by-age.md)
- [Homework help and tutoring](tutoring.md)
- [Exams and assessment](exams.md)
- [Parent dashboard and controls](parents.md)
- [Child safety protocols](safety.md)
- [Curriculum integration](curriculum.md)

## Skill Output:

**Output Type(s):** [text, markdown, configuration, guidance]

**Output Format:** [Markdown guidance with structured learning plans, reports, practice content, and local workspace configuration.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces age-adapted educational guidance and may propose local files under ~/school/ for child profiles, progress, calendars, resources, exams, and settings.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
