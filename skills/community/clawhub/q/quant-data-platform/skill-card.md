## Description:

Quant Data Platform provides data infrastructure for Chinese A-share quantitative trading, including real-time quotes, historical market data, alternative data, factor data, and data quality monitoring.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jason-aka-chen](https://clawhub.ai/user/jason-aka-chen)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and quantitative trading teams use this skill to access and prototype A-share market data workflows for backtesting, research, live data review, factor analysis, and data quality checks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Production-looking market data APIs may silently return mock or random financial data.

Mitigation: Remove or explicitly gate mock/random paths before live trading, automated decisions, compliance checks, or serious backtests.

Risk: Market data results may lack clear source and provenance labeling.

Mitigation: Require every result to identify its data source and provenance before using it in analysis or trading workflows.

Risk: External data provider integrations may expose tokens or share requests with third-party services.

Mitigation: Pin dependencies, protect the Tushare token, and treat provider calls as external data sharing.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/jason-aka-chen/skills/quant-data-platform)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with Python and shell examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce or reference market data records, factor values, quality metrics, and configuration details for external data providers.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
