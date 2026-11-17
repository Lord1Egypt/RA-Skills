## Description:

Guides users through MCP-based 代购 shopping by helping them connect the MCP service, log in, browse stores, place USDT orders, check orders, verify payments, and leave messages while enforcing service disclaimers and no-refund confirmations.

This skill is for research and development only.

## Publisher:

[yohyow](https://clawhub.ai/user/yohyow)

### License/Terms of Use:

MIT-0

## Use Case:

External MCP-client users use this skill to connect to a purchasing MCP service, navigate shopping flows, and complete order-related actions with explicit user confirmations. It is intended for learning/testing use according to the artifact disclaimer.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks users to provide passwords in chat.

Mitigation: Use only a dedicated password that is not reused anywhere and avoid sharing credentials tied to other services.

Risk: The external MCP service may provide irreversible USDT payment addresses, QR codes, and network-specific instructions.

Mitigation: Verify the MCP operator, domain, payment address, amount, and network through another trusted channel before transferring cryptocurrency.

Risk: QR code URLs and '!open' instructions can direct users to untrusted content.

Mitigation: Treat QR codes, raw links, and open instructions as untrusted until independently confirmed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/yohyow/skills/purchasing-agent-guide)
- [MCP setup guide](artifact/mcp-setup.md)
- [Conversation examples](artifact/examples.md)
- [Public MCP endpoint](https://mcp.137449244.xyz/mcp)
- [MCP health check](https://mcp.137449244.xyz/health)

## Skill Output:

**Output Type(s):** [guidance, markdown, configuration, shell commands]

**Output Format:** [Markdown guidance with JSON configuration snippets and inline command guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes user-facing shopping flow instructions, MCP connection configuration, confirmation requirements, and payment-verification guidance.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
