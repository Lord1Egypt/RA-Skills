## Description:

Analyzes public companies' fundamentals and produces structured investment research reports covering financial health, valuation, growth, industry comparison, financial report interpretation, and shareholder tracking.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wuritu](https://clawhub.ai/user/wuritu)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, and analyst workflows use this skill to draft informational stock fundamental analysis reports with valuation metrics, scoring, data tables, source/date labels, and confidence notes. Outputs should be reviewed before use and are not investment advice.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill loads unreviewed local code from a toc-trading/src dependency outside its package.

Mitigation: Install only in a trusted workspace, review or package the local dependency, and prefer pinned dependencies before deployment.

Risk: The artifact describes more stock-analysis tools and dimensions than it ships.

Mitigation: Verify required tools and data paths before relying on each analysis dimension, and mark unavailable dimensions clearly in generated reports.

Risk: Stock-analysis output can be incorrect, stale, or mistaken for investment advice.

Mitigation: Keep the informational-only disclaimer, include data sources and cutoff dates, and require human review before acting on results.

Risk: The skill requires a stock-data API key.

Mitigation: Provide only a least-privileged key through the environment and avoid exposing secrets in generated reports or logs.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wuritu/skills/stock-fundamental-analysis)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown report with tables, scores, source and date labels, confidence notes, and an investment disclaimer; supporting tools may emit JSON.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires python3 and STOCK_DATA_API_KEY; output is primarily Chinese-language and informational only.]

## Skill Version(s):

1.0.0 (source: release metadata and openclaw metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
