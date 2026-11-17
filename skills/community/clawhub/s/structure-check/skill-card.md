## Description:

Mechanically checks a task-derived checklist against code structure and reports pass or fail results through exit codes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[return054](https://clawhub.ai/user/return054)

### License/Terms of Use:

MIT-0

## Use Case:

Developers use the skill after coding tasks to check that requested code structures are present, exported, called, or implemented beyond a stub.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A structural verdict may be mistaken for proof of overall correctness, and checks can add unnecessary follow-up work.

Mitigation: Keep checklist items tied to the requested work, review proposed changes, and run behavioral tests alongside structural checks.

## Reference(s):

- [Structure Check on ClawHub](https://clawhub.ai/return054/skills/structure-check)

## Skill Output:

**Output Type(s):** [JSON, text]

**Output Format:** [JSON requirement checklist input and plain-text structural verdict output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Node.js 18 or later; structural checks do not establish behavioral correctness.]

## Skill Version(s):

1.0.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
