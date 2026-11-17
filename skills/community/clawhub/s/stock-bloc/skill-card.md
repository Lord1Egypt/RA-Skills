## Description:

Helps agents access Stock Bloc market data, quant scores, SEC filings, research, forecasts, and earnings packs through paid USDC-per-call requests on Base.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jaywestphilly](https://clawhub.ai/user/jaywestphilly)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to retrieve market intelligence and SEC data, generate research and earnings materials, and evaluate strategies through paid Stock Bloc endpoints.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Automated payment authorization or retries can incur unintended USDC charges.

Mitigation: Require per-call confirmation and configure wallet limits, endpoint allowlists, and monthly spend caps before use.

## Reference(s):

- [Stock Bloc machine documentation](https://stockbloc.ai.studio/llms.txt)
- [Stock Bloc x402 discovery](https://stockbloc.ai.studio/.well-known/x402)
- [Stock Bloc OpenAPI specification](https://stockbloc.ai.studio/api/v1/openapi.json)
- [Stock Bloc MCP endpoint](https://stockbloc.ai.studio/api/mcp/rpc)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, API requests]

**Output Format:** [Markdown with API request and payment-flow instructions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Paid requests require USDC payment authorizations on Base.]

## Skill Version(s):

2.2.0 (source: skill frontmatter and server-resolved release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
