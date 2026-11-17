## Description:

Monitor async tasks by polling their state and sending Discord, Telegram, session, or file notifications when status changes or completion events occur.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lanyasheng](https://clawhub.ai/user/lanyasheng)

### License/Terms of Use:

MIT

## Use Case:

Developers and agent operators use this skill to register long-running workflow tasks, poll state through adapters, and notify the right channel when task state changes or reaches a terminal status.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Under-scoped local paths and task IDs can cause unintended file reads, deletes, or writes.

Mitigation: Allow only trusted agents to write task records, validate task IDs and packet/status/notification paths, and confine those paths to intended directories before enabling the watcher.

Risk: A scheduled watcher can repeatedly process unsafe or malformed shared task records.

Mitigation: Run the watcher with a low-privilege account and defer cron setup until task record sources and notification paths have been reviewed.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/lanyasheng/skills/task-watcher)
- [README.md](artifact/README.md)
- [SKILL.md](artifact/SKILL.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, JSON]

**Output Format:** [Markdown guidance with Python and shell command snippets; JSON task, audit, and notification records when helper scripts are run.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses local JSONL task storage, audit logs, and notification files for watcher state and delivery tracking.]

## Skill Version(s):

1.2.1 (source: server release evidence; artifact SKILL.md and _meta.json list 1.2.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
