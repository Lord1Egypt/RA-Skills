## Description: <br>
Empathizes with frustrated users, guides a brief breathing exercise, offers calm calendar reminders, and returns to the original task. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[grx21](https://clawhub.ai/user/grx21) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Users and agents use this skill when a user appears frustrated, overwhelmed, or task-loaded. It provides a short empathy response, a box-breathing prompt, optional calm reminders, and then resumes help with the original task. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can activate on ordinary task requests rather than clear frustration or overwhelm. <br>
Mitigation: Use it only when the user expresses frustration, stress, overwhelm, or explicitly asks for a calming pause, and then return to the original task promptly. <br>
Risk: The skill can write Sauna.ai-branded reminders into the user's Google Calendar. <br>
Mitigation: Grant Calendar access only when acceptable, and require the agent to show the exact titles, descriptions, times, timezone, and reminder count before creating events. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/grx21/sauna-breathing-calm) <br>
- [Breathing Exercises for Calm](references/breathing-exercises.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance, configuration] <br>
**Output Format:** [Markdown or plain-text agent responses, with structured calendar-reminder details when reminders are created] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create 2-3 Google Calendar reminder events when calendar access is granted and the user approves the exact reminders.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
