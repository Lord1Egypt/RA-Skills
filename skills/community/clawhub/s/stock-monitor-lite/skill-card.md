## Description:

Stock Monitor Lite monitors a configured China-focused stock, ETF, and gold watchlist for cost, price-move, volume, technical-indicator, gap, trailing-stop, and volatility alerts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[skytodmoon](https://clawhub.ai/user/skytodmoon)

### License/Terms of Use:

MIT-0

## Use Case:

External users use this skill to run scheduled OpenClaw monitoring of configured stocks, ETFs, and gold instruments and receive alert reports with market signals and informational suggestions. It is intended for notification and review workflows, not automated trading.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The bundled watchlist includes private-looking cost basis values that may expose portfolio positions or trading context in generated reports.

Mitigation: Review and replace the watchlist and all cost values before installing or scheduling the skill.

Risk: Recurring OpenClaw tasks and channel pushes can repeatedly send stock symbols, names, cost basis values, and profit/loss reports through the configured notification channel.

Mitigation: Enable scheduled runs and channel delivery only after confirming the selected channel is appropriate for this information.

Risk: The skill queries Sina and Eastmoney for market and news data, which discloses the configured symbols to external data services.

Mitigation: Use only symbols that are acceptable to share with those data sources and keep the watchlist minimal.

Risk: Generated trading suggestions may be misleading or over-weight lagging technical indicators.

Mitigation: Treat reports as informational alerts and review signals independently before making any investment decision.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/skytodmoon/skills/stock-monitor-lite)
- [Sina Finance quote endpoint](https://hq.sinajs.cn)
- [Eastmoney K-line endpoint](https://push2his.eastmoney.com/api/qt/stock/kline/get)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Chinese-language text or Markdown-style alert report with inline HTML bold tags]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports can include configured cost basis, profit/loss percentages, market data source labels, and an informational-only notice.]

## Skill Version(s):

1.0.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
