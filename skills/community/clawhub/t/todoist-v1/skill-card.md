## Description:

Manage Todoist tasks -- list, create, complete, update, and organize tasks and projects.

This skill is ready for commercial/non-commercial use.

## Publisher:

[fluidiguana](https://clawhub.ai/user/fluidiguana)

### License/Terms of Use:


## Use Case:

Developers and external users use this skill as a Todoist API v1 reference for managing tasks, projects, and sections through authenticated curl commands.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill uses a user-provided Todoist personal API token, which can allow the agent to access or change Todoist data.

Mitigation: Install only when the agent should use that Todoist token, keep the token in the TODOIST_TOKEN environment variable, and review intended access before use.

Risk: Mutating commands can create, update, complete, or delete Todoist items.

Mitigation: Review mutating commands before execution, especially deletion, and prefer completing tasks unless deletion is clearly intended.

## Reference(s):

- [Todoist API v1 endpoint](https://api.todoist.com/api/v1/)
- [Todoist developer token settings](https://app.todoist.com/app/settings/integrations/developer)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [References Todoist API responses that are returned as JSON by the service.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
