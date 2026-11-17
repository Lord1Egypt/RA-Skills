## Description:

Builds a read-only revision plan from the signed-in user's uNotes flashcard decks, quizzes, study streak, and quota information.

This skill is ready for commercial/non-commercial use.

## Publisher:

[devino](https://clawhub.ai/user/devino)

### License/Terms of Use:

MIT-0

## Use Case:

Students with a connected uNotes account use this skill to review their decks, quizzes, and study streak and get an actionable revision plan. They can also ask about their remaining quota.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Connecting uNotes gives the agent access to personal study and quota information.

Mitigation: Connect only if comfortable sharing this information with the agent; use the signed-in account's read-only data for summaries.

Risk: A revision plan could imply scores or progress that uNotes does not return.

Mitigation: Report only returned data; do not invent scores or progress percentages.

## Reference(s):

- [Planning Revision on ClawHub](https://clawhub.ai/devino/skills/unotes-planning-revision)

## Skill Output:

**Output Type(s):** [Text, Guidance]

**Output Format:** [Markdown]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read-only course-by-course revision summary; quota details on request.]

## Skill Version(s):

1.0.1 (source: server-resolved release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
