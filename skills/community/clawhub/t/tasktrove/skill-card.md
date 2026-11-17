## Description:

Manage todos via Tasktrove API. Use for listing, creating, completing, or updating tasks. Triggers on task/todo requests like "what's on my todo list", "add a task", "mark X done", "what's due today".

This skill is ready for commercial/non-commercial use.

## Publisher:

[willwebberley](https://clawhub.ai/user/willwebberley)

### License/Terms of Use:


## Use Case:

External users and developers use this skill to manage tasks in a self-hosted Tasktrove instance, including listing, creating, completing, searching, and updating todos through the Tasktrove API.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can use TASKTROVE_TOKEN with a TASKTROVE_HOST configured over plain HTTP, which may expose the token on an untrusted network.

Mitigation: Use HTTPS-only TASKTROVE_HOST values for remote instances and avoid sending tokens over plain HTTP.

Risk: The artifact documents task deletion through the Tasktrove API, which can remove user task data.

Mitigation: Require explicit user confirmation before any delete request.

## Reference(s):

- [Tasktrove](https://tasktrove.io)
- [Tasktrove GitHub repository](https://github.com/dohsimpson/tasktrove)
- [Tasktrove ClawHub skill page](https://clawhub.ai/willwebberley/skills/tasktrove)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown with inline bash, curl, and Python command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce API request examples and task-management command guidance.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
