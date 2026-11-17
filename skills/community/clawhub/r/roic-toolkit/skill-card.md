## Description:

核心ROIC（投入资本回报率）深度分析助手。当用户提到 ROIC、投入资本回报率、资本效率、核心盈利能力、资本回报率分析、穿透ROIC、NOPAT、投入资本计算时自动使用。支持A股、港股、美股上市公司的ROIC精确计算。

This skill is ready for commercial/non-commercial use.

## Publisher:

[cgxxxxxxxxxxxx](https://clawhub.ai/user/cgxxxxxxxxxxxx)

### License/Terms of Use:

MIT-0

## Use Case:

External users and analysts use this skill to calculate and review core ROIC, NOPAT, invested capital, and multi-year capital efficiency for A-share, Hong Kong, and U.S. listed companies. It can run bundled Python scripts for baseline data collection and then guides manual review of annual-report footnotes before final conclusions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The package includes unrelated QQ bot setup instructions and dependencies that do not match the ROIC analysis purpose.

Mitigation: Do not follow the bundled QQ bot README or install the listed bot dependencies for ROIC analysis; run only the ROIC workflow for explicit ROIC tasks.

Risk: The skill fetches external financial data, SEC filings, and annual-report material, and its generated reports may be incomplete or stale.

Mitigation: Treat generated reports as drafts; verify source filings, data fields, and report dates before relying on the analysis.

Risk: Certain ROIC adjustments require judgment, including hidden financial assets, long-term equity investment splits, and acquired intangible amortization.

Mitigation: Manually review annual-report notes for all warning-marked items and document any final adjustments before presenting conclusions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/cgxxxxxxxxxxxx/skills/roic-toolkit)
- [finance-data API](https://www.codebuddy.cn/v2/tool/financedata)
- [SEC EDGAR company search](https://www.sec.gov/cgi-bin/browse-edgar)
- [Eastmoney annual-report notices](https://data.eastmoney.com/notices/)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, guidance]

**Output Format:** [Markdown reports, JSON data files, and shell command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated financial reports are drafts and may include manual-review warnings for annual-report footnotes and unavailable fields.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
