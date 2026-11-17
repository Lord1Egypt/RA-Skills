## Description:

Automated financial indicator analysis for S&P 500 and NASDAQ stocks that scores and ranks stocks by weighted financial health metrics, detects red flags, and generates sector-level rankings.

This skill is ready for commercial/non-commercial use.

## Publisher:

[terrycarter1985](https://clawhub.ai/user/terrycarter1985)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, analysts, and agents use this skill to analyze CSV or JSON stock datasets, compare S&P 500 and NASDAQ equities, generate financial screening reports, identify high-risk stocks, and summarize sector rankings. It also provides guidance for Feishu/Lark permission settings when sharing generated reports.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated Markdown reports can include values from input datasets, so untrusted stock data may alter or inject content when reports are published or imported into collaboration tools.

Mitigation: Use trusted financial datasets, review generated Markdown before sharing, and sanitize or escape input-derived text before publishing reports.

Risk: Feishu/Lark permission guidance is advisory and does not enforce document access controls.

Mitigation: Manually configure and verify document permissions, link-sharing settings, external collaborator access, and access expiry in Feishu/Lark before sharing reports.

Risk: Financial scores and rankings depend on user-supplied data quality and fixed threshold logic.

Mitigation: Validate source data, treat results as screening support rather than investment advice, and review high-impact decisions with appropriate financial or compliance expertise.

## Reference(s):

- [Financial Indicators Reference](references/indicators.md)
- [SEC EDGAR](https://www.sec.gov/cgi-bin/browse-edgar)
- [Financial Modeling Prep](https://financialmodelingprep.com/)
- [Alpha Vantage](https://www.alphavantage.co/)
- [ClawHub Skill Page](https://clawhub.ai/terrycarter1985/skills/us-stock-financial-analyzer)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown reports or structured JSON generated from CSV/JSON financial data, plus usage commands and permission guidance.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs include financial health scores, metric scores, red flags, top and bottom stock rankings, and sector rankings.]

## Skill Version(s):

1.2.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
