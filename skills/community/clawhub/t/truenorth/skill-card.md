## Description: <br>
TrueNorth crypto market intelligence: technical analysis (RSI, MACD, Bollinger Bands), derivatives (funding rates, open interest), DeFi (TVL, fees), token performance, events, liquidation risk, token unlock, and more. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[truenorth-lj](https://clawhub.ai/user/truenorth-lj) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and developers use this skill to ask an agent for read-only crypto market intelligence, including technical indicators, derivatives data, DeFi metrics, token events, performance rankings, unlocks, and liquidation-risk context. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Crypto-related query text may be sent to TrueNorth's API, and market data can be misread as personal financial advice. <br>
Mitigation: Avoid sending secrets, account details, wallet addresses, or sensitive personal financial information, and treat the returned analysis as informational market context rather than trading instruction. <br>


## Reference(s): <br>
- [TrueNorth web app](https://app.true-north.xyz) <br>
- [TrueNorth CLI npm package](https://www.npmjs.com/package/@truenorth-ai/cli) <br>
- [ClawHub skill page](https://clawhub.ai/truenorth-lj/truenorth) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, JSON, guidance] <br>
**Output Format:** [Markdown summaries with inline shell commands and JSON-backed analysis.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Commands use the local tn CLI with --json and call TrueNorth's read-only public API.] <br>

## Skill Version(s): <br>
0.4.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
