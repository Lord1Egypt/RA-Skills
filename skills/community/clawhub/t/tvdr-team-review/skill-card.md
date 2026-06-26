## Description: <br>
Guides a team through hourly retrospectives that capture mistakes, lessons learned, improvement actions, and reusable knowledge artifacts. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[admirobot](https://clawhub.ai/user/admirobot) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Team leads, project managers, and agent teams use this skill to run regular retrospectives, track decisions and task status, and turn repeated errors into reusable skill files, Obsidian notes, and memory logs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill asks agents to persist and share team memory broadly, which can expose secrets, personal data, or sensitive task context if boundaries are not set. <br>
Mitigation: Define allowed read and write locations before use, exclude secrets and personal data from shared memory, and require human review before generated skill files or persistent notes become active. <br>
Risk: Automated reminders, restarts, forwarding, or log access could affect team workflows beyond the intended retrospective process. <br>
Mitigation: Make cron jobs, auto-restart behavior, A2A forwarding, Feishu reminders, and API-log access opt-in, reversible, and scoped to approved channels. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/admirobot/tvdr-team-review) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Guidance, Configuration] <br>
**Output Format:** [Markdown templates, checklists, process guidance, and knowledge-base entries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce reusable skill files, Obsidian notes, memory logs, task records, decision registers, and retrospective action items.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
