## Description:

Trading Quant helps agents fetch real-time market data and produce multi-factor analysis for A-shares, US stocks, Hong Kong stocks, precious metals, capital flows, market anomalies, and global market overviews.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lanyasheng](https://clawhub.ai/user/lanyasheng)

### License/Terms of Use:

MIT

## Use Case:

Developers and analysts use this skill to route agent requests through quantitative market-data tools, including stock quotes, scoring, capital-flow checks, limit-up/down scans, and global market summaries. Outputs are for data display and analysis only, not investment advice.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill calls public finance and news websites, so queried symbols and analysis timing may be exposed to third-party services and affected by their availability.

Mitigation: Install and run the skill in an isolated Python environment, and review outbound network access before use.

Risk: The skill writes local market-data caches that may retain queried symbols, snapshots, and derived market state.

Mitigation: Store caches only in approved workspaces and clear them when local retention is not desired.

Risk: Optional sentiment model warm-up or downloads may retrieve mutable HuggingFace artifacts.

Mitigation: Avoid optional sentiment model warm-up and downloads unless HuggingFace network access and model provenance are approved.

Risk: Financial analysis output may be mistaken for investment advice.

Mitigation: Use the output as data analysis only and require human review before any trading or investment decision.

## Reference(s):

- [Trading Quant ClawHub skill page](https://clawhub.ai/lanyasheng/skills/trading-quant)

## Skill Output:

**Output Type(s):** [text, JSON, shell commands, guidance]

**Output Format:** [JSON responses and Markdown guidance with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Market-data freshness depends on public data sources and local caches.]

## Skill Version(s):

1.0.0 (source: frontmatter and server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
