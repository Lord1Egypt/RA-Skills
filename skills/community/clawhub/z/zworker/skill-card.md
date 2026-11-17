## Description:

Zworker lets an agent control a local zworker AI automation app for task management, schedule control, user synchronization, and notification forwarding.

This skill is ready for commercial/non-commercial use.

## Publisher:

[peterpan0630](https://clawhub.ai/user/peterpan0630)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and operators use this skill to inspect and trigger local zworker tasks, manage schedules, sync OpenClaw user routing data, and forward zworker notifications.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can trigger local zworker tasks and change schedule state.

Mitigation: Use only with a trusted local Zworker instance and require explicit confirmation before task execution or schedule changes.

Risk: Identity sync and notification forwarding can misroute or expose user messages if user IDs or channels are wrong.

Mitigation: Confirm which OpenClaw user IDs and channels may be synced, and avoid fallback notification routing when a user ID is missing.

Risk: The local zworker HTTP service is documented as unauthenticated.

Mitigation: Keep the service limited to trusted local access and review network exposure before installing or using the skill.

## Reference(s):

- [Zworker HTTP API endpoints](references/api_endpoints.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Shell commands, Configuration guidance]

**Output Format:** [Markdown or plain text status messages, with JSON available from helper scripts.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [UTF-8 text; paginated task and schedule list outputs default to 24 items.]

## Skill Version(s):

1.0.3 (source: server release metadata and artifact/version.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
