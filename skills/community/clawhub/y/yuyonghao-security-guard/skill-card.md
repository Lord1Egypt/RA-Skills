## Description:

Provides role-based access control, input and output content review, sensitive operation confirmation, and audit logging for JavaScript agent workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yuyonghao-123](https://clawhub.ai/user/yuyonghao-123)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent builders use this skill to add permission checks, content safety review, confirmation gates for high-risk operations, and audit reporting around agent actions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Advertised security controls may silently fail or be bypassed.

Mitigation: Review and fix control gaps before relying on the skill as an enforcement boundary for high-risk operations, custom role policies, blocked content patterns, or output redaction.

Risk: Audit logs may contain operation metadata and are written to a configured local log directory.

Mitigation: Confirm the log storage location, retained metadata, retention period, and access controls before deployment.

Risk: High-risk operations depend on confirmation handling by the integrating agent or application.

Mitigation: Test confirmation event handling and deny-by-default behavior in the target runtime before enabling sensitive actions.

## Reference(s):

- [Security Guard on ClawHub](https://clawhub.ai/yuyonghao-123/skills/yuyonghao-security-guard)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JavaScript code examples, shell commands, configuration snippets, and JSON-like check and report objects.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce allow/deny results, warning lists, sanitized text, confirmation events, audit log entries, and audit summary reports.]

## Skill Version(s):

0.1.0 (source: server release evidence and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
