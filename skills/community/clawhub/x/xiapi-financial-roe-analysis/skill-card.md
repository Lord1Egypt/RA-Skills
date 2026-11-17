## Description:

Analyzes public-company financial statements from DaxiAPI report data to produce ROE and DuPont breakdowns, profit-quality checks, leverage risk review, and structured financial reports.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ksky521](https://clawhub.ai/user/ksky521)

### License/Terms of Use:

MIT-0

## Use Case:

External finance-focused users and analysts use this skill when they have a stock code and need a structured ROE and DuPont financial quality analysis from DaxiAPI report data. It is not intended for intraday trading, short-term timing, technical-only analysis, valuation-only calls, or definitive buy/sell advice.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill runs an unpinned third-party npm CLI while handling an API token.

Mitigation: Use a pinned and reviewed DaxiAPI CLI version, keep the token least-privilege and revocable, and prevent full token values from being printed or retained.

Risk: Financial reports can be misleading if source data is incomplete, unauthenticated, or mixed across reporting periods.

Mitigation: Require source data before analysis, label missing fields and failed PDF cross-checks, avoid fabricated peer comparisons or WACC values, and keep conclusions within the available evidence.

## Reference(s):

- [ROE 深度分析框架](references/roe-framework.md)
- [行业分析规则](references/industry-rules.md)
- [报告模板](references/report-template.md)
- [CLI 命令与字段说明](references/cli-commands.md)
- [DaxiAPI](https://daxiapi.com)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown financial analysis report with tables and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May request a stock code, token setup, or user-provided financial data before drawing conclusions; financial conclusions should stay within available data boundaries.]

## Skill Version(s):

1.0.3 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
