## Description: <br>
全功能智能股票监控预警系统。支持成本百分比、均线金叉死叉、RSI超买超卖、成交量异动、跳空缺口、动态止盈等7大预警规则。符合中国投资者习惯（红涨绿跌）。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jiahl0910](https://clawhub.ai/user/jiahl0910) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Investors and operators use this skill to monitor configured A-share, ETF, and gold holdings, generate threshold-based alerts, and review technical-signal summaries. It is intended to support monitoring and decision review, not to automate trading decisions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill contains hardcoded watchlist entries and cost values that may not match the user's holdings. <br>
Mitigation: Review and edit the watchlist, ticker symbols, markets, costs, and alert thresholds before running the monitor. <br>
Risk: Starting the daemon enables continuous background polling and logging. <br>
Mitigation: Start the daemon only when ongoing monitoring is intended, check its status and logs, and stop it when monitoring is no longer needed. <br>
Risk: Ticker, stock-name, and quote lookups are sent to Sina and Eastmoney market-data services. <br>
Mitigation: Run the skill only when those external lookups are acceptable for the configured symbols and names. <br>
Risk: Generated alerts and suggestions can be incomplete, delayed, or unsuitable as trading advice. <br>
Mitigation: Use alerts as monitoring inputs only and make investment decisions with independent review. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/jiahl0910/stock-monitor-skill-0-1-0) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/jiahl0910) <br>
- [Eastmoney market data endpoint](https://push2his.eastmoney.com/api/qt/stock/kline/get) <br>
- [Sina Finance quote endpoint](https://hq.sinajs.cn/list=) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown and terminal text with inline shell commands and alert messages] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include market-data alerts, technical-signal summaries, watchlist configuration guidance, and daemon control commands.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
