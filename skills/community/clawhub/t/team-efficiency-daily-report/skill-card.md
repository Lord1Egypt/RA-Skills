## Description:

Generate team efficiency daily report automatically.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bondli](https://clawhub.ai/user/bondli)

### License/Terms of Use:

MIT-0

## Use Case:

Employees and managers use this skill to collect configured team-efficiency dashboard data and generate daily delivery-status reports for team syncs, delivery monitoring, and management updates.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may reuse an authenticated browser session to access internal dashboard and API data.

Mitigation: Run it only with explicit authorization for the configured dashboard, and review the dashboard URL and API endpoint before execution.

Risk: Generated JSON and Markdown reports may contain internal team-efficiency data saved on the local filesystem.

Mitigation: Store outputs in an access-controlled location and define a retention or deletion process for generated report files.

Risk: Unattended cron execution can repeatedly collect data without ongoing operator review.

Mitigation: Enable scheduling only in an isolated environment with pinned dependencies and a documented removal path.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/bondli/skills/team-efficiency-daily-report)
- [ClawHub publisher profile](https://clawhub.ai/user/bondli)

## Skill Output:

**Output Type(s):** [Markdown, JSON, Files]

**Output Format:** [Daily Markdown report and JSON data files saved by date]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a configured dashboard URL, data API, and column mapping; generated files may contain internal team-efficiency data.]

## Skill Version(s):

1.0.0 (source: server release metadata; artifact package.json reports 1.0.2)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
