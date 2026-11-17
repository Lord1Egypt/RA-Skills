## Description:

Three-factor stock analysis combining DCF valuation, Livermore trend trading rules, and VIX market sentiment to generate high-confidence buy signals for US equities.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lyflyd](https://clawhub.ai/user/lyflyd)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to screen US equities, compare value, trend, and market sentiment signals, and prepare buy-or-hold analysis for independent review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can produce BUY signals, position sizing, target prices, and stop-loss levels that may be incorrect or unsuitable for a user's financial situation.

Mitigation: Treat outputs as screening information only, verify assumptions and data independently, and use qualified financial review before making investment decisions.

Risk: API keys may be exposed if users place real credentials in config.yaml or commit local configuration files.

Mitigation: Use the FMP_API_KEY environment variable, keep local config files out of source control, and rotate any credential that may have been exposed.

Risk: Dependency versions are specified with lower bounds, so future package changes may alter behavior or introduce vulnerabilities.

Mitigation: Install in a virtual environment, review and pin dependency versions for production use, and scan the environment before deployment.

Risk: Market data quality, missing financial fields, delayed data, or model assumptions can materially affect valuation and sentiment outputs.

Mitigation: Cross-check source data, review DCF and threshold assumptions, and avoid using a single generated report as the sole decision basis.

## Reference(s):

- [Three-Factor Analysis Methodology](references/methodology.md)
- [Sample Analysis Report](examples/sample_report.md)
- [ClawHub Skill Page](https://clawhub.ai/lyflyd/skills/us-stock-analyzer)
- [Project Homepage](https://github.com/yourusername/us-stock-analyzer)
- [Financial Modeling Prep API](https://financialmodelingprep.com/api/v3)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown-style analysis reports, optional JSON result files, and optional chart image files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses live market and financial data from Yahoo Finance and optional FMP API data; outputs are screening information, not investment advice.]

## Skill Version(s):

1.0.0 (source: release metadata, SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
