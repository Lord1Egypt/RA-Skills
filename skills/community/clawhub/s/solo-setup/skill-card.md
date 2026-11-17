## Description:

Auto-generate project workflow config from existing PRD and CLAUDE.md files with zero questions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[fortunto2](https://clawhub.ai/user/fortunto2)

### License/Terms of Use:

MIT

## Use Case:

Developers use this skill after project scaffolding to create a workflow document for planning and build agents. It derives TDD policy, commit strategy, verification checkpoints, and related workflow guidance from existing project files.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill reads project planning and configuration files and writes docs/workflow.md.

Mitigation: Review the generated workflow document before relying on it for planning or build automation.

Risk: The skill may edit CLAUDE.md, which can affect future agent behavior in the project.

Mitigation: Review any CLAUDE.md diff before continuing with downstream agent workflows.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/fortunto2/skills/solo-setup)
- [Publisher profile](https://clawhub.ai/user/fortunto2)

## Skill Output:

**Output Type(s):** [markdown, configuration, shell commands, guidance]

**Output Format:** [Markdown files and concise agent-facing status text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Creates docs/workflow.md and may update CLAUDE.md to reference the workflow document.]

## Skill Version(s):

2.1.1 (source: server release metadata and SKILL.md metadata.version)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
