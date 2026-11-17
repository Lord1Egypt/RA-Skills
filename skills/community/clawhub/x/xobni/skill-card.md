## Description:

Xobni Email gives AI agents real Xobni.ai email addresses with REST API and MCP access for sending, receiving, searching, attachment handling, and webhook notifications.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ghoshsanjoy78](https://clawhub.ai/user/ghoshsanjoy78)

### License/Terms of Use:


## Use Case:

Developers and agent builders use this skill to connect AI agents to Xobni.ai email inboxes, send and read messages, manage attachments, perform semantic search, and configure email event webhooks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can enable an agent to read email, access attachment contents, and expose message metadata or snippets through webhooks.

Mitigation: Use narrowly scoped API keys, limit access to the intended agent mailbox, and configure webhook URLs only for endpoints you control and trust.

Risk: The skill can enable an agent to send email to external recipients.

Mitigation: Require recipient and content confirmation before sending messages, especially when attachments, cc, or bcc fields are present.

Risk: Persistent webhooks can continue forwarding email events after initial setup.

Mitigation: Review active webhooks regularly, remove unused endpoints, and verify webhook signatures before processing received payloads.

## Reference(s):

- [Xobni.ai REST API Reference](references/api.md)
- [Xobni Agent Setup](https://xobni.ai/agents/new)
- [Xobni API Keys](https://xobni.ai/settings/api-keys)
- [Xobni MCP Endpoint](https://api.xobni.ai/mcp/)
- [ClawHub Skill Page](https://clawhub.ai/ghoshsanjoy78/skills/xobni)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with JSON configuration examples and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Guidance covers REST API calls, MCP configuration, email operations, attachments, semantic search, and webhooks.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
