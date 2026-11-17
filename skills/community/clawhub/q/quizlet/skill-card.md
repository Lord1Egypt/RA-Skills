## Description:

Build high-yield Quizlet study sets, tune Learn and Test sessions, and improve weak cards with spaced repetition diagnostics.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ivangdavila](https://clawhub.ai/user/ivangdavila)

### License/Terms of Use:


## Use Case:

External learners and study-focused agents use this skill to design better Quizlet sets, choose appropriate study modes, plan sessions, and improve weak cards based on retention patterns.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Local study notes may retain exam timelines, study goals, confidence notes, or weak-card patterns in ~/quizlet/.

Mitigation: Review or delete ~/quizlet/ before or after installation if those study details should not persist.

Risk: Poorly scoped or ambiguous cards can create misleading confidence during study.

Mitigation: Keep cards atomic, testable, and tied to the assessment goal; rewrite cards missed repeatedly.

## Reference(s):

- [Quizlet Skill on ClawHub](https://clawhub.ai/ivangdavila/skills/quizlet)
- [Quizlet Skill Homepage](https://clawic.com/skills/quizlet)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance, Configuration]

**Output Format:** [Markdown guidance with study plans, card rewrite recommendations, and local note structure]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May maintain local study memory, weak-card logs, reusable set patterns, and session plans under ~/quizlet/.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
