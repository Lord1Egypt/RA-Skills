## Description:

Route user tasks to the most relevant skills using a layered taxonomy, risk model, and minimum-necessary-loading strategy.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wzk332266](https://clawhub.ai/user/wzk332266)

### License/Terms of Use:

MIT-0

## Use Case:

Agents and developers use this skill to choose the most relevant skill for a task, classify newly added skills, and reason about routing risk before loading action-capable skills.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can influence future skill selection and may steer agents toward action-capable skills.

Mitigation: Review routing recommendations before use and prefer the lowest-risk skill that completes the task.

Risk: The artifact documents maintenance commands for helper scripts that are not included in the release package.

Mitigation: Do not run those commands unless trusted helper implementations are present and resolve from the skill package.

Risk: Routing logs or local extensions could capture sensitive task details.

Mitigation: Avoid recording secrets, customer data, or sensitive prompts in routing logs.

## Reference(s):

- [Skill Taxonomy Router on ClawHub](https://clawhub.ai/wzk332266/skills/skill-taxonomy-router)
- [Change Log](references/change-log.md)
- [Session Layer](references/session-layer.md)
- [Skill Classification Schema](references/skill-classification-schema.md)

## Skill Output:

**Output Type(s):** [guidance, markdown, shell commands, configuration]

**Output Format:** [Markdown guidance with structured routing summaries and optional shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces routing recommendations and risk classifications; it does not execute tools by itself.]

## Skill Version(s):

1.5.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
