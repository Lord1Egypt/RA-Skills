## Description:

Use when creating or improving a skill for an AI agent, especially when the skill needs strong trigger wording, project-local context, references, scripts, tests, self-healing rules, or a completion gate another agent could follow without guessing.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zenchantlive](https://clawhub.ai/user/zenchantlive)

### License/Terms of Use:

MIT

## Use Case:

Developers and agent-skill authors use this skill to create or improve reusable agent skills, route project-specific details into project-local context, and validate that a fresh agent can follow the skill without guessing critical facts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can lead an agent to create or revise project.skill.md, SKILL.md, references, scripts, and tests in a target repository.

Mitigation: Review generated or modified skill files before use, and run validation in a repository where those file changes are expected.

Risk: Project-local context files may accidentally capture secrets or sensitive environment details.

Mitigation: Keep secrets out of project.skill.md and review the file before sharing or using it with an agent.

Risk: The included example/reference workflow can modify generated files such as an example dist directory.

Mitigation: Run the example/reference workflow only where generated files are safe to create or overwrite.

## Reference(s):

- [Writing Better Skills on ClawHub](https://clawhub.ai/zenchantlive/skills/writing-better-skills)
- [Project Skill Context](references/project-skill-context.md)
- [Description Writing](references/description-writing.md)
- [Skill Architecture Levels](references/skill-architecture-levels.md)
- [Script / Test Conventions](references/script-test-conventions.md)
- [Self-Healing Rules](references/self-healing-rules.md)
- [Skill Testing](references/skill-testing.md)
- [Behavioral Validation Checklist](references/behavioral-validation-checklist.md)
- [Completion Gate](references/completion-gate.md)
- [Workflow Patterns](references/workflows.md)
- [Output Patterns](references/output-patterns.md)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown guidance with optional code, shell commands, and configuration files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or revise project.skill.md, SKILL.md, references, scripts, and tests in a target repository.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
