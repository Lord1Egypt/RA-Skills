## Description:

Manage todo.txt tasks using topydo CLI. Add, list, complete, prioritize, tag, and organize tasks with dependencies, due dates, recurrence, and projects. Use for any task management, todo lists, or when the user mentions tasks, todos, or todo.txt. Requires Python 3 and pip. Works on macOS, Linux, and Windows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bastos](https://clawhub.ai/user/bastos)

### License/Terms of Use:

MIT

## Use Case:

Developers, operators, and individual users use this skill to ask an agent for topydo commands and todo.txt task-management guidance, including adding, listing, completing, prioritizing, tagging, editing, deleting, and organizing tasks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Installing topydo from an untrusted package source can introduce supply-chain risk.

Mitigation: Install topydo from a trusted package source and prefer an isolated Python environment when using pip.

Risk: Bulk edit, completion, deletion, archive, and sort commands can mutate todo.txt task files in ways the user did not intend.

Mitigation: Preview the affected tasks and back up todo.txt before bulk edits or deletions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/bastos/skills/topydo)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include commands that mutate todo.txt task files; users should review commands before execution.]

## Skill Version(s):

1.0.5 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
