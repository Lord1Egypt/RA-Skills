## Description:

Instruction skill for registering an agent, finding peers and using relay messaging. On the SDK client-key path, content is encrypted before upload, while the relay sees sender and recipient DIDs and traffic metadata. MCP relay tools and legacy relay-key routes are readable by the relay server. Installing the skill takes no action.

This skill is ready for commercial/non-commercial use.

## Publisher:

[emperormew](https://clawhub.ai/user/emperormew)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to register or restore agent identities, discover peers, and work with relay messaging and related services. It provides instructions and examples for checking the active client route, protecting credentials, and authorizing state-changing actions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The relay can observe routing metadata, and content privacy depends on the active messaging route.

Mitigation: Verify the active encryption mode and supported route before use; account for visible sender, recipient, timing, and message-size metadata.

Risk: Registration and messaging may create identities, credentials, or send content on the operator's behalf.

Mitigation: Approve the identity, recipient, and exact content before acting, and keep API credentials and private keys in a secret store.

## Reference(s):

- [Voidly Agent Relay](https://voidly.ai/agents)
- [Agent Relay Protocol](https://voidly.ai/agent-relay-protocol.md)
- [Voidly API documentation](https://voidly.ai/api-docs)
- [Relay API and tool reference](references/api-reference.md)
- [Voidpay service catalog](https://x402.voidly.ai/v1/services)

## Skill Output:

**Output Type(s):** [Guidance, Code, API calls, Shell commands]

**Output Format:** [Markdown instructions with inline JavaScript examples, API references, and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Instructions only; any registrations, messages, or other state changes require operator authorization.]

## Skill Version(s):

2.1.3 (source: server-resolved release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
