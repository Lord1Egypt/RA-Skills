## Description: <br>
日历同步工具基础版 helps an agent create calendar events, set reminders, view schedules, search events, and synchronize calendar entries across Google Calendar, Apple Calendar, and Outlook. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[thcjp](https://clawhub.ai/user/thcjp) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and individual operators use this skill to have an agent create reminders, review upcoming schedules, search events, and coordinate one-at-a-time synchronization across personal calendar platforms. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may handle credentials and synchronize or modify external calendar events while under-disclosing those actions. <br>
Mitigation: Review requested calendar changes before execution, confirm timezone and target platforms, and provide only the credentials or API access needed for the intended calendar account. <br>
Risk: The broad environment-variable check may expose sensitive variable names or secret-adjacent configuration in logs. <br>
Mitigation: Avoid running the broad environment-variable check; inspect only named required variables and keep secret values masked. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/thcjp/skills/ws-calendar-tool-free) <br>


## Skill Output: <br>
**Output Type(s):** [Text, JSON, Shell commands, Configuration guidance] <br>
**Output Format:** [Markdown guidance with JSON responses and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May propose command execution, configuration checks, external calendar-provider synchronization, and event creation; review target platforms, timezone, and credential use before running actions.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
