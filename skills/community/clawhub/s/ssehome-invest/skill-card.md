## Description:

基于 baostock 金融数据库和 tavily-search 智能搜索的股票投资分析技能，提供完整的多时间框架技术分析、市场热点资讯追踪和投资报告生成功能。

This skill is ready for commercial/non-commercial use.

## Publisher:

[ssehome](https://clawhub.ai/user/ssehome)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to generate stock research reports for A-share equities, combining baostock market data, technical indicators, market news search, sentiment summaries, and investment-risk caveats.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The release ships an apparent hard-coded Tavily API key.

Mitigation: Revoke or remove the shipped key before installation and provide a user-owned Tavily key through a minimal environment variable or skill-specific secret file.

Risk: The skill reads a shared secrets file more broadly than needed.

Mitigation: Scope credentials to this skill and review secret-file access before running the analysis scripts.

Risk: Stock symbols, company names, and industry queries may be sent to Tavily during analysis.

Mitigation: Treat analyzed tickers and company names as information disclosed to Tavily, and disable or reconfigure news search when that disclosure is not acceptable.

## Reference(s):

- [baostock documentation](https://baostock.com/baostock/index.php/%E9%A6%96%E9%A1%B5)
- [Tavily documentation](https://docs.tavily.com/)
- [Tavily API key dashboard](https://app.tavily.com/)

## Skill Output:

**Output Type(s):** [analysis, markdown, files, guidance]

**Output Format:** [Markdown report with tabular technical analysis, market-news summaries, sentiment assessment, and investment-risk caveats]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Returns the report text and writes a stock-specific Markdown report under data/.]

## Skill Version(s):

1.0.4 (source: release evidence and SKILL.md, released 2026-04-07)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
