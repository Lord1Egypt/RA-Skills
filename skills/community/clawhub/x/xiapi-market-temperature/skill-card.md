## Description: <br>
分析A股市场温度指标，通过估值温度、恐贪指数、趋势温度、动量温度判断市场冷热程度。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ksky521](https://clawhub.ai/user/ksky521) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to fetch DaxiAPI market-temperature data and produce structured A-share market heat, sentiment, valuation, style-rotation, scenario, and action-orientation reports. It is intended for market-level analysis, not individual stock, sector, bond, futures, foreign-exchange, intraday signal, or automated-trading requests. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Users may expose a third-party DaxiAPI token through shared shell history, synced configuration files, or token-in-URL examples. <br>
Mitigation: Prefer Authorization bearer headers or environment variables, avoid token-in-URL usage, and do not place real tokens in shared shell history or synced dotfiles. <br>
Risk: Market reports may be mistaken for personalized trading instructions. <br>
Mitigation: Treat buy/sell and allocation language as informational market-level analysis, include risk disclaimers, and review outputs critically before making financial decisions. <br>
Risk: Delayed or abnormal market-temperature data may produce misleading conclusions. <br>
Mitigation: Check data dates and completeness, flag zero or missing values as possible update delays, and avoid absolute predictions when indicators conflict. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ksky521/xiapi-market-temperature) <br>
- [Publisher profile](https://clawhub.ai/user/ksky521) <br>
- [DaxiAPI](https://daxiapi.com) <br>
- [Market temperature API endpoint](https://daxiapi.com/coze/get_market_temp) <br>
- [CLI 命令参考](references/cli-commands.md) <br>
- [API 参考文档](references/api-reference.md) <br>
- [Token 配置指南](references/token-setup.md) <br>
- [字段说明](references/field-descriptions.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown report with tables and inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a third-party DaxiAPI token and produces informational market-level analysis rather than personalized financial advice.] <br>

## Skill Version(s): <br>
1.0.2 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
