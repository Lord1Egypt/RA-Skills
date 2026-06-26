## Description: <br>
Manage Todoist tasks. Use when the user mentions "todoist", "my tasks", "task list", "add a task", "complete task", or wants to interact with their Todoist account. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[LuoAndOrder](https://clawhub.ai/user/LuoAndOrder) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Employees, external users, and developers use this skill to inspect, add, edit, complete, reopen, and delete Todoist tasks through the td CLI. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can add, edit, complete, reopen, or delete live Todoist tasks through the td CLI. <br>
Mitigation: Review proposed write or delete commands and task IDs before execution; use read-only list, today, or show commands when only inspecting tasks. <br>
Risk: Read commands may use cached Todoist data unless the skill runs td sync or includes --sync. <br>
Mitigation: Run td sync or include --sync before acting on time-sensitive task data. <br>
Risk: The required td CLI and installation sources are third-party tooling. <br>
Mitigation: Verify the Homebrew tap or Cargo package source before installation. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/LuoAndOrder/todoist-rs) <br>
- [Publisher profile](https://clawhub.ai/user/LuoAndOrder) <br>
- [Todoist CLI project homepage](https://github.com/LuoAndOrder/todoist-rs) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May propose commands that read cached Todoist data or write changes through the td CLI; users should review write and delete actions before execution.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
