## Description:

Records, updates, deletes, and summarizes daily work items in a local SQLite work log, including entry-level and day-level history.

This skill is ready for commercial/non-commercial use.

## Publisher:

[seanmwx](https://clawhub.ai/user/seanmwx)

### License/Terms of Use:

MIT-0

## Use Case:

Codex users use this skill to keep a local, queryable record of daily work and generate daily or weekly progress summaries. It also supports correcting work logs, deleting mistaken entries, and inspecting edit history.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Replacing a day, clearing a day, updating an entry, or deleting an entry changes the current local work-log database.

Mitigation: Confirm the exact date or entry id before executing mutating actions, and use day or entry history commands when the user needs to review changes.

Risk: The local SQLite work log may contain sensitive work details entered by the user.

Mitigation: Keep the database in the intended local path or an explicit user-provided path, avoid recording secrets, and use separate database names or paths when isolation is needed.

## Reference(s):

- [Commands Reference](references/commands.md)
- [Chat Reference](references/chat_reference.md)
- [Chinese Output Templates](references/chinese_output.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown summaries and shell commands based on JSON command output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses explicit dates and local SQLite database paths when recording, changing, or reporting work logs.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
