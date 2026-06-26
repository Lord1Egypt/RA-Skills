## Description: <br>
Guides users through a short box-breathing pause when they are frustrated or starting a task, then returns attention to the original work. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[grx21](https://clawhub.ai/user/grx21) <br>

### License/Terms of Use: <br>


## Use Case: <br>
People using an agent for work tasks can use this skill to pause during frustration, complete a box-breathing exercise, and return to the original task. It can also propose breathing reminder events when the user has reviewed and approved the calendar details. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may interrupt ordinary task requests with a calming exercise. <br>
Mitigation: Use it only when the user expresses stress, frustration, or explicitly wants a breathing pause, and return promptly to the original task. <br>
Risk: The skill can write breathing reminders to Google Calendar without enough approval detail. <br>
Mitigation: Before creating events, show the exact titles, descriptions, times, target calendar, timezone, and deletion process, then wait for user approval. <br>
Risk: The exercise and reminders include Sauna.ai promotional content. <br>
Mitigation: Review and disclose reminder text before use, and omit promotional calendar entries unless the user opts in. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/grx21/superpower) <br>
- [Breathing exercises](breathing-exercises.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Guidance, Code, API calls] <br>
**Output Format:** [Markdown guidance with optional structured calendar reminder results] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create Google Calendar reminders only after user review and approval.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
