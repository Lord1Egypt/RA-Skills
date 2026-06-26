## Description: <br>
Create a recurring Google Calendar event with attendees. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[googleworkspace-bot](https://clawhub.ai/user/googleworkspace-bot) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and workspace operators use this recipe to create a weekly Google Calendar event with attendees and verify it appears on the agenda. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Running the sample command unchanged can create a recurring event on the primary calendar and invite the sample attendee. <br>
Mitigation: Confirm gws is authenticated to the intended Google account and replace the calendar, time, recurrence rule, timezone, and attendee email before execution. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Guidance] <br>
**Output Format:** [Markdown with inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires the gws CLI, Google Workspace authentication for the intended account, and the gws-calendar skill before execution.] <br>

## Skill Version(s): <br>
1.0.12 (source: release evidence); artifact metadata version 0.22.5 <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
