## Description: <br>
ValueScan data-query skill for cryptocurrency market analysis, including token search, K-line data, major fund-flow analysis, and on-chain data queries. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[valuescan-io](https://clawhub.ai/user/valuescan-io) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External analysts, traders, and agent developers use this skill to query ValueScan for cryptocurrency token discovery, market data, fund-flow signals, on-chain address trends, and support or resistance indicators. The outputs are decision-support data and should not be treated as guaranteed investment outcomes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires ValueScan API credentials for signed requests. <br>
Mitigation: Use scoped credentials where possible, store them only in the expected credential location, and rotate them if exposure is suspected. <br>
Risk: Market queries, token identifiers, and wallet addresses requested for analysis may be sent to ValueScan. <br>
Mitigation: Clarify the user's intent before sending sensitive wallet-address analysis inputs and avoid submitting data that is not needed for the requested query. <br>
Risk: Some authenticated ValueScan calls consume credits. <br>
Mitigation: Resolve ambiguous or broad market questions before invoking paid endpoints, and explain when a query may spend credits. <br>
Risk: The older AI market-analysis subscription endpoint is documented as deprecated with service ending on 2026-06-01. <br>
Mitigation: Prefer the documented replacement endpoint, POST /ai/getMarketAnalysisList, for market-analysis history requests. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/valuescan-io/valuescan-skill) <br>
- [ValueScan homepage](https://www.valuescan.ai) <br>
- [ValueScan API documentation](https://claw.valuescan.io) <br>
- [ValueScan API SDK README](script/sdk/README.md) <br>
- [Common API enums](references/enums.json) <br>
- [Token list API reference](references/base/token-list.json) <br>
- [Market analysis list API reference](references/ai/market-analysis-list.json) <br>
- [Realtime fund API reference](references/fund/realtime-fund.json) <br>
- [Large trade API reference](references/chain/large-trade.json) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with JSON API data and JavaScript request-signing examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include ValueScan API calls, signed request headers, token identifiers, wallet-address analysis inputs, and credit-consuming authenticated queries.] <br>

## Skill Version(s): <br>
1.0.7 (source: server release evidence and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
