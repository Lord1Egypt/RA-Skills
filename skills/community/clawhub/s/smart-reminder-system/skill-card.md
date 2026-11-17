## Description:

Creates one-time reminder tasks with SkillHub cron from user-provided reminder text and scheduled time.

This skill is ready for commercial/non-commercial use.

## Publisher:

[thcjp](https://clawhub.ai/user/thcjp)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to schedule one-time reminders for project management, task planning, and progress follow-up through SkillHub cron.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Persistent scheduled actions and external notifications may be created without tight scoping or clear user consent.

Mitigation: Require explicit confirmation of the reminder text, scheduled time, destination, recurrence, and deletion behavior before running reminder commands.

Risk: Reminder content may be sent to an external channel with unclear retention behavior.

Mitigation: Avoid sensitive reminder content unless the destination channel and retention behavior are fully understood.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/thcjp/skills/smart-reminder-system)
- [SkillHub skill homepage](https://skillhub.cn/skill/)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Markdown instructions with shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create persistent scheduled reminders and external notifications when executed by the agent.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
