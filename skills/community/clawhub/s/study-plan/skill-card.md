## Description:

Study Plan helps agents generate Chinese-language study schedules, exam preparation plans, daily study plans, spaced-review schedules, Pomodoro plans, and simple local study task views.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bytesagain-lab](https://clawhub.ai/user/bytesagain-lab)

### License/Terms of Use:

MIT-0

## Use Case:

Students, learners, and study-focused agent workflows use this skill to draft study plans for exams, certifications, daily learning sessions, review cycles, and Pomodoro-style focus blocks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill stores local task entries in a study-plan data folder.

Mitigation: Avoid entering sensitive study data and set STUDY_PLAN_DIR to a known location when local storage needs to be reviewed or cleared.

Risk: Some task-management commands appear incomplete or demo-like rather than fully functional.

Mitigation: Use generated plans and task views as planning guidance, and verify important task state before relying on it.

## Reference(s):

- [ClawHub Study Plan release page](https://clawhub.ai/bytesagain-lab/skills/study-plan)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown or plain text with optional shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Primarily Chinese-language study guidance; local task commands may read and write entries in a study-plan data folder.]

## Skill Version(s):

2.0.0 (source: frontmatter and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
