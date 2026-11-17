## Description:

Manage follow-up items and remind users during heartbeat checks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[suidge](https://clawhub.ai/user/suidge)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agent operators use this skill to let an agent maintain local follow-up items, ask for missing reminder details, and surface due reminders during heartbeat checks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Reminder text and context are stored in the local memory/todo.json file.

Mitigation: Install only where local todo storage is acceptable, and avoid placing sensitive information in reminder descriptions or context.

Risk: The security summary notes a cleanup bug affecting the expected 24-hour deletion of cancelled items.

Mitigation: Fix or account for the cancelled-item cleanup behavior before relying on the skill for retention-sensitive workflows.

Risk: Heartbeat reminders continue until a pending item is completed or cancelled.

Mitigation: Keep completion and cancellation routing available, and review pending items regularly to prevent stale repeated reminders.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/suidge/skills/suidge-todo-tracker)
- [README](artifact/README.md)
- [Setup Guide](artifact/setup.md)
- [Data Structure](artifact/data-structure.md)
- [Usage Examples](artifact/examples.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JSON file updates and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes and reads local todo state in memory/todo.json; no API credentials or external tools are required by the release metadata.]

## Skill Version(s):

1.3.0 (source: SKILL.md frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
