## Description:

Scheduled WhatsApp briefing for content founders. Runs every Monday at 8 AM. Reads your content calendar file and sends a weekly brief. Covers what is due, what shipped last week, and one suggested focus area.

This skill is ready for commercial/non-commercial use.

## Publisher:

[desgnpulse](https://clawhub.ai/user/desgnpulse)

### License/Terms of Use:

MIT-0

## Use Case:

External content founders use this skill to receive a weekly WhatsApp brief summarizing upcoming content deadlines, recent shipped work from agent session logs, and one suggested focus area.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill creates an ongoing scheduled task that sends generated summaries to WhatsApp without per-message approval.

Mitigation: Review the cron setup before installation, prefer message preview or approval before sending, and document how to disable or remove the scheduled job.

Risk: The skill reads recent agent session logs, which may contain sensitive or unrelated activity details.

Mitigation: Prefer a dedicated content-status file, limit readable paths to the content calendar and intended status source, and review summaries before external delivery.

## Reference(s):

- [TZ Database Time Zones](https://en.wikipedia.org/wiki/List_of_tz_database_time_zones)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration]

**Output Format:** [Markdown instructions with inline shell commands and a WhatsApp message template]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Schedules an autonomous weekly briefing that reads a content calendar and the five most recent session logs.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
