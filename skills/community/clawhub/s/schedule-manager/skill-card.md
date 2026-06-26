## Description: <br>
Helps agents view, add, edit, pause, delete, and clean up scheduled tasks and one-time reminders. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cowboy231](https://clawhub.ai/user/cowboy231) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Employees, external users, and developers can use this skill to manage recurring local reminders, one-time reminders, and schedule-related task configuration from an OpenClaw workspace. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can create and change cron jobs on the user's machine. <br>
Mitigation: Review schedule changes before running commands and prefer a release with explicit confirmations, validation, managed cron entries, and clear cleanup instructions. <br>
Risk: Reminder content may be sent through Feishu with incomplete privacy disclosure. <br>
Mitigation: Avoid sensitive reminder text and confirm notification destinations and privacy expectations before use. <br>


## Reference(s): <br>
- [ClawHub skill release](https://clawhub.ai/cowboy231/schedule-manager) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration] <br>
**Output Format:** [CLI text output with Markdown-backed task configuration and YAML-like temporary reminder records] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May write schedule files and crontab entries in the user's OpenClaw workspace.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
