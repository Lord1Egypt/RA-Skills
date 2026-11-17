## Description:

Use when an AI agent needs to send one outbound email through Qubrics with human approval, including a status notification or delegated agent send. Trigger when preparing the exact message for approval, executing an approved send, or reconciling an uncertain retry. Use only for a single-message workflow; bulk and batch sends are outside its scope.

This skill is ready for commercial/non-commercial use.

## Publisher:

[roshanjonah](https://clawhub.ai/user/roshanjonah)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to prepare and send one individually approved outbound email through Qubrics, then report the actual send status.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: An email or attachment could be sent with unintended content or to the wrong recipient.

Mitigation: Obtain approval of the exact sender, recipients, subject, body, and attachments, and verify the authorised Sending connection identity before sending.

Risk: An uncertain send retry could create a duplicate or conflict with the original request.

Mitigation: Retry only with the same idempotency key and unchanged approved payload; reconcile the original attempt when its outcome is uncertain.

## Reference(s):

- [Qubrics MCP setup](https://qubrics.com/docs/ai-integrations/mcp)
- [Qubrics Sending attachments](https://qubrics.com/docs/sending/attachments)
- [Qubrics HTTP sending](https://qubrics.com/docs/sending/http)
- [Qubrics idempotency](https://qubrics.com/docs/sending/idempotency)
- [Qubrics delegated agent access](https://qubrics.com/docs/ai-integrations/agent-access)

## Skill Output:

**Output Type(s):** [Text, JSON, Shell commands, Guidance]

**Output Format:** [Markdown instructions with JSON email payload examples and CLI or HTTP commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Single-message workflow; bulk and batch sends are outside scope.]

## Skill Version(s):

2.0.4 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
