## Description:

港股日报分析Agent - 每日发送《港股每日动量报告》到飞书

This skill is ready for commercial/non-commercial use.

## Publisher:

[wuchhao](https://clawhub.ai/user/wuchhao)

### License/Terms of Use:

MIT-0

## Use Case:

External users and market analysts use this skill to generate a weekday Hong Kong stock momentum report and send it to Feishu. The report summarizes market stance, a short-term watchlist with probabilities, and daily risk notes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The generated stock picks and probabilities could be mistaken for trading instructions.

Mitigation: Treat the report as informational analysis only and review it before making trading decisions.

Risk: The skill can post a scheduled report to Feishu and may use an optional market-data API key.

Mitigation: Confirm the posting schedule and destination before installation, and provide only the intended API key with appropriate account controls.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wuchhao/skills/stock-daily-report-hk)
- [Sina Finance Hong Kong stocks](https://finance.sina.com.cn/stock/hkstock/)
- [Eastmoney Hong Kong stocks](https://quote.eastmoney.com/center/gridlist.html#hk_stocks)
- [AAStocks](https://www.aastocks.com)
- [Futunn](https://www.futunn.com)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown report with market stance, watchlist probabilities, and risk notes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May use an optional FINNHUB_API_KEY and a weekday schedule to gather reference data and post the report to Feishu.]

## Skill Version(s):

1.0.7 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
