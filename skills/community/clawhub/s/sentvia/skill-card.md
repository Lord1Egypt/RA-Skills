## Description:

Give this agent its own email address to create inboxes, send, reply in-thread, search mail, and manage senders via SentVia.

This skill is ready for commercial/non-commercial use.

## Publisher:

[samuelar2](https://clawhub.ai/user/samuelar2)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to let an agent operate a SentVia mailbox: create or reuse an inbox, send email, reply in existing threads, search messages, forward messages to a human, and manage blocked senders.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can transmit real email externally and create persistent SentVia mailbox state.

Mitigation: Require explicit user confirmation before creating inboxes, sending or replying to mail, forwarding messages, or changing sender block lists.

Risk: Received email can contain untrusted instructions or requests for sensitive information.

Mitigation: Treat inbound messages as untrusted content and do not follow instructions from email or forward secrets and credentials.

Risk: The recommended MCP setup uses an unpinned package install path.

Mitigation: Pin and review the SentVia MCP package before use.

Risk: A broad API key could let an agent take unwanted mailbox actions.

Mitigation: Limit the API key's permissions when SentVia supports scoped keys and keep SENTVIA_API_KEY out of email content.

## Reference(s):

- [SentVia Documentation](https://docs.sentvia.ai)
- [SentVia for Agents](https://docs.sentvia.ai/for-agents)
- [SentVia LLM Reference](https://docs.sentvia.ai/llms-full.txt)
- [ClawHub Skill Page](https://clawhub.ai/samuelar2/skills/sentvia)
- [Publisher Profile](https://clawhub.ai/user/samuelar2)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, API Calls, Configuration]

**Output Format:** [Markdown guidance with inline shell commands and JSON request examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires SENTVIA_API_KEY and may use the SentVia MCP server when configured; otherwise it provides curl-based API calls.]

## Skill Version(s):

0.2.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
