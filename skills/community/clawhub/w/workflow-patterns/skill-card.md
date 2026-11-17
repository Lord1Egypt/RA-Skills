## Description:

Systematic task implementation using TDD, phase checkpoints, and structured commits.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wpank](https://clawhub.ai/user/wpank)

### License/Terms of Use:


## Use Case:

Developers and coding agents use this skill to implement planned work with a test-first lifecycle, phase checkpoints, quality gates, and traceable commits.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Mutable install commands can resolve different package contents over time.

Mitigation: Install a pinned ClawHub package version or reviewed commit instead of @latest or a mutable GitHub path.

Risk: The workflow asks agents to update plans and create git commits, which can change repository history and project state.

Mitigation: Review proposed file changes and commit messages before allowing commits, and require explicit approval at phase checkpoints.

## Reference(s):

- [Workflow Patterns on ClawHub](https://clawhub.ai/wpank/skills/workflow-patterns)
- [TDD Quick Reference](references/tdd-quick-reference.md)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Shell commands]

**Output Format:** [Markdown guidance with checklists, task-status examples, commit-message examples, and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires explicit user approval before advancing past phase checkpoints.]

## Skill Version(s):

1.0.0 (source: server release metadata; artifact frontmatter states 2.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
