## Description:

Automatically posts a daily Chinese-language morning brief with the current date, week number, weekend and holiday countdowns, and week, month, and year progress percentages.

This skill is ready for commercial/non-commercial use.

## Publisher:

[foxseller](https://clawhub.ai/user/foxseller)

### License/Terms of Use:

MIT-0

## Use Case:

Users and teams use this skill to receive an automatic morning reminder with China holiday countdowns and time-progress context. It is suited for personal or workplace daily briefing workflows that benefit from scheduled calendar status updates.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill contacts an external holiday-calendar endpoint and uses the returned holiday dates in its brief.

Mitigation: Review the endpoint trust and validate the generated dates before relying on the brief for planning decisions.

Risk: The skill writes a local holiday cache file.

Mitigation: Run it with expected workspace permissions and refresh or delete the cache if holiday data becomes stale.

Risk: Dependency versions are specified as ranges rather than exact pins.

Mitigation: Use a lockfile or pinned dependency versions for repeatable installation and stronger supply-chain control.

## Reference(s):

- [China Holiday Calendar Data Source](https://github.com/lanceliao/china-holiday-calender)

## Skill Output:

**Output Type(s):** [text]

**Output Format:** [Plain text Chinese morning brief]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Scheduled daily cron output; holiday calendar data is cached locally.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact package metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
