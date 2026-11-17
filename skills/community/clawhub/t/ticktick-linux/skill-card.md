## Description:

Manage TickTick tasks (add, list, complete) via the local `tickrs` CLI.

This skill is ready for commercial/non-commercial use.

## Publisher:

[davidsmorais](https://clawhub.ai/user/davidsmorais)

### License/Terms of Use:


## Use Case:

External users and developers use this skill to list TickTick tasks, create tasks, complete tasks by ID, and list projects through an authenticated local tickrs CLI.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: User-provided task fields in command templates may expose shell injection risk.

Mitigation: Use only in controlled environments with trusted task input, or change commands to use shell-free argument arrays with robust escaping and validation.

Risk: Creating or completing tasks modifies TickTick task data using configured credentials.

Mitigation: Authenticate only with the intended TickTick account and review task IDs and task content before executing create or complete actions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/davidsmorais/skills/ticktick-linux)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration instructions, API Calls]

**Output Format:** [Markdown guidance with inline shell commands and JSON CLI output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires local tickrs authentication and TickTick API credentials.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
