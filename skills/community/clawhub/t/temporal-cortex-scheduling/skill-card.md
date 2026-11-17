## Description:

List events, find free slots, and book meetings across Google Calendar, Outlook, and CalDAV. Multi-calendar availability merging, recurring event expansion, and atomic booking with Two-Phase Commit conflict prevention.

This skill is ready for commercial/non-commercial use.

## Publisher:

[billylui](https://clawhub.ai/user/billylui)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to inspect calendars, find open time, expand recurring schedules, compose meeting proposals, and book confirmed meetings across supported calendar providers.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The MCP server handles OAuth tokens and can access configured calendar providers.

Mitigation: Install only when that calendar access is acceptable, treat credentials.json as sensitive secret material, and prefer Docker containment for higher assurance.

Risk: Installation runs calendar-authentication code from npm and uses a downloaded native binary.

Mitigation: Use the pinned package @temporal-cortex/cortex-mcp@0.9.1 and verify release checksums before first use.

Risk: Booking tools can create calendar events or bookings on external calendars.

Mitigation: Confirm booking details with the user before write tools run, and check availability before booking.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/billylui/skills/temporal-cortex-scheduling)
- [Temporal Cortex homepage](https://temporal-cortex.com)
- [Temporal Cortex skills repository](https://github.com/temporal-cortex/skills)
- [Temporal Cortex MCP package](https://www.npmjs.com/package/@temporal-cortex/cortex-mcp)
- [Calendar Tools Reference](references/CALENDAR-TOOLS.md)
- [Multi-Calendar Operations](references/MULTI-CALENDAR.md)
- [RRULE Guide](references/RRULE-GUIDE.md)
- [Booking Safety](references/BOOKING-SAFETY.md)
- [Temporal Links](references/TEMPORAL-LINKS.md)
- [Open Scheduling Guide](references/OPEN-SCHEDULING.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with tool workflows, tables, JSON examples, and shell command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs may guide calls to an MCP server that reads calendar data and can create calendar bookings after user confirmation.]

## Skill Version(s):

0.9.1 (source: server release evidence and artifact metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
