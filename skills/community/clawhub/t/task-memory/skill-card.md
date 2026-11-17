## Description:

Task Memory helps agents persistently register, check, update, complete, archive, and purge long-running tasks in todo.json so commitments are not lost between sessions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[huyaohuahk](https://clawhub.ai/user/huyaohuahk)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use Task Memory to make an agent record promised or delegated tasks, check overdue and upcoming items at session start or heartbeat time, and mark work done or removed.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The task manager reads and writes a hard-coded todo file outside the skill directory.

Mitigation: Fix or configure the storage path before running the skill so it only accesses the intended workspace todo file.

Risk: Task titles, notes, and deadlines may contain sensitive information stored on disk.

Mitigation: Review what task text is stored and avoid recording secrets or sensitive personal data in todo entries.

Risk: External QQ/IM reminder forwarding is under-scoped.

Mitigation: Do not enable external reminder forwarding without explicit destination controls and redaction for sensitive task text.

## Reference(s):

- [CHANGELOG](references/CHANGELOG.md)
- [Todo JSON template](references/todo.json)
- [ClawHub skill page](https://clawhub.ai/huyaohuahk/skills/task-memory)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and JSON-backed task records]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Stores task titles, notes, deadlines, tags, status, and archive entries in a todo JSON file.]

## Skill Version(s):

1.2.0 (source: server release evidence and changelog, released 2026-04-01)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
