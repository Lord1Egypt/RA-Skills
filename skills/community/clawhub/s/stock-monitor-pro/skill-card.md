## Description:

Stock Monitor Pro is a Chinese-market stock monitoring and alerting skill for A-shares and ETFs, with daily close reports, price and cost-basis alerts, technical indicators, volume anomaly monitoring, redundant data sources, and error notifications.

This skill is ready for commercial/non-commercial use.

## Publisher:

[eaveluo](https://clawhub.ai/user/eaveluo)

### License/Terms of Use:

MIT

## Use Case:

External users and developers use this skill to monitor configured Chinese-market holdings, receive price and indicator alerts, and generate end-of-day portfolio summaries. It is intended for informational monitoring workflows, not as a sole basis for trading decisions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill runs as a background process and repeatedly queries third-party market-data providers.

Mitigation: Run it only in an environment where persistent monitoring and outbound finance-data requests are acceptable, and review the polling frequency before deployment.

Risk: Market data may come from third-party providers or plaintext fallback sources.

Mitigation: Verify alerts against trusted data sources before acting on them, especially when a fallback source or data-source error notification is reported.

Risk: Generated alerts and suggestions can resemble investment advice.

Mitigation: Treat outputs as informational signals only and require independent financial review before making trading decisions.

Risk: Proxy, scraping, and anti-bot behavior may be unsuitable for some deployments.

Mitigation: Review or remove scraping, browser-header simulation, random-delay, and proxy-related behavior before commercial or managed use.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/eaveluo/skills/stock-monitor-pro)
- [Publisher profile](https://clawhub.ai/user/eaveluo)
- [Sina Finance market data endpoint](https://hq.sinajs.cn/list=)
- [Eastmoney quote and kline data endpoint](https://push2his.eastmoney.com/api/qt/stock/kline/get)
- [Tencent Finance market data endpoint](https://qt.gtimg.cn/q=)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown and terminal text with Python configuration examples and shell command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces stock alerts, data-source diagnostics, and daily close summaries for configured watchlists.]

## Skill Version(s):

2.1.0 (source: SKILL.md frontmatter, ClawHub release metadata, artifact metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
