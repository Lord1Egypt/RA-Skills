## Description: <br>
基于TDX API的股票数据查询技能，提供A股市场实时行情、K线、分时成交、股票搜索、指数、ETF、市场统计、新闻和公告等查询能力。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bensema](https://clawhub.ai/user/bensema) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to configure and call a TDX-compatible stock data API for A-share market lookup, historical data retrieval, task management, and related market-data workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill runs local Python code and contacts external market-data services. <br>
Mitigation: Install and run it only in environments approved for outbound market-data API access, and configure API endpoints through trusted environment variables. <br>
Risk: Market data and generated signals may be incomplete, delayed, or unsuitable as financial advice. <br>
Mitigation: Treat outputs as informational or educational data and validate decisions against authoritative financial sources and qualified review. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/bensema/tdx-api-skill) <br>
- [README.md](artifact/README.md) <br>
- [SKILL.md](artifact/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [API Calls, Code, Shell commands, Configuration instructions, Guidance] <br>
**Output Format:** [Markdown guidance with Python examples, shell commands, and JSON-like API responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a configured TDX_API_URL; AKSHARE_API_URL is optional for stock news queries.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and artifact __version__) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
