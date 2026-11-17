## Description:

Calendar helps users create events, set reminders, review upcoming schedules, and detect time conflicts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[fhbillwer](https://clawhub.ai/user/fhbillwer)

### License/Terms of Use:

MIT-0

## Use Case:

People using an agent for personal or work schedule management use this skill to create calendar entries, set reminders, check daily or weekly plans, and identify scheduling conflicts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad activation triggers could cause accidental calendar handling when the user did not intend to manage a schedule.

Mitigation: Review the trigger list before deployment and narrow or disable triggers where unexpected calendar actions would be disruptive.

Risk: Calendar events may contain personal information stored locally in /workspace/data/calendar/.

Mitigation: Confirm the local storage location, apply workspace access controls, and avoid storing sensitive details unless needed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/fhbillwer/skills/ws-calendar)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance, Files]

**Output Format:** [Plain text or Markdown responses, with local calendar data records when events are saved.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May store schedule data locally under /workspace/data/calendar/.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
