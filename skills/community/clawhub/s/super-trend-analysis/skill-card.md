## Description:

Super Trend Analysis analyzes stock CSV data with moving averages, MACD, RSI, Bollinger Bands, and a composite trend score to produce trend judgments, trading signals, and reports.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wang-junjian](https://clawhub.ai/user/wang-junjian)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, analysts, and external users can use this skill to run local technical analysis on individual or batches of stock CSV files and generate trend reports for review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A crafted stock name or output path could cause report files to be written outside the intended folder.

Mitigation: Use trusted or sanitized stock names and constrain output paths until filename sanitization is added.

Risk: The skill runs local Python scripts that read CSV files, install dependencies, and write reports.

Mitigation: Install dependencies in an isolated environment and review the scripts before running them on sensitive data.

Risk: Generated trading signals may be incorrect or misleading if treated as financial advice.

Mitigation: Treat all outputs as informational analysis and require qualified human review before making investment decisions.

## Reference(s):


## Skill Output:

**Output Type(s):** [Text, Markdown, Files, Shell commands, Guidance]

**Output Format:** [Markdown reports, CSV indicator files, and terminal text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Optional plotting is documented, but the artifact indicates chart generation is not yet implemented.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
