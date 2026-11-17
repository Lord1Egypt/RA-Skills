## Description:

Tracks locally logged API token counts and generates daily or weekly Markdown reports with usage totals, trend indicators, and simple estimates.

This skill is ready for commercial/non-commercial use.

## Publisher:

[timyljob2011-sudo](https://clawhub.ai/user/timyljob2011-sudo)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and teams use this skill to log token counts locally and generate daily or weekly usage summaries for budget awareness and trend review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Local token-count history is persisted and may be written outside the documented skill folder.

Mitigation: Review and, if needed, fix the data path before running scripts; store logs only in an approved local location.

Risk: Recurring reports can be enabled through cron and may run commands automatically after installation.

Mitigation: Inspect any cron job before enabling scheduled reports, including the command path, schedule, and execution environment.

Risk: The skill describes automatic token recording, but the provided logger requires token counts to be supplied.

Mitigation: Wire reliable token-count collection into the logger or treat generated reports as manually maintained estimates rather than authoritative usage accounting.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/timyljob2011-sudo/skills/token-tracker-daily)
- [Artifact README](artifact/README.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown reports and command-line guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Persists local token-count history; reports depend on token counts supplied to the logger.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
