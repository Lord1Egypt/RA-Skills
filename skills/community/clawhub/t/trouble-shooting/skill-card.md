## Description:

Trouble Shooting helps an agent isolate error investigation in a Git worktree or subagent while preserving the main conversation context.

This skill is ready for commercial/non-commercial use.

## Publisher:

[graceqx](https://clawhub.ai/user/graceqx)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill when a coding issue or runtime error needs isolated investigation. It guides troubleshooting in a temporary worktree when possible, or through subagent analysis when a worktree is not available, so the main task context can continue afterward.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can perform high-impact Git operations, including creating worktrees, merging a troubleshooting branch into the current branch, and force-deleting temporary worktrees or branches.

Mitigation: Use explicit commands, review the active troubleshooting snapshot before finishing, and inspect proposed changes before applying or discarding them.

Risk: The security evidence identifies a data-loss risk if the finish action is mistyped or invoked through automation.

Mitigation: Avoid automated finish calls unless action validation is fixed, and manually confirm whether the intended action is apply or discard before running the finish script.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/graceqx/skills/trouble-shooting)

## Skill Output:

**Output Type(s):** [guidance, shell commands, JSON, files]

**Output Format:** [Markdown guidance with optional JSON script output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create troubleshooting state files and temporary Git worktrees during use.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
