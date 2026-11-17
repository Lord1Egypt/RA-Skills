## Description:

TopoLift's negotiation dialect for AI agents teaches the public closed vocabulary for regimes, strategies, signal keys, citation grammar, and the supported live API access paths.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jgeraci](https://clawhub.ai/user/jgeraci)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to understand TopoLift's negotiation response dialect and call the live reasoning API through MCP, Bearer-key API requests, or x402 micropayments.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Negotiation scenarios may include sensitive counterpart details, business goals, reservation prices, or confidential strategy sent to a third-party service.

Mitigation: Use the skill only with negotiation details that are approved for TopoLift processing, and redact counterpart identities and confidential strategy where possible.

Risk: The MCP install path uses an unpinned package that receives a TopoLift API key.

Mitigation: Pin and verify the MCP package version, and use a narrow, revocable API key.

Risk: x402 pay-per-call usage can trigger paid transactions from autonomous agents.

Mitigation: Require explicit approval or wallet limits before x402 paid calls.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jgeraci/skills/topolift-negotiation-atoms-lite)
- [TopoLift homepage](https://topolift.ai)
- [Live dialect endpoint](https://api.topolift.ai/v1/dialect)
- [TopoLift API](https://api.topolift.ai)
- [TopoLift MCP package](https://pypi.org/project/topolift-mcp/)
- [Official MCP registry search](https://registry.modelcontextprotocol.io/v0/servers?search=topolift)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration]

**Output Format:** [Markdown with inline shell commands and API request examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May guide agents to call a third-party API using MCP, Bearer authentication, or x402 payment.]

## Skill Version(s):

1.2.1 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
