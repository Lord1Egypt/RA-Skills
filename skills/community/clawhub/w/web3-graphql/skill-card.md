## Description:

Use Ask GraphQL MCP to handle Web3 and on-chain questions through GraphQL endpoints, especially SubQuery and SubGraph endpoints, by routing natural-language tasks through the graphql_agent MCP tool or HTTP JSON-RPC fallback.

This skill is ready for commercial/non-commercial use.

## Publisher:

[subquery-network](https://clawhub.ai/user/subquery-network)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and analysts use this skill to answer Web3 and on-chain questions, debug GraphQL queries, and produce endpoint-specific analysis through Ask GraphQL MCP. It is intended for workflows involving public or authorized SubQuery, SubGraph, and similar GraphQL endpoints.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Web3 GraphQL requests and optional private endpoint authorization may be routed through the Hermes Ask GraphQL MCP gateway.

Mitigation: Use the skill only with endpoints and prompts approved for that external service, and confirm third-party gateway use is acceptable before sending private endpoint authorization.

Risk: API keys or bearer tokens could be exposed if pasted directly into chat.

Mitigation: Use a protected secret store or short-lived, read-only credentials, and rotate any token that may have been exposed.

## Reference(s):

- [Ask GraphQL MCP ClawHub skill page](https://clawhub.ai/subquery-network/skills/web3-graphql)
- [Ask GraphQL MCP templates](artifact/references/config-templates.md)
- [Ask GraphQL MCP tools and prompts](artifact/references/tools-and-prompts.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, API Calls, Configuration, Guidance]

**Output Format:** [Markdown responses with optional JSON configuration blocks and MCP call guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include assumptions, MCP answer summaries, query details returned by MCP, endpoint checks, and next-step guidance.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
