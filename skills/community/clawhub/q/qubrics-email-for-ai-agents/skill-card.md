## Description:

Use when an AI agent needs to send one outbound email through Qubrics with human approval, including a status notification or delegated agent send.

This skill is ready for commercial/non-commercial use.

## Publisher:

[roshanjonah](https://clawhub.ai/user/roshanjonah)

### License/Terms of Use:

MIT-0

## Use Case:

AI agents use this skill to prepare and send one user-approved email through an authorized Qubrics Sending connection, then report the actual result. It is intended for developers and agent operators handling one message at a time.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: An incorrect sender, recipient, subject, body, or attachment could be sent externally.

Mitigation: Review the complete message and obtain explicit user approval before sending; verify that the selected connection is authorized for the intended account.

Risk: An uncertain send result could lead to a duplicate or altered retry.

Mitigation: Retry only with the same idempotency key and unchanged payload; reconcile the original attempt when its outcome or payload is unclear.

## Reference(s):

- [Qubrics MCP connection setup](https://qubrics.com/docs/ai-integrations/mcp)
- [Qubrics HTTP sending](https://qubrics.com/docs/sending/http)
- [Qubrics sending idempotency](https://qubrics.com/docs/sending/idempotency)
- [Qubrics delegated agent access](https://qubrics.com/docs/ai-integrations/agent-access)
- [Qubrics sending attachments](https://qubrics.com/docs/sending/attachments)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, API calls, JSON]

**Output Format:** [Markdown guidance with CLI examples and JSON request examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Covers one outbound email per workflow; bulk and batch sends are out of scope.]

## Skill Version(s):

2.0.8 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
