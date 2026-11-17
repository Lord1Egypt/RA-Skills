## Description:

Manage tasks, projects, and notes in tududi (self-hosted task manager). Use for todo lists, task management, project organization.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chrisvel](https://clawhub.ai/user/chrisvel)

### License/Terms of Use:


## Use Case:

Developers and agents use this skill to manage a trusted tududi instance through documented API calls for tasks, projects, inbox items, tags, and task filters.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A misconfigured base URL or overly broad API token could cause the agent to access or modify the wrong tududi instance.

Mitigation: Configure TUDUDI_URL only for a trusted instance and use an API token with the least access needed.

Risk: The documented DELETE operations can remove tasks or inbox items when given an incorrect UID.

Mitigation: Review destructive commands and confirm the target UID before execution.

## Reference(s):


## Skill Output:

**Output Type(s):** [Shell commands, API Calls, Configuration instructions, Guidance]

**Output Format:** [Markdown with inline bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires TUDUDI_URL and TUDUDI_API_TOKEN to be configured for the target tududi instance.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
