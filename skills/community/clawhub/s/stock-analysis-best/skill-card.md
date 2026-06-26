## Description: <br>
对上市公司进行系统性投资价值分析，包括基本面、技术面、估值和同业对比，并可生成 HTML/PDF 报告。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[newhackerman](https://clawhub.ai/user/newhackerman) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Investors, analysts, and finance-focused agents use this skill to gather public market data and produce structured investment-value analysis for A-shares, Hong Kong stocks, and U.S. stocks. It supports company analysis, technical checks, peer comparison, valuation, and downloadable report generation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The report feature starts an unauthenticated local HTTP server on port 8888. <br>
Mitigation: Use the report feature only where port 8888 is not exposed beyond the local machine or container, and stop the background server when finished. <br>
Risk: The skill can produce ratings, target prices, stop-losses, and allocation percentages that may be interpreted as actionable investment advice. <br>
Mitigation: Treat outputs as educational analysis, review source data and assumptions, and obtain qualified financial advice before making investment decisions. <br>
Risk: The skill fetches public market data and writes cached results, so data may be delayed, unavailable, or stale. <br>
Mitigation: Confirm market data freshness before relying on a report and fall back to authoritative filings or market-data providers when accuracy is material. <br>


## Reference(s): <br>
- [ClawHub skill listing](https://clawhub.ai/newhackerman/stock-analysis-best) <br>
- [Valuation methods reference](artifact/references/valuation-methods.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, code] <br>
**Output Format:** [Markdown and shell-command guidance with generated HTML reports that users can print or save as PDF] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May fetch public market data, cache JSON/text results, and start a local HTTP server on port 8888 for report access.] <br>

## Skill Version(s): <br>
1.4.0 (source: server release metadata; artifact files also mention 1.4.1 and 1.3.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
