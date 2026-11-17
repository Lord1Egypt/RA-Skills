## Description:

Team Collaboration helps an agent work with a local team collaboration system for projects, requirements, tasks, bugs, documents, milestones, discussions, notifications, roles, and permissions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[magiesky](https://clawhub.ai/user/magiesky)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, project managers, and team agents use this skill to create, read, update, and delete collaboration records in a trusted local backend. It supports project planning, requirement tracking, task execution, bug triage, documentation, milestones, discussions, notifications, and role management.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill exposes high-impact delete and access-control actions.

Mitigation: Require explicit user confirmation before deletes, role changes, and permission changes.

Risk: Published reusable credentials and documented API-key patterns can be unsafe if reused.

Mitigation: Rotate or remove any matching credentials and do not treat documented passwords or API keys as safe defaults.

Risk: The localhost HTTP and WebSocket services can become exposed if tunneled or shared without additional controls.

Mitigation: Use only with a trusted local backend, and avoid network exposure unless TLS and authentication are added.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/magiesky/skills/team-collaboration)
- [Publisher profile](https://clawhub.ai/user/magiesky)

## Skill Output:

**Output Type(s):** [API Calls, JSON, Guidance]

**Output Format:** [JSON responses from local HTTP API calls, with text guidance for using available actions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Maintains an in-process bearer token after login and communicates with a localhost backend on port 8080.]

## Skill Version(s):

1.0.2 (source: server release metadata; artifact frontmatter and skill.json report 3.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
