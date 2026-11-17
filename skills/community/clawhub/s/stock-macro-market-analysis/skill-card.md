## Description:

Generates Chinese-language macro and market analysis reports for A-share, U.S., and Hong Kong equities, covering index trends, market sentiment, capital flows, macro data, policy effects, global linkages, and sector rotation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wuritu](https://clawhub.ai/user/wuritu)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to produce broad market commentary, pre-market or post-market summaries, and sector-rotation analysis for Chinese-language stock and macro market workflows. Outputs should be treated as general information, not personalized investment advice.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Market scores, rankings, and position suggestions may be mistaken for personalized investment advice.

Mitigation: Use the output only as general market information, review source data and assumptions, and keep the disclaimer in generated reports.

Risk: Several helper scripts and the daily report template referenced by the skill are not present in the artifact.

Mitigation: Confirm package completeness or provide the missing tools and template before relying on the automated workflow.

Risk: Analysis quality depends on external stock data availability and the configured STOCK_DATA_API_KEY.

Mitigation: Verify data freshness, source coverage, and API availability before acting on conclusions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wuritu/skills/stock-macro-market-analysis)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown market analysis report with structured JSON examples and inline shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs should include data sources, timestamps, confidence labels, and a financial disclaimer; the package declares python3 and STOCK_DATA_API_KEY requirements.]

## Skill Version(s):

1.0.0 (source: release evidence and OpenClaw metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
