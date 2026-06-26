## Description: <br>
Real-time BTC, ETH, and SOL market scanner that uses RSI, EMA, MACD, volume, and multi-timeframe scoring to produce crypto trading-signal analysis. <br>

This skill is for research and development only. <br>

## Publisher: <br>
[sg345662365-oss](https://clawhub.ai/user/sg345662365-oss) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to have an agent scan BTC, ETH, and SOL market data across multiple timeframes and produce trading-signal analysis for monitoring, research, and risk-aware decision support. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill references private exchange access and possible leveraged trade execution. <br>
Mitigation: Keep exchange API keys read-only by default, require manual confirmation before any order placement, and use tightly scoped exchange permissions. <br>
Risk: Crypto trading signals can be incorrect, stale, or financially harmful if treated as advice. <br>
Mitigation: Use the output as research support only, review market context independently, and apply strict position-size and leverage limits. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/sg345662365-oss/vane-crypto-market-scanner) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown or plain-text trading-signal analysis with scores, indicators, position-sizing guidance, and risk notes] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May reference configurable symbols, timeframes, minimum score thresholds, leverage limits, and exchange access settings.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
