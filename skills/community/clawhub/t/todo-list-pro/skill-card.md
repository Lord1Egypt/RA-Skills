## Description:

Track local todo or work-report items in a SQLite database, including planned work, progress amounts, completion status, deletion, and archiving.

This skill is ready for commercial/non-commercial use.

## Publisher:

[seanmwx](https://clawhub.ai/user/seanmwx)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to persist local work items, update progress, list current tasks, summarize completion, archive history, and permanently delete tasks only after explicit confirmation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill creates and maintains local todo data in a SQLite database.

Mitigation: Use the disclosed default path unless a custom or test database path is intentionally configured.

Risk: Permanent deletion removes todo rows from the local database.

Mitigation: Use deletion only after explicit confirmation; use archiving when historical retention is intended.

## Reference(s):

- [Command Reference](references/commands.md)
- [Natural-Language Reference](references/chat_reference.md)
- [Storage Model](references/storage.md)
- [ClawHub Skill Page](https://clawhub.ai/seanmwx/skills/todo-list-pro)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and JSON-oriented CLI usage]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The skill stores task state in a local SQLite database and prefers JSON output when command results will be reused.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
