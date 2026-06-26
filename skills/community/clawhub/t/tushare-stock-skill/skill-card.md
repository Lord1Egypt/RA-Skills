## Description: <br>
面向中国 A 股的 Tushare 专用技能，提供股票数据获取、个股分析与交易观察能力。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Magica-Chen](https://clawhub.ai/user/Magica-Chen) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to query and analyze China A-share stock data through Tushare. It supports stock data retrieval, individual-stock fundamentals and valuation analysis, risk signals, funds-flow review, leaderboard data, and technical trading observations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a Tushare token and can optionally read it from a file path. <br>
Mitigation: Provide only the intended TUSHARE_TOKEN, and set TUSHARE_STOCK_ENV_FILE only to a small file containing that token. <br>
Risk: Runtime commands access external Tushare endpoints, and realtime crawler data may have compliance or reliability limits. <br>
Mitigation: Treat returned market data as external-source data, verify important results against authoritative sources, and confirm that use of realtime endpoints fits the deployment context. <br>
Risk: Unpinned Python dependencies can change behavior over time in production or automated workflows. <br>
Mitigation: Install in a virtual environment and pin dependencies for production or automated trading workflows. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/Magica-Chen/tushare-stock-skill) <br>
- [Project homepage](https://github.com/Magica-Chen/tushare-stock-skill) <br>
- [Tushare official stock-data index](https://tushare.pro/document/2?doc_id=14) <br>
- [Machine-readable stock endpoint catalog](references/stock_endpoints.json) <br>
- [Human-readable stock endpoint summary](references/stock_endpoints.md) <br>
- [Technical indicator registry](scripts/trading_analysis.py) <br>


## Skill Output: <br>
**Output Type(s):** [text, json, shell commands, configuration, guidance] <br>
**Output Format:** [Structured JSON with Simplified Chinese text and occasional shell command examples.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include raw Tushare rows, analysis summaries, called endpoint names, and access-limit notes.] <br>

## Skill Version(s): <br>
1.0.3 (source: frontmatter and release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
