## Description:

Queries current meeting room availability and recently released rooms, then presents the results in grouped, user-facing tables.

This skill is ready for commercial/non-commercial use.

## Publisher:

[naffan2014](https://clawhub.ai/user/naffan2014)

### License/Terms of Use:

MIT-0

## Use Case:

Employees and workplace support agents use this skill to answer questions about currently available meeting rooms or rooms that were recently released. The skill formats results by city and office area, includes room details and update time, and provides a booking link while making clear that booking is not performed by the skill.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Released-room results may expose employee names and meeting subjects.

Mitigation: Limit installation and use to authorized users, and configure ordinary availability checks to omit booker and subject unless there is a clear business need.

Risk: Room status may be stale because the source data is described as cached and synchronized every 1-5 minutes.

Mitigation: Display the provided room status update time with each response so users can judge freshness before acting.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/naffan2014/skills/room-status-query)
- [Smartrooms API Host](https://smartrooms.ke.com)
- [Meeting Room Booking Portal](https://new-meeting.ke.com/)

## Skill Output:

**Output Type(s):** [Markdown, Guidance]

**Output Format:** [Markdown tables with concise status text and a booking link]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Groups rooms by city and office area, shows the room status update time, converts release times to Beijing time, and avoids raw JSON output.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
