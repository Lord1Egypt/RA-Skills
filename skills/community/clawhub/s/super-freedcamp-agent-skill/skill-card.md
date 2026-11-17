## Description:

This skill lets an agent use the Freedcamp REST API to discover projects, list and update tasks, create tasks, add comments, inspect task lists, and manage notification read state through a Node.js CLI.

This skill is ready for commercial/non-commercial use.

## Publisher:

[subaru0573](https://clawhub.ai/user/subaru0573)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, operations teams, and project collaborators can use this skill to automate Freedcamp task tracking workflows, including project discovery, task creation, status updates, comments, task lists, and notifications.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can create or modify Freedcamp tasks, comments, and notification state in a live workspace.

Mitigation: Install it only for workspaces where those write actions are acceptable, and test write paths on throwaway tasks before broader use.

Risk: Reusable Freedcamp session credentials are cached locally.

Mitigation: Treat the session cache as sensitive, restrict file access to the local user, set FREEDCAMP_SESSION_PATH to a controlled location when needed, and remove cached credentials when access is no longer required.

Risk: The demo script can load credentials from a shared .env file.

Mitigation: Avoid running the demo in shared workspaces and prefer runtime credential injection or scoped OpenClaw configuration for API keys and secrets.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/subaru0573/skills/super-freedcamp-agent-skill)
- [Freedcamp](https://freedcamp.com)
- [Freedcamp API v1](https://freedcamp.com/api/v1)
- [Freedcamp API credentials](https://freedcamp.com/manage/account#integrations-api)
- [Reference and implementation notes](references/REFERENCE.md)

## Skill Output:

**Output Type(s):** [JSON, Shell commands, Configuration instructions]

**Output Format:** [JSON API responses and Markdown instructions with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires FREEDCAMP_API_KEY and FREEDCAMP_API_SECRET; write operations can modify live Freedcamp tasks, comments, and notification state.]

## Skill Version(s):

1.0.0 (source: server release evidence and _meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
