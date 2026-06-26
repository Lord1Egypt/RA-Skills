## Description: <br>
智能提醒小管家，支持定时提醒、情绪联动提醒、场景化提醒。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[786793119](https://clawhub.ai/user/786793119) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users use this skill to manage local reminders, including scheduled reminders, enable or disable states, emotion-linked suggestions, and weather-related reminders. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The submitted package references a helper Python script that is not included in the artifact. <br>
Mitigation: Review any separately obtained script before running it. <br>
Risk: Reminder content is retained locally under ~/.memory/reminders/reminders.json. <br>
Mitigation: Avoid storing highly sensitive reminders unless local retention is acceptable. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/786793119/smart-reminder-companion) <br>
- [Publisher profile](https://clawhub.ai/user/786793119) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown with inline shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires python3 and stores reminder data locally under ~/.memory/reminders/reminders.json.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
