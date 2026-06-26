## Description: <br>
Task Manager records, tracks, and manages assistant tasks in a local Markdown task log, including task status, task type, invoked capabilities, required permissions, dependencies, and summary statistics. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[quenfly](https://clawhub.ai/user/quenfly) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Users and assistant operators use this skill to keep a persistent local record of one-time and ongoing tasks, update task status, query task history, and recalculate task statistics. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Task records may include sensitive details if users place secrets or private context in task descriptions. <br>
Mitigation: Avoid placing secrets in task descriptions and review TASKS.md periodically. <br>
Risk: The skill writes and updates a local TASKS.md file, so an unintended path could affect the wrong task log. <br>
Mitigation: Customize the storage path when needed and run the helper script only against the intended task-log file. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/quenfly/task-manager-easy) <br>


## Skill Output: <br>
**Output Type(s):** [markdown, shell commands, guidance] <br>
**Output Format:** [Markdown task records with optional shell command output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes and updates a local TASKS.md task log and can recalculate summary counts with the bundled Node.js helper script.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
