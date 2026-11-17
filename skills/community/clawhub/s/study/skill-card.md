## Description:

Study helps agents turn courses, syllabi, exams, deadlines, notes, and revision problems into dated study plans, retrieval practice, spaced review, coursework triage, and exam preparation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ivangdavila](https://clawhub.ai/user/ivangdavila)

### License/Terms of Use:

MIT-0

## Use Case:

Students and study-support agents use this skill to plan a term, run study sessions, prioritize assessments, and prepare for exams. It is designed to scaffold, quiz, drill, and critique rather than produce work that will be submitted for credit.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill keeps persistent local notes about courses, grades, exam dates, mistakes, study partners, projects, and bookings under ~/Clawic/data.

Mitigation: Install only when that local recordkeeping is acceptable, and review the disclosed Clawic data paths before use.

Risk: Users may paste sensitive credentials or identity data into study records.

Mitigation: Do not paste passwords, API keys, proctoring passcodes, payment cards, or ID-document numbers; store only pointers such as keychain, environment-variable, password-manager, or local-file references.

Risk: Study guidance may affect graded academic work or assessment integrity.

Mitigation: Use the skill for scaffolding, hints, quizzing, drills, and critique, and do not use it to produce work that will be submitted for credit.

## Reference(s):

- [ClawHub Study skill page](https://clawhub.ai/ivangdavila/skills/study)
- [Clawic Study skill page](https://clawic.com/skills/study)

## Skill Output:

**Output Type(s):** [text, markdown, configuration, guidance]

**Output Format:** [Markdown and structured study records]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose local note updates under disclosed Clawic data paths; does not submit, upload, or transmit work on the user's behalf.]

## Skill Version(s):

1.0.3 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
