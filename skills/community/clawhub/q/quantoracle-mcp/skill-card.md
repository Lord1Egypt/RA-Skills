## Description:

Provides deterministic quantitative finance calculations through an MCP server, including options pricing, Greeks, risk metrics, portfolio optimization, Monte Carlo simulation, statistics, crypto/DeFi, macro/FX, and time value of money.

This skill is ready for commercial/non-commercial use.

## Publisher:

[fel123](https://clawhub.ai/user/fel123)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and agent users use this MCP server to run deterministic quantitative finance calculations for options pricing, portfolio risk, technical indicators, crypto/DeFi analysis, macro/FX calculations, and time value of money workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Calculation inputs may be sent to QuantOracle's remote backend.

Mitigation: Avoid submitting sensitive trading, portfolio, or client data unless the provider's data handling terms are acceptable.

Risk: The MCP HTTP service may expose broad unauthenticated access if reachable from untrusted networks.

Mitigation: Run it bound to localhost or behind authentication and network access controls.

Risk: The skill relies on mutable remote services.

Mitigation: Use a pinned package version and restrict the backend URL to a trusted origin.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/fel123/skills/quantoracle-mcp)
- [ClawHub Metadata Homepage](https://github.com/QuantOracledev/quantoracle)
- [Hosted MCP Endpoint](https://mcp.quantoracle.dev/mcp)
- [QuantOracle API Documentation](https://api.quantoracle.dev/docs)

## Skill Output:

**Output Type(s):** [JSON, API Calls, Configuration]

**Output Format:** [JSON MCP tool responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Returns deterministic calculation results; remote backend use, free daily limits, and x402 paid continuation are described by the release evidence.]

## Skill Version(s):

2.1.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
