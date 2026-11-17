## Description:

Access and manage Shortcut.com project-management stories, epics, workflows, comments, and dependency links through the Shortcut REST API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[incognos](https://clawhub.ai/user/incognos)

### License/Terms of Use:


## Use Case:

Developers and project teams use this skill to inspect Shortcut backlog data and create or update stories, epics, comments, workflow state, and dependency links from an agent session.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can make real Shortcut project-management changes using a full member-level token.

Mitigation: Require the agent to show an exact preview before creating or changing stories, epics, comments, workflow state, or dependency links.

Risk: Shortcut API tokens have broad member-level access and may be persisted on disk by the skill setup flow.

Mitigation: Prefer a temporary session environment variable when possible, keep any saved token file permission-restricted, and rotate the token if logs or process telemetry may have captured it.

Risk: Workflow state IDs vary by Shortcut workspace, so using assumed IDs can update stories incorrectly.

Mitigation: Fetch and verify workspace workflow states before applying story state changes.

## Reference(s):

- [Shortcut REST API v3](https://developer.shortcut.com/api/rest/v3)
- [Bulk Epic + Story Creation](references/create-stories.md)
- [ClawHub skill page](https://clawhub.ai/incognos/skills/shortcut-skill)

## Skill Output:

**Output Type(s):** [Markdown, Shell commands, API Calls, Configuration, Guidance]

**Output Format:** [Markdown with inline bash and jq command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs may include Shortcut story, epic, workflow, comment, and dependency data returned as JSON or summarized tables.]

## Skill Version(s):

1.0.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
