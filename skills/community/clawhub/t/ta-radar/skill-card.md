## Description: <br>
Multi-Dimensional Technical Analysis Radar for cryptocurrencies that supports spot trading pairs and on-chain contract addresses and generates objective technical analysis reports with EMA, RSI, MACD, Bollinger Bands, support and resistance levels, and trend analysis. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[deanpeng-dotcom](https://clawhub.ai/user/deanpeng-dotcom) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to request cryptocurrency technical analysis for a trading pair or EVM contract address. The agent fetches public market data, computes common indicators, and returns a human-readable report; it should not be treated as financial advice. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends queried symbols or contract addresses to public market-data services and a public proxy. <br>
Mitigation: Use only non-sensitive symbols or addresses and review the configured public endpoints before use. <br>
Risk: The generated report could be mistaken for investment advice. <br>
Mitigation: Present the output as technical analysis only and do not use it as financial advice. <br>
Risk: The embedded script is incomplete in the reviewed artifact. <br>
Mitigation: Review the current SKILL.md and verify the complete script before installing or running the skill. <br>


## Reference(s): <br>
- [TA Radar ClawHub listing](https://clawhub.ai/deanpeng-dotcom/ta-radar) <br>
- [Server-resolved source repository](https://github.com/clawhub/ta-radar) <br>
- [Private deployment guide](references/deployment.md) <br>
- [Binance K-line endpoint](https://api.binance.info/api/v3/klines) <br>
- [Gate.io candlesticks endpoint](https://api.gateio.ws/api/v4/spot/candlesticks) <br>
- [DexScreener search endpoint](https://api.dexscreener.com/latest/dex/search) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown-style technical analysis report with plain text indicator values, conclusions, and explanations] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires TA_SYMBOL and optionally TA_INTERVAL; supported intervals are 1h, 4h, and 1d.] <br>

## Skill Version(s): <br>
1.2.0 (source: SKILL.md frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
