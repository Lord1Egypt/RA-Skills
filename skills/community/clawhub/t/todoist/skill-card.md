## Description:

Manage tasks and projects in Todoist. Use when user asks about tasks, to-dos, reminders, or productivity.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mjrussell](https://clawhub.ai/user/mjrussell)

### License/Terms of Use:


## Use Case:

External users and agents use this skill to inspect, create, update, search, and complete Todoist tasks, projects, labels, and comments through the Todoist CLI.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requires CLI access to a Todoist account through TODOIST_API_TOKEN.

Mitigation: Use a token only in trusted environments, avoid placing it directly in shell history, and rotate or revoke it if exposure is suspected.

Risk: The installation instructions use a global npm package with a semver range.

Mitigation: Prefer a pinned, reviewed CLI version and avoid running npm install with elevated privileges.

Risk: Commands can complete, move, reopen, or delete Todoist tasks.

Mitigation: Verify task IDs and command intent before running state-changing actions.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/mjrussell/skills/todoist)
- [Todoist](https://todoist.com)
- [Todoist API Token Settings](https://todoist.com/app/settings/integrations/developer)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with Todoist CLI command examples and short task-management guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires the todoist CLI and a Todoist API token.]

## Skill Version(s):

0.2.1 (source: server-resolved release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
