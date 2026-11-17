## Description:

Coordinates parallel multi-agent coding sprints with git worktree isolation, mandatory conflict planning, and coordinator-reviewed merges.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jdh3](https://clawhub.ai/user/jdh3)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineering teams use this skill to split two or more coding tasks into isolated worktrees, plan conflicts before agents run, review diffs, merge accepted work, and clean up sprint resources.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Cleanup has under-scoped destructive behavior and command-execution risks from task metadata.

Mitigation: Use only trusted task files and cleanup package files, and review cleanup inputs before execution.

Risk: Malformed metadata could delete local directories or execute unintended shell commands.

Mitigation: Validate task IDs and cleanup package paths before running cleanup.

Risk: The cleanup flow includes shell execution and a destructive removal fallback.

Mitigation: Prefer safer versions that avoid bash -c, remove the rm -rf fallback, and keep logs in a clearly repo-local location.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jdh3/skills/swarm-sprint)
- [example-tasks.json](references/example-tasks.json)
- [test-tasks.json](references/test-tasks.json)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JSON task definitions and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces task-package configuration for subagents and cleanup guidance for sprint resources.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
