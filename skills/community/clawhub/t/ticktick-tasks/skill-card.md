## Description:

TickTick task manager integration for listing projects and tasks, creating tasks, completing tasks, deleting tasks, and supporting reminder-oriented task management after OAuth setup via `ticktick-setup`.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kaiofreitas](https://clawhub.ai/user/kaiofreitas)

### License/Terms of Use:


## Use Case:

External users and developers use this skill to manage TickTick projects and tasks from an agent workflow, including listing, creating, completing, and deleting tasks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: OAuth client secrets may be exposed when passed directly on the command line during setup.

Mitigation: Use a secure prompt, restricted configuration file, or credential store when available, and avoid storing real client secrets in shell history.

Risk: Task deletion can remove TickTick tasks when project or task IDs are wrong.

Mitigation: Verify the target project and task IDs before running delete commands, and prefer listing the project data immediately before deletion.

## Reference(s):

- [TickTick Developer Portal](https://developer.ticktick.com)
- [TickTick Open API Base URL](https://api.ticktick.com/open/v1)

## Skill Output:

**Output Type(s):** [Shell commands, Guidance, Configuration]

**Output Format:** [Markdown with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires OAuth setup before task operations; commands may create, complete, or delete TickTick tasks.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
