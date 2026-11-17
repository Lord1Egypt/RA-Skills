## Description:

Manage ClickUp tasks by listing, creating, updating statuses, and retrieving details through the ClickUp API with a configured workspace and API token.

This skill is ready for commercial/non-commercial use.

## Publisher:

[savelieve](https://clawhub.ai/user/savelieve)

### License/Terms of Use:

MIT

## Use Case:

External users and developers use this skill to let an agent read ClickUp tasks, create tasks, update task status, retrieve task details, and search a ClickUp workspace with a configured token.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can use a configured ClickUp token to read and change task data.

Mitigation: Install only when agent access to ClickUp is intended and scope the token to the minimum workspace access needed.

Risk: Incorrect list IDs, task IDs, or status values could create or update the wrong ClickUp records.

Mitigation: Verify identifiers and requested status changes before allowing create or update actions.

Risk: CLICKUP_API_TOKEN is a secret that could expose workspace data if mishandled.

Mitigation: Store the token in environment variables or managed secret storage rather than in shared files or prompts.

## Reference(s):

- [ClickUp API v2](https://api.clickup.com/api/v2)

## Skill Output:

**Output Type(s):** [Text, JSON, Guidance]

**Output Format:** [Text summaries with JSON task data]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May perform ClickUp read and write actions when supplied valid credentials.]

## Skill Version(s):

1.0.2 (source: ClawHub release metadata; artifact frontmatter and package.json report 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
