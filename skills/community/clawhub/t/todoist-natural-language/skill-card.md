## Description:

Integrate with Todoist task management using natural language for listing, creating, updating, completing, and organizing tasks and projects.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hail2skins](https://clawhub.ai/user/hail2skins)

### License/Terms of Use:

MIT

## Use Case:

OpenClaw users use this skill to manage Todoist tasks and projects through conversational requests or direct CLI commands. It is useful for checking task lists, adding tasks with natural-language due dates, completing tasks, and reviewing projects from an agent workflow.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can make live changes to a user's Todoist account, including creating, updating, completing, reopening, and deleting tasks.

Mitigation: Confirm destructive or ambiguous requests before execution and use the skill only when the user accepts account-changing Todoist API access.

Risk: The skill requires a sensitive Todoist API token.

Mitigation: Provide TODOIST_API_KEY only through a protected environment variable and avoid exposing it in prompts, logs, or shared command output.

Risk: Date-based filters can produce incorrect results if timezone configuration is wrong.

Mitigation: Set TZ explicitly when accurate today, tomorrow, or overdue filtering matters.

Risk: The release evidence notes broader-than-needed install guidance in the README.

Mitigation: Install using the user-scoped skill path and avoid sudo global installation commands.

## Reference(s):

- [Todoist API v1 Reference](artifact/references/api.md)
- [Todoist REST API v1 documentation](https://developer.todoist.com/api/v1/)
- [Todoist Sync API documentation](https://developer.todoist.com/sync/v9/)
- [Todoist developer integrations settings](https://todoist.com/app/settings/integrations/developer)

## Skill Output:

**Output Type(s):** [text, JSON, shell commands, configuration, guidance]

**Output Format:** [Natural-language agent guidance with CLI commands that return JSON task and project data.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires TODOIST_API_KEY; optional TZ controls timezone-sensitive date filtering.]

## Skill Version(s):

1.0.8 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
