## Description:

Automatic interrupted-task resume workflow with queueing and recovery. Use when a user asks to resume interrupted work after temporary context switches, protect priority tasks from drift, or enforce "finish current task then auto-resume previous interrupted task" behavior.

This skill is ready for commercial/non-commercial use.

## Publisher:

[richardsun700](https://clawhub.ai/user/richardsun700)

### License/Terms of Use:


## Use Case:

External users and developers use this skill to help OpenClaw agents preserve interrupted task state, resume queued work in FIFO order, and inspect or recover queue status across sessions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can store task context across sessions, which may capture secrets, private logs, regulated data, or other sensitive information.

Mitigation: Use opt-in activation, avoid sensitive content in queued context, and review queued context before storage or replay.

Risk: Automatic resume and watchdog behavior may continue work without current user confirmation.

Mitigation: Require confirmation before enqueueing or resuming work, and add expiry and revocation controls for any watchdog job.

Risk: Session-log recovery can replay stale or untrusted context if logs are not restricted to trusted sources.

Mitigation: Restrict recovery to trusted session logs and verify the next step and acceptance criteria before resuming.

## Reference(s):

- [Task Resume README](README.md)
- [ClawHub Skill Page](https://clawhub.ai/richardsun700/skills/task-resume)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with inline bash commands and JSON command output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces queue-management commands and structured statuses for add, pop, list, status, clear, and recover flows.]

## Skill Version(s):

1.3.0 (source: server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
