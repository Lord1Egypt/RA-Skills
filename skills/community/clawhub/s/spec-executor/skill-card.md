## Description:

Execution companion for spec-workflow: state navigation, task tracking via tasks.md, incremental delivery, and session recovery.

This skill is ready for commercial/non-commercial use.

## Publisher:

[naozixu](https://clawhub.ai/user/naozixu)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill after spec-workflow has produced a plan to execute planned implementation tasks, keep tasks.md current, verify progress, and recover safely after interruptions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can direct an agent to modify project code and update task state.

Mitigation: Use it only with a reviewed spec-workflow tasks.md file, and require the agent to show diffs before commit approval.

Risk: Malformed or stale tasks.md state can cause the agent to resume from the wrong task.

Mitigation: Validate tasks.md structure before execution and reconcile discrepancies with the user before continuing.

Risk: Continuous mode may allow multiple planned tasks to be completed in one session.

Mitigation: Enable continuous mode only with explicit user authorization and verify each task independently before moving to the next one.

## Reference(s):


## Skill Output:

**Output Type(s):** [guidance, markdown, code, shell commands, configuration]

**Output Format:** [Markdown guidance with inline commands and repository edits]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Updates tasks.md and may stage or commit repository changes only after review and explicit authorization.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
