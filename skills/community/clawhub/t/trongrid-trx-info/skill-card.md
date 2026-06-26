## Description: <br>
Query TRX token fundamentals including price, supply, burn rate, market cap, staking yield, and network economics. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[greason](https://clawhub.ai/user/greason) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, analysts, and external users use this skill to produce TRX tokenomics reports that combine TronGrid on-chain data, market data, burn estimates, staking yield estimates, and network economics. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may perform public web and TronGrid lookups when invoked. <br>
Mitigation: Install and enable it only for TRX token analysis workflows where those public lookups are expected. <br>
Risk: Crypto price, burn, supply, staking-yield, and value-assessment outputs may be time-sensitive or mistaken for financial advice. <br>
Mitigation: Treat generated reports as informational, verify current figures against authoritative market and blockchain sources, and avoid relying on the output as investment advice. <br>


## Reference(s): <br>
- [TronGrid MCP Guide](https://developers.tron.network/reference/mcp-api) <br>
- [TRX price and supply analysis example](examples/trx-price-and-supply.md) <br>
- [TRX burn rate analysis example](examples/trx-burn-analysis.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, API calls, guidance] <br>
**Output Format:** [Markdown report with TRX market metrics, supply estimates, burn analysis, staking-yield estimates, and explanatory guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May use public web and TronGrid lookups when invoked; crypto price, supply, burn, and yield outputs are informational rather than financial advice.] <br>

## Skill Version(s): <br>
1.0.4 (source: release metadata; artifact metadata reports 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
