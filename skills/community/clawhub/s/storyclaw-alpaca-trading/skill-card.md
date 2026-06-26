## Description: <br>
US stock and crypto trading via Alpaca API. Paper trading (simulated) and real trading supported. Real-time quotes, orders, positions, RSI strategy. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[patches429](https://clawhub.ai/user/patches429) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to inspect Alpaca account data, fetch market quotes and indicators, and prepare or execute stock and crypto trades through Alpaca credentials. It supports paper trading by default but can also operate against live trading endpoints when configured. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can operate with Alpaca credentials that have trading authority, including live trading endpoints. <br>
Mitigation: Use paper-trading credentials by default and require a separate human confirmation before any live order is submitted. <br>
Risk: Strategy scripts can place or rotate trades without the same enforced confirmation step described in the skill instructions. <br>
Mitigation: Review the strategy scripts before use and avoid running aggressive or momentum strategies unless the trading plan and order behavior are understood. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/patches429/storyclaw-alpaca-trading) <br>
- [Alpaca paper trading API](https://paper-api.alpaca.markets) <br>
- [Alpaca market data API](https://data.alpaca.markets) <br>
- [Alpaca live trading API](https://api.alpaca.markets) <br>
- [Alpaca account setup](https://app.alpaca.markets/brokerage/new-account) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, Guidance, Text] <br>
**Output Format:** [Markdown with inline shell commands and command output descriptions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Node.js and Alpaca API credentials.] <br>

## Skill Version(s): <br>
0.1.0 (source: frontmatter and release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
