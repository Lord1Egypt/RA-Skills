## Description: <br>
查询A股、港股、美股股票的实时行情，包括价格、涨跌幅、开盘价、成交量等详细数据。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[MrBlackerX](https://clawhub.ai/user/MrBlackerX) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agents use this skill to look up current stock quote data by ticker-like symbol for supported A-share and Hong Kong markets. It returns current price, daily change, open/high/low, volume, value, turnover, and market labels when available. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Stock symbols queried through the skill are sent to an external stock data service. <br>
Mitigation: Use the skill only when it is acceptable for the queried symbols to be visible to that provider. <br>
Risk: The artifact documentation mentions US stocks, but the executable evidence supports A-share and Hong Kong symbols and returns an error for other symbol formats. <br>
Mitigation: Validate market coverage before relying on the skill for unsupported markets. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/MrBlackerX/stock) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands] <br>
**Output Format:** [Plain text stock quote summary from a CLI command] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The command accepts one stock symbol and prints quote fields or an error message.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
