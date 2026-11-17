## Description:

Generator for file-based task state machines (registry + task folders + lifecycle state + queue files + cron specs/jobs) for long-running work.

This skill is ready for commercial/non-commercial use.

## Publisher:

[moodykong](https://clawhub.ai/user/moodykong)

### License/Terms of Use:


## Use Case:

Developers and agents use this skill to create and manage durable OpenClaw task workspaces with registry entries, lifecycle state, task documentation, optional queues, and optional cron scheduling.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Cron helper commands can create persistent scheduled OpenClaw jobs.

Mitigation: Run cron-add or cron-rm only when persistent scheduling is intended, and review the cron expression, message, agent, timezone, and job name before execution.

Risk: Unsafe cron names can overwrite or delete writable JSON files outside the intended task crons directory.

Mitigation: Use filesystem-safe cron names tied to the task slug and review generated cron spec paths until the helper validates names and confines cron spec files.

Risk: Machine-specific configuration can target the wrong workspace or timezone.

Mitigation: Set WORKSPACE_DIR and DEFAULT_CRON_TZ for the local machine before running lifecycle or cron commands.

## Reference(s):

- [Task Father ClawHub page](https://clawhub.ai/moodykong/skills/task-father)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with inline shell commands, file paths, and configuration values]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or update task directories, registry rows, lifecycle JSON, queue files, cron JSON specs, and scheduled OpenClaw cron jobs when the generated commands are run.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
