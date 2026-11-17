## Description:

Workspace-local task management powered by Taskwarrior for adding, organizing, and tracking tasks by project, tags, due dates, and priority with all data stored inside the active workspace.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aghareza](https://clawhub.ai/user/aghareza)

### License/Terms of Use:


## Use Case:

Developers and agents use this skill to manage workspace-scoped Taskwarrior tasks without writing to global Taskwarrior configuration by default. It supports common task workflows including add, list, modify, complete, annotate, project, tag, due-date, and priority operations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Taskwarrior may be unavailable in the runtime environment.

Mitigation: Validate availability with task --version and ask the environment owner to install Taskwarrior in the runtime image if it is missing.

Risk: The skill creates and updates Taskwarrior files inside .openclaw/taskwarrior in the active workspace.

Mitigation: Keep TASKRC and TASKDATA scoped to the workspace-local Taskwarrior directory and show focused verification output after mutations.

Risk: Deletes, purges, global Taskwarrior storage, or broad bulk changes can modify more task data than intended.

Mitigation: Require explicit user wording for destructive, global, or bulk operations and preview matching tasks before broad changes.

## Reference(s):

- [ClawHub taskwarrior skill page](https://clawhub.ai/aghareza/skills/taskwarrior)
- [Workspace data layout](references/workspace_data_layout.md)
- [Taskwarrior cheatsheet](references/taskwarrior_cheatsheet.md)
- [Safe command policy](references/safe_command_policy.md)
- [Examples](references/examples.md)
- [ClawHub notes](references/clawhub_notes.md)
- [Taskwarrior availability](references/install.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown text with inline shell commands and focused Taskwarrior verification output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or update Taskwarrior state under .openclaw/taskwarrior in the active workspace.]

## Skill Version(s):

0.1.3 (source: evidence.release.version)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
