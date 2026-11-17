## Description:

Durable queue-task helper for resumable, idempotent batch jobs in task-father task folders.

This skill is ready for commercial/non-commercial use.

## Publisher:

[moodykong](https://clawhub.ai/user/moodykong)

### License/Terms of Use:


## Use Case:

Developers and operators use Queue Task to set up and inspect durable task-folder queues for long-running, resumable batch jobs. It helps create queue state files, track progress, manage stale locks, and produce a worker template for batch execution.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Task slugs can escape the intended task folder and create or modify files elsewhere writable by the agent.

Mitigation: Use only simple slugs made from letters, numbers, underscores, or hyphens, and reject absolute paths, path separators, dot components, and resolved paths outside the configured task root.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/moodykong/skills/queue-task)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and JSON status output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Creates and updates task-folder state files such as queue.jsonl, progress.json, done.jsonl, failed.jsonl, and lock.json.]

## Skill Version(s):

0.1.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
