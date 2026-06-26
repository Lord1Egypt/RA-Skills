## Description: <br>
Task Supervisor helps agents manage complex long-running tasks with step tracking, checkpoint files, and periodic progress reports. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Mashirops](https://clawhub.ai/user/Mashirops) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Agents use this skill when handling large tasks with multiple steps or extended duration. It helps decompose work, track progress in task files, report status, and resume paused work. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Persistent task files can contain private task details or sensitive context. <br>
Mitigation: Avoid recording secrets or private details in task logs, and review task files before sharing status updates. <br>
Risk: Recurring progress reporters can send task details to an external chat service without clear privacy boundaries. <br>
Mitigation: Confirm the intended chat service and recipient before enabling reports, and remove reporter schedules when work is paused, completed, or abandoned. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/Mashirops/task-supervisor) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown task files with inline shell commands and concise status updates] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates persistent task logs and may schedule recurring progress reporters for external chat updates.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
