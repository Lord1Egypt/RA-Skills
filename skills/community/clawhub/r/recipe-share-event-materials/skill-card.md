## Description: <br>
Share Google Drive files with all attendees of a Google Calendar event. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[googleworkspace-bot](https://clawhub.ai/user/googleworkspace-bot) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Employees or operators with Google Workspace access use this recipe to share a selected Drive file with attendees from a Google Calendar event and verify the resulting permissions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The recipe can grant Google Drive access to the wrong people if the calendar event, file, or attendee list is incorrect. <br>
Mitigation: Confirm the exact event, Drive file, and recipients before creating permissions, then review the permission list after sharing. <br>
Risk: Drive access may remain longer than intended for external guests or broad meeting lists. <br>
Mitigation: Revoke permissions after the event when access should be temporary. <br>
Risk: Execution depends on local gws tooling and referenced Google Workspace skills. <br>
Mitigation: Install and use this recipe only in environments where the gws toolchain and required skills are trusted. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/googleworkspace-bot/recipe-share-event-materials) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Guidance] <br>
**Output Format:** [Markdown with inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires the gws binary and the gws-calendar and gws-drive skills.] <br>

## Skill Version(s): <br>
1.0.12 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
