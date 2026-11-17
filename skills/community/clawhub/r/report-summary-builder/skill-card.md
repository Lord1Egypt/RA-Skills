## Description:

Builds weekly and monthly Markdown work summaries from existing daily report files.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bounding-elk](https://clawhub.ai/user/bounding-elk)

### License/Terms of Use:

MIT-0

## Use Case:

Employees and teams use this skill to turn existing daily Markdown reports into weekly or monthly work summaries with completed work, priorities, risks, plans, data source dates, and a short user-facing summary.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Weekly or monthly summary files may overwrite existing reports in the configured output directories.

Mitigation: Confirm the /data/reports paths and overwrite expectations before scheduled or repeated use.

Risk: Summaries can be incomplete when daily report files are missing for part of the reporting period.

Mitigation: Keep the required missing-report notice in the generated summary and review the source date range before sharing.

Risk: A summary may mislead readers if it adds conclusions not supported by the daily reports.

Mitigation: Review generated reports against the source daily Markdown files and keep the skill's no-fabrication rule in force.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/bounding-elk/skills/report-summary-builder)

## Skill Output:

**Output Type(s):** [Markdown, Files, Text]

**Output Format:** [Markdown report file plus a brief user-facing text summary]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reads daily Markdown reports from /data/reports/daily/ and writes weekly or monthly summaries to the configured report directories.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
