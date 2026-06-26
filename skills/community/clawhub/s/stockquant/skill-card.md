## Description: <br>
A股量化一站式：选股 + 持仓策略 + 个股分析（代码/名称查询，返回行情+日K+15分钟K+资金面+板块+公告）。Python 出数据+hint，LLM 按 [TASK] 推导决策。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[er6y](https://clawhub.ai/user/er6y) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use Stockquant to screen A-share candidates, review holdings and sell plans, and analyze individual stocks using market data, strategy hints, confidence labels, and risk-control prompts. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Stock screening and trade-plan suggestions may be incorrect, stale, or unsuitable for a user's financial situation. <br>
Mitigation: Treat outputs as decision support only; review confidence labels, evidence cards, and every suggested ORDER line before taking any downstream action. <br>
Risk: An optional Tushare token may be stored in local plaintext configuration. <br>
Mitigation: Save a token only when plaintext local storage is acceptable, and clear local configuration when it is no longer needed. <br>
Risk: Local caches, logs, and configuration can persist market data or user-provided settings after use. <br>
Mitigation: Clear local config, cache, and log files when the workflow is complete or when working on a shared machine. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/er6y/stockquant) <br>
- [Publisher profile](https://clawhub.ai/user/er6y) <br>
- [SKILL.md](SKILL.md) <br>
- [README.md](README.md) <br>
- [East Money finance data source](https://finance.eastmoney.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown/text CLI guidance with shell commands, market-data tables, NEXT_STEP task blocks, and structured ORDER signature lines] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces recommendations and trade-plan proposals for review; it does not connect to a brokerage or execute trades.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
