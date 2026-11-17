## Description:

Reliable runbook for scheduled reminders and notification workflows with OpenClaw cron.

This skill is ready for commercial/non-commercial use.

## Publisher:

[atomiccn](https://clawhub.ai/user/atomiccn)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and skill authors use this runbook to create or review scheduled reminder and notification workflows, including payload selection, session targeting, reminder text, validation, and troubleshooting.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Webhook delivery can expose reminder or run-result content to an unintended external endpoint if configured without care.

Mitigation: Use webhook delivery only for explicit user intent; confirm the destination is trusted, authenticated, HTTPS-protected, and receives only the minimum needed content.

Risk: Scheduled reminders can arrive at the wrong time or in the wrong place when timezone, payload type, or session target assumptions are not checked.

Mitigation: Validate the schedule shape, payload type, session target, enabled state, delivery mode, and timezone assumptions before relying on the job.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/atomiccn/skills/scheduler-notification-runbook)

## Skill Output:

**Output Type(s):** [guidance, markdown, configuration]

**Output Format:** [Markdown runbook guidance with inline configuration names and examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Provides decision rules, validation checks, and troubleshooting steps for scheduled reminder workflows.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
