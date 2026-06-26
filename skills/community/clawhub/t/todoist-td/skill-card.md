## Description: <br>
Use the td (Todoist CLI) to read and manage Todoist todos/to-dos/tasks from the terminal. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mattjefferson](https://clawhub.ai/user/mattjefferson) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and developers use this skill to let an agent consult and manage their Todoist tasks through the td CLI, including agenda review, task creation, updates, completion, and deletion. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Installing or updating the upstream td CLI can introduce normal supply-chain risk. <br>
Mitigation: Review or pin the upstream Todoist CLI before running setup commands. <br>
Risk: Generic task or agenda requests may cause the agent to access Todoist task data. <br>
Mitigation: Use the skill only for intended Todoist workflows and confirm before destructive actions such as deletion. <br>


## Reference(s): <br>
- [Todoist CLI](https://github.com/Doist/todoist-cli) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown with inline shell commands and Todoist task summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May use td JSON or NDJSON output when listing or reading tasks.] <br>

## Skill Version(s): <br>
0.1.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
