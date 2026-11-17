## Description:

Structured Task Planning V2 helps agents decompose work into confirmed steps, run each step asynchronously through isolated subagents, verify results, track state, monitor heartbeat checks, and interrupt tasks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[scotthuang](https://clawhub.ai/user/scotthuang)

### License/Terms of Use:


## Use Case:

Developers and agent users use this skill to turn complex requests into step-by-step task plans, execute those steps asynchronously, and keep the main session responsive while progress is tracked and verified.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Automatic cron heartbeat jobs, subagent orchestration, local session-history reads, and task-state file writes can affect shared or important workspaces.

Mitigation: Review the skill before installation, use it only in workspaces where those behaviors are acceptable, and monitor created task directories and cron entries.

Risk: Cancellation and cleanup paths can affect cron jobs, local task directories, session history, and potentially unrelated processes.

Mitigation: Avoid relying on the interruption flow until process killing is narrowed to verified child processes and task IDs are validated.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/scotthuang/skills/stp)
- [STP skill changelog](artifact/CHANGELOG.md)
- [Main session guide](artifact/scripts/MAIN_SESSION_GUIDE.md)

## Skill Output:

**Output Type(s):** [markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown instructions with inline shell commands and task-state files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces task plans, status updates, verification prompts, and cleanup records for asynchronous task execution.]

## Skill Version(s):

1.0.7 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
