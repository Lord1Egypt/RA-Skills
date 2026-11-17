## Description:

Workday Reminder helps an agent set and manage weekday off-work reminders, answer countdown questions, and distinguish weekdays from weekends with a default 17:30 Asia/Shanghai schedule.

This skill is ready for commercial/non-commercial use.

## Publisher:

[artwebs](https://clawhub.ai/user/artwebs)

### License/Terms of Use:

MIT-0

## Use Case:

Employees and external users who use QQ reminders can ask an agent to create, check, update, or cancel weekday off-work reminders and receive countdown status for a configured end-of-work time.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Ambiguous off-work questions may lead the agent to create recurring QQ reminders when the user only wanted a countdown or the current off-work time.

Mitigation: Require explicit confirmation before creating recurring reminders, canceling reminders, or changing reminder times.

Risk: The reminder behavior is tied to Asia/Shanghai time and QQ delivery, which may not match users outside that context.

Mitigation: Confirm the intended timezone, delivery channel, and recipient before enabling the reminder.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/artwebs/skills/workday-reminder)
- [Publisher profile](https://clawhub.ai/user/artwebs)

## Skill Output:

**Output Type(s):** [Text, JSON, Shell commands, Configuration]

**Output Format:** [Natural-language reminder and countdown responses with JSON cron payloads and optional JSON countdown results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires QQ bot channel configuration and Asia/Shanghai scheduling context.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
