## Description:

Study Buddy helps learners create flashcards, take quizzes, review with spaced repetition, plan study sessions, manage notes, use Pomodoro timing, and track progress while keeping study data local.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mkpareek0315](https://clawhub.ai/user/mkpareek0315)

### License/Terms of Use:


## Use Case:

External learners use this skill as a local study assistant for flashcards, quizzes, spaced repetition, study plans, Pomodoro sessions, notes, practice questions, and progress tracking.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Local study records may include sensitive notes, cards, quiz scores, plans, and history.

Mitigation: Review the stored data under ~/.openclaw/study-buddy/ and add clear delete or export controls before using the skill with sensitive material.

Risk: Broad activation phrases may cause the study assistant to run when the user intended a different learning-related task.

Mitigation: Narrow activation phrases during deployment if the environment needs more precise skill routing.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/mkpareek0315/skills/study-buddy-ai)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown-style conversational responses with occasional JSON examples and shell commands.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create and update local study data files under ~/.openclaw/study-buddy/.]

## Skill Version(s):

1.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
