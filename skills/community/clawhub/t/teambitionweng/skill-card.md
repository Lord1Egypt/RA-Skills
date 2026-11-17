## Description:

Create and query tasks in TeamBition with support for multiple app configurations and automatic token management.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wengjianmin19850412](https://clawhub.ai/user/wengjianmin19850412)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and workspace operators use this skill to let agents create TeamBition project tasks and retrieve task details through a configured TeamBition application.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends TeamBition credentials and task data to TeamBition APIs.

Mitigation: Use least-privilege TeamBition credentials and avoid placing secrets or sensitive business content in task titles or descriptions.

Risk: The create_task action can create remote tasks in a TeamBition workspace.

Mitigation: Review create_task calls before allowing an agent to automate task creation.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wengjianmin19850412/skills/teambitionweng)

## Skill Output:

**Output Type(s):** [API Calls, JSON]

**Output Format:** [JSON TeamBition API response]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Creates remote TeamBition tasks for create_task and returns task details for get_task.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
