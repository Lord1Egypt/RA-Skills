## Description: <br>
Task Tracker Pro helps agents persist multi-step task plans, progress, recovery state, and multi-agent coordination in local Markdown task files. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yurio99](https://clawhub.ai/user/yurio99) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to break multi-step work into file-backed checklists, update progress as steps complete, and resume unfinished work after an interrupted session. It also supports coordinating responsibilities across multiple agents. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Task details persist in local Markdown files and can carry sensitive work context across sessions. <br>
Mitigation: Avoid writing secrets or highly sensitive details into task names, steps, or logs, and review existing task files when starting a new session. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/yurio99/task-tracker-pro) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown task files with concise status updates and inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Persists task state in local files under the agent workspace.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
