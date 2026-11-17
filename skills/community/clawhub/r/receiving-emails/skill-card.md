## Description:

This skill guides applications and AI agents in receiving, processing, replying to, and forwarding email with Mailtrap Inbound Email.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mailtrap](https://clawhub.ai/user/mailtrap)

### License/Terms of Use:

MIT-0

## Use Case:

Developers building email-to-ticket, document-intake, or agent-inbox workflows use this skill to configure Mailtrap Inbound Email and process received messages, attachments, replies, forwards, and webhooks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Email content is untrusted input and may contain instructions that could trigger consequential actions.

Mitigation: Allowlist trusted senders and require human approval for consequential actions.

Risk: The examples use a Mailtrap API token, and the security review advises checking trust in the service and token use.

Mitigation: Keep the token secret and use it only in workflows authorized to access the relevant Mailtrap inboxes and account resources.

Risk: The security review is incomplete because some local references were unresolved.

Mitigation: Review the unresolved integration references and confirm the Mailtrap service and token use are appropriate before deployment.

## Reference(s):

- [Mailtrap Inbound Email overview](https://docs.mailtrap.io/inbound-email/overview.md)
- [Mailtrap Inbound API reference](https://docs.mailtrap.io/developers/inbound/)
- [Mailtrap inbound webhook documentation](https://docs.mailtrap.io/inbound-email/webhooks.md)
- [Mailtrap forward rules API reference](https://docs.mailtrap.io/developers/inbound/forward-rules)
- [Mailtrap MCP server](https://github.com/mailtrap/mailtrap-mcp)

## Skill Output:

**Output Type(s):** [Guidance, Code, Shell commands, Configuration instructions]

**Output Format:** [Markdown with inline HTTP, JSON, and shell examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [None]

## Skill Version(s):

1.0.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
