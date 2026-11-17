## Description:

Load, analyze, and report on structured data from CSV/Excel/JSON files.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhaocaixia888](https://clawhub.ai/user/zhaocaixia888)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, analysts, and external users can use this skill to inspect structured CSV, Excel, JSON, or TSV datasets, compute descriptive statistics, identify anomalies, analyze trends and correlations, and produce concise analysis reports with chart recommendations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Optional package installation can introduce supply-chain or environment risk.

Mitigation: Use an isolated virtual environment and approved package sources before installing pandas or openpyxl.

Risk: Datasets provided for analysis may contain sensitive or confidential information.

Mitigation: Provide only datasets the agent is authorized to read and summarize, and redact sensitive fields when possible.

Risk: Statistical summaries, correlations, and anomaly flags can be misleading when data quality is poor or assumptions are not reviewed.

Mitigation: Review missing values, outliers, calculation methods, and stated caveats before using findings for decisions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/zhaocaixia888/skills/zcx-data-analyzer)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, guidance]

**Output Format:** [Markdown reports, tabular summaries, optional Python snippets, and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include descriptive statistics, anomaly rows, trend summaries, correlation notes, visualization recommendations, and explicit caveats.]

## Skill Version(s):

1.1.1 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
