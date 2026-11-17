## Description:

Interact with a Vikunja task management instance via its REST API to manage tasks, projects, labels, assignees, reminders, and task relationships.

This skill is ready for commercial/non-commercial use.

## Publisher:

[seergs](https://clawhub.ai/user/seergs)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and Vikunja users use this skill to let an agent manage projects, tasks, labels, assignees, reminders, and task relationships through a configured Vikunja REST API token.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The configured Vikunja API token can read and modify task-management data available to that token.

Mitigation: Use a token scoped as narrowly as Vikunja allows and install the skill only for agents that should operate on the target Vikunja instance.

Risk: The skill can delete tasks, remove labels or assignees, and change task relationships.

Mitigation: Confirm destructive or removal actions with the user before making the corresponding API request.

Risk: Paginated API responses can omit additional results if only the first page is used.

Mitigation: Follow pagination headers to fetch subsequent pages or clearly tell the user when results are truncated.

## Reference(s):

- [Vikunja API Endpoint Reference](references/endpoints.md)
- [Project homepage](https://github.com/seergs/vikunja-skill)
- [ClawHub skill page](https://clawhub.ai/seergs/skills/vikunja-api)

## Skill Output:

**Output Type(s):** [Text, Markdown, API Calls, Configuration Guidance]

**Output Format:** [Markdown text with REST API request guidance and structured task summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires VIKUNJA_BASE_URL and VIKUNJA_API_TOKEN.]

## Skill Version(s):

1.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
