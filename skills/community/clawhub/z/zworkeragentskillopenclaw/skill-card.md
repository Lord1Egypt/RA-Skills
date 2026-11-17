## Description:

Controls a local zworker AI automation application through HTTP APIs for task management, schedule control, user information synchronization, and message notification forwarding.

This skill is ready for commercial/non-commercial use.

## Publisher:

[peterpan0630](https://clawhub.ai/user/peterpan0630)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to inspect and control zworker automations from an OpenClaw agent, including listing or running tasks, enabling or disabling schedules, syncing channel user identifiers, and forwarding zworker notifications.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can trigger zworker automations and change schedules through a local API without an authentication layer shown in the artifact.

Mitigation: Install and use it only when the local zworker service is intentionally running and trusted, and review task or schedule identifiers before execution.

Risk: Notification forwarding can send messages to a default or recent recipient when no user identifier is present.

Mitigation: Review message-forwarding behavior and avoid ambiguous or default recipients for sensitive notifications.

Risk: User synchronization sends channel and user identifiers to the local zworker service.

Mitigation: Sync only the intended channels and user identifiers, and limit use to trusted local environments.

## Reference(s):

- [Zworker HTTP API endpoints](references/api_endpoints.md)
- [ClawHub skill page](https://clawhub.ai/peterpan0630/skills/zworkeragentskillopenclaw)
- [ClawHub publisher profile](https://clawhub.ai/user/peterpan0630)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown and JSON/text command output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs may include task and schedule lists, success or failure messages, notification content, and command guidance for local zworker API operations.]

## Skill Version(s):

1.0.2 (source: artifact/version.json and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
