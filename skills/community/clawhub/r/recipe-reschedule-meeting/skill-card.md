## Description: <br>
Move a Google Calendar event to a new time and automatically notify all attendees. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[googleworkspace-bot](https://clawhub.ai/user/googleworkspace-bot) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Agents and users managing Google Workspace calendars use this recipe to find an existing Google Calendar event, review its details, and reschedule it with attendee notifications. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The recipe can update the wrong calendar event or notify attendees with an unintended time change. <br>
Mitigation: Before running the patch, verify the Google account, calendar, event ID, attendee list, start and end time, and timezone. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/googleworkspace-bot/recipe-reschedule-meeting) <br>
- [Publisher profile: googleworkspace-bot](https://clawhub.ai/user/googleworkspace-bot) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown recipe with inline shell commands and JSON parameters] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires the gws CLI and the gws-calendar skill; the calendar patch sends updates to attendees.] <br>

## Skill Version(s): <br>
1.0.12 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
