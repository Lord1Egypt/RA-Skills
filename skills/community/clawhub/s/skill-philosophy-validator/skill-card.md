## Description:

Validates OpenClaw skill designs against five core principles and produces prioritized review guidance that preserves the skill's intended behavior.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kangyishuai](https://clawhub.ai/user/kangyishuai)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and skill authors use this skill to review SKILL.md files and related support files for skill design quality, trigger specificity, common pitfalls, and actionable improvement priorities.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The broad trigger scope may run during ordinary skill editing and produce review guidance when a separate validation pass was not explicitly requested.

Mitigation: Review whether the validation report is relevant to the current editing task before applying its recommendations.

Risk: The skill produces design recommendations that could change a skill's behavior if applied without review.

Mitigation: Apply recommendations selectively and preserve the original skill's core capabilities, trigger intent, and referenced support files.

## Reference(s):

- [Design Philosophy Reference](references/design-philosophy.md)
- [ClawHub Skill Page](https://clawhub.ai/kangyishuai/skills/skill-philosophy-validator)

## Skill Output:

**Output Type(s):** [guidance, markdown, text]

**Output Format:** [Markdown review report]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses the user's language for the report and includes an overall assessment, principle-by-principle findings, prioritized actions, highlights, and capability preservation notes.]

## Skill Version(s):

1.0.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
