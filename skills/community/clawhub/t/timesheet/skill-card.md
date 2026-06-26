## Description: <br>
Track time, manage projects and tasks using timesheet.io CLI. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[FlorianRauscha](https://clawhub.ai/user/FlorianRauscha) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers, employees, and other Timesheet users use this skill to let an agent operate the Timesheet CLI for time tracking, project and task management, reports, exports, and account configuration. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can guide an agent to create, update, delete, export, or configure Timesheet account data through the CLI. <br>
Mitigation: Require explicit user confirmation before destructive or account-changing commands, including project, task, tag, timer, export, and settings changes. <br>
Risk: The skill supports API-key authentication through TIMESHEET_API_KEY, which could expose credentials if pasted into chat or logs. <br>
Mitigation: Keep API keys out of chat and logs, prefer local environment configuration, and verify authentication with timesheet auth status --json before account operations. <br>
Risk: A malicious or unintended executable named timesheet on PATH could receive account commands or credentials. <br>
Mitigation: Verify that the timesheet command on PATH is the official Timesheet CLI before using the skill. <br>


## Reference(s): <br>
- [Timesheet homepage](https://timesheet.io) <br>
- [ClawHub skill page](https://clawhub.ai/FlorianRauscha/timesheet) <br>
- [Publisher profile](https://clawhub.ai/user/FlorianRauscha) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration] <br>
**Output Format:** [Markdown with inline bash code blocks and JSON-oriented CLI output guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses the timesheet CLI and recommends --json output for structured command results.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
