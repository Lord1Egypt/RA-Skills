## Description:

Analyzes China A-share stocks and ETFs across technical, valuation, risk, and fundamental dimensions and generates investment-analysis reports.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jy02577302-ux](https://clawhub.ai/user/jy02577302-ux)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, and investment researchers use this skill to analyze A-share stocks or ETFs, screen candidates, compare valuation and risk metrics, and draft Markdown or Word-style reports for human review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Investment reports and recommendations may be generated from mock or placeholder data.

Mitigation: Require source-data checks and human financial review before relying on any recommendation or report.

Risk: Unsafe local file-writing or cache behavior could expose or overwrite unintended local data.

Mitigation: Restrict output paths, validate ticker inputs, and clear or isolate cache directories between runs.

Risk: Authenticated data access could tempt users to provide browser session cookies.

Mitigation: Do not provide browser session cookies; use public data sources or vetted credentials only.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/jy02577302-ux/skills/stock-analysis-cn)
- [API Usage Guide for Stock Analysis](references/api_usage.md)
- [Factor Investing Reference](references/factors.md)
- [Technical Indicators Reference](references/indicators.md)
- [Valuation Benchmarks for A-Share Market](references/valuation_benchmarks.md)
- [Reference Documentation for Stock Analysis](references/api_reference.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown reports, tabular screening results, Python usage snippets, and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Scripts may write reports to a user-specified output path and may use a local cache when fetching market data.]

## Skill Version(s):

1.0.0 (source: server release metadata and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
