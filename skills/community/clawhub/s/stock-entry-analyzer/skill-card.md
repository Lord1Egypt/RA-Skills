## Description:

Stock Entry Analyzer analyzes stock and fund entry timing with BIAS, moving averages, MACD, RSI, KDJ, volume, fund-flow, and valuation checks, then returns an informational scored checklist and report.

This skill is ready for commercial/non-commercial use.

## Publisher:

[liuli4](https://clawhub.ai/user/liuli4)

### License/Terms of Use:

MIT-0

## Use Case:

External ClawHub users use this skill to screen watched stocks or funds and analyze a single symbol for entry timing based on technical indicators and valuation signals. Developers or operators may also run its bundled scripts for scheduled monitoring reports.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Bundled executable scripts can run local commands, call other finance-data skills, and pass the runtime environment to those tools.

Mitigation: Review scripts before execution, keep only needed finance-data integrations, and avoid exposing broad environment variables or credentials to downstream tools.

Risk: Some legacy scripts read an EastMoney credential vault.

Mitigation: Remove or restrict legacy scripts that access finance credentials unless that behavior is required and approved for the deployment environment.

Risk: Buy, sell, or entry outputs may be mistaken for personal financial advice.

Mitigation: Treat the reports as informational technical-analysis summaries and verify investment decisions through independent financial review.

## Reference(s):

- [Indicators](references/indicators.md)
- [Liu Chenming BIAS Method](references/liu-chenming-method.md)
- [Scoring Rules](references/scoring-rules.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown reports with scoring tables and checklists; optional JSON or plain text from helper scripts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs are informational stock-analysis summaries and should not be treated as personal financial advice.]

## Skill Version(s):

4.0.0 (source: server release evidence and README changelog)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
