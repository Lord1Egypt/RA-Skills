## Description: <br>
Create Zoom meetings and add them to Google Calendar events with conference data, including the Zoom video entry, icon, and notes. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Shaharsha](https://clawhub.ai/user/Shaharsha) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to create Zoom meetings and attach them to new or existing Google Calendar events. It is intended for workflows where Zoom Server-to-Server OAuth credentials and Google Calendar CLI authentication are already configured. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses powerful Zoom and Google Calendar credentials and can modify calendar events. <br>
Mitigation: Use it only with accounts you are comfortable modifying, verify the exact calendar event ID before running it, and keep Zoom and Google credentials scoped and protected. <br>
Risk: Incorrect timezone or meeting details could create or update the wrong calendar information. <br>
Mitigation: Confirm the event ID, title, start time, duration, and timezone expectations before execution. <br>
Risk: Temporary token handling and shell JSON construction may expose credentials or produce malformed API payloads in some environments. <br>
Mitigation: Review the script before installation, prefer hardened token cleanup, and consider generating JSON payloads with jq. <br>


## Reference(s): <br>
- [Zoom Calendar Skill Page](https://clawhub.ai/Shaharsha/zoom-calendar) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with bash commands and setup instructions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The workflow creates a Zoom meeting, patches a Google Calendar event, and prints the join URL, meeting ID, and password.] <br>

## Skill Version(s): <br>
1.1.0 (source: release metadata and skill metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
