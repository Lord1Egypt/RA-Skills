## Description:

Creates recurring workday stand-up reminders with configurable hours, interval, timezone, language, message style, and optional holiday skipping.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tinalucky](https://clawhub.ai/user/tinalucky)

### License/Terms of Use:

MIT-0

## Use Case:

Employees and desk workers use this skill to set up recurring movement reminders during work hours. It helps an agent create, describe, and manage cron-based stand-up reminders with sensible defaults and user-controlled schedule changes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill creates ongoing cron reminders that may keep firing after the user's needs or work schedule change.

Mitigation: Confirm the desired reminder schedule, timezone, language, and work hours before creation, and use the documented list, update, pause, or remove commands when reminders are no longer wanted.

Risk: Holiday skipping depends on the executing agent correctly identifying holidays and adjusted workdays.

Mitigation: Enable holiday skipping only when useful for the user, and ask the user to confirm regional holiday behavior when dates are outside the agent's reliable knowledge.

## Reference(s):

- [Message Templates](artifact/references/messages.md)
- [Holiday Skip Guide](artifact/references/holidays.md)

## Skill Output:

**Output Type(s):** [text, configuration, shell commands, guidance]

**Output Format:** [Markdown text with cron configuration examples and reminder-management commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Creates ongoing cron reminders; users can list, update, pause, resume, or remove reminders.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
