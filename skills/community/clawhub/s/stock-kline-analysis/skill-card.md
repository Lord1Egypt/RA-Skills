## Description:

Given a stock name or code, this skill auto-detects the market, fetches six months of daily K-line data, computes technical indicators, renders a chart, and produces structured trend, valuation, relative-strength, and event-aware risk analysis.

This skill is ready for commercial/non-commercial use.

## Publisher:

[iideas18](https://clawhub.ai/user/iideas18)

### License/Terms of Use:

MIT-0

## Use Case:

External users, analysts, and developers use this skill to generate stock K-line charts and concise technical analysis from a stock name or code. It is most directly supported for A-share symbols, with documented HK and US symbol handling.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill contacts AkShare for public market, financial, and macro-event data, and those sources may be unavailable, delayed, or incomplete.

Mitigation: Verify important values against primary market or issuer sources before relying on the analysis.

Risk: The generated analysis could be mistaken for investment advice.

Mitigation: Treat the output as informational only and independently review any trading or portfolio decision.

Risk: The skill saves chart and report files to the selected local output directory.

Mitigation: Run it in a trusted workspace and review generated files before sharing them.

Risk: Evidence indicates reliable operation is primarily expected for A-share symbols, despite HK and US examples in the documentation.

Mitigation: Confirm non-A-share results against another data source and note unsupported valuation sections when data is unavailable.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/iideas18/skills/stock-kline-analysis)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance, files]

**Output Format:** [Structured text or Markdown-style analysis, plus locally saved TXT reports and PNG K-line charts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs depend on public AkShare market and financial data availability; reports are informational and not investment advice.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
