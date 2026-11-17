## Description:

Use when starting feature work that needs isolation from the current branch, or before executing a plan or fanning out parallel stations - sets up an isolated workspace using the harness's native worktree tool, falling back to a git worktree. Triggers on "worktree", "isolate this work", "don't touch my branch", "work on a copy".

This skill is ready for commercial/non-commercial use.

## Publisher:

[escoffier-labs](https://clawhub.ai/user/escoffier-labs)

### License/Terms of Use:

MIT-0

## Use Case:

Developers use this skill to prepare an isolated workspace before feature work, executing a plan, or coordinating parallel work, so changes can be kept separate from their current branch.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: If isolation fails, setup may continue on and modify the original branch despite the skill's isolation goal.

Mitigation: Require approval before changes or commits on the original branch and before continuing there after isolation fails; use an external worktree directory or local Git exclusion when appropriate.

## Reference(s):

- [Worktree on ClawHub](https://clawhub.ai/escoffier-labs/skills/skillet-worktree)

## Skill Output:

**Output Type(s):** [Shell commands, Guidance]

**Output Format:** [Markdown with shell commands and operational guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May set up a worktree, install project dependencies, and run build or test commands.]

## Skill Version(s):

1.0.0 (source: server-resolved release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
