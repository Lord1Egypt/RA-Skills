## Description:

股票盯盯 - 全功能智能股票监控预警系统。支持成本百分比、均线金叉死叉、RSI超买超卖、成交量异动、跳空缺口、动态止盈等7大预警规则。符合中国投资者习惯（红涨绿跌）。

This skill is ready for commercial/non-commercial use.

## Publisher:

[koradji77](https://clawhub.ai/user/koradji77)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to configure and run Chinese stock, ETF, and gold monitoring that checks price, volume, technical indicators, and cost-basis thresholds. The skill produces alerts and close-summary text that can be reviewed or routed to Feishu-style notifications.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles sensitive trading and cost-basis data in local files and alert messages.

Mitigation: Review notification content before use and avoid sending sensitive cost-basis data unless that exposure is acceptable.

Risk: The security evidence reports under-scoped Feishu notification behavior that should be reviewed before installation.

Mitigation: Remove or replace the default Feishu target and confirm exactly where alerts are sent before enabling notifications.

Risk: The skill persists trader-pattern and close-summary data locally.

Mitigation: Disable persistence if it is not needed, or periodically delete the local database and cache.

Risk: Long-lived daemon or cron usage can amplify dependency and process-control issues.

Mitigation: Pin dependencies and harden control.sh PID handling before running the monitor as a persistent process.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/koradji77/skills/stock-watcher-cn)
- [README](artifact/README.md)
- [用户指南](artifact/用户指南.md)
- [股票盯盯详细使用说明](artifact/股票盯盯详细使用说明.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with Python configuration snippets and shell commands; runtime output is plain-text stock alerts and close summaries.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Alerts may include market prices, holdings cost basis, technical indicators, and Feishu notification text.]

## Skill Version(s):

4.0.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
