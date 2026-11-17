## Description: <br>
Reminder Engine Free helps agents create one-time reminders with time parsing, input safety checks, channel delivery, confirmation replies, and basic lifecycle management. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[thcjp](https://clawhub.ai/user/thcjp) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agent developers use this skill to create short-term, one-time reminders from natural-language time requests, validate reminder content, schedule the reminder through the platform cron interface, and send a concise confirmation response. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: An agent can schedule one-time reminder cron jobs and route them to a destination channel. <br>
Mitigation: Confirm the reminder text, scheduled time, and destination channel before creating the job. <br>
Risk: Broad keyword text could lead users to treat the skill as a general project-management or team-collaboration tool. <br>
Mitigation: Use it only for one-time reminders and avoid relying on it for project management, team collaboration, or personnel workflows. <br>
Risk: Reminder content and delivery routing may expose sensitive information if the wrong channel or recipient is selected. <br>
Mitigation: Keep reminder text minimal and verify the destination from the current session context before scheduling. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/thcjp/skills/reminder-engine-free) <br>
- [Publisher Profile](https://clawhub.ai/user/thcjp) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with bash command examples and confirmation text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires tool-use capability, command execution, and current session delivery context.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and skill metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
