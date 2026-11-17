## Description:

Generates a single-file, offline HTML quiz app for students, with practice, exam, memorization, and wrong-answer review modes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[duzhilei951](https://clawhub.ai/user/duzhilei951)

### License/Terms of Use:

MIT-0

## Use Case:

Teachers, tutors, and education content authors use this skill to turn pasted or loosely formatted question sets into a deployable offline quiz page for student practice, testing, memorization, and wrong-answer review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated quiz apps may store scores and wrong-answer history in the browser.

Mitigation: Before sharing with students, add or verify a clear local-storage notice and provide a way to clear saved learning records.

Risk: Imported learning-record JSON could come from an untrusted source.

Mitigation: Use care when importing records and share import files only through trusted channels.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/duzhilei951/skills/quiz-app-generator)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Files, Guidance]

**Output Format:** [Single-file HTML with inline CSS and JavaScript, plus brief Markdown usage guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated apps are designed to run offline with no external dependencies and may persist quiz progress in browser localStorage.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
