## Description:

Guides agents through Git worktree management for parallel development, including branch creation, agent launches, merging, and cleanup.

This skill is ready for commercial/non-commercial use.

## Publisher:

[loonghao](https://clawhub.ai/user/loonghao)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to guide parallel AI agents in separate Git worktrees and bring their changes back into a shared repository.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill instructs agents to post final outcomes to an issue or task tracker without clear user opt-in.

Mitigation: Require the user's approval of the destination and exact comment before posting.

Risk: Merge and cleanup commands can remove worktrees or branches containing local work.

Mitigation: Inspect worktree status and branch state before merging or removing anything.

Risk: Hooks and agent-launch commands can run additional processes in a worktree.

Mitigation: Review configured hooks and launch commands before executing them.

## Reference(s):

- [worktrunk on ClawHub](https://clawhub.ai/loonghao/skills/worktrunk)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Configuration guidance]

**Output Format:** [Markdown with bash and TOML examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Guidance for worktree creation, agent launches, merges, and cleanup.]

## Skill Version(s):

1.0.1 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
