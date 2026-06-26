## Description: <br>
投研鸭二级市场每日策略简报，每工作日更新，每4小时刷新行情。覆盖美股M7、GICS全板块、亚太、大宗、加密、聪明钱、AI产业链、预测市场，一键获取专业级市场洞察。支持历史归档查询和跨天趋势对比。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zewujiang](https://clawhub.ai/user/zewujiang) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and market-focused agents use this skill to fetch current or archived 投研鸭 secondary-market strategy briefings, summarize market conditions, and compare recent trends across equities, sectors, commodities, crypto, smart money, AI supply chain, and prediction-market signals. The skill is informational and should not be treated as financial advice. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may trigger outbound requests to api.touyanduck.com for market briefing data. <br>
Mitigation: Install and invoke it only when those outbound requests are acceptable, and use explicit invocation when tighter control is needed. <br>
Risk: Market commentary can be mistaken for personalized financial advice or may reflect delayed data. <br>
Mitigation: Treat outputs as informational market commentary, check the briefing timestamp before answering, and preserve the skill's disclaimer that it is not investment advice. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/zewujiang/touyanduck-briefing) <br>
- [Latest briefing Markdown endpoint](https://api.touyanduck.com/briefing.md) <br>
- [Archive index endpoint](https://api.touyanduck.com/archive/index.json) <br>
- [Latest briefing JSON endpoint](https://api.touyanduck.com/briefing.json) <br>
- [Markets JSON endpoint](https://api.touyanduck.com/markets.json) <br>
- [Watchlist JSON endpoint](https://api.touyanduck.com/watchlist.json) <br>
- [Risk radar JSON endpoint](https://api.touyanduck.com/radar.json) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, API Calls, Guidance] <br>
**Output Format:** [Markdown responses derived from remote Markdown or JSON briefing data, with inline shell command examples in the skill instructions.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The source briefing is refreshed every workday with market data refreshed every four hours; agents are instructed to check the briefing timestamp before answering.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
