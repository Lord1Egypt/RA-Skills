## Description: <br>
QuantOracle exposes deterministic quantitative-finance calculators and composite workflows to agents through MCP, covering options pricing, Greeks, risk metrics, portfolio optimization, Monte Carlo, statistics, crypto/DeFi, FX/macro, TVM, strategy backtesting, rebalancing, options strategy selection, and hedging. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[fel123](https://clawhub.ai/user/fel123) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use QuantOracle to add quantitative finance calculations, risk analysis, portfolio workflows, and paid composite finance workflows to MCP-compatible agents. It is suited for finance calculation support, not as a substitute for human investment judgment or compliance review. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Finance and trading calculation inputs are sent to the external QuantOracle API through the MCP server. <br>
Mitigation: Avoid sending confidential trading, portfolio, or customer data unless that external processing is acceptable for the deployment. <br>
Risk: Paid composite workflows can settle USDC payments when an x402-capable wallet is enabled. <br>
Mitigation: Do not enable or provide an x402 wallet unless paid calls are intended; prefer wallet or client-side spending limits for paid workflows. <br>
Risk: Quantitative finance outputs may be used incorrectly as investment or risk-management decisions. <br>
Mitigation: Treat outputs as calculation support and require qualified review before financial, trading, or compliance use. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/fel123/quantoracle) <br>
- [Publisher profile](https://clawhub.ai/user/fel123) <br>
- [Source repository](https://github.com/QuantOracledev/quantoracle) <br>
- [Browser calculators](https://quantoracle.dev) <br>
- [MCP endpoint](https://mcp.quantoracle.dev/mcp) <br>
- [Full API documentation](https://api.quantoracle.dev/openapi.json) <br>
- [Endpoint catalog](https://api.quantoracle.dev/tools) <br>
- [npm package](https://www.npmjs.com/package/quantoracle-mcp) <br>
- [x402 protocol](https://x402.org) <br>


## Skill Output: <br>
**Output Type(s):** [text, json, configuration, shell commands, guidance] <br>
**Output Format:** [JSON tool responses, Markdown guidance, and shell/configuration snippets for MCP setup] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May call an external QuantOracle API; paid composite workflows require an explicit x402-capable wallet and return 402 when no wallet is configured.] <br>

## Skill Version(s): <br>
2.1.2 (source: server release metadata; artifact frontmatter states 2.4.1) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
