## Description: <br>
Kalshi helps agents query read-only Kalshi prediction-market data for sports events, series, markets, trades, and candlestick price history. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[antonelli182](https://clawhub.ai/user/antonelli182) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to discover Kalshi sports prediction markets, retrieve open event and market data, and inspect implied probabilities and OHLC price history. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Kalshi prices are prediction-market probabilities, not sports scores, match results, or financial advice. <br>
Mitigation: Present prices as 0-100 implied probabilities and use sport-specific data sources when the user asks for schedules, scores, or statistics. <br>
Risk: The skill assumes the runtime provides the referenced sports-skills CLI or Python SDK. <br>
Mitigation: Confirm the runtime has the required CLI or SDK before use and review generated commands before execution. <br>


## Reference(s): <br>
- [Kalshi API](https://api.elections.kalshi.com/trade-api/v2) <br>
- [Kalshi API Reference](references/api-reference.md) <br>
- [Valid Commands & Common Mistakes](references/commands.md) <br>
- [Sport Codes & Series Tickers](references/series-tickers.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, code, guidance] <br>
**Output Format:** [Markdown with inline shell and Python examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Read-only market data guidance; no credentials are requested by the skill.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
