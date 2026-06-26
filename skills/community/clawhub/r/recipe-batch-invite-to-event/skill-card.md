## Description: <br>
Add a list of attendees to an existing Google Calendar event and send notifications. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[googleworkspace-bot](https://clawhub.ai/user/googleworkspace-bot) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Employees, administrators, and agents managing Google Workspace calendars use this skill to add multiple attendees to an existing event and send invite notifications through a repeatable CLI workflow. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The patch step modifies an existing calendar event and can email invite notifications to every added attendee. <br>
Mitigation: Verify the active Google account, calendar event ID, and attendee email list before running the patch command. <br>
Risk: Using the wrong event ID or attendee list could update the wrong event or notify unintended recipients. <br>
Mitigation: Fetch the event before the update and verify the attendee list again after the update. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/googleworkspace-bot/recipe-batch-invite-to-event) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, API Calls] <br>
**Output Format:** [Markdown with inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires the gws CLI and the gws-calendar prerequisite skill.] <br>

## Skill Version(s): <br>
1.0.12 (source: release evidence; skill metadata version 0.22.5) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
