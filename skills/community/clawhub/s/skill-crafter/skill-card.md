## Description:

Skill Crafter helps agents create, revise, validate, and register high-quality skills using a four-layer skill structure and a four-phase workflow.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tuobadaidai](https://clawhub.ai/user/tuobadaidai)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent builders use this skill to turn workflows or user requirements into structured agent skills, including skill scaffolding, drafting, quality checks, registration, and later iteration.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can create or modify skills and then submit or register them without a clear final user review step.

Mitigation: Require a mandatory confirmation step that shows the generated skill path and a concise summary before registration.

Risk: Generated skills may include network setup behavior such as cloning external source code.

Mitigation: Require user approval before any generated skill performs network setup such as git clone.

## Reference(s):

- [Skill Crafter on ClawHub](https://clawhub.ai/tuobadaidai/skills/skill-crafter)
- [Quality Checklist](artifact/references/checklist.md)
- [Complete Example](artifact/references/example-complete.md)
- [Four-Layer Skill Structure](artifact/references/four-layers.md)
- [Iteration Guide](artifact/references/iteration.md)
- [Output Patterns](artifact/references/output-patterns.md)
- [Phase Mapping](artifact/references/phase-mapping.md)
- [Workflow Patterns](artifact/references/workflows.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with inline code blocks, generated skill files, shell commands, and configuration-oriented instructions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or modify skill directories and propose registration commands as part of the skill-authoring workflow.]

## Skill Version(s):

1.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
