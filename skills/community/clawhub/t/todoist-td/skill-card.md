## Description:

Use the td (Todoist CLI) to read and manage Todoist todos/to-dos/tasks from the terminal.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mattjefferson](https://clawhub.ai/user/mattjefferson)

### License/Terms of Use:


## Use Case:

External users and developers use this skill to let an agent inspect Todoist agendas, list tasks and projects, add new tasks, and update or complete existing tasks through the td CLI.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad agenda, checklist, and task triggers can cause the agent to access or change Todoist data when the user intended a non-Todoist workflow.

Mitigation: Confirm that generic task or agenda requests are meant for Todoist before allowing reads or edits.

Risk: The install instructions build todoist-cli from an unpinned GitHub checkout, which can change over time.

Mitigation: Prefer a reviewed, pinned todoist-cli release when installing the dependency.

Risk: Todoist task updates and deletes can change user data.

Mitigation: Ask for clarification when multiple tasks match and confirm before destructive delete actions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/mattjefferson/skills/todoist-td)
- [Todoist CLI repository](https://github.com/Doist/todoist-cli)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline shell commands and JSON-oriented CLI output guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses parseable td CLI output such as JSON or NDJSON when listing or reading tasks.]

## Skill Version(s):

0.1.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
