## Description: <br>
Analyzes uploaded CSV, Excel, JSON, TSV, SQL-export, or pasted table data and returns a structured report with data overview, findings, anomalies, quality notes, and actionable recommendations. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[a799549967-lang](https://clawhub.ai/user/a799549967-lang) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Business users, analysts, and operators use this skill in OpenClaw to turn uploaded or pasted tabular data into a plain-language markdown analysis report. It is intended for exploratory summaries, anomaly detection, trend review, data quality checks, and follow-up reporting without writing code. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Uploaded file contents, row samples, prompts, and derived reports may be sent to the user's configured AI provider, which can expose confidential, regulated, customer, financial, or proprietary data. <br>
Mitigation: Review before installing for sensitive-data workflows; use anonymized data or an AI provider whose privacy, retention, and compliance terms are acceptable. <br>
Risk: The artifact's user-facing safety language may understate third-party AI-provider processing risk. <br>
Mitigation: Tell users that configured AI providers may process uploaded data and require approval before using confidential or regulated datasets. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/a799549967-lang/smart-data-analyst) <br>
- [Operation guide](artifact/操作说明.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown report with tables, findings, anomaly warnings, data quality notes, and recommendations.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Shows a data overview before deeper analysis, uses Chinese for Chinese datasets, and may sample very large datasets while stating the sample size.] <br>

## Skill Version(s): <br>
1.3.0 (source: server-resolved release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
