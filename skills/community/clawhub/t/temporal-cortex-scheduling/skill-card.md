## Description: <br>
List events, find free slots, book meetings, merge multi-calendar availability, expand recurring events, and use atomic booking with Two-Phase Commit conflict prevention across Google Calendar, Outlook, and CalDAV. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[billylui](https://clawhub.ai/user/billylui) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Employees, external users, and developers use this skill to let an MCP-compatible agent discover calendars, inspect availability, expand recurring schedules, compose scheduling proposals, and book meetings across connected calendar providers. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The MCP server needs sensitive calendar access and may optionally access contacts. <br>
Mitigation: Review provider OAuth permissions, protect the local credential files, and prefer Local Mode unless cross-user Open Scheduling is required. <br>
Risk: Booking tools can create calendar events and send attendee details through Temporal Links. <br>
Mitigation: Require explicit user confirmation before calling booking tools or sending scheduling proposals, and verify attendee details before use. <br>
Risk: Calendar conflicts or concurrent booking attempts can affect scheduling accuracy. <br>
Mitigation: Use availability checks before booking and fall back to alternative slots when a conflict is reported. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/billylui/temporal-cortex-scheduling) <br>
- [Temporal Cortex homepage](https://temporal-cortex.com) <br>
- [Temporal Cortex MCP package](https://www.npmjs.com/package/@temporal-cortex/cortex-mcp) <br>
- [Calendar Tools Reference](references/CALENDAR-TOOLS.md) <br>
- [Multi-Calendar Operations](references/MULTI-CALENDAR.md) <br>
- [Booking Safety](references/BOOKING-SAFETY.md) <br>
- [Open Scheduling Guide](references/OPEN-SCHEDULING.md) <br>
- [RRULE Guide](references/RRULE-GUIDE.md) <br>
- [Temporal Links](references/TEMPORAL-LINKS.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands plus MCP tool outputs in TOON or JSON.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Calendar and optional contact data may be sensitive; booking tools can create calendar events after user confirmation.] <br>

## Skill Version(s): <br>
0.9.1 (source: server evidence, release metadata, and frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
