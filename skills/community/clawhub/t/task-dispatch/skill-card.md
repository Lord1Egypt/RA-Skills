## Description: <br>
Task scheduling and dispatching for task boards. Use when setting up periodic task dispatch, checking for dispatchable tasks, creating subagents to execute tasks, or verifying task completion. Supports task board APIs like ClawBoard. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cccaptain0129](https://clawhub.ai/user/cccaptain0129) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to configure task-board dispatch, select auto-executable tasks, delegate them to subagents, verify deliverables, and update task status. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill guides users to install and run an external ClawBoard service before dispatching tasks. <br>
Mitigation: Review the ClawBoard repository and installer before execution, as directed by the server security guidance. <br>
Risk: Task-board API tokens are copied into workspace environment files. <br>
Mitigation: Use a least-privilege token and keep workspace .env files private and out of source control. <br>
Risk: Recurring dispatch can cause automatic subagent execution and task-state updates. <br>
Mitigation: Enable scheduled dispatch only for task boards where automatic execution and status updates are expected. <br>


## Reference(s): <br>
- [Task Dispatch Configuration](references/config.md) <br>
- [Subagent Dispatch Template](references/dispatch-template.md) <br>
- [ClawBoard repository](https://github.com/CCCaptain0129/ClawBoard.git) <br>
- [ClawHub skill page](https://clawhub.ai/cccaptain0129/task-dispatch) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands, JSON cron configuration, API examples, and completion-signal templates] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May generate cron configuration JSON and task-dispatch prompts for subagents.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
