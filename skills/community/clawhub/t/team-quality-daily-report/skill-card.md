## Description:

Generate team quality daily report automatically

This skill is ready for commercial/non-commercial use.

## Publisher:

[bondli](https://clawhub.ai/user/bondli)

### License/Terms of Use:

MIT-0

## Use Case:

Employees, team leads, and quality managers use this skill to fetch team quality dashboard metrics, compare them with the previous day, and generate daily quality reports for synchronization, monitoring, and management review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill uses an authenticated browser session to capture and replay dashboard API requests.

Mitigation: Install it only for a trusted internal dashboard, use a dedicated browser profile or automation account, and keep the dashboard URL and API same-origin or explicitly approved.

Risk: Generated quality metrics and reports are stored locally under the user's home directory.

Mitigation: Protect ~/openclaw-skill-data with restrictive permissions and align retention with internal privacy and revocation requirements.

Risk: Scheduled execution can repeatedly access dashboard data without interactive review.

Mitigation: Do not enable cron scheduling until access scope, retention, and revocation expectations are clear.

## Reference(s):


## Skill Output:

**Output Type(s):** [Markdown, JSON, Files]

**Output Format:** [Markdown daily report and JSON metric snapshot saved as dated files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Stores dated outputs under ~/openclaw-skill-data/team-quality-daily-report/.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
