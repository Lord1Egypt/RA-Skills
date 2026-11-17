## Description:

全功能智能股票监控预警系统。支持成本百分比、均线金叉死叉、RSI超买超卖、成交量异动、跳空缺口、动态止盈等7大预警规则。符合中国投资者习惯（红涨绿跌）。

This skill is ready for commercial/non-commercial use.

## Publisher:

[thirtyfang](https://clawhub.ai/user/thirtyfang)

### License/Terms of Use:

MIT

## Use Case:

External users can run this skill to monitor configured A-share, ETF, and gold positions for price, volume, moving-average, RSI, gap, and trailing-profit alert conditions. It produces ranked alert messages and market context for review, not investment advice.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A background monitor repeatedly sends watchlist-related queries to third-party financial services.

Mitigation: Run it only when that data sharing is acceptable, review configured holdings before use, and stop the daemon when monitoring is no longer needed.

Risk: Holdings and cost-basis values can expose sensitive portfolio information if committed or shared.

Mitigation: Keep edited configuration local, avoid committing portfolio details, and remove personal holdings before publishing logs or code.

Risk: Alert messages and generated suggestions may be mistaken for financial advice.

Mitigation: Treat alerts as review prompts, verify recommendations independently, and separate monitoring signals from investment decisions.

Risk: Some provider endpoints and source disclosures are incomplete or mixed across HTTP and HTTPS.

Mitigation: Prefer a version that documents data providers clearly and uses HTTPS for all network requests.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/thirtyfang/skills/stock-monitor-skill)
- [Publisher Profile](https://clawhub.ai/user/thirtyfang)
- [Eastmoney Suggest API](https://searchapi.eastmoney.com/api/suggest/get)
- [Sina Finance Search](https://search.sina.com.cn/?q={name}&c=news&sort=time)
- [Sina Quotes API](https://quotes.sina.cn/cn/api/quotes.php?symbol={code}&source=sina)
- [Eastmoney Quote API](https://push2.eastmoney.com/api/qt/stock/get)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown-style alert messages with inline shell commands and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Alerts may include prices, percentage changes, trigger details, sentiment summaries, and suggested review actions.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
