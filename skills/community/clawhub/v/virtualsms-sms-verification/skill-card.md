## Description:

Real SIM-card phone numbers for SMS verification across 2000+ services and 145+ countries, exposed to agents through the VirtualSMS MCP server.

This skill is ready for commercial/non-commercial use.

## Publisher:

[virtualsms](https://clawhub.ai/user/virtualsms)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, and agent operators use this skill when an agent needs to acquire a temporary real-SIM number, receive an SMS or OTP code, and manage the verification order lifecycle.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles sensitive authentication and account-verification workflows.

Mitigation: Use it only for accounts where third-party temporary SMS verification is allowed and acceptable, and avoid banking or high-value identity accounts.

Risk: The VirtualSMS API key can authorize account and order-management actions.

Mitigation: Keep the API key scoped and rotated, and require explicit user confirmation before buying numbers, retrieving OTPs, or canceling orders.

Risk: The local stdio path uses an unpinned npm execution command.

Mitigation: Prefer the hosted MCP endpoint or a pinned, sandboxed local MCP installation.

## Reference(s):

- [VirtualSMS MCP setup](https://virtualsms.io/mcp)
- [VirtualSMS project](https://virtualsms.io)
- [virtualsms-mcp npm package](https://www.npmjs.com/package/virtualsms-mcp)
- [Parent MCP server](https://github.com/virtualsms-io/mcp-server)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration]

**Output Format:** [Markdown with inline JSON and bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May recommend MCP tool calls and order-management actions that require a VirtualSMS API key.]

## Skill Version(s):

1.0.0 (source: server release evidence and skill.yaml)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
