## Description:

Send one or many emails through Qubrics using approved mailbox or agent credentials, idempotency keys, attachments, MCP, CLI, SDKs, or HTTP.

This skill is ready for commercial/non-commercial use.

## Publisher:

[roshanjonah](https://clawhub.ai/user/roshanjonah)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to prepare and send single or batch outbound emails through Qubrics. Sending requires approved credentials and explicit confirmation of the complete sender, recipients, subject, body, and attachments.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Security scan coverage is incomplete because some local references could not be resolved.

Mitigation: Review the skill requirements and confirm that you trust the Qubrics service and the credentials selected for use.

Risk: Sending an email to the wrong recipient or with unintended content can disclose information or create an unwanted communication.

Mitigation: Verify the selected account and confirm every sender, recipient, subject, body, and attachment before sending; do not invent message details.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/roshanjonah/skills/qubrics-send-email)
- [Qubrics project homepage](https://github.com/qubrics/skills)
- [Qubrics Sending API endpoint](https://smtp.qubrics.com/api/v1/emails/send)

## Skill Output:

**Output Type(s):** [Guidance, API calls, Shell commands, Code, JSON, Configuration instructions]

**Output Format:** [Markdown guidance with JSON examples, shell commands, and TypeScript code]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Examples use user-approved message details and credentials supplied through an authorised secret store or profile.]

## Skill Version(s):

2.0.8 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
