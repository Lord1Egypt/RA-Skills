## Description:

Qclaw Workbuddy Bridge connects QClaw or WeChat-originated requests to WorkBuddy execution through a local JSON task queue.

This skill is ready for commercial/non-commercial use.

## Publisher:

[liuboacean](https://clawhub.ai/user/liuboacean)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to configure QClaw to enqueue remote tasks and WorkBuddy to pick up, execute, and report results through a shared local queue.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad QClaw or WeChat requests can be forwarded into autonomous WorkBuddy execution through the shared queue.

Mitigation: Narrow dispatch triggers and require explicit confirmation before file access or other side-effecting work.

Risk: The persistent local queue can contain sensitive personal, business, or task context data.

Mitigation: Avoid placing secrets or sensitive data in the queue and enforce owner-only permissions on queue files.

Risk: A shared JSON queue has weak coordination controls for concurrent readers and writers.

Mitigation: Add file locking or replace the JSON queue with SQLite for stronger consistency.

Risk: WorkBuddy may execute queued tasks with more local access than intended.

Mitigation: Run WorkBuddy in a sandboxed, low-privilege environment.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/liuboacean/skills/qclaw-workbuddy-bridge)
- [Skill Definition](artifact/SKILL.md)
- [Queue Manager Script](artifact/scripts/qclaw_queue.py)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, JSON, guidance]

**Output Format:** [Markdown guidance with shell commands and JSON task records]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces local queue operations for adding, polling, completing, failing, and reading tasks.]

## Skill Version(s):

1.2.0 (source: server release evidence and target metadata; artifact frontmatter says 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
