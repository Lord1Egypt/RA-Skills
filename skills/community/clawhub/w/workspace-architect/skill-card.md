## Description:

Create, analyze, and optimize OpenClaw workspace configuration files (SOUL.md, IDENTITY.md, USER.md, MEMORY.md, TOOLS.md, AGENTS.md, STYLE.md, HEARTBEAT.md) with guided workflows and best practices validation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[luanvha2550-hash](https://clawhub.ai/user/luanvha2550-hash)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw workspace maintainers use this skill to create, audit, and optimize workspace configuration files for clarity, placement, injection order, and safety review before applying changes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Workspace configuration files may contain personal preferences, memory, or rules that affect future agent behavior.

Mitigation: Review generated analysis and proposed changes before applying them, especially changes to SOUL.md, AGENTS.md, MEMORY.md, or USER.md.

Risk: Optimization suggestions could move or condense instructions in a way that changes behavior if accepted without review.

Mitigation: Compare diffs and confirm that critical rules, safety boundaries, and ownership of content remain correct before use.

## Reference(s):

- [OpenClaw Skills Documentation](https://docs.openclaw.ai/tools/skills)
- [Arquivo Specifications - OpenClaw Workspace Files](references/arquivo-specs.md)
- [ClawHub Best Practices & Advanced Examples](references/best-practices.md)
- [Pattern Recognition - Correct vs Incorrect Patterns](references/patterns.md)
- [Guided Creation Questionnaire](references/questionnaire.md)

## Skill Output:

**Output Type(s):** [text, markdown, configuration, guidance, shell commands]

**Output Format:** [Markdown reports, configuration drafts, and command-line text output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Draft workspace file changes are intended for user review before application.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
