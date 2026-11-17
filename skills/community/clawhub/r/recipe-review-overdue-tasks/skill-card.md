## Description:

Find Google Tasks that are past due and need attention.

This skill is ready for commercial/non-commercial use.

## Publisher:

[googleworkspace-bot](https://clawhub.ai/user/googleworkspace-bot)

### License/Terms of Use:

MIT-0

## Use Case:

Users with a configured Google Workspace CLI use this recipe to have an agent list task lists, inspect incomplete Google Tasks, and identify overdue items that need attention.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The agent can list task lists and incomplete Google Tasks from the configured Google Workspace account, which may expose task titles, due dates, or other sensitive task details.

Mitigation: Use only with the intended Google Workspace account and avoid sharing task output outside the authorized workflow.

Risk: The recipe reviews overdue tasks but does not modify or delete them, so follow-up action remains manual or must be handled by a separate approved workflow.

Mitigation: Confirm any prioritization or remediation step before using another tool or skill to change task state.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/googleworkspace-bot/skills/recipe-review-overdue-tasks)
- [Publisher Profile](https://clawhub.ai/user/googleworkspace-bot)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown or concise text summarizing overdue Google Tasks and relevant Google Workspace CLI output.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read-only task review; requires gws and the gws-tasks skill.]

## Skill Version(s):

1.0.12 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
