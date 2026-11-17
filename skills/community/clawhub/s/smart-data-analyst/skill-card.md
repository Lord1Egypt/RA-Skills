## Description:

Upload CSV, Excel, JSON, TSV, or pasted table data to receive a structured data analysis report with insights, anomalies, data quality notes, and recommendations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[a799549967-lang](https://clawhub.ai/user/a799549967-lang)

### License/Terms of Use:

MIT-0

## Use Case:

Employees, analysts, operators, and other non-technical users can upload or paste business data and ask the agent to summarize structure, detect anomalies, identify trends, and produce action-oriented recommendations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Uploaded datasets may contain sensitive or regulated data and may be processed by the user's configured AI provider.

Mitigation: Use only datasets appropriate for the configured AI provider and avoid relying on the skill's privacy wording unless the OpenClaw setup is local-only.

Risk: The active skill instructions include unrelated Telegram promotion.

Mitigation: Review the active instructions before deployment and remove promotional content if it is not acceptable for the target environment.

Risk: Broad natural-language triggers may activate the skill during general data questions.

Mitigation: Confirm user intent and dataset scope before processing uploaded or pasted data.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/a799549967-lang/skills/smart-data-analyst)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown report with overview tables, key findings, anomaly notes, data quality notes, and recommendations]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May sample large datasets and should state the sample size when sampling is used.]

## Skill Version(s):

1.3.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
