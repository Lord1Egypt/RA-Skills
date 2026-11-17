## Description:

Delegate coding tasks to Codex, Claude Code, Pi, or OpenCode agents via background processes for feature work, PR review, refactoring, and iterative codebase changes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tshogx](https://clawhub.ai/user/tshogx)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to delegate substantial coding tasks to external coding agents while keeping execution mode, workspace choice, session monitoring, and cleanup procedures explicit.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill normalizes workflows that disable approvals or sandboxing for delegated coding agents.

Mitigation: Prefer disposable clones or containers, limited credentials, normal approval prompts, and manual review before enabling bypass or yolo-style execution modes.

Risk: Delegated agents may install dependencies, create commits, push branches, comment on PRs, or emit system events with unintended effects.

Mitigation: Review proposed commands and outputs before dependency installation, commits, pushes, PR comments, or OpenClaw system events.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/tshogx/skills/tshogx-coding-agent)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration]

**Output Format:** [Markdown with shell command examples and operational tables]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Instruction-only skill; no structured machine output is produced.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
