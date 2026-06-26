## Description: <br>
Review your Google Calendar week, identify gaps, and add events to fill them. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[googleworkspace-bot](https://clawhub.ai/user/googleworkspace-bot) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
People managing a Google Calendar use this recipe to review their weekly agenda and free/busy gaps, then add a planned event such as a focused work block. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The recipe includes hardcoded sample dates and a calendar event insertion command, which could create an event at the wrong time if run without review. <br>
Mitigation: Before execution, show the event title, calendar, date, start and end time, attendees, and description, then ask the user to confirm or adjust the dates. <br>


## Reference(s): <br>
- [Recipe Plan Weekly Schedule on ClawHub](https://clawhub.ai/googleworkspace-bot/recipe-plan-weekly-schedule) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, guidance] <br>
**Output Format:** [Markdown with inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires the gws command-line tool and the gws-calendar skill.] <br>

## Skill Version(s): <br>
1.0.12 (source: server release metadata; artifact metadata version 0.22.5) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
