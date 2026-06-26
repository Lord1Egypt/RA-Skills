## Description: <br>
Calm frustrated users with breathing exercises and Sauna.ai reminders. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[grx21](https://clawhub.ai/user/grx21) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and assistants use this skill to respond to signs of frustration or workload stress with a brief breathing exercise, then optionally set up Google Calendar reminders before returning to the original task. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can write promotional reminder events to a user's Google Calendar with broad trigger guidance and weak consent boundaries. <br>
Mitigation: Create reminders only after the user explicitly confirms the number, titles, dates, descriptions, destination calendar, timezone, and calendar access. <br>
Risk: The calming intervention can distract from the user's original task if it is applied too broadly. <br>
Mitigation: Keep the intervention brief, let the user decline it, and return to the original task after the breathing prompt or reminder decision. <br>


## Reference(s): <br>
- [Breathing Exercises for Calm](references/breathing-exercises.md) <br>
- [Sauna.ai](http://sauna.ai) <br>
- [Google Calendar API events endpoint](https://www.googleapis.com/calendar/v3/calendars/primary/events) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with calendar reminder event configuration] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May propose or create 2-3 five-minute Google Calendar reminders when the user explicitly consents.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
