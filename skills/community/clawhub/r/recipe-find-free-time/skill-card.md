## Description: <br>
Query Google Calendar free/busy status for multiple users to find a meeting slot. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[googleworkspace-bot](https://clawhub.ai/user/googleworkspace-bot) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Employees, external collaborators, and developers use this recipe to query multiple Google Calendar free/busy schedules, identify overlapping availability, and create a meeting event in an available slot. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The recipe can create a Google Calendar event and may notify invitees if executed with the wrong account, attendees, title, start time, or end time. <br>
Mitigation: Before running the insert command, verify the Google account, target calendar, attendees, event title, start time, and end time. <br>
Risk: The recipe depends on the local gws setup and the gws-calendar skill. <br>
Mitigation: Install and use it only in environments where the gws configuration and gws-calendar skill are already trusted. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/googleworkspace-bot/recipe-find-free-time) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Guidance] <br>
**Output Format:** [Markdown with inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces Google Workspace CLI commands and human review guidance for selecting a meeting slot before event creation.] <br>

## Skill Version(s): <br>
1.0.13 (source: ClawHub release evidence; artifact metadata version 0.22.5) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
