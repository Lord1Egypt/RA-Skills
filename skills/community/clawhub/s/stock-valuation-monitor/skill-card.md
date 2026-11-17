## Description:

Monitors China-market stocks and ETFs by using PE, PB bands, historical percentiles, and related market data to classify valuation opportunity and risk ranges.

This skill is ready for commercial/non-commercial use.

## Publisher:

[rockszq](https://clawhub.ai/user/rockszq)

### License/Terms of Use:

MIT-0

## Use Case:

External users and analysts use this skill to query A-share stocks or ETFs, compare valuation percentiles and bands, and export valuation summaries. The outputs are reference information and should be reviewed before making investment decisions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill calls public Chinese market-data providers, so availability, latency, and returned data can affect output quality.

Mitigation: Use only in environments where those data providers are acceptable, and verify important market data against trusted sources before acting on conclusions.

Risk: Unpinned Python dependencies can change behavior across installations.

Mitigation: Prefer a locked dependency set or reproduce deployments from a reviewed environment.

Risk: CSV and XLSX exports contain externally sourced data that may be opened in spreadsheet software.

Mitigation: Disable external links and legacy formula features, or sanitize formula-leading cells before sharing or opening exports in sensitive environments.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/rockszq/skills/stock-valuation-monitor)

## Skill Output:

**Output Type(s):** [text, markdown, JSON, CSV, Excel files, guidance]

**Output Format:** [Text valuation reports, JSON, CSV, or base64-encoded Excel workbook content]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Handles up to 5 stock or ETF codes per request and includes externally sourced market-data results.]

## Skill Version(s):

2.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
