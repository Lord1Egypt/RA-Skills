## Description:

Structured software engineering workflow with state-driven execution: requirement analysis, technical design, task planning, execution with state navigation, and session recovery.

This skill is ready for commercial/non-commercial use.

## Publisher:

[naozixu](https://clawhub.ai/user/naozixu)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineering teams use this skill to manage complex feature work, architecture changes, and cross-module fixes through a phased requirements, design, task planning, and execution workflow.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can guide code changes and commits during execution, so incorrect plans or task details could lead to unwanted repository changes.

Mitigation: Review and approve the requirements, design, and task plan before execution, and inspect generated diffs and verification results before accepting changes.

Risk: Continuous operation can advance through approved tasks without per-task review.

Mitigation: Use continuous operation only after the task plan is approved and when repository tests, review controls, and rollback practices are in place.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown documents, task tracker updates, code edits, and command guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or update requirements.md, design.md, and tasks.md, and may guide verification commands and commits during execution.]

## Skill Version(s):

1.0.4 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
