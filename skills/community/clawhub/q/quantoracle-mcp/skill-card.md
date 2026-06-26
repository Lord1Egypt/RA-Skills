## Description: <br>
63 deterministic quantitative finance calculations via MCP, covering options pricing, Greeks, implied volatility, exotic derivatives, risk metrics, portfolio optimization, Monte Carlo simulation, statistics, crypto/DeFi, macro/FX, and time value of money. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[fel123](https://clawhub.ai/user/fel123) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External developers and agent users use this MCP server to run deterministic quantitative finance calculations, including options, risk, portfolio optimization, Monte Carlo, statistics, crypto/DeFi, FX, macro, and time value of money workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Local use sends calculation inputs, portfolio details, strategy parameters, and similar financial data to QuantOracle's hosted API. <br>
Mitigation: Install only when that data transfer is acceptable, avoid submitting sensitive financial data, and override the backend URL only for a trusted self-hosted instance. <br>
Risk: The free-call limit can lead to x402 USDC pay-per-call flows after the daily allowance is exhausted. <br>
Mitigation: Keep wallet and payment use manual, monitor usage, and review payment-required responses before continuing through the REST API. <br>
Risk: Exposing the local MCP port could allow untrusted clients to invoke finance tools through the server. <br>
Mitigation: Bind and expose the MCP server only to trusted clients and networks. <br>


## Reference(s): <br>
- [QuantOracle GitHub Repository](https://github.com/QuantOracledev/quantoracle) <br>
- [QuantOracle MCP Endpoint](https://mcp.quantoracle.dev/mcp) <br>
- [QuantOracle API Documentation](https://api.quantoracle.dev/docs) <br>


## Skill Output: <br>
**Output Type(s):** [JSON, API Calls, Financial calculations, Guidance] <br>
**Output Format:** [JSON-formatted MCP tool responses with text guidance for prompts, errors, and payment-required states] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Tool inputs, portfolio details, strategy parameters, and similar financial data are forwarded to QuantOracle's hosted API by default.] <br>

## Skill Version(s): <br>
2.1.2 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
