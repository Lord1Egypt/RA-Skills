## Description:

Manage simple todos with add, list, complete, and remove features using a configurable markdown todo file, priority, and auto-archive settings.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zoran-xc](https://clawhub.ai/user/zoran-xc)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw users use this skill to capture, list, complete, remove, and archive lightweight personal or workspace tasks without setting up a database or external service.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill edits a local todo file and may remove completed tasks when auto-archive is enabled.

Mitigation: Set todo_file to a path the agent may edit and set auto_archive_days to 0 unless automatic removal of old completed tasks is intended.

Risk: Ambiguous matching or corrupted todo-file recovery can create data-loss edge cases.

Mitigation: Require confirmation before deletion, ask for clarification when multiple tasks match, and confirm before archive or corrupted-file recovery actions.

## Reference(s):

- [Simple Todo Manager Skill Page](https://clawhub.ai/zoran-xc/skills/simple-todo-manager)
- [README.md](artifact/README.md)
- [SKILL.md](artifact/SKILL.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Configuration, Guidance]

**Output Format:** [Markdown task lists and concise chat responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses a configurable local todo file, priorities, timestamps, and optional auto-archiving.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
