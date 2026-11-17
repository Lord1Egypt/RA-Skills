## Description:

Use when a user is trying to discover an installable or reusable skill or workflow, especially when they ask for a skill for a task, want to compare nearby skill categories, or need help narrowing discovery results.

This skill is ready for commercial/non-commercial use.

## Publisher:

[littledinoc](https://clawhub.ai/user/littledinoc)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users use this skill to find installable or reusable skills, narrow ambiguous discovery needs, compare nearby skill categories, and receive a small set of relevant recommendations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends search intent, clarifications, recommendation choices, and feedback to a third-party service.

Mitigation: Avoid entering confidential project, customer, or proprietary details when using the skill.

Risk: The skill may show installation commands for recommended skills without fully scoped package or repository validation.

Mitigation: Independently review the package, repository, and exact version or commit before running any install command.

## Reference(s):

- [Skill Compass on ClawHub](https://clawhub.ai/littledinoc/skills/skillcompass)
- [Publisher profile](https://clawhub.ai/user/littledinoc)
- [Skill search service](https://skills.megatechai.com/)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown recommendations with concise fit reasoning and optional inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Returns 1-3 final recommendations after at most two retrieval passes and one clarification question.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
