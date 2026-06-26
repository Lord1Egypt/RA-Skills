## Description: <br>
股票组合管理与预警技能。支持 A 股/港股/美股行情查询、持仓跟踪、收益计算、价格预警、每日推荐。使用免费 API（腾讯财经），数据本地存储。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yinshengf](https://clawhub.ai/user/yinshengf) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to query A-share, Hong Kong, and U.S. stock quotes, track local portfolio holdings, calculate profit and loss, configure price alerts, and generate a daily watchlist. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Portfolio holdings, cost basis, share counts, and alert thresholds are stored in local files. <br>
Mitigation: Use the skill only on trusted workspaces and avoid entering portfolio data that should not be stored locally. <br>
Risk: Queried stock symbols may be sent to Tencent, Sina, or EastMoney APIs over HTTP, and returned prices should not be treated as tamper-resistant. <br>
Mitigation: Use the quote data for convenience checks only and verify important trading decisions against trusted brokerage or market-data sources. <br>
Risk: Daily picks are a rough watchlist and do not perform the fundamental analysis the skill text may imply. <br>
Mitigation: Treat recommendations as informational leads, not investment advice, and apply independent research and risk controls. <br>


## Reference(s): <br>
- [Stock data API documentation](references/api_docs.md) <br>
- [Recommendation strategy](references/recommendation_strategy.md) <br>
- [Cron setup](references/cron_setup.md) <br>
- [ClawHub skill page](https://clawhub.ai/yinshengf/stock-portfolio) <br>
- [Publisher profile](https://clawhub.ai/user/yinshengf) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown tables, plain text status messages, optional JSON from scripts, and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs may include live or delayed market quotes, local portfolio summaries, alert status, and daily watchlist recommendations.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
