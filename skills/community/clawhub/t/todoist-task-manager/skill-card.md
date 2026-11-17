## Description:

Manage Todoist tasks via the `todoist` CLI, including listing, adding, modifying, completing, and deleting tasks with filters, projects, labels, and priorities.

This skill is ready for commercial/non-commercial use.

## Publisher:

[2mawi2](https://clawhub.ai/user/2mawi2)

### License/Terms of Use:


## Use Case:

Developers and Todoist users use this skill to manage Todoist tasks from an agent-assisted terminal workflow. It helps list, create, update, complete, delete, sync, and inspect tasks while applying Todoist filters, projects, labels, priorities, and output options.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Todoist API token exposure could allow access to the user's Todoist account.

Mitigation: Store the token like a password, restrict permissions on ~/.config/todoist/config.json, and avoid committing or sharing it.

Risk: Complete or delete commands can change or remove Todoist tasks.

Mitigation: Preview task IDs and confirm the intended targets before running complete or delete commands.

## Reference(s):

- [Todoist developer token settings](https://app.todoist.com/app/settings/integrations/developer)
- [Todoist filter syntax](https://todoist.com/help/articles/introduction-to-filters-V98wIH)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration]

**Output Format:** [Markdown with inline bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include Todoist CLI commands that read, create, modify, complete, delete, sync, or export tasks.]

## Skill Version(s):

1.0.0 (source: release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
