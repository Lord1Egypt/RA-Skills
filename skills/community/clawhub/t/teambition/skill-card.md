## Description:

Create and query TeamBition tasks across configured applications, projects, and organizations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wengjianmin19850412](https://clawhub.ai/user/wengjianmin19850412)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to integrate TeamBition task management into workflows, creating tasks and retrieving task details with configured app credentials and project defaults.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can create TeamBition business tasks with configured credentials, which may modify workspaces without a clear confirmation or target restriction.

Mitigation: Configure agents so task creation requires clear user intent or confirmation before writing to business workspaces.

Risk: TeamBition app secrets or access tokens provide task read/write access.

Mitigation: Install only if the publisher is trusted, use least-privileged TeamBition apps or tokens, and restrict credentials to appropriate projects where supported.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wengjianmin19850412/skills/teambition)

## Skill Output:

**Output Type(s):** [JSON, API responses, Configuration guidance]

**Output Format:** [JSON object containing raw TeamBition API response data or validation error codes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires configured TeamBition app credentials, with an optional access token, organization ID, and default project ID.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
