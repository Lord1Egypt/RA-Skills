## Description: <br>
Schedule Manager Free helps an agent turn natural-language timing requests into one-off or recurring local schedules with time-zone awareness and execution logs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[thcjp](https://clawhub.ai/user/thcjp) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, developers, and agent operators use this skill to create, inspect, pause, resume, and delete local reminder or automation schedules from natural-language requests while preserving task definitions across agent restarts. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Task text, preferences, and execution history are stored in local plaintext schedule files. <br>
Mitigation: Avoid putting secrets or highly sensitive personal details into scheduled task text, and review jobs.json and history files periodically. <br>
Risk: Scheduled tasks that call other skills may access capabilities beyond simple reminders. <br>
Mitigation: Require explicit user confirmation before granting another skill or permission to a scheduled task. <br>
Risk: Schedules only execute while the agent environment is available, so offline periods can delay or skip work. <br>
Mitigation: Check the schedule and execution history after restarts and use an external scheduler for critical time-sensitive obligations. <br>


## Reference(s): <br>
- [Schedule Manager Free on ClawHub](https://clawhub.ai/thcjp/skills/schedule-manager-free) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown and plain text with inline shell commands and JSON configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create or update local schedule files under ~/workspace/schedule when the user asks the agent to manage tasks.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and artifact metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
