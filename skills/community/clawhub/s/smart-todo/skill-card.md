## Description:

Smart Todo helps an AI assistant manage todo items with priority labels, status tracking, duplicate detection, context capture, reminders, and automatic archiving.

This skill is ready for commercial/non-commercial use.

## Publisher:

[13770626440](https://clawhub.ai/user/13770626440)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to create, inspect, update, and archive todo items through natural-language interactions. It is especially useful for preserving task state during interruptions, subject to local privacy review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can save conversation excerpts, workspace paths, file names, and memory-derived references in plaintext todo context.

Mitigation: Review the configured storage location, avoid capturing sensitive workspaces, and redact or disable context capture before using it with confidential data.

Risk: The skill instructions describe keeping context even when a user declines creating a todo.

Mitigation: Constrain or edit that behavior before installation so declined todo creation does not silently persist context.

## Reference(s):

- [Todo Template](references/todo_template.md)
- [ClawHub Skill Listing](https://clawhub.ai/13770626440/skills/smart-todo)

## Skill Output:

**Output Type(s):** [text, markdown, files, configuration, guidance]

**Output Format:** [Markdown todo files and conversational text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes active and archived todo records to a local configured storage path.]

## Skill Version(s):

1.0.0 (source: server release metadata and README changelog, released 2026-03-31)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
