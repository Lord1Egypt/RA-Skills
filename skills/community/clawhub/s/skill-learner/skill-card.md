## Description:

Identify repeated workflows, recurring user asks, common failures, and reusable procedures that should become new skills or improvements to existing skills.

This skill is ready for commercial/non-commercial use.

## Publisher:

[noahfleming](https://clawhub.ai/user/noahfleming)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to recognize repeated workflows, recurring corrections, and common failures, then decide whether to create or improve skill knowledge, add supporting references or scripts, or keep the guidance as a smaller local rule.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The agent may recommend a new skill or local rule that captures a repeated pattern incorrectly.

Mitigation: Review proposed skill, script, reference, or rule changes before creation or modification.

Risk: Overly broad recommendations could add unnecessary skill documentation or duplicate existing skills.

Mitigation: Confirm that the pattern is real and reusable, and prefer improving an existing skill or using a local rule when that is sufficient.

## Reference(s):

- [Skill Learner on ClawHub](https://clawhub.ai/noahfleming/skills/skill-learner)

## Skill Output:

**Output Type(s):** [guidance, markdown, configuration]

**Output Format:** [Markdown guidance with structured recommendations]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [No executable code; produces recommendations for reusable skill knowledge, references, scripts, or local rules.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
