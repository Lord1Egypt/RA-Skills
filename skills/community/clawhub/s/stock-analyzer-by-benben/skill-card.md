## Description:

Stock Analyzer fetches public market data, calculates technical and fundamental indicators, generates Markdown reports and optional charts, and provides simple historical-trend price predictions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[utopiabenben](https://clawhub.ai/user/utopiabenben)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers can use this skill to analyze publicly traded stocks, inspect technical and fundamental signals, and create reviewable reports from Yahoo Finance data. Its generated predictions and trading language should be treated as informational analysis, not financial advice.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: User-supplied ticker symbols can affect where report and chart files are written.

Mitigation: Run the skill in a virtual environment without elevated privileges, use ordinary ticker symbols, and keep report and chart paths constrained to the configured output directory.

Risk: Generated analyses and simple historical-trend predictions may be mistaken for investment recommendations.

Mitigation: Treat outputs as informational analysis only and review financial decisions independently before acting.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/utopiabenben/skills/stock-analyzer-by-benben)

## Skill Output:

**Output Type(s):** [Text, Markdown, Files, Charts, Guidance]

**Output Format:** [Console text, Markdown reports, and optional PNG chart files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports and charts are written under the configured output directory; market data comes from Yahoo Finance and may be delayed.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact skill.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
