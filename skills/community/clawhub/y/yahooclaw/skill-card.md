## Description: <br>
Yahoo Claw provides Yahoo Finance market data integration for OpenClaw, including stock quotes, historical prices, company financials, dividends, news, and technical indicators. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[leohuang8688](https://clawhub.ai/user/leohuang8688) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent builders use this skill to let OpenClaw agents retrieve and summarize public market data for equities, including quotes, history, dividends, news, sentiment, and technical indicators. Outputs should be treated as informational finance data rather than investment advice. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Outbound requests to Yahoo Finance and potentially Alpha Vantage may expose queried ticker symbols and depend on third-party service availability. <br>
Mitigation: Install only in environments where these outbound providers are approved, and configure any provider credentials through environment variables. <br>
Risk: Server security evidence reports an exposed Alpha Vantage API key in test code. <br>
Mitigation: Remove the hardcoded key before deployment and rotate the exposed Alpha Vantage credential. <br>
Risk: Server security evidence reports direct buy/sell wording without clear financial-advice warnings. <br>
Mitigation: Present technical signals as informational only, add prominent financial-risk disclaimers, and require human review before investment decisions. <br>


## Reference(s): <br>
- [Yahoo Finance](https://finance.yahoo.com/) <br>
- [Alpha Vantage API Key Documentation](https://www.alphavantage.co/support/#api-key) <br>
- [OpenClaw Documentation](https://docs.openclaw.ai/) <br>
- [ClawHub Skill Page](https://clawhub.ai/leohuang8688/yahooclaw) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, guidance] <br>
**Output Format:** [JSON-like result objects with concise text summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include prices, volumes, market metadata, timestamps, sentiment labels, and technical indicator recommendations.] <br>

## Skill Version(s): <br>
0.1.7 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
