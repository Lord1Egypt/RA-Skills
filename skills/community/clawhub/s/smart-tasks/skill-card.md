## Description:

Intelligent task management using workspace Markdown files for natural language CRUD, context-aware reminders, priority briefings, and weekly reviews.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dgkim311](https://clawhub.ai/user/dgkim311)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use Smart Tasks to let an agent create, update, complete, and query personal workspace tasks stored in Markdown. It is intended for personal task tracking, priority briefings, deadline reminders, and weekly reviews rather than calendar scheduling or multi-collaborator project management.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill writes and moves workspace task files that may contain private task context.

Mitigation: Install only where workspace-level task tracking is intended, and review task contents and storage before use.

Risk: Optional cron reminders may send task or memory context through a configured messaging channel.

Mitigation: Review schedules, channels, and reminder prompts before enabling cron jobs, especially when task files or memory entries contain sensitive information.

Risk: Optional workspace integration diffs modify agent operating instructions for task awareness.

Mitigation: Apply workspace integration changes only after user review and approval.

## Reference(s):

- [Smart Tasks Skill](https://clawhub.ai/dgkim311/skills/smart-tasks)
- [File Structure Reference](references/file-structure.md)
- [Task File Format Reference](references/task-format.md)
- [Context Window Management Strategy](references/context-strategy.md)
- [Cron Job Templates](references/cron-templates.md)
- [Workspace Integration Guide](references/workspace-integration.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown files and concise chat guidance, with optional shell command snippets.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes and moves files under tasks/; optional workspace integration changes and cron reminders require user approval.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
