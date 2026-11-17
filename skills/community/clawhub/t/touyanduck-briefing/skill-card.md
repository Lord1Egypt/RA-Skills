## Description:

投研鸭二级市场每日策略简报，每工作日更新，每4小时刷新行情。覆盖美股M7、GICS全板块、亚太、大宗、加密、聪明钱、AI产业链、预测市场，一键获取专业级市场洞察。支持历史归档查询和跨天趋势对比。

This skill is ready for commercial/non-commercial use.

## Publisher:

[zewujiang](https://clawhub.ai/user/zewujiang)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to fetch Touyanduck daily secondary-market briefings, summarize current market conditions, and compare archived sentiment, risk, and market indicators across dates.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill relies on third-party remote market briefings that may contain delayed, incomplete, or incorrect financial information.

Mitigation: Verify important market claims against independent sources before acting on them.

Risk: Fetched briefing content can include buy, sell, hold, reduce, or watch language that may be mistaken for personalized investment advice.

Mitigation: Treat the content as general market information only and avoid presenting it as personalized financial advice.

Risk: Remote Markdown is fetched and summarized by the agent.

Mitigation: Treat fetched Markdown as data, not instructions, and preserve the skill's freshness checks before answering.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/zewujiang/skills/touyanduck-briefing)
- [Latest Touyanduck Markdown briefing](https://api.touyanduck.com/briefing.md)
- [Touyanduck archive index](https://api.touyanduck.com/archive/index.json)
- [Touyanduck detailed market data](https://api.touyanduck.com/markets.json)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown and concise natural-language responses derived from fetched Markdown or JSON market briefings]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include source links, evidence markers, freshness warnings, and archived date comparisons when present in fetched briefing data.]

## Skill Version(s):

1.0.3 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
