## Description:

Pushes completed task results to a negative-screen notification service using a standardized JSON payload for task content, metadata, status, and Markdown-formatted details.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ganhaiyang3](https://clawhub.ai/user/ganhaiyang3)

### License/Terms of Use:

MIT-0

## Use Case:

OpenClaw users and developers use this skill to package task-completion results as JSON and push them to a negative-screen notification endpoint. It is intended for workflows that need task status, Markdown content, timestamps, and push responses returned in a consistent format.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Task content, task metadata, UID, and API-key-authenticated requests may be sent to a hardcoded Huawei endpoint.

Mitigation: Avoid sending sensitive task content unless the endpoint and data flow are acceptable; use dry-run or validation-only workflows before live pushes.

Risk: API key and UID values may be exposed in console output or logs.

Mitigation: Review output and log files after use, rotate exposed credentials, and require the publisher to redact headers and credential values before deployment.

Risk: Documentation and implementation disagree about configurable endpoints, authentication handling, and record-saving controls.

Mitigation: Confirm runtime configuration behavior before installation and disable or clean local records when push history should not be retained.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/ganhaiyang3/skills/push-task-to-negative-screen)
- [README](artifact/README.md)
- [Security Statement](artifact/SECURITY.md)
- [Update System](artifact/UPDATE_SYSTEM.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown instructions, shell commands, JSON request and response payloads, and plain-text status messages]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create local logs and optional push records; network push behavior can be avoided with dry-run mode.]

## Skill Version(s):

1.0.21 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
