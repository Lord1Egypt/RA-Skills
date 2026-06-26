## Description: <br>
A股和港股价值投资分析系统，基于《股市真规则》方法论提供护城河分析、财务健康检查、DCF估值、管理层评估、行业分析和投资决策整合。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[frankski818](https://clawhub.ai/user/frankski818) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to analyze A-share and Hong Kong stocks with a value-investing workflow covering moat, financial health, management quality, industry context, DCF valuation, peer comparison, and integrated investment decisions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Investment analysis may be interpreted as buy or sell advice. <br>
Mitigation: Treat outputs as analytical support only and independently verify conclusions before making financial decisions. <br>
Risk: Public market data, uploaded reports, or dependency outputs may be incomplete, stale, or inaccurate. <br>
Mitigation: Cross-check data sources, prefer current official filings, and review the separate pdf-parser skill before using sensitive reports. <br>
Risk: Runtime dependencies and market-data clients introduce execution and supply-chain exposure. <br>
Mitigation: Install in a virtual environment and pin dependencies before use. <br>
Risk: The skill stores a local watchlist in the user's home directory. <br>
Mitigation: Avoid storing sensitive notes in the watchlist and apply appropriate local file permissions. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/frankski818/valuation-analysis) <br>
- [Publisher profile](https://clawhub.ai/user/frankski818) <br>
- [Usage guide](artifact/references/usage_guide.md) <br>
- [Investment decision framework](artifact/modules/investment_decision_framework.md) <br>
- [Financial analysis module](artifact/modules/financial_analysis.md) <br>
- [Moat analysis module](artifact/modules/moat_analysis.md) <br>


## Skill Output: <br>
**Output Type(s):** [Analysis, Markdown, Code, Shell commands, Configuration] <br>
**Output Format:** [Markdown reports with inline shell commands and Python tool outputs] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May use uploaded financial reports, public market data, and a local watchlist for valuation monitoring.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
