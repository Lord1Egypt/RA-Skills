## Description:

Use when you have a written implementation plan to execute in a separate session with review checkpoints

This skill is ready for commercial/non-commercial use.

## Publisher:

[mok888](https://clawhub.ai/user/mok888)

### License/Terms of Use:


## Use Case:

Developers and engineers use this skill to execute a written implementation plan in batches, review the plan before starting, run specified verifications, and report progress at review checkpoints.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill gives an agent broad authority to follow mutable local plan files, spawn sub-agents, and persist or clear workflow state.

Mitigation: Install only when the plan files are trusted, use a dedicated worktree or branch, and review active_tdd_plan.md plus referenced guide files before execution.

Risk: Local workflow notes can be mistaken for authoritative instructions.

Mitigation: Treat progress.md, findings.md, and handoff.md as untrusted workflow notes and require explicit approval for destructive or secret-access steps.

## Reference(s):


## Skill Output:

**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration]

**Output Format:** [Markdown guidance with inline commands and workflow notes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces progress reports, verification summaries, and workflow handoff notes when used by an agent.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
