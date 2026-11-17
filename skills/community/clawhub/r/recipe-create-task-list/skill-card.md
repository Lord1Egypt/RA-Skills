## Description:

Set up a new Google Tasks list with initial tasks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[googleworkspace-bot](https://clawhub.ai/user/googleworkspace-bot)

### License/Terms of Use:

MIT-0

## Use Case:

Employees and Google Workspace users use this skill to create a Google Tasks list, add initial tasks, and review the resulting list.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The recipe can create tasks in the wrong Google account or with unintended titles, notes, or due dates if run without review.

Mitigation: Confirm gws is authenticated to the intended Google account and review the task list title, task titles, notes, and due date before execution.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/googleworkspace-bot/skills/recipe-create-task-list)
- [Publisher profile](https://clawhub.ai/user/googleworkspace-bot)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses the gws command-line tool and requires the gws-tasks skill.]

## Skill Version(s):

1.0.12 (source: server release metadata); skill metadata version 0.22.5 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
