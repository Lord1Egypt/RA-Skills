## Description:

Aggregate sales data from OKKI CRM and Campaign Tracker to generate weekly and monthly reports with alerts and Discord delivery.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cjboy007](https://clawhub.ai/user/cjboy007)

### License/Terms of Use:

MIT-0

## Use Case:

Sales and operations teams use this skill to collect OKKI CRM and optional campaign metrics, calculate funnel and trend indicators, generate weekly or monthly sales reports, and prepare alerts for Discord delivery.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can use broad local credential and configuration files for OKKI CRM access.

Mitigation: Run it in a dedicated workspace or service account with access limited to the intended OKKI CRM config and token files.

Risk: The Discord push flow can prepare arbitrary local report file contents for delivery.

Mitigation: Confirm Discord delivery is intended and restrict report inputs to approved report paths before running push commands.

Risk: Scheduled weekly and monthly runs can repeatedly collect data and prepare outbound alerts.

Mitigation: Confirm cron schedules and destination channels are wanted before enabling automation.

Risk: CRM authentication may be configured with non-approved endpoints.

Mitigation: Require HTTPS and approved hosts for CRM authentication and API access.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/cjboy007/skills/ssa-sales-dashboard)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown reports, JSON metrics and snapshots, console summaries, and Discord push instruction JSON]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes local report, snapshot, latest metrics, calculated metrics, and log files when run outside dry-run mode.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
