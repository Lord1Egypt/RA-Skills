## Description:

QuantOracle exposes deterministic quantitative finance calculators and composite workflows to agents over MCP, covering options pricing, Greeks, exotic derivatives, risk metrics, portfolio optimization, Monte Carlo, statistics, crypto/DeFi, FX/macro, time value of money, backtesting, rebalancing, strategy selection, and hedging.

This skill is ready for commercial/non-commercial use.

## Publisher:

[fel123](https://clawhub.ai/user/fel123)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use QuantOracle to run deterministic finance calculations and composite analysis workflows from MCP-compatible clients. It supports pricing, Greeks, risk metrics, optimization, backtesting, hedging, and DeFi/FX/macro calculations without an API key for the free tier.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The setup can run the QuantOracle MCP npm package or connect to a hosted MCP endpoint, and the security summary flags the install path as needing review.

Mitigation: Use a pinned, reviewed package version or reviewed endpoint configuration, and restrict the MCP server's filesystem and environment access before enabling it.

Risk: Paid composite workflows can use wallet-based x402 payments when an x402-capable wallet is provided.

Mitigation: Do not provide an x402 wallet unless paid composite calls are intended, and configure wallet access and spending review outside the skill.

## Reference(s):

- [QuantOracle homepage](https://github.com/QuantOracledev/quantoracle)
- [Browser calculators](https://quantoracle.dev)
- [Hosted MCP endpoint](https://mcp.quantoracle.dev/mcp)
- [npm package](https://www.npmjs.com/package/quantoracle-mcp)
- [API documentation](https://api.quantoracle.dev/openapi.json)
- [Endpoint catalog](https://api.quantoracle.dev/tools)
- [x402 protocol](https://x402.org)

## Skill Output:

**Output Type(s):** [JSON, Guidance, Configuration]

**Output Format:** [JSON responses from MCP tools, with human-readable financial calculation results and setup guidance in Markdown]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Free tier is rate-limited to 1,000 calls per IP per day; paid composite workflows use per-call USDC payments through x402 when an x402-capable wallet is provided.]

## Skill Version(s):

2.1.2 (source: server release metadata; artifact frontmatter says 2.4.1)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
