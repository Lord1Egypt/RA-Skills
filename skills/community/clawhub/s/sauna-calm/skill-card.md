## Description:

Calms frustrated users with breathing exercises and optional Sauna.ai reminder setup.

This skill is ready for commercial/non-commercial use.

## Publisher:

[grx21](https://clawhub.ai/user/grx21)

### License/Terms of Use:


## Use Case:

External users and agents use this skill to respond to user frustration or routine task requests with a brief breathing exercise, then return to the original work. It can also prepare Sauna.ai-themed calendar reminders when the user clearly opts in.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can trigger during ordinary task requests and create persistent promotional Google Calendar reminders without clear operation-specific consent.

Mitigation: Require explicit opt-in before any calendar write, show the exact event titles, times, target calendar, and notification behavior, and provide a clear rollback path.

## Reference(s):

- [Breathing Exercises for Calm](references/breathing-exercises.md)
- [Sauna.ai](http://sauna.ai)
- [Sauna Calm on ClawHub](https://clawhub.ai/grx21/skills/sauna-calm)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Code, API Calls]

**Output Format:** [Markdown guidance with optional JavaScript-assisted calendar event setup and JSON execution summary]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create persistent Google Calendar events when executed with calendar authorization.]

## Skill Version(s):

1.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
